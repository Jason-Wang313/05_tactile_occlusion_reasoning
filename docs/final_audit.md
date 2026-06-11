# Final Audit

## 1. Chosen Thesis
Robotic manipulation under visual occlusion should reason over contact-equivalence classes rather than single reconstructed hidden shapes. Two hidden geometries are equivalent for the current manipulation step if every relevant contact would have the same outcome.

## 2. Field Assumption Broken
The broken assumption is that reducing uncertainty over all visually hidden geometry is equivalent to reducing manipulation-relevant ambiguity. The evidence shows that dense hidden-state entropy can be dominated by geometry that does not affect the pending contact.

## 3. New Central Mechanism
The central mechanism is a task-indexed quotient representation over hidden geometries. Tactile probes are selected to split contact-outcome equivalence classes, not to reconstruct every hidden surface cell.

## 4. Genuine Novelty
Prior work already covers tactile sensing, visuo-tactile fusion, active touch, pose estimation, and tactile shape reconstruction. The novelty is narrower: represent vision-censored geometry as contact-equivalence classes and stop once the remaining hidden geometries are decision-equivalent for the current manipulation.

## 5. Closest Hostile Prior Work
- TouchAnything: Diffusion-Guided 3D Reconstruction from Sparse Robot Touches (2026).
- Visual-Tactile Fusion for 3D Objects Reconstruction from a Single Depth View and a Single Gripper Touch for Robotics Tasks (2021).
- TouchSDF: A DeepSDF Approach for 3D Shape Reconstruction Using Vision-Based Tactile Sensing (2024).
- Active Tactile Exploration Based on Cost-Aware Information Gain Maximization (2018).
- ViTaSCOPE: Visuo-tactile Implicit Representation for In-hand Pose and Extrinsic Contact Estimation (2025).

These threaten broad claims about tactile hidden-shape inference, so the paper avoids that broad claim.

## 6. Literature Coverage
The repository contains `docs/related_work_matrix.csv` with 1332 entries, `docs/literature_map.md` with the 1000-paper landscape sweep plus a 300-paper serious skim and 240-paper deep-read extraction protocol, and `docs/hostile_prior_work.md` with a 100-paper hostile set.

## 7. Proof / Formal-Claim Status
A modest decision-equivalence condition is stated in the paper: if task loss depends on hidden geometry only through the relevant contact-outcome map, then unresolved ambiguity inside one contact-equivalence class cannot change the Bayes decision over the current action set. This is a formal observation, not a full theorem about scalable 3D inference.

## 8. Strongest Evidence
The runnable synthetic manipulation task isolates visual censoring of a hidden insertion channel among 12 lanes plus 64 irrelevant hidden decorative bits. At four noiseless tactile probes, contact-equivalence reaches 100.0% success, dense entropy reaches 10.2%, and critical-cell entropy reaches 41.0%. At four probes with 5% binary tactile noise, contact-equivalence reaches 83.2%.

## 9. Biggest Weaknesses
- Evidence is synthetic and intentionally stylized.
- No real-robot tactile sensor validation is provided.
- Exact quotient maintenance is not shown to scale to high-dimensional 3D objects.
- Deformable, articulated, and calibration-drifting contacts are outside the supported claim.
- Learned visuo-tactile foundation models are discussed as hostile prior work but not empirically compared.

## 10. Paper-Readiness Judgment
Workshop. The mechanism is crisp and the evidence supports the assumption break, but a main-conference submission would need stronger real-robot or realistic 3D evidence.

## 11. Exact Downloads PDF Path
`C:/Users/wangz/Downloads/05.pdf`

## 12. GitHub URL
`https://github.com/Jason-Wang313/05_tactile_occlusion_reasoning`

## 13. Desktop Copy Status
pending orchestrator copy
