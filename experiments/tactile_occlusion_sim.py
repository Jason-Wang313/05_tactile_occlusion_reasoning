import csv
import math
import random
import sys
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"
PROGRESS = RESULTS / "simulation_progress.txt"
REQUIRED_OUTPUTS = [
    RESULTS / "evidence_summary.csv",
    RESULTS / "noise_ablation.csv",
    RESULTS / "main_success_table.tex",
    RESULTS / "noise_success_table.tex",
    RESULTS / "ascii_success_plot.txt",
    RESULTS / "README.md",
]


LANES = 12
DECOR_BITS = 64
DECOR_GROUP = 4
TRIALS = 2000
BUDGETS = list(range(0, 9))
NOISES = [0.0, 0.02, 0.05, 0.10, 0.20]
SEED = 505
METHODS = [
    "visual_only",
    "random",
    "dense_entropy",
    "dense_contact_only",
    "critical_cell_entropy",
    "contact_equivalence",
]


@dataclass
class Probe:
    name: str
    kind: str
    payload: object


def entropy(probs):
    total = sum(probs)
    if total <= 0:
        return 0.0
    h = 0.0
    for p in probs:
        if p <= 0:
            continue
        q = p / total
        h -= q * math.log(q, 2)
    return h


def binary_entropy(p):
    if p <= 0.0 or p >= 1.0:
        return 0.0
    return -p * math.log(p, 2) - (1.0 - p) * math.log(1.0 - p, 2)


def make_probes():
    probes = []
    for start in range(0, DECOR_BITS, DECOR_GROUP):
        bits = tuple(range(start, min(start + DECOR_GROUP, DECOR_BITS)))
        probes.append(Probe(f"decor[{bits[0]}:{bits[-1]}]", "decor", bits))
    for lane in range(LANES):
        probes.append(Probe(f"lane_is_{lane}", "lane", lane))
    # Balanced tactile sweeps over contact manifolds. A sweep returns whether
    # the hidden insertion channel lies in the swept subset; it does not reveal
    # decorative geometry outside the future contact path.
    for width in [6, 4, 3, 2, 1]:
        for start in range(0, LANES, width):
            subset = tuple(range(start, min(start + width, LANES)))
            if 0 < len(subset) < LANES:
                probes.append(Probe(f"sweep_{subset[0]}_{subset[-1]}", "split", subset))
    return probes


PROBES = make_probes()


class Belief:
    def __init__(self, noise):
        self.noise = noise
        self.c_weights = [1.0 / LANES for _ in range(LANES)]
        self.decor_known = set()
        self.used = set()

    def copy(self):
        other = Belief(self.noise)
        other.c_weights = list(self.c_weights)
        other.decor_known = set(self.decor_known)
        other.used = set(self.used)
        return other

    def normalize(self):
        total = sum(self.c_weights)
        if total <= 0:
            self.c_weights = [1.0 / LANES for _ in range(LANES)]
        else:
            self.c_weights = [w / total for w in self.c_weights]

    def h_contact(self):
        return entropy(self.c_weights)

    def h_full(self):
        return self.h_contact() + (DECOR_BITS - len(self.decor_known))

    def p_probe_true(self, probe):
        if probe.kind == "decor":
            # Unknown decorative bits are iid Bernoulli(0.5); the exact bit
            # vector has high entropy but no effect on the manipulation contact.
            unknown = [b for b in probe.payload if b not in self.decor_known]
            return 0.5 if unknown else 1.0
        if probe.kind == "lane":
            lane = probe.payload
            return self.c_weights[lane]
        if probe.kind == "split":
            subset = set(probe.payload)
            return sum(w for i, w in enumerate(self.c_weights) if i in subset)
        return 0.0

    def expected_contact_gain(self, probe):
        before = self.h_contact()
        if probe.kind == "decor":
            return 0.0
        p_true = self.p_probe_true(probe)
        p_obs_true = p_true * (1.0 - self.noise) + (1.0 - p_true) * self.noise
        expected_after = 0.0
        for obs in [True, False]:
            p_obs = p_obs_true if obs else 1.0 - p_obs_true
            if p_obs <= 1e-12:
                continue
            after = self.copy()
            after.update_with_observation(probe, obs, hypothetical=True)
            expected_after += p_obs * after.h_contact()
        return before - expected_after

    def expected_full_gain(self, probe):
        if probe.kind == "decor":
            unknown = [b for b in probe.payload if b not in self.decor_known]
            return float(len(unknown))
        before = self.h_full()
        p_true = self.p_probe_true(probe)
        p_obs_true = p_true * (1.0 - self.noise) + (1.0 - p_true) * self.noise
        expected_after = 0.0
        for obs in [True, False]:
            p_obs = p_obs_true if obs else 1.0 - p_obs_true
            if p_obs <= 1e-12:
                continue
            after = self.copy()
            after.update_with_observation(probe, obs, hypothetical=True)
            expected_after += p_obs * after.h_full()
        return before - expected_after

    def expected_lane_gain(self, probe):
        if probe.kind != "lane":
            return -1.0
        return self.expected_contact_gain(probe)

    def update_with_observation(self, probe, obs, hypothetical=False):
        if not hypothetical:
            self.used.add(probe.name)
        if probe.kind == "decor":
            for bit in probe.payload:
                self.decor_known.add(bit)
            return
        if probe.kind == "lane":
            lane = probe.payload
            for i, weight in enumerate(self.c_weights):
                truth = i == lane
                like = (1.0 - self.noise) if obs == truth else self.noise
                self.c_weights[i] = weight * like
            self.normalize()
            return
        if probe.kind == "split":
            subset = set(probe.payload)
            for i, weight in enumerate(self.c_weights):
                truth = i in subset
                like = (1.0 - self.noise) if obs == truth else self.noise
                self.c_weights[i] = weight * like
            self.normalize()


