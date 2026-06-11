# Novelty Decision

## Selected Thesis
Robotic manipulation under visual occlusion should reason over **contact-equivalence classes** rather than single reconstructed shapes: two hidden geometries are equivalent only if every currently relevant manipulation contact would have the same outcome. A small number of tactile probes can then split the equivalence classes that matter for the next action, without solving full shape reconstruction.

## Why This Direction Survived The Hostile Set
Prior work already covers tactile sensing, visuotactile fusion, tactile shape reconstruction, active touch, and contact-aided state estimation. The selected direction changes the central mechanism: the representation is a partition over hidden geometries indexed by manipulation contact outcomes. The evidence must therefore show that reconstructing visually plausible shapes or reducing generic uncertainty can choose the wrong touch/plan when the decisive variable is an occluded contact boundary.

## Chosen Field Box
Multimodal tactile perception for robot manipulation, specifically hidden-geometry inference under visual censoring.

## Non-Goals
- Not a new tactile sensor.
- Not a larger model or better dataset.
- Not a benchmark-only paper.
- Not generic uncertainty estimation, active learning, verifier stacking, LLM planning, or reinforcement learning.
- Not claiming full real-robot validation.
