# Novelty Boundary Map

## What The Field Already Covers
- Tactile sensing hardware and datasets.
- Contact-aided pose estimation and tactile object recognition.
- Tactile or visuotactile shape reconstruction.
- Active haptic exploration and uncertainty reduction.
- Learning policies that use tactile feedback during grasping/manipulation.

## Hidden Assumptions That May Be False
1. Visible pixels identify the object sufficiently for downstream contact planning.
2. Unseen geometry can be treated as generic epistemic uncertainty.
3. A shape prior that looks plausible is enough if its reconstruction loss is low.
4. Touch is merely another observation channel to fuse into a latent vector.
5. The same active exploration objective should apply to visible and occluded regions.
6. Occlusion is a camera nuisance, not a structural censoring operator.
7. Contact success can be evaluated after selecting a plan rather than represented during perception.
8. Robot actions reveal information only by sampling more data, not by changing the equivalence class of possible worlds.
9. All hidden geometry errors have equal decision cost.
10. Training distributions contain the hidden-geometry alternatives that matter at test time.
11. A single MAP reconstruction is sufficient for manipulation.
12. If pose is correct, contact-relevant shape uncertainty is secondary.
13. The tactile sensor contact patch can be interpreted without considering the planned wrench/contact mode.
14. Free-space observations from vision constrain hidden solid occupancy enough.
15. Object rigidity makes contact inference simple.
16. The backside or underside of an object is irrelevant until grasping fails.
17. The robot can afford enough exploratory touches to reconstruct the whole object.
18. High-capacity fusion models will learn which tactile signals break occlusion.
19. Benchmarks with random train/test splits expose hidden-geometry brittleness.
20. Uncertainty calibration solves hidden geometry ambiguity.
21. The planner consumes geometry as a fixed mesh rather than a set of manipulation-contingent alternatives.
22. Tactile evidence should update a dense shape, not a task-level contact-feasibility partition.

## Candidate Directions That Break Assumptions
- **Occlusion-equivalence contact partitioning:** Maintain equivalence classes of visually indistinguishable geometries and split them only by contacts that change feasible manipulation modes.
- **Manipulation-contingent tactile tomography:** Choose touches whose normals/wrenches disambiguate hidden geometry along planned contact manifolds rather than maximizing global information gain.
- **Counterfactual contact certificates:** Represent what contact outcome would have occurred under each hidden geometry alternative and reject plans with ambiguous certificates.
- **Censored-world residual dynamics:** Model tactile prediction errors as violations of a vision censoring assumption, not as generic sensor noise.
- **Task-loss amodal shape sets:** Output a set of shape hypotheses equivalent under vision but separated by downstream manipulation loss.

## Chosen Direction
**Occlusion-equivalence contact partitioning:** Maintain equivalence classes of visually indistinguishable geometries and split them only by contacts that change feasible manipulation modes.

## Boundary Against Hostile Prior Work
The hostile set makes generic tactile reconstruction, visuotactile fusion, active touch, and contact-aided pose estimation non-novel. The boundary is to make the central object not a better reconstructed mesh, not an uncertainty scalar, and not a learned fusion embedding, but a manipulation-indexed partition of the geometries that vision censors into the same observation.

## Strongest Hostile Rows
- TouchAnything: Diffusion-Guided 3D Reconstruction from Sparse Robot Touches (2026): threatens using tactile contacts to reconstruct object shape; leaves open a mechanism that represents vision-censored geometry as an equivalence class and uses contact to split only manipulation-relevant alternatives.
- Visual-Tactile Fusion for 3D Objects Reconstruction from a Single Depth View and a Single Gripper Touch for Robotics Tasks (2021): threatens using tactile contacts to reconstruct object shape; leaves open a mechanism that represents vision-censored geometry as an equivalence class and uses contact to split only manipulation-relevant alternatives.
- Simultaneous Tactile Localization And Reconstruction of an Object During Robotic Manipulation (2021): threatens using tactile contacts to reconstruct object shape; leaves open a mechanism that represents vision-censored geometry as an equivalence class and uses contact to split only manipulation-relevant alternatives.
- 3-D Dense Reconstruction of Vision-Based Tactile Sensor With Coded Markers (2023): threatens using tactile contacts to reconstruct object shape; leaves open a mechanism that represents vision-censored geometry as an equivalence class and uses contact to split only manipulation-relevant alternatives.
- Capturing forceful interaction with deformable objects using a deep learning-powered stretchable tactile array (2024): threatens using tactile contacts to reconstruct object shape; leaves open a mechanism that represents vision-censored geometry as an equivalence class and uses contact to split only manipulation-relevant alternatives.
- High-Precision 3D Reconstruction Study with Emphasis on Refractive Calibration of GelStereo-Type Sensors (2023): threatens using tactile contacts to reconstruct object shape; leaves open a mechanism that represents vision-censored geometry as an equivalence class and uses contact to split only manipulation-relevant alternatives.
- Tac2Pose: Tactile object pose estimation from the first touch (2023): threatens using tactile contacts to reconstruct object shape; leaves open a mechanism that represents vision-censored geometry as an equivalence class and uses contact to split only manipulation-relevant alternatives.
- TouchSDF: A DeepSDF Approach for 3D Shape Reconstruction Using Vision-Based Tactile Sensing (2024): threatens using tactile contacts to reconstruct object shape; leaves open a mechanism that represents vision-censored geometry as an equivalence class and uses contact to split only manipulation-relevant alternatives.
- Play it by Ear: Learning Skills amidst Occlusion through Audio-Visual Imitation Learning (2022): threatens generic fusion of visual and tactile streams for manipulation; leaves open a mechanism that represents vision-censored geometry as an equivalence class and uses contact to split only manipulation-relevant alternatives.
- End-to-End Diffusion-Based 3D Object Reconstruction From Robotic Tactile Sensing (2025): threatens using tactile contacts to reconstruct object shape; leaves open a mechanism that represents vision-censored geometry as an equivalence class and uses contact to split only manipulation-relevant alternatives.
- Virtual Reality Mediated Haptic Robot Telemanipulation Without Cameras: Technology and Pilot Study (2026): threatens using tactile contacts to reconstruct object shape; leaves open a mechanism that represents vision-censored geometry as an equivalence class and uses contact to split only manipulation-relevant alternatives.
- In-Hand Manipulation of Unknown Objects with Tactile Sensing for Insertion (2022): threatens using tactile contacts to reconstruct object shape; leaves open a mechanism that represents vision-censored geometry as an equivalence class and uses contact to split only manipulation-relevant alternatives.
- Active Tactile Exploration Based on Cost-Aware Information Gain Maximization (2018): threatens using tactile contacts to reconstruct object shape; leaves open a mechanism that represents vision-censored geometry as an equivalence class and uses contact to split only manipulation-relevant alternatives.
- Design and Calibration of a Force/Tactile Sensor for Dexterous Manipulation (2019): threatens generic fusion of visual and tactile streams for manipulation; leaves open a mechanism that represents vision-censored geometry as an equivalence class and uses contact to split only manipulation-relevant alternatives.
- DTactive: A Vision-Based Tactile Sensor with Active Surface (2024): threatens using tactile contacts to reconstruct object shape; leaves open a mechanism that represents vision-censored geometry as an equivalence class and uses contact to split only manipulation-relevant alternatives.