def observe(probe, true_lane, decor, rng, noise):
    if probe.kind == "decor":
        return tuple(decor[i] for i in probe.payload)
    if probe.kind == "lane":
        truth = true_lane == probe.payload
    elif probe.kind == "split":
        truth = true_lane in set(probe.payload)
    else:
        truth = False
    if rng.random() < noise:
        return not truth
    return truth


def choose_probe(method, belief, rng):
    unused = [p for p in PROBES if p.name not in belief.used]
    if not unused:
        return None
    if method == "visual_only":
        return None
    if method == "random":
        return rng.choice(unused)
    if method == "dense_entropy":
        return max(unused, key=lambda p: (belief.expected_full_gain(p), -len(p.name)))
    if method == "dense_contact_only":
        # Boundary control: dense entropy is evaluated only over probes that can
        # affect the pending contact. It should agree with contact-equivalence
        # when irrelevant hidden geometry has already been ruled out.
        contact_probes = [p for p in unused if p.kind in {"lane", "split"}]
        return max(contact_probes, key=lambda p: (belief.expected_full_gain(p), p.kind == "split"))
    if method == "critical_cell_entropy":
        lane_probes = [p for p in unused if p.kind == "lane"]
        if not lane_probes:
            return rng.choice(unused)
        return max(lane_probes, key=lambda p: belief.expected_lane_gain(p))
    if method == "contact_equivalence":
        contact_probes = [p for p in unused if p.kind in {"lane", "split"}]
        return max(contact_probes, key=lambda p: (belief.expected_contact_gain(p), p.kind == "split"))
    raise ValueError(f"unknown method {method}")


def select_action(belief, rng):
    max_weight = max(belief.c_weights)
    winners = [i for i, w in enumerate(belief.c_weights) if abs(w - max_weight) < 1e-12]
    return rng.choice(winners)


def run_trial(method, budget, noise, rng):
    true_lane = rng.randrange(LANES)
    decor = [rng.randrange(2) == 1 for _ in range(DECOR_BITS)]
    belief = Belief(noise=noise)
    contact_probes = 0
    decor_probes = 0
    for _ in range(budget):
        probe = choose_probe(method, belief, rng)
        if probe is None:
            break
        obs = observe(probe, true_lane, decor, rng, noise)
        if probe.kind == "decor":
            # The exact decorative values are irrelevant; knowing them removes
            # dense geometry entropy but leaves the contact class unchanged.
            belief.update_with_observation(probe, obs, hypothetical=False)
            decor_probes += 1
        else:
            belief.update_with_observation(probe, obs, hypothetical=False)
            contact_probes += 1
    action = select_action(belief, rng)
    success = 1 if action == true_lane else 0
    return {
        "success": success,
        "regret": 1 - success,
        "posterior_contact_entropy": belief.h_contact(),
        "posterior_full_entropy": belief.h_full(),
        "contact_probes": contact_probes,
        "decor_probes": decor_probes,
    }


def score_belief(belief, true_lane, contact_probes, decor_probes, rng):
    action = select_action(belief, rng)
    success = 1 if action == true_lane else 0
    return {
        "success": success,
        "regret": 1 - success,
        "posterior_contact_entropy": belief.h_contact(),
        "posterior_full_entropy": belief.h_full(),
        "contact_probes": contact_probes,
        "decor_probes": decor_probes,
    }


