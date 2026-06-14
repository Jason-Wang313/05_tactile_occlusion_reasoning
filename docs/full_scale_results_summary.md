# Full-Scale Tactile Occlusion Results Summary

The expanded suite remains synthetic. It tests whether tactile probes should split contact-equivalence classes rather than dense hidden geometry when visually hidden variables include manipulation-irrelevant degrees of freedom.

## Scale

- Seed scale: `10`.
- Compact metric rows: `10120`.
- Evaluated trials counted across rows: `242880`.

## Main Budget-4 Readout

- `dense_entropy` success: `0.083`.
- `dense_contact_only` success: `1.000`.
- `critical_cell_entropy` success: `0.425`.
- `contact_equivalence` success: `1.000`.
- `expected_regret` success: `0.825`.
- `sampled_equivalence` success: `0.967`.

## Irrelevant Hidden-State Scaling

- With 256 decorative bits at budget 4, dense entropy success is `0.079` and contact-equivalence is `1.000`.
- With 0 decorative bits at budget 4, dense entropy success is `1.000` and contact-equivalence is `1.000`.

## Noise Taxonomy

- Contact-equivalence at 20% symmetric noise: `0.442`.
- Contact-equivalence at 20% false-positive noise: `0.683`.
- Contact-equivalence at 20% false-negative noise: `0.713`.

## Figures

- `paper/figures/main_success_budget.png`
- `paper/figures/probe_allocation.png`
- `paper/figures/decor_scaling.png`
- `paper/figures/lane_scaling.png`
- `paper/figures/noise_taxonomy.png`
- `paper/figures/prior_stress.png`
- `paper/figures/probe_library.png`
- `paper/figures/negative_controls.png`
