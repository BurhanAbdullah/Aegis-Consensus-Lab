# PBFT / weighted-certificate semantics — tag4

## Protocol context
A vote is bound to `(height, view, phase, proposal_id)`. A validator may contribute at most one vote to a certificate for that exact context. A certificate is valid only if the sum of governance weights of its distinct voters reaches the current quorum weight.

## Safety assumption
Honest validators do not sign two conflicting proposal IDs for the same `(height, view, phase)`. Byzantine validators may equivocate.

## Weighted intersection lemma
For normalized total governance weight 1, two sets each having weight at least q have intersection weight at least `max(0, 2q-1)`.

If Byzantine weight is at most b and
`2q-1>b`,
the intersection contains positive honest weight. Under the honest non-equivocation assumption, two conflicting certificates cannot both exist.

## Availability
Let h be the honest participating governance weight in the relevant round. A valid certificate can be formed whenever `q <= h` and the participating honest voters support the same proposal.

The conservative sufficient bound `h >= 1-b` yields `q <= 1-b`.

## Important scope
This is a weighted certificate safety/availability result, not a complete asynchronous PBFT liveness theorem. Network synchrony, view changes, leader replacement, authentication, and message delivery assumptions must be added before stronger liveness language is used.

## Why this matters for the paper
The adaptive quorum is now evaluated against explicit certificate semantics rather than treating a scalar percentage as an abstract 'consensus score'. This makes the analytical boundary testable in the protocol implementation.
