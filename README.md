# Tactile Occlusion Reasoning

This repository contains the paper package for `05_tactile_occlusion_reasoning`.

## Thesis

Robotic manipulation under visual occlusion should reason over contact-equivalence classes rather than single reconstructed shapes. Two hidden geometries are equivalent for the current manipulation step when every relevant contact would have the same outcome. Tactile probes should split those classes instead of reconstructing all visually censored geometry.

## Key Files

- `paper/main.tex`: anonymous ICLR-style manuscript.
- `paper/references.bib`: sanitized bibliography.
- `experiments/tactile_occlusion_sim.py`: runnable controlled evidence.
- `results/`: cached tables and CSV outputs from the simulation.
- `docs/submission_readiness_decision.md`: v2 submission decision.
- `docs/submission_attack_log.md`: hostile submission-hardening audit.
- `docs/related_work_matrix.csv`: 1332-entry literature matrix.
- `docs/literature_map.md`: landscape, skim, and deep-read summary.
- `docs/hostile_prior_work.md`: 100-paper hostile prior-work set.
- `docs/novelty_boundary_map.md`: hidden assumptions and boundary claims.
- `docs/final_audit.md`: final readiness audit.

## Run Evidence

```powershell
python experiments/tactile_occlusion_sim.py
```

The script reuses complete cached outputs unless run with `--force`.

## Submission-Hardening v2

The v2 pass adds a dense contact-only boundary control. At budget 4 over 2000
trials, full dense entropy reaches 8.6% success after spending all four probes
on irrelevant decorative bits; critical-cell entropy reaches 41.5%;
contact-equivalence reaches 100.0%; and dense contact-only also reaches 100.0%.
The supported claim is therefore narrow: contact-equivalence helps when visually
hidden state contains manipulation-irrelevant degrees of freedom, not when an
oracle has already filtered the state to contact-relevant variables.

## Build Paper

From `paper/`:

```powershell
pdflatex -interaction=nonstopmode -halt-on-error main.tex
bibtex main
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
```

The required final PDF for the batch is saved outside the repo at:

```text
C:/Users/wangz/Downloads/05.pdf
```
