# Validation Findings — Initial Deep Pass

## 1. Existing theorem audit
The repository already contains an independent `research_validation/theorem_audit.py` audit. It explicitly tests the proposed Lambda = recovery/loss condition against two bounded recurrences and searches for counterexamples. The audit's interpretation is that Lambda alone cannot be accepted as a universal theorem; validity is recurrence-specific.

A local reproduction of the same recurrence logic produced 3,360 parameter/initial-condition cases and 797 mismatches between `Lambda >= 1` and positive terminal trust mass. This confirms that the old universal Lambda claim must not be carried into the rebuilt paper.

## 2. Current consensus implementation mismatch
`core/consensus.sh` on tag4 currently implements scalar integer trust with initialization 100, decay 1, slashing 20, recovery 2, minimum active trust 30, maximum trust 150, and a quorum equal to two-thirds of the active total trust. This is not the four-dimensional normalized trust + predictive risk containment + adaptive quorum formulation targeted by the Transactions rebuild.

The implementation also computes the quorum threshold before vote processing and applies recovery during vote processing afterward. Therefore the exact state transition represented by the current script is not the same as a simple simultaneous trust/quorum recursion.

## 3. Physical AC claim gate
The existing `research_validation/physical_claim_gate.py` requires four exact raw artifacts for the previously reported 9,450-case AC-grid claim. At least the first required raw result path is not present on tag4, so that claim cannot currently be marked verified. The rebuilt paper must not present that physical-grid claim as established until the exact artifacts and recomputation exist.

## 4. Immediate scientific consequence
The rebuild should not patch the old theorem around the existing script. Instead, the paper's theoretical model and implementation must be jointly redesigned, then the experiments regenerated from that final model.

## 5. New analytical direction
The candidate theory in `THEORY_V1.md` replaces the old universal Lambda theorem with:
- an explicit bounded affine trust recurrence;
- an exact equilibrium and convergence result;
- a weighted quorum intersection/liveness window;
- an adaptive-quorum security–availability boundary.

This is the current candidate direction, not yet a final theorem set.
