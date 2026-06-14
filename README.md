# Tactile Occlusion Reasoning

This repository contains the final full-scale paper package for `05_tactile_occlusion_reasoning`.

## Thesis

Robotic manipulation under visual occlusion should reason over contact-equivalence classes rather than single reconstructed shapes. Two hidden geometries are equivalent for the current manipulation step when every relevant contact would have the same outcome. Tactile probes should split those classes instead of reconstructing all visually censored geometry.

## Final Artifact

- Canonical PDF: `C:/Users/wangz/Downloads/05.pdf`
- Verified page count: 27 pages
- Verified PDF size: 1,040,865 bytes
- Full-scale compact metric rows: 10,120
- Evaluated trials counted across rows: 242,880

The final manuscript is synthetic but substantially expanded beyond the earlier short version. It includes main budget curves, decorative-variable scaling, contact-class scaling, tactile noise taxonomy, prior stress, probe-library ablations, boundary controls, approximate quotient probing, formal notes, implementation guidance, hardware-validation protocol, and failure-mode analysis.

## Key Files

- `paper/main.tex`: anonymous ICLR-style manuscript.
- `paper/references.bib`: sanitized bibliography.
- `experiments/tactile_occlusion_sim.py`: original v2 controlled simulator.
- `experiments/run_full_scale_tactile_occlusion.py`: final full-scale suite runner.
- `results/full_scale/`: compact CSV outputs, summary JSON, and figures from the final run.
- `paper/figures/`: figures copied into the manuscript build.
- `docs/full_scale_execution_plan.md`: detailed pre-edit execution plan.
- `docs/full_scale_results_summary.md`: final result summary for the expanded suite.
- `docs/final_audit.md`: final readiness audit.

## Run Full-Scale Evidence

Run suites sequentially to keep memory usage light:

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

## Main Budget-4 Result

At budget four in the final main suite:

- Dense entropy: 0.083 success.
- Dense contact-only: 1.000 success.
- Critical-cell entropy: 0.425 success.
- Contact-equivalence: 1.000 success.
- Expected-regret probing: 0.825 success.
- Sampled equivalence: 0.967 success.

The supported claim remains narrow: contact-equivalence helps when visually hidden state contains manipulation-irrelevant degrees of freedom. It is not an advantage over an oracle that has already filtered the state to contact-relevant variables.

## Build Paper

From `paper/`:

```powershell
pdflatex -interaction=nonstopmode -halt-on-error main.tex
bibtex main
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
```
