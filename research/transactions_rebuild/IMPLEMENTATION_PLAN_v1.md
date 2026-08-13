# Implementation Plan v1 — tag4

## Canonical module boundaries

### detector/evidence
Input: measurement/innovation trace.
Output: normalized evidence E_i,k in [0,1].
Constraint: no ground-truth attack label may enter the evidence computation.

### trust
Input: T_i,k, E_i,k, recovery parameters.
Output: T_i,k+1 and tau_i,k.

### risk
Input: R_i,k, E_i,k, observable drift D_i,k.
Output: R_i,k+1.

### governance
Input: tau_i,k and R_i,k.
Output: G_i,k, active set, aggregate trust, quorum fraction q_k.

### consensus
Input: authenticated phase votes and G_i,k/q_k.
Output: certificate weight, decision, equivocation events.

### scenarios
Generates deterministic attack/noise schedules from a seed. It must not implement trust or quorum equations.

### runner
Runs scenarios against the deterministic protocol kernel and writes round-level traces plus aggregate metrics.

## Required trace schema
Each round must contain at minimum:
`seed, round, height, view, validator_id, honest_ground_truth, trust_crypto, trust_behavior, trust_latency, trust_sensor, tau, evidence, drift, risk, influence, active, total_weight, quorum_fraction, quorum_weight, prepare_weight, commit_weight, finalized, equivocation`.

## Determinism requirement
Given identical scenario file, parameters, and seed, the kernel must produce byte-equivalent or numerically equivalent traces. Randomness is permitted only in the scenario generator and measurement-noise layer.

## Test gates
Before experiment generation:
1. trust bounds;
2. risk bounds;
3. influence bounds;
4. quorum bounds;
5. deterministic replay;
6. certificate intersection counterexample search for b >= 1/3;
7. certificate safety tests for b < 1/3 under theorem assumptions;
8. availability tests under honest participation loss;
9. parameter-boundary tests;
10. regression test that the production kernel matches the reference equations on fixed traces.

## Migration policy
Do not delete legacy code yet. Mark it as legacy and isolate it from the final runner until the replacement kernel passes all tests. This preserves reproducibility of earlier repository results while preventing accidental use in final experiments.
