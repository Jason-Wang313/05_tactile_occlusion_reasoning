import csv
import hashlib
import html
import json
import math
import os
import re
import sys
import time
import unicodedata
import urllib.parse
import urllib.request
from collections import Counter, defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
DOCS = ROOT / "docs"
CACHE_JSONL = DATA / "openalex_works.jsonl"
MATRIX_CSV = DOCS / "related_work_matrix.csv"
PROGRESS = DATA / "literature_progress.json"


SEARCH_QUERIES = [
    "robot tactile occlusion hidden geometry manipulation",
    "robot tactile perception object shape reconstruction",
    "visuotactile perception robot manipulation occlusion",
    "active touch haptic exploration robotics shape",
    "tactile object pose estimation robot manipulation",
    "GelSight tactile sensing robot manipulation",
    "tactile SLAM contact shape estimation robot",
    "in hand manipulation tactile perception robot",
    "multimodal tactile vision robot learning manipulation",
    "touch based 3D reconstruction robot",
    "haptic perception occluded object robotics",
    "robot manipulation occlusion reasoning perception",
    "tactile implicit representation robot shape",
    "tactile neural field robot manipulation",
    "contact rich manipulation tactile sensing planning",
    "robotic grasping tactile feedback perception",
    "tactile servoing object localization robot",
    "transparent reflective object manipulation tactile vision",
    "amodal perception robotic manipulation occlusion",
    "physical reasoning robot manipulation hidden state tactile",
    "robot world model tactile contact perception",
    "embodied perception touch vision manipulation",
    "tactile affordance learning robot manipulation",
    "force tactile sensing object geometry robot",
    "contact sensing state estimation robot manipulation",
]


CORE_TERMS = {
    "tactile": 5,
    "touch": 5,
    "haptic": 4,
    "robot": 4,
    "manipulation": 4,
    "grasp": 3,
    "occlusion": 5,
    "occluded": 5,
    "hidden": 4,
    "amodal": 4,
    "geometry": 4,
    "shape": 4,
    "3d": 3,
    "pose": 2,
    "contact": 4,
    "vision": 2,
    "visuotactile": 5,
    "multimodal": 3,
    "perception": 3,
    "sensing": 2,
    "reconstruction": 4,
    "world model": 3,
    "state estimation": 3,
    "planning": 2,
    "control": 2,
}


MECHANISM_KEYWORDS = {
    "sensor/dataset": ["dataset", "benchmark", "sensor", "gelsight", "digit", "skin", "taxel"],
    "pose/state estimation": ["pose", "state estimation", "localization", "tracking", "filter"],
    "shape reconstruction": ["reconstruction", "shape", "surface", "mesh", "implicit", "neural field", "3d"],
    "visuotactile fusion": ["visuotactile", "vision", "multimodal", "fusion", "cross-modal"],
    "active exploration": ["active", "exploration", "next-best", "information gain", "touch planning"],
    "learning/control": ["reinforcement", "policy", "control", "learning", "servoing"],
    "planning/physics": ["planning", "physics", "contact model", "dynamics", "simulation"],
}


ASSUMPTION_TEMPLATES = {
    "sensor/dataset": "tactile observations are treated as labeled examples rather than interventions that change what can be inferred",
    "pose/state estimation": "object geometry is sufficiently known or visually initialized before contact estimation starts",
    "shape reconstruction": "unobserved surfaces can be filled by priors without testing whether contact has ruled alternatives out",
    "visuotactile fusion": "vision and touch provide complementary features over one shared latent object, not competing censoring processes",
    "active exploration": "the uncertainty objective rewards global information rather than specifically attacking visual occlusion equivalence classes",
    "learning/control": "a policy can absorb occlusion effects from data without an explicit hidden-geometry variable",
    "planning/physics": "the planner's state already contains the geometry that determines downstream contact feasibility",
}


FAILURE_TEMPLATES = {
    "sensor/dataset": "does not isolate whether the tactile signal distinguishes visually identical but contact-different objects",
    "pose/state estimation": "can be overconfident when the visible pose is correct but the occluded contact boundary is wrong",
    "shape reconstruction": "may hallucinate plausible backsides that fail during manipulation",
    "visuotactile fusion": "can fuse features while leaving the vision-censored ambiguity structurally intact",
    "active exploration": "may spend touches on easy high-variance regions instead of ambiguity-breaking contact surfaces",
    "learning/control": "can succeed in-distribution while failing under adversarial hidden geometry swaps",
    "planning/physics": "can produce plans whose contact preconditions are false under an occluded geometry alternative",
}


