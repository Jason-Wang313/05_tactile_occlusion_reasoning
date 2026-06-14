# Reproducibility Checklist

- [x] Full-scale script: `experiments/run_full_scale_tactile_occlusion.py`
- [x] Original v2 script retained: `experiments/tactile_occlusion_sim.py`
- [x] Full-scale outputs: `results/full_scale/*.csv`
- [x] Full-scale summary: `results/full_scale/full_scale_summary.json`
- [x] Full-scale figures: `results/full_scale/figures/*.png`
- [x] Manuscript figures copied to `paper/figures/`
- [x] Paper source: `paper/main.tex`
- [x] Bibliography source: `paper/references.bib`
- [x] Canonical PDF target: `C:/Users/wangz/Downloads/05.pdf`
- [x] Verified canonical PDF page count: 27 pages
- [x] Verified canonical PDF size: 1,040,865 bytes
- [x] Final LaTeX/BibTeX build completed with no unresolved citations or references.
- [x] Final PDF text scan found expected scale claims and no stale hardening/workshop markers.
- [x] Random seeds are deterministic and recorded through the runner's suite/seed schedule.
- [x] Full-scale run uses compact rows and sequential suites to keep memory light.
- [ ] External environment lockfile; not present in this minimal Python/LaTeX repo.

## Reproduction Commands

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
