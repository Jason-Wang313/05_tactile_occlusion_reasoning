# Reviewer Attacks

## Likely Attacks And Responses
1. **This is just active touch.** Response: active touch usually optimizes generic information or reconstruction; the paper optimizes splits of manipulation-relevant contact-equivalence classes.
2. **This is just uncertainty.** Response: uncertainty over dense cells is not the central object; two uncertain shapes may be equivalent for the next contact, while two likely shapes may be decision-critical.
3. **This is just tactile shape reconstruction.** Response: the method can stop before reconstructing the full hidden geometry if the remaining ambiguity is contact-equivalent for the plan.
4. **Simulation is too simple.** Response: true; the paper should be framed as a mechanism paper with a controlled falsification of a field assumption, not as a deployment claim.
5. **Hostile prior already does visuotactile hidden-shape inference.** Response: concede that broad hidden-shape inference is covered; preserve only the narrower claim about task-indexed equivalence partitions.
6. **Probe outcomes are idealized.** Response: add noise ablations and mark real-sensor robustness as future work.

## Closest Hostile Prior Work
- TouchAnything: Diffusion-Guided 3D Reconstruction from Sparse Robot Touches (2026): shape reconstruction; visuotactile fusion; threatens using tactile contacts to reconstruct object shape.
- Visual-Tactile Fusion for 3D Objects Reconstruction from a Single Depth View and a Single Gripper Touch for Robotics Tasks (2021): sensor/dataset; pose/state estimation; shape reconstruction; threatens using tactile contacts to reconstruct object shape.
- Simultaneous Tactile Localization And Reconstruction of an Object During Robotic Manipulation (2021): sensor/dataset; pose/state estimation; shape reconstruction; threatens using tactile contacts to reconstruct object shape.
- 3-D Dense Reconstruction of Vision-Based Tactile Sensor With Coded Markers (2023): sensor/dataset; pose/state estimation; shape reconstruction; threatens using tactile contacts to reconstruct object shape.
- Capturing forceful interaction with deformable objects using a deep learning-powered stretchable tactile array (2024): pose/state estimation; shape reconstruction; active exploration; threatens using tactile contacts to reconstruct object shape.
- High-Precision 3D Reconstruction Study with Emphasis on Refractive Calibration of GelStereo-Type Sensors (2023): sensor/dataset; pose/state estimation; shape reconstruction; threatens using tactile contacts to reconstruct object shape.
- Tac2Pose: Tactile object pose estimation from the first touch (2023): sensor/dataset; pose/state estimation; shape reconstruction; threatens using tactile contacts to reconstruct object shape.
- TouchSDF: A DeepSDF Approach for 3D Shape Reconstruction Using Vision-Based Tactile Sensing (2024): sensor/dataset; pose/state estimation; shape reconstruction; threatens using tactile contacts to reconstruct object shape.
- Play it by Ear: Learning Skills amidst Occlusion through Audio-Visual Imitation Learning (2022): pose/state estimation; visuotactile fusion; learning/control; threatens generic fusion of visual and tactile streams for manipulation.
- End-to-End Diffusion-Based 3D Object Reconstruction From Robotic Tactile Sensing (2025): sensor/dataset; pose/state estimation; shape reconstruction; threatens using tactile contacts to reconstruct object shape.
