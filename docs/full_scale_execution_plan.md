# Full-Scale Execution Plan

Paper 05: Tactile Occlusion Reasoning

## Current Claim

The current paper claims that manipulation under visual occlusion should reason over contact-equivalence classes rather than reconstructing every visually hidden shape variable. Two hidden geometries are equivalent for the current manipulation step when every relevant contact would have the same outcome. Tactile probes should split those contact-outcome classes rather than maximize information gain over all hidden geometry.

The current evidence is a stylized synthetic lane task: vision censors one hidden insertion channel among 12 lanes and also censors 64 irrelevant decorative bits. Dense entropy spends probes on decorative bits and reaches 8.6% success at budget 4, critical-cell entropy reaches 41.5%, contact-equivalence reaches 100.0%, and dense contact-only also reaches 100.0%. This is a useful mechanism test, but the paper is only 7 pages and the evidence is too narrow for the batch-final standard.

## Main Gaps To Close

1. The current paper is far below the page threshold.
2. The current experiment has one lane count, one decorative-bit count, one probe library, one visual-censoring structure, and a small noise sweep.
3. The dense contact-only control narrows the claim but needs to be part of a broader boundary map.
4. The paper does not yet test irrelevant-variable scaling, contact-class count scaling, tactile noise asymmetry, prior skew, visual ambiguity size, approximate quotient inference, or non-equivalence negative controls.
5. The paper needs stronger baselines: random, dense entropy, dense contact-only, critical-cell entropy, contact-equivalence, hybrid dense/contact objectives, myopic regret, oracle contact-relevance filtering, and sampled quotient approximations.
6. The final manuscript needs fuller formal setup, theorem/proposition statements, suite descriptions, ablations, failure cases, related work boundary, limitations, reproducibility, and appendix audit.

## Target Experiments

1. Main expanded lane benchmark
   - Sweep lane counts such as 8, 12, 16, and 24.
   - Sweep probe budgets from 0 to at least 10.
   - Compare dense entropy, dense contact-only, critical-cell entropy, contact-equivalence, random, hybrid objectives, and oracle filtered controls.
   - Report success, regret, posterior contact entropy, posterior full entropy, contact probes, decorative probes, and probe efficiency.

2. Irrelevant hidden-state scaling
   - Sweep decorative bits such as 0, 16, 64, 128, and 256.
   - Show exactly when dense reconstruction becomes distracted.
   - Confirm dense contact-only removes the gap when irrelevant variables are filtered.

3. Contact-complexity scaling
   - Increase hidden contact classes and sweep partition granularity.
   - Test whether balanced contact-equivalence sweeps scale better than one-cell probing.

4. Tactile noise taxonomy
   - Go beyond symmetric binary noise.
   - Include false-positive, false-negative, asymmetric, and drift-like noise.
   - Report graceful degradation and failure thresholds.

5. Prior and visual-censoring stress
   - Test uniform, skewed, and multi-modal lane priors.
   - Vary how many lanes vision leaves plausible.
   - Include occlusion patterns where vision rules out part of the contact space.

6. Probe-library ablations
   - Single-cell probes only.
   - Balanced sweeps only.
   - Mixed sweep widths.
   - Noisy/decorative distractor probes.
   - Cost-weighted probes where wide sweeps cost more.

7. Approximate quotient inference
   - Add sampled posterior variants or coarse hashed contact partitions.
   - Measure whether approximate quotienting keeps the advantage when exact enumeration is not available.

8. Negative controls
   - No decorative bits: dense entropy and contact-equivalence should agree.
   - All hidden bits contact-relevant: dense reconstruction should not be unfairly penalized.
   - Oracle contact-relevance filter: dense contact-only should match equivalence.
   - Non-stationary contact map: stale equivalence classes should fail.

9. Runtime and memory reporting
   - Store compact per-condition metrics only.
   - Avoid raw per-trial trajectory dumps.
   - Include reproducibility commands and row counts.

## Baselines And Comparators

Required methods:

1. Visual only.
2. Random probe selection.
3. Dense entropy over all hidden variables.
4. Dense contact-only oracle filtered control.
5. Critical-cell entropy.
6. Contact-equivalence.
7. Hybrid dense/contact objective with several mixing weights.
8. Myopic expected-regret reduction.
9. Oracle binary-search/contact split upper reference.
10. Approximate sampled contact-equivalence.

## Figures And Tables

Planned final figures:

1. Tactile occlusion schematic.
2. Main success-vs-budget curves.
3. Probe allocation curves showing decorative versus contact probes.
4. Decorative-bit scaling heatmap/curves.
5. Lane-count scaling curves.
6. Noise taxonomy curves.
7. Prior-skew/visual-censoring stress figure.
8. Probe-library ablation figure.
9. Negative-control figure.
10. Approximate quotient figure.

Planned tables:

1. Main benchmark table.
2. Dense/decorative scaling summary.
3. Noise taxonomy summary.
4. Probe allocation summary.
5. Negative-control summary.
6. Runtime and row-count table.
7. Claim-support matrix.

## Writing Expansion Strategy

The final manuscript should become a full 25+ page paper through real content:

1. Expanded introduction motivating why reconstruction is the wrong default target under contact-specific decisions.
2. Formal setup for hidden geometry, visual censoring, contact-outcome maps, equivalence classes, losses, and tactile observations.
3. Propositions for decision-equivalence, dense-entropy distraction, and boundary cases where dense and quotient objectives coincide.
4. Related work separated into tactile sensing, reconstruction, active haptics, visuo-tactile fusion, task-aware exploration, and equivalence/abstraction.
5. Detailed experimental protocol and baseline definitions.
6. Full suite results with positive, boundary, and negative findings.
7. Honest limitations: stylized simulator, no hardware, exact quotient scalability, tactile calibration, learned policy comparisons.
8. Reproducibility appendix with row counts, commands, and RAM-light execution details.

## Page-Count Strategy

The final PDF must be at least 25 pages and must not be copied to Downloads until it is final. Page growth must come from the expanded experiment suites, figures, tables, formal statements, related work boundary, limitations, and reproducibility appendix. No padding.

## RAM-Light Execution Strategy

1. Run suites sequentially.
2. Write compact per-condition metrics to `results/full_scale/`.
3. Do not store raw per-trial trajectories.
4. Use deterministic seeds and resumable suite-level outputs.
5. Generate figures from compact CSVs.
6. Keep trial counts high enough for stable means while avoiding memory-heavy raw logs.

## Acceptance Checklist

Before Paper 05 can be considered final:

1. This plan exists before experiment/manuscript edits.
2. Existing v2 evidence is reproduced or superseded.
3. Full-scale experiment runner completes and writes compact CSVs.
4. Final figures and tables are generated from full-scale outputs.
5. Manuscript is rewritten as a full final paper.
6. Local compiled PDF is at least 25 pages.
7. PDF body scan confirms no hardening prompt text, internal decision labels, or accidental file-path/provenance text.
8. `C:\Users\wangz\Downloads\05.pdf` is overwritten only after final verification.
9. README, claims, rigor checklist, final audit, readiness decision, reviewer attacks, reproducibility checklist, and version log are updated.
10. Local build PDF is removed after the verified Downloads copy exists.
11. Repository is committed and pushed.
12. Only then may work proceed to Paper 06.
