# Adversarial Validation v1 — tag4

## Objective
Attempt to falsify the certificate safety theorem rather than merely confirm nominal examples.

## Attack classes
1. Exact safety-boundary quorum: q=(1+b)/2.
2. Just-below and just-above the boundary.
3. Byzantine-only intersection attempt.
4. Conflicting proposal certificates.
5. Duplicate-voter double counting.
6. Cross-height certificate replay.
7. Cross-view certificate replay.
8. Cross-phase certificate replay.
9. Proposal-hash substitution.
10. Byzantine weight concentrated on the intersection.

## Required theorem check
For normalized total governance weight 1 and Byzantine weight <=b, two q-quorums have intersection at least 2q-1. Therefore if 2q-1>b, their intersection contains honest governance weight. With honest non-equivocation, two conflicting certificates cannot both be valid for the same context.

## Boundary rule
Equality is unsafe for the strict safety theorem. The implementation must preserve this strict inequality without floating-point artifacts.

## Pass criterion
Every generated adversarial case must either be rejected by certificate validation or satisfy the theorem's explicit assumptions. A discovered valid conflicting certificate is a blocking failure.
