# AEGIS v4
## Safety and Protocol Invariants

Status: Experimental

---

# 1. Purpose

This document defines the intended safety and stability
properties of AEGIS v4.

These invariants describe conditions that should remain true
during protocol execution.

---

# 2. Safety Invariants

## INV-1
### No Conflicting Finalization

Two honest validators must never finalize conflicting blocks
for the same consensus height.

Formally:

if:

FINALIZED(B1, h)

and:

FINALIZED(B2, h)

then:

B1 = B2

for all honest validators.

Purpose:

- preserve ledger consistency
- prevent forks among honest validators

---

## INV-2
### Weighted Quorum Intersection

Any two commit quorums must intersect in sufficient honest trust weight.

Formally:

INTERSECTION(Q1, Q2) != empty

where:

Q1 = commit quorum
Q2 = commit quorum

Purpose:

- preserve Byzantine safety
- prevent conflicting commits

NOTE:

This property is not yet formally proven.

---

## INV-3
### Trust Bounds

Validator trust must remain bounded.

For every validator V:

0 <= trust(V) <= MAX_TRUST

Purpose:

- prevent runaway trust inflation
- stabilize consensus dynamics

---

## INV-4
### Trust Velocity Limiting

Trust changes must remain bounded per round.

Formally:

|trust(t+1) - trust(t)| <= MAX_TRUST_STEP

Purpose:

- resist rapid manipulation
- reduce oscillation instability

---

## INV-5
### Adaptive Quorum Correctness

Consensus finalization requires:

commit_weight >= quorum_threshold

Purpose:

- preserve weighted Byzantine safety
- ensure sufficient validator participation

---

# 3. Liveness Invariants

## INV-6
### Honest Progress

If sufficient honest trust exists,
consensus should eventually finalize.

Purpose:

- preserve protocol progress
- avoid permanent deadlock

NOTE:

This property is not yet formally proven.

---

## INV-7
### Recovery Stability

Honest validators should gradually recover trust.

Recovery rate must be slower than slashing rate.

Purpose:

- resist trust farming
- maintain hysteresis

---

## INV-8
### Dynamic Primary Stability

The primary validator should eventually converge
toward highly reliable validators.

Purpose:

- improve consensus survivability
- reduce unstable leadership

---

# 4. Security Invariants

## INV-9
### Signature Integrity

Every accepted validator message must contain
a valid cryptographic signature.

Purpose:

- prevent forgery
- preserve validator authenticity

---

## INV-10
### Replay Resistance

Previously finalized blocks must not be replayable
as fresh consensus proposals.

Purpose:

- prevent duplicate consensus injection
- preserve ledger uniqueness

---

## INV-11
### Equivocation Detection

Validators must not issue conflicting prepare
or commit messages for the same height.

Detected equivocation results in slashing.

Purpose:

- prevent Byzantine vote splitting
- preserve consensus integrity

---

# 5. Predictive Stability Invariants

## INV-12
### Future Quorum Survivability

Consensus should remain stable under projected
future trust degradation.

Predictive-safe consensus requires:

future_commit_weight >= future_quorum

across simulation horizon k.

Purpose:

- detect unstable consensus states
- resist cascading degradation

---

## INV-13
### Entropy Preservation

Validator trust distribution should not collapse
into excessive concentration.

Low entropy may indicate:

- validator centralization
- quorum capture
- malicious trust dominance

Purpose:

- preserve decentralization
- resist adaptive capture

---

# 6. Experimental Assumptions

Current assumptions:

- partial synchrony
- bounded validator count
- trusted cryptographic primitives
- deterministic local execution
- simplified network timing

---

# 7. Known Unproven Properties

The following remain unproven:

- weighted quorum intersection proof
- asynchronous liveness
- trust convergence proof
- probabilistic adversarial bounds
- adaptive quorum formal correctness

These are active research areas.

---

# 8. Research Goal

The long-term objective is to establish:

- adaptive Byzantine resilience
- trust-aware quorum safety
- predictive consensus survivability
- stable temporal trust evolution
- cyber-physical consensus robustness