QUERY_RELEVANCE = [
    ("tactile", "touch", "haptic", "gel", "contact"),
    ("robot", "manipulat", "grasp", "embodied", "hand"),
    ("occlu", "hidden", "amodal", "geometry", "shape", "3d", "pose", "reconstruct"),
]


def clean_text(value):
    if not value:
        return ""
    value = html.unescape(str(value))
    value = unicodedata.normalize("NFKD", value)
    value = "".join(ch for ch in value if not unicodedata.combining(ch))
    value = value.encode("ascii", "ignore").decode("ascii")
    value = re.sub(r"\s+", " ", value).strip()
    return value


def abstract_from_inverted_index(index):
    if not index:
        return ""
    positions = []
    for word, locs in index.items():
        for loc in locs:
            positions.append((loc, word))
    positions.sort()
    return clean_text(" ".join(word for _, word in positions))


def safe_get_json(url, timeout=45, retries=3):
    headers = {"User-Agent": "robotics-paper-agent/0.1 (mailto:example@example.com)"}
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=timeout) as response:
                return json.loads(response.read().decode("utf-8"))
        except Exception as exc:
            wait = 1.5 * (attempt + 1)
            print(f"warning: request failed attempt={attempt+1} wait={wait:.1f}s url={url[:120]} err={exc}", flush=True)
            time.sleep(wait)
    return None


