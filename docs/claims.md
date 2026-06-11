# Claims

## Supported By Runnable Evidence
1. In a stylized manipulation world with visually censored hidden notches, many geometries share the same visual observation but differ in whether a planned contact trajectory collides, slips through a gap, or reaches a stable pocket.
2. A contact-equivalence partition can identify the hidden geometry class needed for a manipulation decision using fewer probes than dense reconstruction over all cells.
3. A global information-gain probe can be suboptimal when it reduces uncertainty in regions irrelevant to the pending manipulation contact.
4. A single MAP or mean reconstruction can select an unsafe plan when the posterior is multi-modal over contact outcomes.

## Formal Claims To Check
1. If the task loss depends only on a contact-outcome map, then two hidden geometries with the same map are decision-equivalent for that task.
2. A probe that splits contact-outcome classes can reduce worst-case task regret even when it does not maximally reduce entropy over dense geometry.

## Unsupported Or Only Partially Supported
1. Real tactile sensors will provide clean enough contact outcomes for the proposed partition without calibration drift.
2. The mechanism scales directly to deformable or articulated objects.
3. The mechanism outperforms modern learned visuotactile foundation models on real robots.
4. The partition can be maintained exactly in high-dimensional 3D without approximate hashing or learned surrogates.
