# Experiment Rigor Checklist

- [x] Detailed full-scale execution plan written before editing the paper.
- [x] Same probe budgets used across compared methods.
- [x] Same hidden-lane task family and probe library used within each suite condition.
- [x] Final full-scale runner stores compact metrics rather than raw trajectories.
- [x] Main budget sweep regenerated with seed scale 10 and 24 trials per seed/condition.
- [x] Decorative-bit scaling regenerated for 0, 16, 64, 128, and 256 bits.
- [x] Contact-class/lane scaling regenerated for multiple lane counts.
- [x] Noise taxonomy includes symmetric, false-positive, false-negative, and drift-like noise.
- [x] Prior stress includes uniform, skewed, bimodal, and visually narrowed priors.
- [x] Probe-library ablations include mixed, cells-only, sweeps-only, balanced-only, and contact-only controls.
- [x] Negative controls include no-decor, oracle-filtered, decor-dominant, and cells-only/no-sweeps cases.
- [x] Boundary control preserved: dense contact-only reaches 1.000 when irrelevant probes are filtered.
- [x] Final manuscript compiled to 27 pages and verified before copying to the canonical PDF path.
- [ ] Real tactile sensor validation.
- [ ] Realistic 3D geometry or physics validation.
- [ ] Learned policy or learned reconstruction planner comparison.