def run_trajectory(method, max_budget, noise, rng):
    true_lane = rng.randrange(LANES)
    decor = [rng.randrange(2) == 1 for _ in range(DECOR_BITS)]
    belief = Belief(noise=noise)
    score_rng = random.Random(rng.randrange(2**32))
    contact_probes = 0
    decor_probes = 0
    records = []

    for budget in range(max_budget + 1):
        records.append(score_belief(belief, true_lane, contact_probes, decor_probes, score_rng))
        if budget == max_budget:
            break
        probe = choose_probe(method, belief, rng)
        if probe is None:
            continue
        obs = observe(probe, true_lane, decor, rng, noise)
        belief.update_with_observation(probe, obs, hypothetical=False)
        if probe.kind == "decor":
            decor_probes += 1
        else:
            contact_probes += 1
    return records


def summarize(values):
    if not values:
        return 0.0
    return sum(values) / len(values)


def run_all(trials=TRIALS):
    RESULTS.mkdir(exist_ok=True)
    rows = []
    noise_rows = []
    rng = random.Random(SEED)
    max_budget = max(BUDGETS)
    main_runs = {(budget, method): [] for budget in BUDGETS for method in METHODS}

    for method in METHODS:
        for _ in range(trials):
            trial_records = run_trajectory(method, max_budget, 0.0, rng)
            for budget in BUDGETS:
                main_runs[(budget, method)].append(trial_records[budget])
        PROGRESS.write_text(f"completed_method={method}\n", encoding="utf-8")

    for budget in BUDGETS:
        for method in METHODS:
            trial_rows = main_runs[(budget, method)]
            rows.append({
                "budget": budget,
                "noise": 0.0,
                "method": method,
                "success_rate": summarize([r["success"] for r in trial_rows]),
                "mean_regret": summarize([r["regret"] for r in trial_rows]),
                "posterior_contact_entropy": summarize([r["posterior_contact_entropy"] for r in trial_rows]),
                "posterior_full_entropy": summarize([r["posterior_full_entropy"] for r in trial_rows]),
                "contact_probes": summarize([r["contact_probes"] for r in trial_rows]),
                "decor_probes": summarize([r["decor_probes"] for r in trial_rows]),
            })

    for noise in NOISES:
        for method in METHODS:
            trial_rows = [run_trial(method, 4, noise, rng) for _ in range(trials)]
            noise_rows.append({
                "budget": 4,
                "noise": noise,
                "method": method,
                "success_rate": summarize([r["success"] for r in trial_rows]),
                "mean_regret": summarize([r["regret"] for r in trial_rows]),
                "posterior_contact_entropy": summarize([r["posterior_contact_entropy"] for r in trial_rows]),
                "posterior_full_entropy": summarize([r["posterior_full_entropy"] for r in trial_rows]),
                "contact_probes": summarize([r["contact_probes"] for r in trial_rows]),
                "decor_probes": summarize([r["decor_probes"] for r in trial_rows]),
            })
        PROGRESS.write_text(f"completed_noise={noise}\n", encoding="utf-8")

    write_csv(RESULTS / "evidence_summary.csv", rows)
    write_csv(RESULTS / "noise_ablation.csv", noise_rows)
    write_main_table(rows)
    write_noise_table(noise_rows)
    write_ascii_plot(rows)
    write_readme(rows, noise_rows)
    print(f"wrote {RESULTS / 'evidence_summary.csv'}")
    print(f"wrote {RESULTS / 'noise_ablation.csv'}")


def write_csv(path, rows):
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def pct(x):
    return f"{100.0 * x:.1f}"