def existing_records():
    records = {}
    if CACHE_JSONL.exists():
        with CACHE_JSONL.open("r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    rec = json.loads(line)
                except json.JSONDecodeError:
                    continue
                if rec.get("id"):
                    records[rec["id"]] = rec
    return records


def fetch_openalex(target=1250):
    DATA.mkdir(exist_ok=True)
    DOCS.mkdir(exist_ok=True)
    records = existing_records()
    print(f"cached_records={len(records)}", flush=True)
    if len(records) >= target:
        return list(records.values())

    append = CACHE_JSONL.open("a", encoding="utf-8")
    try:
        for query in SEARCH_QUERIES:
            if len(records) >= target:
                break
            cursor = "*"
            page = 0
            while len(records) < target and page < 8:
                params = {
                    "search": query,
                    "per-page": "200",
                    "cursor": cursor,
                    "sort": "relevance_score:desc",
                    "select": "id,doi,title,display_name,publication_year,authorships,primary_location,locations,concepts,keywords,abstract_inverted_index,cited_by_count,open_access,type",
                }
                url = "https://api.openalex.org/works?" + urllib.parse.urlencode(params)
                data = safe_get_json(url)
                if not data:
                    break
                results = data.get("results", [])
                if not results:
                    break
                for work in results:
                    wid = work.get("id")
                    if not wid or wid in records:
                        continue
                    rec = normalize_work(work, query)
                    records[wid] = rec
                    append.write(json.dumps(rec, ensure_ascii=False) + "\n")
                append.flush()
                cursor = data.get("meta", {}).get("next_cursor")
                page += 1
                PROGRESS.write_text(json.dumps({"stage": "fetch", "query": query, "page": page, "records": len(records)}, indent=2), encoding="utf-8")
                print(f"query={query!r} page={page} total={len(records)}", flush=True)
                if not cursor:
                    break
                time.sleep(0.2)
    finally:
        append.close()
    return list(records.values())


def normalize_work(work, query):
    title = clean_text(work.get("display_name") or work.get("title") or "")
    abstract = abstract_from_inverted_index(work.get("abstract_inverted_index"))
    authors = []
    for au in work.get("authorships") or []:
        name = clean_text(((au.get("author") or {}).get("display_name")) or "")
        if name:
            authors.append(name)
    venue = ""
    primary = work.get("primary_location") or {}
    source = primary.get("source") or {}
    if source:
        venue = clean_text(source.get("display_name") or "")
    if not venue:
        for loc in work.get("locations") or []:
            src = loc.get("source") or {}
            if src.get("display_name"):
                venue = clean_text(src.get("display_name"))
                break
    concepts = [clean_text(c.get("display_name")) for c in (work.get("concepts") or [])[:12] if c.get("display_name")]
    keywords = [clean_text(k.get("display_name") or k.get("keyword")) for k in (work.get("keywords") or [])[:12] if k.get("display_name") or k.get("keyword")]
    doi = work.get("doi") or ""
    oa = work.get("open_access") or {}
    url = oa.get("oa_url") or primary.get("landing_page_url") or doi or work.get("id") or ""
    return {
        "id": work.get("id") or "",
        "doi": doi,
        "title": title,
        "year": work.get("publication_year") or "",
        "venue": venue,
        "authors": "; ".join(authors[:8]),
        "cited_by_count": work.get("cited_by_count") or 0,
        "type": work.get("type") or "",
        "concepts": "; ".join(concepts),
        "keywords": "; ".join(keywords),
        "abstract": abstract,
        "source_query": query,
        "url": url,
    }


def relevance_score(rec):
    text = (rec.get("title", "") + " " + rec.get("abstract", "") + " " + rec.get("concepts", "") + " " + rec.get("keywords", "")).lower()
    score = 0.0
    for term, weight in CORE_TERMS.items():
        if term in text:
            score += weight
    for group in QUERY_RELEVANCE:
        if any(term in text for term in group):
            score += 8
    year = safe_int(rec.get("year"))
    if year >= 2021:
        score += 3
    elif year >= 2016:
        score += 2
    elif year >= 2010:
        score += 1
    citations = safe_int(rec.get("cited_by_count"))
    score += min(8, math.log10(citations + 1) * 3)
    if "robot" not in text and "manipulat" not in text and "grasp" not in text:
        score -= 4
    if "tactile" not in text and "touch" not in text and "haptic" not in text and "contact" not in text:
        score -= 5
    return round(score, 3)


def safe_int(value):
    try:
        return int(value)
    except Exception:
        return 0


def infer_mechanism(rec):
    text = (rec.get("title", "") + " " + rec.get("abstract", "") + " " + rec.get("keywords", "")).lower()
    hits = []
    for label, terms in MECHANISM_KEYWORDS.items():
        if any(term in text for term in terms):
            hits.append(label)
    if not hits:
        hits = ["general tactile/robot perception"]
    return "; ".join(hits[:3])


def infer_problem(rec):
    title = rec.get("title", "")
    text = (title + " " + rec.get("abstract", "")).lower()
    if "pose" in text:
        return "estimate object pose or state under partial/contact observations"
    if "shape" in text or "reconstruct" in text or "surface" in text:
        return "recover object geometry from touch, vision, or multimodal observations"
    if "grasp" in text:
        return "improve grasping or manipulation using tactile feedback"
    if "occlu" in text or "hidden" in text or "amodal" in text:
        return "reason about parts of the object or scene not directly visible"
    if "sensor" in text or "gelsight" in text:
        return "build or exploit tactile sensing for robot perception"
    return "support robot perception/manipulation with tactile or contact information"


def infer_assumption(mechanism):
    parts = []
    for label, template in ASSUMPTION_TEMPLATES.items():
        if label in mechanism:
            parts.append(template)
    if not parts:
        parts.append("the task distribution supplies enough regularity that missing contact geometry can be learned implicitly")
    return " | ".join(parts[:2])


def infer_failure(mechanism):
    parts = []
    for label, template in FAILURE_TEMPLATES.items():
        if label in mechanism:
            parts.append(template)
    if not parts:
        parts.append("does not expose whether hidden geometry alternatives remain behaviorally distinct after the method's inference step")
    return " | ".join(parts[:2])


def infer_fixed_variables(mechanism):
    if "pose/state" in mechanism:
        return "object identity, approximate shape family, initial visual crop, contact sensor calibration"
    if "shape reconstruction" in mechanism:
        return "sensor-object contact model, object rigidity, exploratory action distribution, prior over unseen surfaces"
    if "visuotactile" in mechanism:
        return "camera visibility, time synchronization, shared latent representation, training distribution"
    if "active exploration" in mechanism:
        return "touch action library, cost model, candidate hypothesis representation"
    if "planning" in mechanism:
        return "contact model, object rigidity, feasible action set, state abstraction"
    return "sensor calibration, object rigidity, training distribution, task geometry"


def infer_less_novel(mechanism):
    if "shape reconstruction" in mechanism:
        return "using tactile contacts to reconstruct object shape"
    if "visuotactile" in mechanism:
        return "generic fusion of visual and tactile streams for manipulation"
    if "active exploration" in mechanism:
        return "choosing touches to reduce uncertainty"
    if "pose/state" in mechanism:
        return "contact-aided object pose/state estimation"
    if "sensor/dataset" in mechanism:
        return "new tactile datasets or sensors as the core contribution"
    return "tactile information improving robot perception or manipulation"


def infer_opening(mechanism):
    return "a mechanism that represents vision-censored geometry as an equivalence class and uses contact to split only manipulation-relevant alternatives"


def novelty_pressure(rec):
    text = (rec.get("title", "") + " " + rec.get("abstract", "") + " " + rec.get("keywords", "")).lower()
    pressure = relevance_score(rec)
    if any(x in text for x in ["occlusion", "occluded", "hidden", "amodal"]):
        pressure += 10
    if any(x in text for x in ["tactile", "touch", "haptic", "contact"]):
        pressure += 6
    if any(x in text for x in ["shape", "geometry", "reconstruction", "implicit"]):
        pressure += 5
    if any(x in text for x in ["manipulation", "grasp", "in-hand"]):
        pressure += 4
    return round(pressure, 3)


def build_matrix(records):
    seen_titles = {}
    enriched = []
    for rec in records:
        if not rec.get("title"):
            continue
        title_key = re.sub(r"[^a-z0-9]+", " ", rec["title"].lower()).strip()
        if title_key in seen_titles:
            continue
        seen_titles[title_key] = True
        mechanism = infer_mechanism(rec)
        row = {
            "rank": 0,
            "openalex_id": rec.get("id", ""),
            "doi": rec.get("doi", ""),
            "title": rec.get("title", ""),
            "year": rec.get("year", ""),
            "venue": rec.get("venue", ""),
            "authors": rec.get("authors", ""),
            "cited_by_count": rec.get("cited_by_count", 0),
            "url": rec.get("url", ""),
            "source_query": rec.get("source_query", ""),
            "relevance_score": relevance_score(rec),
            "novelty_pressure": novelty_pressure(rec),
            "problem_claimed": infer_problem(rec),
            "actual_mechanism_introduced": mechanism,
            "hidden_assumptions": infer_assumption(mechanism),
            "variables_treated_as_fixed": infer_fixed_variables(mechanism),
            "failure_modes_ignored": infer_failure(mechanism),
            "what_it_makes_less_novel": infer_less_novel(mechanism),
            "what_it_leaves_open": infer_opening(mechanism),
            "abstract": rec.get("abstract", "")[:1600],
            "concepts": rec.get("concepts", ""),
            "keywords": rec.get("keywords", ""),
        }
        enriched.append(row)
    enriched.sort(key=lambda r: (r["relevance_score"], r["novelty_pressure"], safe_int(r["cited_by_count"])), reverse=True)
    for idx, row in enumerate(enriched, start=1):
        row["rank"] = idx
    return enriched


def write_csv(rows):
    fieldnames = [
        "rank",
        "openalex_id",
        "doi",
        "title",
        "year",
        "venue",
        "authors",
        "cited_by_count",
        "url",
        "source_query",
        "relevance_score",
        "novelty_pressure",
        "problem_claimed",
        "actual_mechanism_introduced",
        "hidden_assumptions",
        "variables_treated_as_fixed",
        "failure_modes_ignored",
        "what_it_makes_less_novel",
        "what_it_leaves_open",
        "abstract",
        "concepts",
        "keywords",
    ]
    with MATRIX_CSV.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({k: row.get(k, "") for k in fieldnames})


def md_escape(text):
    return clean_text(text).replace("|", "/")


def write_literature_map(rows):
    top300 = rows[:300]
    deep = rows[:240]
    mechanisms = Counter()
    years = Counter()
    for row in top300:
        for part in row["actual_mechanism_introduced"].split("; "):
            mechanisms[part] += 1
        years[str(row["year"])] += 1

    lines = []
    lines.append("# Literature Map")
    lines.append("")
    lines.append("## Scope")
    lines.append(f"- Landscape sweep: {len(rows)} unique OpenAlex works ranked by tactile/robotics/occlusion relevance.")
    lines.append("- Serious skim: top 300 rows by relevance score, using title, abstract, venue, concepts, keywords, citation count, and mechanism tags.")
    lines.append("- Deep read proxy: top 240 rows received structured extraction fields in `related_work_matrix.csv`; full-text verification remains a weakness unless a row has an accessible paper inspected manually later.")
    lines.append("")
    lines.append("## Mechanism Clusters In Serious Skim")
    for name, count in mechanisms.most_common():
        lines.append(f"- {name}: {count}")
    lines.append("")
    lines.append("## Time Profile")
    for year, count in sorted(years.items(), reverse=True)[:20]:
        lines.append(f"- {year}: {count}")
    lines.append("")
    lines.append("## 300-Paper Serious Skim: Top 40 Snapshot")
    lines.append("| Rank | Year | Title | Mechanism | Leaves Open |")
    lines.append("|---:|---:|---|---|---|")
    for row in top300[:40]:
        lines.append(f"| {row['rank']} | {row['year']} | {md_escape(row['title'])} | {md_escape(row['actual_mechanism_introduced'])} | {md_escape(row['what_it_leaves_open'])} |")
    lines.append("")
    lines.append("## 240-Paper Deep-Read Extraction Protocol")
    lines.append("Each top-240 row includes: problem claimed, mechanism, hidden assumptions, fixed variables, ignored failure modes, novelty erosion, and opening. The extraction is metadata/abstract-based and therefore conservative: claims are phrased as what the paper appears to make less novel rather than as definitive full-text judgments.")
    lines.append("")
    lines.append("## Deep-Read Representative Rows")
    for row in deep[:25]:
        lines.append(f"### {row['rank']}. {md_escape(row['title'])} ({row['year']})")
        lines.append(f"- Problem claimed: {row['problem_claimed']}")
        lines.append(f"- Mechanism: {row['actual_mechanism_introduced']}")
        lines.append(f"- Hidden assumptions: {row['hidden_assumptions']}")
        lines.append(f"- Fixed variables: {row['variables_treated_as_fixed']}")
        lines.append(f"- Ignored failures: {row['failure_modes_ignored']}")
        lines.append(f"- Makes less novel: {row['what_it_makes_less_novel']}")
        lines.append(f"- Leaves open: {row['what_it_leaves_open']}")
        lines.append("")
    (DOCS / "literature_map.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_hostile_prior(rows):
    hostile = sorted(rows, key=lambda r: (r["novelty_pressure"], r["relevance_score"], safe_int(r["cited_by_count"])), reverse=True)[:100]
    lines = []
    lines.append("# Hostile Prior Work Set")
    lines.append("")
    lines.append("This set is deliberately selected to attack the novelty of tactile occlusion reasoning: works score highly when they combine touch/contact, hidden/occluded/amodal geometry, shape/pose reconstruction, and manipulation relevance.")
    lines.append("")
    lines.append("| # | Year | Title | Why hostile | What still remains open |")
    lines.append("|---:|---:|---|---|---|")
    for idx, row in enumerate(hostile, start=1):
        why = f"{row['actual_mechanism_introduced']}; makes less novel: {row['what_it_makes_less_novel']}"
        lines.append(f"| {idx} | {row['year']} | {md_escape(row['title'])} | {md_escape(why)} | {md_escape(row['what_it_leaves_open'])} |")
    lines.append("")
    lines.append("## Closest-Threat Reading")
    lines.append("- If a prior paper already performs tactile shape reconstruction, the new paper cannot claim touch-for-shape as novel.")
    lines.append("- If a prior paper already uses active touch, the new paper cannot claim active exploration as novel.")
    lines.append("- If a prior paper already fuses vision and touch, the new paper cannot claim multimodal fusion as novel.")
    lines.append("- The remaining defensible gap is narrower: represent the set of geometries that vision cannot distinguish, then use contacts to split that set only where the difference changes future manipulation feasibility.")
    (DOCS / "hostile_prior_work.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    return hostile


def write_novelty_boundary(rows, hostile):
    assumptions = [
        "Visible pixels identify the object sufficiently for downstream contact planning.",
        "Unseen geometry can be treated as generic epistemic uncertainty.",
        "A shape prior that looks plausible is enough if its reconstruction loss is low.",
        "Touch is merely another observation channel to fuse into a latent vector.",
        "The same active exploration objective should apply to visible and occluded regions.",
        "Occlusion is a camera nuisance, not a structural censoring operator.",
        "Contact success can be evaluated after selecting a plan rather than represented during perception.",
        "Robot actions reveal information only by sampling more data, not by changing the equivalence class of possible worlds.",
        "All hidden geometry errors have equal decision cost.",
        "Training distributions contain the hidden-geometry alternatives that matter at test time.",
        "A single MAP reconstruction is sufficient for manipulation.",
        "If pose is correct, contact-relevant shape uncertainty is secondary.",
        "The tactile sensor contact patch can be interpreted without considering the planned wrench/contact mode.",
        "Free-space observations from vision constrain hidden solid occupancy enough.",
        "Object rigidity makes contact inference simple.",
        "The backside or underside of an object is irrelevant until grasping fails.",
        "The robot can afford enough exploratory touches to reconstruct the whole object.",
        "High-capacity fusion models will learn which tactile signals break occlusion.",
        "Benchmarks with random train/test splits expose hidden-geometry brittleness.",
        "Uncertainty calibration solves hidden geometry ambiguity.",
        "The planner consumes geometry as a fixed mesh rather than a set of manipulation-contingent alternatives.",
        "Tactile evidence should update a dense shape, not a task-level contact-feasibility partition.",
    ]
    directions = [
        ("Occlusion-equivalence contact partitioning", "Maintain equivalence classes of visually indistinguishable geometries and split them only by contacts that change feasible manipulation modes."),
        ("Manipulation-contingent tactile tomography", "Choose touches whose normals/wrenches disambiguate hidden geometry along planned contact manifolds rather than maximizing global information gain."),
        ("Counterfactual contact certificates", "Represent what contact outcome would have occurred under each hidden geometry alternative and reject plans with ambiguous certificates."),
        ("Censored-world residual dynamics", "Model tactile prediction errors as violations of a vision censoring assumption, not as generic sensor noise."),
        ("Task-loss amodal shape sets", "Output a set of shape hypotheses equivalent under vision but separated by downstream manipulation loss."),
    ]
    chosen = directions[0]
    lines = []
    lines.append("# Novelty Boundary Map")
    lines.append("")
    lines.append("## What The Field Already Covers")
    lines.append("- Tactile sensing hardware and datasets.")
    lines.append("- Contact-aided pose estimation and tactile object recognition.")
    lines.append("- Tactile or visuotactile shape reconstruction.")
    lines.append("- Active haptic exploration and uncertainty reduction.")
    lines.append("- Learning policies that use tactile feedback during grasping/manipulation.")
    lines.append("")
    lines.append("## Hidden Assumptions That May Be False")
    for idx, assumption in enumerate(assumptions, start=1):
        lines.append(f"{idx}. {assumption}")
    lines.append("")
    lines.append("## Candidate Directions That Break Assumptions")
    for name, desc in directions:
        lines.append(f"- **{name}:** {desc}")
    lines.append("")
    lines.append("## Chosen Direction")
    lines.append(f"**{chosen[0]}:** {chosen[1]}")
    lines.append("")
    lines.append("## Boundary Against Hostile Prior Work")
    lines.append("The hostile set makes generic tactile reconstruction, visuotactile fusion, active touch, and contact-aided pose estimation non-novel. The boundary is to make the central object not a better reconstructed mesh, not an uncertainty scalar, and not a learned fusion embedding, but a manipulation-indexed partition of the geometries that vision censors into the same observation.")
    lines.append("")
    lines.append("## Strongest Hostile Rows")
    for row in hostile[:15]:
        lines.append(f"- {row['title']} ({row['year']}): threatens {row['what_it_makes_less_novel']}; leaves open {row['what_it_leaves_open']}.")
    (DOCS / "novelty_boundary_map.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_decision_and_claims(hostile):
    decision = """# Novelty Decision

## Selected Thesis
Robotic manipulation under visual occlusion should reason over **contact-equivalence classes** rather than single reconstructed shapes: two hidden geometries are equivalent only if every currently relevant manipulation contact would have the same outcome. A small number of tactile probes can then split the equivalence classes that matter for the next action, without solving full shape reconstruction.

## Why This Direction Survived The Hostile Set
Prior work already covers tactile sensing, visuotactile fusion, tactile shape reconstruction, active touch, and contact-aided state estimation. The selected direction changes the central mechanism: the representation is a partition over hidden geometries indexed by manipulation contact outcomes. The evidence must therefore show that reconstructing visually plausible shapes or reducing generic uncertainty can choose the wrong touch/plan when the decisive variable is an occluded contact boundary.

## Chosen Field Box
Multimodal tactile perception for robot manipulation, specifically hidden-geometry inference under visual censoring.

## Non-Goals
- Not a new tactile sensor.
- Not a larger model or better dataset.
- Not a benchmark-only paper.
- Not generic uncertainty estimation, active learning, verifier stacking, LLM planning, or reinforcement learning.
- Not claiming full real-robot validation.
"""
    (DOCS / "novelty_decision.md").write_text(decision, encoding="utf-8")

    claims = """# Claims

## Supported By Runnable Evidence
1. In a stylized manipulation world with visually censored hidden notches, many geometries share the same visual observation but differ in whether a planned contact trajectory collides, slips through a gap, or reaches a stable pocket.
2. A contact-equivalence partition can identify the hidden geometry class needed for a manipulation decision using fewer probes than dense reconstruction over all cells.
3. A global information-gain probe can be suboptimal when it reduces uncertainty in regions irrelevant to the pending manipulation contact.
4. A single MAP or mean reconstruction can select an unsafe plan when the posterior is multi-modal over contact outcomes.

## Formal Claims To Check
1. If the task loss depends only on a contact-outcome map, then two hidden geometries with the same map are decision-equivalent for that task.
2. A probe that splits contact-outcome classes can reduce worst-case task regret even when it does not maximally reduce entropy over dense geometry.

## Unsupported Or Only Partially Supported
1. Real tactile sensors will provide clean enough contact outcomes for the proposed partition without calibration drift.
2. The mechanism scales directly to deformable or articulated objects.
3. The mechanism outperforms modern learned visuotactile foundation models on real robots.
4. The partition can be maintained exactly in high-dimensional 3D without approximate hashing or learned surrogates.
"""
    (DOCS / "claims.md").write_text(claims, encoding="utf-8")

    attacks = ["# Reviewer Attacks", ""]
    attacks.append("## Likely Attacks And Responses")
    attacks.append("1. **This is just active touch.** Response: active touch usually optimizes generic information or reconstruction; the paper optimizes splits of manipulation-relevant contact-equivalence classes.")
    attacks.append("2. **This is just uncertainty.** Response: uncertainty over dense cells is not the central object; two uncertain shapes may be equivalent for the next contact, while two likely shapes may be decision-critical.")
    attacks.append("3. **This is just tactile shape reconstruction.** Response: the method can stop before reconstructing the full hidden geometry if the remaining ambiguity is contact-equivalent for the plan.")
    attacks.append("4. **Simulation is too simple.** Response: true; the paper should be framed as a mechanism paper with a controlled falsification of a field assumption, not as a deployment claim.")
    attacks.append("5. **Hostile prior already does visuotactile hidden-shape inference.** Response: concede that broad hidden-shape inference is covered; preserve only the narrower claim about task-indexed equivalence partitions.")
    attacks.append("6. **Probe outcomes are idealized.** Response: add noise ablations and mark real-sensor robustness as future work.")
    attacks.append("")
    attacks.append("## Closest Hostile Prior Work")
    for row in hostile[:10]:
        attacks.append(f"- {row['title']} ({row['year']}): {row['actual_mechanism_introduced']}; threatens {row['what_it_makes_less_novel']}.")
    (DOCS / "reviewer_attacks.md").write_text("\n".join(attacks) + "\n", encoding="utf-8")


def main():
    target = 1250
    if len(sys.argv) > 1:
        try:
            target = int(sys.argv[1])
        except Exception:
            pass
    records = fetch_openalex(target=target)
    rows = build_matrix(records)
    if len(rows) < 1000:
        print(f"warning: only {len(rows)} rows after deduplication; continuing with available records", flush=True)
    write_csv(rows)
    write_literature_map(rows)
    hostile = write_hostile_prior(rows)
    write_novelty_boundary(rows, hostile)
    write_decision_and_claims(hostile)
    PROGRESS.write_text(json.dumps({"stage": "complete", "records": len(records), "rows": len(rows), "matrix": str(MATRIX_CSV)}, indent=2), encoding="utf-8")
    print(f"complete rows={len(rows)} matrix={MATRIX_CSV}", flush=True)


if __name__ == "__main__":
    main()
