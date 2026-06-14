# Runnable Evidence

The final evidence is a controlled hidden-geometry task. Vision censors a hidden contact lane and also censors decorative hidden variables that are informative to touch but irrelevant to the current manipulation outcome. The manipulation succeeds only if the robot resolves the contact class needed by the pending action.

## Final Full-Scale Suite

Run:

```powershell
python experiments/run_full_scale_tactile_occlusion.py --suite main --seed-scale 10 --trials 24 --fresh
python experiments/run_full_scale_tactile_occlusion.py --suite decor --seed-scale 10 --trials 24
python experiments/run_full_scale_tactile_occlusion.py --suite lanes --seed-scale 10 --trials 24
python experiments/run_full_scale_tactile_occlusion.py --suite noise --seed-scale 10 --trials 24
python experiments/run_full_scale_tactile_occlusion.py --suite prior --seed-scale 10 --trials 24
python experiments/run_full_scale_tactile_occlusion.py --suite library --seed-scale 10 --trials 24
python experiments/run_full_scale_tactile_occlusion.py --suite negative --seed-scale 10 --trials 24
python experiments/run_full_scale_tactile_occlusion.py --suite summarize --seed-scale 10
```

Outputs:

- `results/full_scale/main_budget.csv`
- `results/full_scale/decor_scaling.csv`
- `results/full_scale/lane_scaling.csv`
- `results/full_scale/noise_taxonomy.csv`
- `results/full_scale/prior_stress.csv`
- `results/full_scale/probe_library.csv`
- `results/full_scale/negative_controls.csv`
- `results/full_scale/full_scale_summary.json`
- `results/full_scale/figures/*.png`

## Scale

- Compact metric rows: 10,120
- Evaluated trials counted across rows: 242,880

## Main Budget-4 Readout

- Dense entropy: 0.083 success.
- Dense contact-only: 1.000 success.
- Critical-cell entropy: 0.425 success.
- Contact-equivalence: 1.000 success.
- Expected-regret probing: 0.825 success.
- Sampled equivalence: 0.967 success.

## Original Short-Run Evidence

The earlier v2 script remains available:

```powershell
python experiments/tactile_occlusion_sim.py
```

Its cached outputs are retained for continuity:

- `results/evidence_summary.csv`
- `results/noise_ablation.csv`
- `results/main_success_table.tex`
- `results/noise_success_table.tex`
- `results/ascii_success_plot.txt`
