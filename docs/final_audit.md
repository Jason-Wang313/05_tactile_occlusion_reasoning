# Final Audit

## 1. Chosen Thesis

Robotic manipulation under visual occlusion should reason over contact-equivalence classes rather than single reconstructed hidden shapes. Two hidden geometries are equivalent for the current manipulation step if every relevant contact would have the same outcome.

## 2. Field Assumption Broken

The broken assumption is that reducing uncertainty over all visually hidden geometry is equivalent to reducing manipulation-relevant ambiguity. The final evidence shows that dense hidden-state entropy can be dominated by geometry that does not affect the pending contact.

## 3. New Central Mechanism

The central mechanism is a task-indexed quotient representation over hidden geometries. Tactile probes are selected to split contact-outcome equivalence classes, not to reconstruct every hidden surface cell.

## 4. Literature Coverage

The repository contains `docs/related_work_matrix.csv` with 1332 entries, `docs/literature_map.md` with the 1000-paper landscape sweep plus serious skim/deep-read summaries, `docs/hostile_prior_work.md` with a 100-paper hostile set, and `docs/novelty_boundary_map.md` with the claim boundary against tactile reconstruction and active touch.

## 5. Final Evidence

The final full-scale run contains 10,120 compact metric rows and 242,880 evaluated trials counted across rows. At budget four in the main suite, dense entropy reaches 0.083 success, dense contact-only reaches 1.000, critical-cell entropy reaches 0.425, expected-regret probing reaches 0.825, sampled equivalence reaches 0.967, and exact contact-equivalence reaches 1.000.

## 6. Boundary Findings

The strongest boundary is explicit: when decorative variables are removed or an oracle contact-only library is used, dense entropy reaches 1.000. This means the paper is not a universal attack on entropy or reconstruction. The claim is that dense hidden-state objectives are misaligned when they include manipulation-irrelevant hidden variables.

## 7. Failure Findings

Contact-equivalence degrades under tactile noise, reaching 0.442 at 20% symmetric noise. It also depends on a useful probe library, falling to 0.433 in the cells-only/no-sweeps control. These failures are reported in the manuscript rather than hidden.

## 8. Biggest Weaknesses

- Evidence is synthetic and intentionally stylized.
- No real-robot tactile sensor validation is provided.
- Exact quotient maintenance is not shown to scale to high-dimensional 3D objects.
- Deformable, articulated, and calibration-drifting contacts are outside the supported claim.
- Learned visuo-tactile foundation models are discussed as hostile prior work but not empirically compared.

## 9. Paper-Readiness Judgment

Final full-scale synthetic mechanism paper. The manuscript is submission-ready under the batch standard because it is 27 pages, contains new full-scale evidence, includes strong baselines and boundary controls, and states its limitations clearly. It should still be framed as a synthetic mechanism paper, not a real-robot deployment result.

## 10. Exact Canonical PDF Path

`C:/Users/wangz/Downloads/05.pdf`

Verified page count: 27 pages.

Verified PDF size: 1,040,865 bytes.

Verified SHA256: `BF717DB37975A5CC91C024F8936DCFE78C55C32DC6605D07BFDCBE9E6D0E570E`.

## 11. VLA-Style Boxed-Link Audit

96 link annotations on pages `[(1, 15), (2, 35), (3, 8), (4, 4), (6, 2), (7, 2), (10, 6), (11, 9), (12, 9), (13, 6)]`; colors green = 87, red = 9, cyan = 0; all borders `(0, 0, 1)`.

## 12. Visual Link Audit

Pages 1, 2, 3, 4, 6, 7, 10, 11, 12, and 13 rendered after export; green citation/URL boxes and red internal-reference boxes are crisp and aligned.

## 13. Filename Policy

No duplicate `C:/Users/wangz/Downloads/5.pdf` was created, and local `paper/main.pdf` was removed after the canonical copy.

## 14. GitHub URL

`https://github.com/Jason-Wang313/05_tactile_occlusion_reasoning`
