# Weighted Quorum Safety Proof v1 — tag4

## Definitions
Let the active governance weight be normalized to 1. Let B be the Byzantine validator set with total governance weight w(B)<=b. A certificate is a set of authenticated votes for one proposal/context with total distinct-voter governance weight at least q.

Honest validators sign at most one conflicting proposal per height/view/phase. Byzantine validators may sign arbitrarily many proposals.

## Lemma 1 — Weighted intersection
For any two validator sets A and C with w(A)>=q and w(C)>=q,

w(A∩C) >= w(A)+w(C)-1 >= 2q-1.

This follows from w(A∪C)<=1 and inclusion-exclusion.

## Lemma 2 — Honest intersection under Byzantine bound
If

q > (1+b)/2,

then any two quorum certificates intersect in positive honest governance weight.

Proof: by Lemma 1, w(A∩C)>=2q-1>b>=w(B). Therefore A∩C cannot consist entirely of Byzantine validators. Hence A∩C contains positive honest weight.

## Theorem — Certificate safety
Under authenticated vote uniqueness, honest non-equivocation, total normalized governance weight 1, and Byzantine weight at most b, if

q>(1+b)/2,

then two conflicting certificates for the same height/view/phase cannot both be valid.

Proof: suppose conflicting certificates A and C exist. Lemma 2 gives an honest validator of positive governance weight in A∩C. That honest validator would have had to sign both conflicting proposals, contradicting honest non-equivocation. Therefore conflicting certificates cannot coexist.

## Availability lemma
Let h be the governance weight of honest validators that actually participate in the phase. If

q <= h,

then an honest certificate is possible, assuming participating honest validators vote for the valid proposal and authentication/communication assumptions required by the protocol hold.

## Conservative availability corollary
If h>=1-b, then q<=1-b is sufficient for the conservative availability bound.

## Nonempty operating interval
A threshold satisfying both safety and conservative availability exists iff

(1+b)/2 < 1-b,

which is equivalent to

b < 1/3.

For b>=1/3, no scalar quorum fraction can simultaneously satisfy these two sufficient conditions. This is an important boundary result, not an implementation failure.

## Scope and limitations
This proof is a certificate-level safety theorem. It does not by itself prove full PBFT liveness, view-change correctness, network synchrony, detector correctness, or convergence of trust/risk dynamics. Those properties require separate assumptions and proofs.

The theorem applies to governance weights fixed for the certificate context. If governance weights can change during a certificate, the certificate must bind the weight snapshot or an equivalent version identifier; otherwise the proof does not apply directly.
