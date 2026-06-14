# Child Status: 05_tactile_occlusion_reasoning

## Current Stage

Stage 9: final full-scale pass complete. This changeset records the 27-page final manuscript, full-scale evidence, refreshed docs, and verified canonical PDF.

## Last Completed Step

- Compiled the final manuscript to 27 pages.
- Verified `C:/Users/wangz/Downloads/05.pdf` at 1,040,865 bytes.
- Verified expected text claims in the canonical PDF: 10,120 compact rows, 242,880 evaluated trials counted across rows, dense entropy 0.083, and 20% symmetric-noise contact-equivalence 0.442.
- Verified no stale hardening/workshop markers in extracted final PDF text.

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

## Next Step

- Proceed to paper 06 after this final full-scale changeset is pushed.
