# Submission Readiness Decision

## Decision

Workshop-only.

## Rationale

The v2 paper is stronger because it adds the dense contact-only boundary control. The result is now more honest and harder to dismiss: contact-equivalence wins over full dense entropy only when the hidden state contains manipulation-irrelevant variables, and it agrees with dense entropy once those variables are removed.

The manuscript is not submit-ready for a main conference because the evidence remains a stylized synthetic task with idealized binary tactile observations and no 3D or hardware validation.

## Required Before Main-Conference Submission

- Realistic 3D hidden-contact benchmark or hardware experiment.
- Approximate quotient inference method for non-enumerated geometry.
- Comparison against learned visuo-tactile policies or reconstruction-driven planners.
- More realistic tactile noise and calibration drift model.
