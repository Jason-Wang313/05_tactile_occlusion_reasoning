# Reviewer Attacks

## Likely Attacks And Responses

1. **This is just active touch.** Response: active touch usually optimizes generic information or reconstruction; the paper optimizes splits of manipulation-relevant contact-equivalence classes.
2. **This is just uncertainty.** Response: uncertainty over dense cells is not the central object; two uncertain shapes may be equivalent for the next contact, while two likely shapes may be decision-critical.
3. **This is just tactile shape reconstruction.** Response: the method can stop before reconstructing full hidden geometry if the remaining ambiguity is contact-equivalent for the current plan.
4. **Simulation is too simple.** Response: true; the paper is framed as a synthetic mechanism paper. The final version expands scope with seven suites, 10,120 compact rows, and explicit boundary controls.
5. **Hostile prior already does visuo-tactile hidden-shape inference.** Response: concede broad hidden-shape inference; preserve only the narrower claim about task-indexed equivalence partitions.
6. **Probe outcomes are idealized.** Response: the final noise taxonomy reports degradation, including contact-equivalence at 0.442 under 20% symmetric noise. Real-sensor robustness remains a limitation.
7. **Dense entropy is a straw baseline.** Response: dense contact-only is included and reaches 1.000 at budget four. The paper's actual claim is about unfiltered dense hidden-state objectives.
8. **The probe library does all the work.** Response: probe-library ablations show this dependency directly; cells-only/no-sweeps falls to 0.433 while mixed probes reach 1.000.
9. **The method will not scale exactly.** Response: exact scalable 3D quotient maintenance is not claimed; sampled equivalence is included as an approximate step, and scalable approximation is future work.

## Closest Hostile Prior Work

- TouchAnything: Diffusion-Guided 3D Reconstruction from Sparse Robot Touches (2026): shape reconstruction; threatens broad hidden-shape inference claims.
- Visual-Tactile Fusion for 3D Objects Reconstruction from a Single Depth View and a Single Gripper Touch for Robotics Tasks (2021): visuo-tactile reconstruction; threatens generic touch-for-shape claims.
- Simultaneous Tactile Localization And Reconstruction of an Object During Robotic Manipulation (2021): localization and reconstruction; threatens broad reconstruction novelty.
- 3-D Dense Reconstruction of Vision-Based Tactile Sensor With Coded Markers (2023): dense tactile reconstruction; threatens sensor/reconstruction claims.
- Capturing forceful interaction with deformable objects using a deep learning-powered stretchable tactile array (2024): tactile sensing and deformable interaction; highlights missing hardware scope.
- Tac2Pose: Tactile object pose estimation from the first touch (2023): tactile state estimation; threatens pose/state versions of the claim.
- TouchSDF: A DeepSDF Approach for 3D Shape Reconstruction Using Vision-Based Tactile Sensing (2024): implicit tactile shape reconstruction; threatens shape-inference framing.
- Active Tactile Exploration Based on Cost-Aware Information Gain Maximization (2018): active haptic information gain; threatens generic active-touch framing.
- End-to-End Diffusion-Based 3D Object Reconstruction From Robotic Tactile Sensing (2025): learned reconstruction; motivates the paper's boundary against reconstruction claims.
