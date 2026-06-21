# Submission Version Log

## v3 - 2026-06-14

- Wrote the full-scale execution plan before editing the paper.
- Added `experiments/run_full_scale_tactile_occlusion.py`.
- Ran seven full-scale suites sequentially with seed scale 10 and 24 trials per seed/condition.
- Generated 10,120 compact metric rows and 242,880 evaluated trials counted across rows.
- Added full-scale figures and copied them into `paper/figures/`.
- Rewrote the manuscript into a 27-page final synthetic mechanism paper.
- Added expanded appendices covering artifact inventory, formal notes, probe design, metric interpretation, implementation guidance, hardware-validation protocol, failure modes, and final audit checks.
- Verified `C:/Users/wangz/Downloads/05.pdf` at 27 pages and 1,040,865 bytes.

## Final-link-hardening - 2026-06-21

- Added explicit VLA-style `\hypersetup` policy after the existing `hyperref` import; the prior final PDF had 30 cyan link boxes.
- Rebuilt from `paper/` with `pdflatex`, `bibtex`, `pdflatex`, `pdflatex`.
- Canonical PDF: `C:/Users/wangz/Downloads/05.pdf` (27 pages, 1,040,865 bytes).
- SHA256: `BF717DB37975A5CC91C024F8936DCFE78C55C32DC6605D07BFDCBE9E6D0E570E`.
- Link inventory: 96 annotations on pages `[(1, 15), (2, 35), (3, 8), (4, 4), (6, 2), (7, 2), (10, 6), (11, 9), (12, 9), (13, 6)]`; green = 87, red = 9, cyan = 0; all borders `(0, 0, 1)`.
- Rendered pages 1, 2, 3, 4, 6, 7, 10, 11, 12, and 13 after export and confirmed crisp green citation/URL boxes and red internal-reference boxes.
- Local `paper/main.pdf` removed after the canonical copy.
- No additional `C:/Users/wangz/Downloads/5.pdf` duplicate was created.

## v2 - 2026-06-12

- Added dense contact-only boundary control to the original simulator.
- Regenerated 2000-trial evidence and noise ablations for the short manuscript.
- Narrowed the claim to settings where irrelevant hidden variables remain in the dense hidden state.

## v1 - 2026-06-11

- Initial paper package, literature audit, synthetic evidence, compiled PDF, and GitHub push.
