# Submission Attack Log

## Paper 05 v2

- Attack: The dense-entropy baseline is straw because it is forced to value irrelevant decorative geometry.
  - Response: Added dense contact-only control. It removes decorative probes and reaches 100.0% success at budget 4, matching contact-equivalence.
  - Residual risk: This narrows the claim to settings where irrelevant hidden variables remain in the state.
- Attack: The synthetic world is too simple and noiseless.
  - Response: Existing noise stress was regenerated with the v2 method set. Contact-equivalence reaches 92.7% at 2% binary noise, 82.8% at 5%, 68.1% at 10%, and 43.3% at 20%.
  - Residual risk: Binary observation noise is not a calibrated tactile sensor model.
- Attack: Exact quotient maintenance may not scale.
  - Response: Paper keeps this as an explicit limitation and does not claim scalable 3D inference.
- Attack: Recent visuo-tactile reconstruction work already solves hidden geometry.
  - Response: The claim is restricted to task-indexed equivalence partitions, not general hidden-shape reconstruction.
