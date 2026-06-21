# Child Status: 05_tactile_occlusion_reasoning

## Current Stage

VLA-style boxed-link hardening complete. This changeset records the same
27-page final manuscript and full-scale evidence, with the final canonical PDF
rebuilt to remove cyan link boxes and match the visible VLA-v4 role model.

## Last Completed Step

- Compiled the final manuscript to 27 pages.
- Added explicit VLA-style boxed-link policy after the existing `hyperref` import in `paper/main.tex`.
- Verified `C:/Users/wangz/Downloads/05.pdf` at 1,040,865 bytes with SHA256 `BF717DB37975A5CC91C024F8936DCFE78C55C32DC6605D07BFDCBE9E6D0E570E`.
- Verified final link inventory: 96 annotations on pages `[(1, 15), (2, 35), (3, 8), (4, 4), (6, 2), (7, 2), (10, 6), (11, 9), (12, 9), (13, 6)]`; colors green = 87, red = 9, cyan = 0; all borders `(0, 0, 1)`.
- Rendered and visually inspected pages 1, 2, 3, 4, 6, 7, 10, 11, 12, and 13; highlighted boxes are crisp and aligned.
- Verified expected text claims in the canonical PDF: 10,120 compact rows, 242,880 evaluated trials counted across rows, dense entropy 0.083, and 20% symmetric-noise contact-equivalence 0.442.
- Verified no stale hardening/workshop markers in extracted final PDF text.
- Verified no duplicate `C:/Users/wangz/Downloads/5.pdf` was created.

## Full-Scale Evidence

- Runner: `experiments/run_full_scale_tactile_occlusion.py`
- Seed scale: 10
- Trials per seed/condition: 24
- Compact metric rows: 10,120
- Evaluated trials counted across rows: 242,880
- Figures: `paper/figures/*.png`

## Main Budget-4 Result

- Dense entropy: 0.083
- Dense contact-only: 1.000
- Critical-cell entropy: 0.425
- Contact-equivalence: 1.000
- Expected regret: 0.825
- Sampled equivalence: 0.967

## Final PDF

- Canonical path: `C:/Users/wangz/Downloads/05.pdf`
- Page count: 27
- Size: 1,040,865 bytes
- SHA256: `BF717DB37975A5CC91C024F8936DCFE78C55C32DC6605D07BFDCBE9E6D0E570E`
- VLA-style link inventory: 96 annotations, green = 87, red = 9, cyan = 0, all borders `(0, 0, 1)`

## Next Step

- Proceed to paper 04 after this VLA-style boxed-link hardening changeset is pushed.
