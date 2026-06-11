import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MATRIX = ROOT / "docs" / "related_work_matrix.csv"
OUT = ROOT / "docs" / "paper_context_rows.md"


FIELDS = [
    "rank",
    "year",
    "title",
    "authors",
    "venue",
    "doi",
    "url",
    "problem_claimed",
    "actual_mechanism_introduced",
    "hidden_assumptions",
    "what_it_makes_less_novel",
    "what_it_leaves_open",
]


def compact(text, limit=260):
    text = " ".join((text or "").split())
    if len(text) <= limit:
        return text
    return text[: limit - 3].rstrip() + "..."


def load_rows():
    with MATRIX.open("r", encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))
    for row in rows:
        try:
            row["_rank_int"] = int(row.get("rank", "999999"))
        except ValueError:
            row["_rank_int"] = 999999
    rows.sort(key=lambda r: r["_rank_int"])
    return rows


def emit_row(row):
    lines = [f"### {row.get('rank')}. {row.get('title')} ({row.get('year')})"]
    for field in FIELDS[3:]:
        lines.append(f"- {field}: {compact(row.get(field, ''))}")
    return "\n".join(lines)


def main():
    rows = load_rows()
    title_needles = [
        "TouchAnything",
        "Visual-Tactile Fusion for 3D Objects Reconstruction",
        "Tac2Pose",
        "TouchSDF",
        "Active Tactile Exploration Based on Cost-Aware Information Gain",
        "Simultaneous Tactile Localization",
        "NormalFlow",
        "ViTaSCOPE",
        "Touch if it's Transparent",
        "More Than a Feeling",
        "DIGIT",
        "GelSight",
        "Proactive Tactile Exploration",
        "ForceFlow",
    ]
    selected = rows[:35]
    seen = {row["title"] for row in selected}
    for needle in title_needles:
        low = needle.lower()
        for row in rows:
            if low in row.get("title", "").lower() and row["title"] not in seen:
                selected.append(row)
                seen.add(row["title"])
                break
    lines = [
        "# Paper Context Rows",
        "",
        f"Loaded {len(rows)} rows from `docs/related_work_matrix.csv`.",
        "Selected rows combine the top ranked matrix entries with named hostile/context papers.",
        "",
    ]
    for row in selected:
        lines.append(emit_row(row))
        lines.append("")
    OUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"wrote {OUT}")
    print(f"selected_rows={len(selected)}")


if __name__ == "__main__":
    main()