def write_main_table(rows):
    wanted_budgets = [0, 2, 4, 6, 8]
    wanted_methods = ["visual_only", "dense_entropy", "dense_contact_only", "critical_cell_entropy", "contact_equivalence"]
    labels = {
        "visual_only": "Visual only",
        "dense_entropy": "Dense entropy",
        "dense_contact_only": "Dense contact-only",
        "critical_cell_entropy": "Critical-cell entropy",
        "contact_equivalence": "Contact-equivalence",
    }
    index = {(r["budget"], r["method"]): r for r in rows}
    lines = []
    lines.append("\\begin{tabular}{lrrrrr}")
    lines.append("\\toprule")
    lines.append("Method & B=0 & B=2 & B=4 & B=6 & B=8 \\\\")
    lines.append("\\midrule")
    for method in wanted_methods:
        vals = [pct(index[(b, method)]["success_rate"]) for b in wanted_budgets]
        lines.append(f"{labels[method]} & " + " & ".join(vals) + " \\\\")
    lines.append("\\bottomrule")
    lines.append("\\end{tabular}")
    (RESULTS / "main_success_table.tex").write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_noise_table(rows):
    wanted_methods = ["dense_entropy", "dense_contact_only", "critical_cell_entropy", "contact_equivalence"]
    labels = {
        "dense_entropy": "Dense entropy",
        "dense_contact_only": "Dense contact-only",
        "critical_cell_entropy": "Critical-cell entropy",
        "contact_equivalence": "Contact-equivalence",
    }
    index = {(r["noise"], r["method"]): r for r in rows}
    lines = []
    lines.append("\\begin{tabular}{lrrrrr}")
    lines.append("\\toprule")
    lines.append("Method & 0\\% & 2\\% & 5\\% & 10\\% & 20\\% \\\\")
    lines.append("\\midrule")
    for method in wanted_methods:
        vals = [pct(index[(n, method)]["success_rate"]) for n in NOISES]
        lines.append(f"{labels[method]} & " + " & ".join(vals) + " \\\\")
    lines.append("\\bottomrule")
    lines.append("\\end{tabular}")
    (RESULTS / "noise_success_table.tex").write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_ascii_plot(rows):
    labels = {
        "visual_only": "visual",
        "dense_entropy": "dense",
        "dense_contact_only": "dctrl",
        "critical_cell_entropy": "cell",
        "contact_equivalence": "equiv",
    }
    lines = ["Success rate by probe budget (each # is about 5 percentage points)", ""]
    for method in ["visual_only", "dense_entropy", "dense_contact_only", "critical_cell_entropy", "contact_equivalence"]:
        lines.append(labels[method])
        for row in rows:
            if row["method"] == method:
                lines.append(f"  B={row['budget']}: " + "#" * int(round(row["success_rate"] * 20)) + f" {pct(row['success_rate'])}%")
        lines.append("")
    (RESULTS / "ascii_success_plot.txt").write_text("\n".join(lines), encoding="utf-8")


def write_readme(rows, noise_rows):
    by_key = {(r["budget"], r["method"]): r for r in rows}
    ce4 = by_key[(4, "contact_equivalence")]["success_rate"]
    dense4 = by_key[(4, "dense_entropy")]["success_rate"]
    dense_contact4 = by_key[(4, "dense_contact_only")]["success_rate"]
    cell4 = by_key[(4, "critical_cell_entropy")]["success_rate"]
    text = f"""# Runnable Evidence

The simulation is a controlled hidden-geometry task. Vision censors a hidden insertion channel among {LANES} possible lanes and also censors {DECOR_BITS} irrelevant decorative bits. The manipulation succeeds only if the robot chooses the true hidden channel. All methods receive the same probe budget and probe library.

The key distinction is objective, not sensor access:

- Dense entropy greedily reduces entropy of the full hidden geometry, so it spends early probes on irrelevant decorative bits.
- Dense contact-only is a boundary control that removes the irrelevant decorative probes from the dense objective.
- Critical-cell entropy probes lane cells, so it attacks the right variable but only by one lane at a time.
- Contact-equivalence chooses tactile sweeps that split the manipulation contact outcome class.

At budget 4 with noiseless probes, contact-equivalence reaches {pct(ce4)}% success, dense entropy reaches {pct(dense4)}%, dense contact-only reaches {pct(dense_contact4)}%, and critical-cell entropy reaches {pct(cell4)}%. The contact-only control marks the boundary: once irrelevant hidden geometry is removed from the dense state, dense entropy and contact-equivalence agree.

Run:

```powershell
python experiments/tactile_occlusion_sim.py
```

Outputs:

- `results/evidence_summary.csv`
- `results/noise_ablation.csv`
- `results/main_success_table.tex`
- `results/noise_success_table.tex`
- `results/ascii_success_plot.txt`
"""
    (RESULTS / "README.md").write_text(text, encoding="utf-8")


def outputs_complete():
    for path in REQUIRED_OUTPUTS:
        if not path.exists() or path.stat().st_size == 0:
            return False
    with (RESULTS / "evidence_summary.csv").open("r", encoding="utf-8", newline="") as f:
        if sum(1 for _ in csv.DictReader(f)) < len(BUDGETS) * len(METHODS):
            return False
    with (RESULTS / "noise_ablation.csv").open("r", encoding="utf-8", newline="") as f:
        if sum(1 for _ in csv.DictReader(f)) < len(NOISES) * len(METHODS):
            return False
    return True


if __name__ == "__main__":
    if "--force" not in sys.argv and "--quick" not in sys.argv and outputs_complete():
        print(f"reusing complete simulation outputs in {RESULTS}")
        sys.exit(0)
    if "--quick" in sys.argv:
        TRIALS = 300
        run_all(trials=TRIALS)
    else:
        run_all()
