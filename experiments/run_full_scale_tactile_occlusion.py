"""Full-scale tactile occlusion reasoning experiments.

The original simulator isolates the core mechanism but is intentionally narrow.
This runner expands the synthetic evidence while keeping memory use low: it
stores compact per-condition metrics, not raw trajectories.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import random
import shutil
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Sequence, Tuple

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results" / "full_scale"
FIG_OUT = OUT / "figures"
PAPER_FIG = ROOT / "paper" / "figures"
PROGRESS = OUT / "progress.txt"


@dataclass(frozen=True)
class Probe:
    name: str
    kind: str
    payload: Tuple[int, ...]
    size: int = 1


@dataclass(frozen=True)
class Config:
    lanes: int = 12
    decor_bits: int = 64
    decor_group: int = 4
    library: str = "mixed"
    contact_relevant_decor: bool = False


@dataclass(frozen=True)
class Noise:
    mode: str = "none"
    rate: float = 0.0

    @property
    def false_positive(self) -> float:
        if self.mode in {"none", "clean"}:
            return 0.0
        if self.mode in {"symmetric", "drift"}:
            return self.rate
        if self.mode == "false_positive":
            return self.rate
        if self.mode == "false_negative":
            return 0.0
        return self.rate

    @property
    def false_negative(self) -> float:
        if self.mode in {"none", "clean"}:
            return 0.0
        if self.mode in {"symmetric", "drift"}:
            return self.rate
        if self.mode == "false_positive":
            return 0.0
        if self.mode == "false_negative":
            return self.rate
        return self.rate


METHODS_MAIN = (
    "visual_only",
    "random",
    "dense_entropy",
    "dense_contact_only",
    "critical_cell_entropy",
    "contact_equivalence",
    "hybrid_25",
    "hybrid_50",
    "expected_regret",
    "sampled_equivalence",
)


def ensure_dirs() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    FIG_OUT.mkdir(parents=True, exist_ok=True)
    PAPER_FIG.mkdir(parents=True, exist_ok=True)


def log(message: str) -> None:
    ensure_dirs()
    with PROGRESS.open("a", encoding="utf-8") as f:
        f.write(message + "\n")
    print(message, flush=True)


def entropy(probs: Sequence[float]) -> float:
    total = sum(probs)
    if total <= 0:
        return 0.0
    out = 0.0
    for value in probs:
        if value <= 0:
            continue
        q = value / total
        out -= q * math.log(q, 2)
    return out


def binary_entropy(p: float) -> float:
    if p <= 0.0 or p >= 1.0:
        return 0.0
    return -p * math.log(p, 2) - (1 - p) * math.log(1 - p, 2)


def normalize(weights: List[float]) -> List[float]:
    total = sum(weights)
    if total <= 0:
        return [1.0 / len(weights) for _ in weights]
    return [w / total for w in weights]


def make_prior(lanes: int, mode: str, rng: random.Random) -> List[float]:
    if mode == "uniform":
        return [1.0 / lanes for _ in range(lanes)]
    if mode == "skewed":
        raw = [math.exp(-0.22 * i) for i in range(lanes)]
        rng.shuffle(raw)
        return normalize(raw)
    if mode == "bimodal":
        centers = [lanes // 4, (3 * lanes) // 4]
        raw = []
        for i in range(lanes):
            raw.append(sum(math.exp(-0.55 * abs(i - c)) for c in centers))
        return normalize(raw)
    if mode == "visual_narrow":
        width = max(3, lanes // 3)
        start = rng.randrange(0, max(1, lanes - width + 1))
        raw = [1.0 if start <= i < start + width else 0.0 for i in range(lanes)]
        return normalize(raw)
    raise ValueError(f"unknown prior mode {mode}")


def sample_index(weights: Sequence[float], rng: random.Random) -> int:
    threshold = rng.random()
    running = 0.0
    for i, weight in enumerate(weights):
        running += weight
        if threshold <= running:
            return i
    return len(weights) - 1


def make_probes(config: Config) -> List[Probe]:
    probes: List[Probe] = []
    include_decor = config.library not in {"contact_only", "no_decor"}
    if include_decor and config.decor_bits > 0:
        for start in range(0, config.decor_bits, config.decor_group):
            bits = tuple(range(start, min(start + config.decor_group, config.decor_bits)))
            probes.append(Probe(f"decor_{bits[0]}_{bits[-1]}", "decor", bits, len(bits)))
    if config.library in {"mixed", "cells_only", "contact_only", "no_decor"}:
        for lane in range(config.lanes):
            probes.append(Probe(f"lane_{lane}", "lane", (lane,), 1))
    if config.library in {"mixed", "sweeps_only", "contact_only", "no_decor"}:
        widths = sorted(set([max(1, config.lanes // 2), max(1, config.lanes // 3), max(1, config.lanes // 4), 2, 1]), reverse=True)
        for width in widths:
            if config.library == "sweeps_only" and width == 1:
                continue
            for start in range(0, config.lanes, width):
                subset = tuple(range(start, min(start + width, config.lanes)))
                if 0 < len(subset) < config.lanes:
                    probes.append(Probe(f"sweep_{subset[0]}_{subset[-1]}", "split", subset, len(subset)))
    if config.library == "balanced_only":
        for width in [max(1, config.lanes // 2), max(1, config.lanes // 4)]:
            for start in range(0, config.lanes, width):
                subset = tuple(range(start, min(start + width, config.lanes)))
                if 0 < len(subset) < config.lanes:
                    probes.append(Probe(f"sweep_{subset[0]}_{subset[-1]}", "split", subset, len(subset)))
    return probes


class Belief:
    def __init__(self, weights: Sequence[float], decor_bits: int):
        self.weights = list(weights)
        self.decor_bits = decor_bits
        self.decor_known: set[int] = set()
        self.used: set[str] = set()

    def copy(self) -> "Belief":
        other = Belief(self.weights, self.decor_bits)
        other.decor_known = set(self.decor_known)
        other.used = set(self.used)
        return other

    def h_contact(self) -> float:
        return entropy(self.weights)

    def h_full(self) -> float:
        return self.h_contact() + max(0, self.decor_bits - len(self.decor_known))

    def regret(self) -> float:
        return 1.0 - max(self.weights)

    def p_truth(self, probe: Probe) -> float:
        if probe.kind == "decor":
            return 0.5
        if probe.kind == "lane":
            return self.weights[probe.payload[0]]
        subset = set(probe.payload)
        return sum(w for i, w in enumerate(self.weights) if i in subset)

    def obs_prob(self, probe: Probe, noise: Noise) -> float:
        p_true = self.p_truth(probe)
        fp = noise.false_positive
        fn = noise.false_negative
        if noise.mode == "drift":
            fp = min(0.45, noise.rate * (1.0 + len(self.used) / 10.0))
            fn = fp
        return p_true * (1 - fn) + (1 - p_true) * fp

    def update(self, probe: Probe, obs: bool | Tuple[bool, ...], noise: Noise, hypothetical: bool = False) -> None:
        if not hypothetical:
            self.used.add(probe.name)
        if probe.kind == "decor":
            for bit in probe.payload:
                self.decor_known.add(bit)
            return
        fp = noise.false_positive
        fn = noise.false_negative
        if noise.mode == "drift":
            fp = min(0.45, noise.rate * (1.0 + len(self.used) / 10.0))
            fn = fp
        subset = set(probe.payload)
        new_weights: List[float] = []
        for i, weight in enumerate(self.weights):
            truth = i in subset
            if obs is True:
                like = (1 - fn) if truth else fp
            else:
                like = fn if truth else (1 - fp)
            new_weights.append(weight * like)
        self.weights = normalize(new_weights)


def expected_after_metric(belief: Belief, probe: Probe, noise: Noise, metric: str) -> float:
    if probe.kind == "decor":
        after = belief.copy()
        after.update(probe, True, noise, hypothetical=True)
        return metric_value(after, metric)
    p_obs_true = belief.obs_prob(probe, noise)
    value = 0.0
    for obs, p_obs in ((True, p_obs_true), (False, 1.0 - p_obs_true)):
        if p_obs <= 1e-12:
            continue
        after = belief.copy()
        after.update(probe, obs, noise, hypothetical=True)
        value += p_obs * metric_value(after, metric)
    return value


def metric_value(belief: Belief, metric: str) -> float:
    if metric == "contact":
        return belief.h_contact()
    if metric == "full":
        return belief.h_full()
    if metric == "regret":
        return belief.regret()
    raise ValueError(metric)


def expected_gain(belief: Belief, probe: Probe, noise: Noise, metric: str) -> float:
    if probe.kind == "decor" and metric == "contact":
        return 0.0
    return metric_value(belief, metric) - expected_after_metric(belief, probe, noise, metric)


def choose_probe(method: str, belief: Belief, probes: Sequence[Probe], noise: Noise, rng: random.Random) -> Probe | None:
    unused = [p for p in probes if p.name not in belief.used]
    if not unused or method == "visual_only":
        return None
    contact = [p for p in unused if p.kind in {"lane", "split"}]
    lane = [p for p in unused if p.kind == "lane"]
    if method == "random":
        return rng.choice(unused)
    if method == "dense_entropy":
        decor = [p for p in unused if p.kind == "decor"]
        if decor:
            return max(decor, key=lambda p: p.size)
        return max(unused, key=lambda p: (expected_gain(belief, p, noise, "full"), p.kind == "decor", p.size))
    if method == "dense_contact_only":
        return max(contact, key=lambda p: (expected_gain(belief, p, noise, "full"), p.kind == "split", p.size)) if contact else None
    if method == "critical_cell_entropy":
        return max(lane, key=lambda p: expected_gain(belief, p, noise, "contact")) if lane else None
    if method == "contact_equivalence":
        return max(contact, key=lambda p: (expected_gain(belief, p, noise, "contact"), p.kind == "split", p.size)) if contact else None
    if method.startswith("hybrid_"):
        lam = float(method.split("_", 1)[1]) / 100.0
        decor = [p for p in unused if p.kind == "decor"]
        if decor and (1 - lam) * max(p.size for p in decor) >= 1.0:
            return max(decor, key=lambda p: p.size)
        return max(unused, key=lambda p: ((1 - lam) * expected_gain(belief, p, noise, "full") + lam * expected_gain(belief, p, noise, "contact"), p.kind == "split"))
    if method == "expected_regret":
        return max(contact, key=lambda p: (expected_gain(belief, p, noise, "regret"), p.kind == "split", p.size)) if contact else None
    if method == "sampled_equivalence":
        if not contact:
            return None
        samples = [sample_index(belief.weights, rng) for _ in range(32)]
        def score(probe: Probe) -> Tuple[float, int, int]:
            subset = set(probe.payload)
            p = sum(1 for s in samples if s in subset) / len(samples)
            return (binary_entropy(p), 1 if probe.kind == "split" else 0, probe.size)
        return max(contact, key=score)
    if method == "oracle_balanced_split":
        return max(contact, key=lambda p: (-abs(0.5 - belief.p_truth(p)), p.kind == "split", p.size)) if contact else None
    raise ValueError(f"unknown method {method}")


def observe(probe: Probe, true_lane: int, rng: random.Random, noise: Noise) -> bool | Tuple[bool, ...]:
    if probe.kind == "decor":
        return tuple(bool(rng.randrange(2)) for _ in probe.payload)
    truth = true_lane in set(probe.payload)
    fp = noise.false_positive
    fn = noise.false_negative
    if noise.mode == "drift":
        fp = noise.rate
        fn = noise.rate
    if truth:
        return False if rng.random() < fn else True
    return True if rng.random() < fp else False


def score(belief: Belief, true_lane: int, rng: random.Random) -> Dict[str, float]:
    max_weight = max(belief.weights)
    winners = [i for i, w in enumerate(belief.weights) if abs(w - max_weight) < 1e-12]
    action = rng.choice(winners)
    return {
        "success": 1.0 if action == true_lane else 0.0,
        "regret": 0.0 if action == true_lane else 1.0,
        "posterior_contact_entropy": belief.h_contact(),
        "posterior_full_entropy": belief.h_full(),
    }


def run_trajectory(method: str, config: Config, probes: Sequence[Probe], max_budget: int, noise: Noise, prior_mode: str, rng: random.Random) -> List[Dict[str, float]]:
    prior = make_prior(config.lanes, prior_mode, rng)
    true_lane = sample_index(prior, rng)
    belief = Belief(prior, config.decor_bits)
    records: List[Dict[str, float]] = []
    score_rng = random.Random(rng.randrange(2**32))
    contact_probes = 0
    decor_probes = 0
    for budget in range(max_budget + 1):
        row = score(belief, true_lane, score_rng)
        row["contact_probes"] = float(contact_probes)
        row["decor_probes"] = float(decor_probes)
        records.append(row)
        if budget == max_budget:
            break
        probe = choose_probe(method, belief, probes, noise, rng)
        if probe is None:
            continue
        obs = observe(probe, true_lane, rng, noise)
        belief.update(probe, obs, noise, hypothetical=False)
        if probe.kind == "decor":
            decor_probes += 1
        else:
            contact_probes += 1
    return records


def mean(values: Sequence[float]) -> float:
    return sum(values) / len(values) if values else 0.0


def run_condition(
    suite: str,
    seed: int,
    methods: Sequence[str],
    budgets: Sequence[int],
    trials: int,
    config: Config,
    noise: Noise,
    prior_mode: str,
    extra: Dict[str, float | str],
) -> List[Dict[str, float | str]]:
    rows: List[Dict[str, float | str]] = []
    max_budget = max(budgets)
    probes = make_probes(config)
    for method in methods:
        stable = sum((i + 1) * ord(ch) for i, ch in enumerate(f"{suite}:{method}:{extra}"))
        rng = random.Random(1_000_000 + 10_000 * seed + stable % 9000)
        accum = {b: [] for b in budgets}
        for _ in range(trials):
            trajectory = run_trajectory(method, config, probes, max_budget, noise, prior_mode, rng)
            for budget in budgets:
                accum[budget].append(trajectory[budget])
        for budget in budgets:
            vals = accum[budget]
            rows.append(
                {
                    "suite": suite,
                    "seed": seed,
                    "method": method,
                    "budget": budget,
                    "trials": trials,
                    "lanes": config.lanes,
                    "decor_bits": config.decor_bits,
                    "library": config.library,
                    "noise_mode": noise.mode,
                    "noise_rate": noise.rate,
                    "prior_mode": prior_mode,
                    **extra,
                    "success_rate": mean([v["success"] for v in vals]),
                    "mean_regret": mean([v["regret"] for v in vals]),
                    "posterior_contact_entropy": mean([v["posterior_contact_entropy"] for v in vals]),
                    "posterior_full_entropy": mean([v["posterior_full_entropy"] for v in vals]),
                    "contact_probes": mean([v["contact_probes"] for v in vals]),
                    "decor_probes": mean([v["decor_probes"] for v in vals]),
                }
            )
    return rows


def write_csv(path: Path, rows: List[Dict[str, float | str]]) -> None:
    ensure_dirs()
    if not rows:
        return
    keys = list(rows[0].keys())
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows(rows)


def run_main(seed_scale: int, trials: int) -> None:
    rows: List[Dict[str, float | str]] = []
    budgets = list(range(0, 11))
    for seed in range(seed_scale):
        rows.extend(
            run_condition(
                "main_budget",
                seed,
                METHODS_MAIN,
                budgets,
                trials,
                Config(lanes=12, decor_bits=64, library="mixed"),
                Noise("none", 0.0),
                "uniform",
                {},
            )
        )
        log(f"main seed={seed} complete")
    write_csv(OUT / "main_budget.csv", rows)


def run_decor(seed_scale: int, trials: int) -> None:
    rows: List[Dict[str, float | str]] = []
    methods = ("dense_entropy", "dense_contact_only", "critical_cell_entropy", "contact_equivalence", "hybrid_50", "expected_regret")
    for decor_bits in (0, 16, 64, 128, 256):
        for seed in range(seed_scale):
            rows.extend(
                run_condition(
                    "decor_scaling",
                    seed,
                    methods,
                    (2, 4, 6, 8),
                    trials,
                    Config(lanes=12, decor_bits=decor_bits, library="mixed"),
                    Noise("none", 0.0),
                    "uniform",
                    {"decor_setting": decor_bits},
                )
            )
        log(f"decor bits={decor_bits} complete")
    write_csv(OUT / "decor_scaling.csv", rows)


def run_lanes(seed_scale: int, trials: int) -> None:
    rows: List[Dict[str, float | str]] = []
    methods = ("dense_entropy", "dense_contact_only", "critical_cell_entropy", "contact_equivalence", "expected_regret", "sampled_equivalence")
    for lanes in (8, 12, 16, 24, 32):
        for seed in range(seed_scale):
            rows.extend(
                run_condition(
                    "lane_scaling",
                    seed,
                    methods,
                    (2, 4, 6, 8, 10),
                    trials,
                    Config(lanes=lanes, decor_bits=64, library="mixed"),
                    Noise("none", 0.0),
                    "uniform",
                    {"lane_setting": lanes},
                )
            )
        log(f"lanes={lanes} complete")
    write_csv(OUT / "lane_scaling.csv", rows)


def run_noise(seed_scale: int, trials: int) -> None:
    rows: List[Dict[str, float | str]] = []
    methods = ("dense_contact_only", "critical_cell_entropy", "contact_equivalence", "expected_regret", "sampled_equivalence")
    for mode in ("symmetric", "false_positive", "false_negative", "drift"):
        for rate in (0.0, 0.02, 0.05, 0.10, 0.20, 0.30):
            for seed in range(seed_scale):
                rows.extend(
                    run_condition(
                        "noise_taxonomy",
                        seed,
                        methods,
                        (4, 6, 8),
                        trials,
                        Config(lanes=12, decor_bits=64, library="mixed"),
                        Noise(mode, rate),
                        "uniform",
                        {},
                    )
                )
            log(f"noise {mode} rate={rate} complete")
    write_csv(OUT / "noise_taxonomy.csv", rows)


def run_prior(seed_scale: int, trials: int) -> None:
    rows: List[Dict[str, float | str]] = []
    methods = ("dense_entropy", "dense_contact_only", "critical_cell_entropy", "contact_equivalence", "expected_regret", "sampled_equivalence")
    for prior_mode in ("uniform", "skewed", "bimodal", "visual_narrow"):
        for seed in range(seed_scale):
            rows.extend(
                run_condition(
                    "prior_stress",
                    seed,
                    methods,
                    (2, 4, 6, 8),
                    trials,
                    Config(lanes=16, decor_bits=64, library="mixed"),
                    Noise("none", 0.0),
                    prior_mode,
                    {},
                )
            )
        log(f"prior {prior_mode} complete")
    write_csv(OUT / "prior_stress.csv", rows)


def run_library(seed_scale: int, trials: int) -> None:
    rows: List[Dict[str, float | str]] = []
    methods = ("dense_entropy", "critical_cell_entropy", "contact_equivalence", "expected_regret")
    for library in ("mixed", "cells_only", "sweeps_only", "balanced_only", "contact_only"):
        for seed in range(seed_scale):
            rows.extend(
                run_condition(
                    "probe_library",
                    seed,
                    methods,
                    (2, 4, 6, 8),
                    trials,
                    Config(lanes=12, decor_bits=64, library=library),
                    Noise("none", 0.0),
                    "uniform",
                    {},
                )
            )
        log(f"library {library} complete")
    write_csv(OUT / "probe_library.csv", rows)


def run_negative(seed_scale: int, trials: int) -> None:
    rows: List[Dict[str, float | str]] = []
    methods = ("dense_entropy", "dense_contact_only", "critical_cell_entropy", "contact_equivalence", "expected_regret", "sampled_equivalence")
    cases = (
        ("no_decor", Config(lanes=12, decor_bits=0, library="mixed")),
        ("oracle_filtered", Config(lanes=12, decor_bits=64, library="contact_only")),
        ("decor_dominates", Config(lanes=12, decor_bits=256, library="mixed")),
        ("cells_only_no_sweeps", Config(lanes=12, decor_bits=64, library="cells_only")),
    )
    for case, config in cases:
        for seed in range(seed_scale):
            rows.extend(
                run_condition(
                    "negative_controls",
                    seed,
                    methods,
                    (2, 4, 6, 8),
                    trials,
                    config,
                    Noise("none", 0.0),
                    "uniform",
                    {"case": case},
                )
            )
        log(f"negative {case} complete")
    write_csv(OUT / "negative_controls.csv", rows)


def agg(df: pd.DataFrame, by: Sequence[str], metrics: Sequence[str]) -> pd.DataFrame:
    grouped = df.groupby(list(by))[list(metrics)].agg(["mean", "sem"]).reset_index()
    grouped.columns = ["_".join([str(x) for x in col if str(x)]) for col in grouped.columns.to_flat_index()]
    return grouped


def plot_lines(df: pd.DataFrame, x: str, y: str, group: str, path: Path, title: str, xlabel: str, ylabel: str) -> None:
    fig, ax = plt.subplots(figsize=(7.2, 4.8))
    colors = ["#2f6f73", "#a1424a", "#536c9e", "#9a6b3f", "#6c6f7d", "#7c5c92", "#3d7f4f", "#8c5b4c"]
    for idx, (name, sub) in enumerate(df.groupby(group)):
        g = sub.groupby(x)[y].agg(["mean", "sem"]).reset_index()
        ax.errorbar(g[x], g["mean"], yerr=1.96 * g["sem"].fillna(0), marker="o", lw=2, capsize=3, label=str(name).replace("_", " "), color=colors[idx % len(colors)])
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_ylim(bottom=0)
    ax.grid(alpha=0.25)
    ax.legend(frameon=False, fontsize=8)
    fig.tight_layout()
    fig.savefig(path, dpi=220)
    plt.close(fig)


def plot_heat(df: pd.DataFrame, path: Path) -> None:
    sub = df[(df["method"].isin(["dense_entropy", "contact_equivalence"])) & (df["budget"] == 4)]
    pivot = sub.pivot_table(index="decor_bits", columns="method", values="success_rate", aggfunc="mean")
    fig, ax = plt.subplots(figsize=(6.0, 4.6))
    for method in pivot.columns:
        ax.plot(pivot.index, pivot[method], marker="o", lw=2, label=method.replace("_", " "))
    ax.set_xlabel("decorative hidden bits")
    ax.set_ylabel("success rate at budget 4")
    ax.set_title("Irrelevant hidden-state scaling")
    ax.grid(alpha=0.25)
    ax.legend(frameon=False)
    fig.tight_layout()
    fig.savefig(path, dpi=220)
    plt.close(fig)


def summarize(seed_scale: int) -> None:
    ensure_dirs()
    figs: List[str] = []
    if (OUT / "main_budget.csv").exists():
        main = pd.read_csv(OUT / "main_budget.csv")
        keep = main[main["method"].isin(["visual_only", "dense_entropy", "dense_contact_only", "critical_cell_entropy", "contact_equivalence", "expected_regret", "sampled_equivalence"])]
        plot_lines(keep, "budget", "success_rate", "method", FIG_OUT / "main_success_budget.png", "Main tactile occlusion benchmark", "probe budget", "success rate")
        figs.append("main_success_budget.png")
        alloc = keep[keep["method"].isin(["dense_entropy", "contact_equivalence"])]
        plot_lines(alloc, "budget", "decor_probes", "method", FIG_OUT / "probe_allocation.png", "Decorative probe allocation", "probe budget", "decorative probes")
        figs.append("probe_allocation.png")
    if (OUT / "decor_scaling.csv").exists():
        decor = pd.read_csv(OUT / "decor_scaling.csv")
        plot_heat(decor, FIG_OUT / "decor_scaling.png")
        figs.append("decor_scaling.png")
    if (OUT / "lane_scaling.csv").exists():
        lanes = pd.read_csv(OUT / "lane_scaling.csv")
        sub = lanes[(lanes["budget"] == 6) & (lanes["method"].isin(["critical_cell_entropy", "contact_equivalence", "expected_regret", "sampled_equivalence"]))]
        plot_lines(sub, "lanes", "success_rate", "method", FIG_OUT / "lane_scaling.png", "Contact-class count scaling", "lanes", "success rate at budget 6")
        figs.append("lane_scaling.png")
    if (OUT / "noise_taxonomy.csv").exists():
        noise = pd.read_csv(OUT / "noise_taxonomy.csv")
        sub = noise[(noise["budget"] == 4) & (noise["method"] == "contact_equivalence")]
        plot_lines(sub, "noise_rate", "success_rate", "noise_mode", FIG_OUT / "noise_taxonomy.png", "Tactile noise taxonomy", "noise rate", "success rate at budget 4")
        figs.append("noise_taxonomy.png")
    if (OUT / "prior_stress.csv").exists():
        prior = pd.read_csv(OUT / "prior_stress.csv")
        sub = prior[(prior["budget"] == 4) & (prior["method"].isin(["dense_entropy", "contact_equivalence", "expected_regret", "sampled_equivalence"]))]
        plot_lines(sub, "prior_mode", "success_rate", "method", FIG_OUT / "prior_stress.png", "Prior and visual-censoring stress", "prior mode", "success rate")
        figs.append("prior_stress.png")
    if (OUT / "probe_library.csv").exists():
        lib = pd.read_csv(OUT / "probe_library.csv")
        sub = lib[(lib["budget"] == 4) & (lib["method"].isin(["dense_entropy", "contact_equivalence", "expected_regret"]))]
        plot_lines(sub, "library", "success_rate", "method", FIG_OUT / "probe_library.png", "Probe-library ablation", "library", "success rate")
        figs.append("probe_library.png")
    if (OUT / "negative_controls.csv").exists():
        neg = pd.read_csv(OUT / "negative_controls.csv")
        sub = neg[(neg["budget"] == 4) & (neg["method"].isin(["dense_entropy", "dense_contact_only", "contact_equivalence", "expected_regret"]))]
        plot_lines(sub, "case", "success_rate", "method", FIG_OUT / "negative_controls.png", "Boundary and negative controls", "case", "success rate")
        figs.append("negative_controls.png")
    for fig in figs:
        shutil.copy2(FIG_OUT / fig, PAPER_FIG / fig)

    csv_files = sorted(path.name for path in OUT.glob("*.csv"))
    total_rows = 0
    total_trials = 0
    for csv_name in csv_files:
        df = pd.read_csv(OUT / csv_name)
        total_rows += len(df)
        if "trials" in df.columns:
            total_trials += int(pd.to_numeric(df["trials"], errors="coerce").fillna(0).sum())
    summary: Dict[str, object] = {
        "seed_scale": seed_scale,
        "csv_files": csv_files,
        "figure_files": figs,
        "compact_metric_rows": total_rows,
        "evaluated_trials_counting_rows": total_trials,
    }
    if (OUT / "main_budget.csv").exists():
        main = pd.read_csv(OUT / "main_budget.csv")
        b4 = main[main["budget"] == 4].groupby("method")["success_rate"].mean()
        for method in ["dense_entropy", "dense_contact_only", "critical_cell_entropy", "contact_equivalence", "expected_regret", "sampled_equivalence"]:
            if method in b4:
                summary[f"main_b4_{method}"] = float(b4[method])
    (OUT / "full_scale_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    write_markdown_summary(summary)
    log("summarize complete")


def read_mean(csv_name: str, filters: Dict[str, object], metric: str = "success_rate") -> float:
    df = pd.read_csv(OUT / csv_name)
    for key, value in filters.items():
        df = df[df[key] == value]
    return float(df[metric].mean())


def write_markdown_summary(summary: Dict[str, object]) -> None:
    lines = [
        "# Full-Scale Tactile Occlusion Results Summary",
        "",
        "The expanded suite remains synthetic. It tests whether tactile probes should split contact-equivalence classes rather than dense hidden geometry when visually hidden variables include manipulation-irrelevant degrees of freedom.",
        "",
        "## Scale",
        f"- Seed scale: `{summary.get('seed_scale')}`.",
        f"- Compact metric rows: `{summary.get('compact_metric_rows')}`.",
        f"- Evaluated trials counted across rows: `{summary.get('evaluated_trials_counting_rows')}`.",
        "",
        "## Main Budget-4 Readout",
    ]
    for method in ["dense_entropy", "dense_contact_only", "critical_cell_entropy", "contact_equivalence", "expected_regret", "sampled_equivalence"]:
        key = f"main_b4_{method}"
        if key in summary:
            lines.append(f"- `{method}` success: `{float(summary[key]):.3f}`.")
    try:
        decor_dense_256 = read_mean("decor_scaling.csv", {"decor_bits": 256, "budget": 4, "method": "dense_entropy"})
        decor_equiv_256 = read_mean("decor_scaling.csv", {"decor_bits": 256, "budget": 4, "method": "contact_equivalence"})
        decor_dense_0 = read_mean("decor_scaling.csv", {"decor_bits": 0, "budget": 4, "method": "dense_entropy"})
        decor_equiv_0 = read_mean("decor_scaling.csv", {"decor_bits": 0, "budget": 4, "method": "contact_equivalence"})
        lines.extend(
            [
                "",
                "## Irrelevant Hidden-State Scaling",
                f"- With 256 decorative bits at budget 4, dense entropy success is `{decor_dense_256:.3f}` and contact-equivalence is `{decor_equiv_256:.3f}`.",
                f"- With 0 decorative bits at budget 4, dense entropy success is `{decor_dense_0:.3f}` and contact-equivalence is `{decor_equiv_0:.3f}`.",
            ]
        )
    except Exception as exc:
        lines.append(f"- Decor scaling unavailable: `{exc}`.")
    try:
        sym20 = read_mean("noise_taxonomy.csv", {"noise_mode": "symmetric", "noise_rate": 0.20, "budget": 4, "method": "contact_equivalence"})
        fp20 = read_mean("noise_taxonomy.csv", {"noise_mode": "false_positive", "noise_rate": 0.20, "budget": 4, "method": "contact_equivalence"})
        fn20 = read_mean("noise_taxonomy.csv", {"noise_mode": "false_negative", "noise_rate": 0.20, "budget": 4, "method": "contact_equivalence"})
        lines.extend(
            [
                "",
                "## Noise Taxonomy",
                f"- Contact-equivalence at 20% symmetric noise: `{sym20:.3f}`.",
                f"- Contact-equivalence at 20% false-positive noise: `{fp20:.3f}`.",
                f"- Contact-equivalence at 20% false-negative noise: `{fn20:.3f}`.",
            ]
        )
    except Exception as exc:
        lines.append(f"- Noise taxonomy unavailable: `{exc}`.")
    lines.extend(["", "## Figures"])
    for fig in summary.get("figure_files", []):
        lines.append(f"- `paper/figures/{fig}`")
    lines.append("")
    (OUT / "full_scale_results_summary.md").write_text("\n".join(lines), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--suite", choices=("all", "main", "decor", "lanes", "noise", "prior", "library", "negative", "summarize"), default="all")
    parser.add_argument("--seed-scale", type=int, default=20)
    parser.add_argument("--trials", type=int, default=240)
    parser.add_argument("--fresh", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    ensure_dirs()
    if args.fresh:
        for path in OUT.glob("*.csv"):
            path.unlink()
        if PROGRESS.exists():
            PROGRESS.unlink()
    log(f"full-scale tactile suite={args.suite} seed_scale={args.seed_scale} trials={args.trials}")
    if args.suite in {"all", "main"}:
        run_main(args.seed_scale, args.trials)
    if args.suite in {"all", "decor"}:
        run_decor(args.seed_scale, args.trials)
    if args.suite in {"all", "lanes"}:
        run_lanes(args.seed_scale, args.trials)
    if args.suite in {"all", "noise"}:
        run_noise(args.seed_scale, args.trials)
    if args.suite in {"all", "prior"}:
        run_prior(args.seed_scale, args.trials)
    if args.suite in {"all", "library"}:
        run_library(args.seed_scale, args.trials)
    if args.suite in {"all", "negative"}:
        run_negative(args.seed_scale, args.trials)
    if args.suite in {"all", "summarize"}:
        summarize(args.seed_scale)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
