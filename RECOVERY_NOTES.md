# Paper 05 Recovery Notes

The next retry should resume from existing artifacts rather than restarting expensive work.

## Valid Artifacts To Reuse
- `docs/related_work_matrix.csv` has 1332 rows.
- `docs/literature_map.md`, `docs/hostile_prior_work.md`, `docs/novelty_boundary_map.md`, `docs/novelty_decision.md`, `docs/claims.md`, and `docs/reviewer_attacks.md` already exist.
- `results/evidence_summary.csv`, `results/noise_ablation.csv`, `results/main_success_table.tex`, `results/noise_success_table.tex`, `results/ascii_success_plot.txt`, and `results/README.md` are complete.
- `experiments/tactile_occlusion_sim.py` has been patched so `python experiments\tactile_occlusion_sim.py` reuses complete outputs and exits quickly unless forced.
- ICLR 2026 template files have been copied into `paper/`: `iclr2026_conference.sty`, `iclr2026_conference.bst`, `math_commands.tex`, `fancyhdr.sty`, and `natbib.sty`.

## Failures Already Seen
- Attempt 1 generated complete simulation outputs but the long simulation command hit a tool timeout before paper build.
- Attempt 2 recovered the simulation cache, then failed on a brittle inline PowerShell bibliography lookup command with a nonzero exit before manuscript/PDF creation.

## Required Recovery Path
1. Do not rerun literature retrieval or force the full simulation.
2. Use the existing literature docs and top rows from `docs/related_work_matrix.csv`; if extra filtering is needed, write a short `.py` helper or use a caught PowerShell command that always records the finding and exits 0.
3. Continue directly with `paper/main.tex`, `paper/references.bib`, top-level `README.md`, and `docs/final_audit.md`.
4. Compile from `paper/` using direct `pdflatex`, `bibtex`, `pdflatex`, `pdflatex` with explicit generous timeouts.
5. Copy the final PDF to `C:/Users/wangz/Downloads/05.pdf`.
6. Commit, create/push public GitHub repo `05_tactile_occlusion_reasoning`, and record the URL in `docs/final_audit.md`.

