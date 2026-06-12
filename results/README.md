# Runnable Evidence

The simulation is a controlled hidden-geometry task. Vision censors a hidden insertion channel among 12 possible lanes and also censors 64 irrelevant decorative bits. The manipulation succeeds only if the robot chooses the true hidden channel. All methods receive the same probe budget and probe library.

The key distinction is objective, not sensor access:

- Dense entropy greedily reduces entropy of the full hidden geometry, so it spends early probes on irrelevant decorative bits.
- Dense contact-only is a boundary control that removes the irrelevant decorative probes from the dense objective.
- Critical-cell entropy probes lane cells, so it attacks the right variable but only by one lane at a time.
- Contact-equivalence chooses tactile sweeps that split the manipulation contact outcome class.

At budget 4 with noiseless probes, contact-equivalence reaches 100.0% success, dense entropy reaches 8.6%, dense contact-only reaches 100.0%, and critical-cell entropy reaches 41.5%. The contact-only control marks the boundary: once irrelevant hidden geometry is removed from the dense state, dense entropy and contact-equivalence agree.

Run:

```powershell
python experiments/tactile_occlusion_sim.py
```

Outputs:

- `results/evidence_summary.csv`
- `results/noise_ablation.csv`
- `results/main_success_table.tex`
- `results/noise_success_table.tex`
- `results/ascii_success_plot.txt`
