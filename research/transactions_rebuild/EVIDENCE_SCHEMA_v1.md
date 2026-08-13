# Detector Evidence Schema v1 — tag4

## Purpose
Define the deterministic interface between detector outputs and the trust dynamics.

## Per-validator detector vector
For validator i and round k:

D_{i,k} = (s^N_{i,k}, s^C_{i,k}, s^J_{i,k}, s^R_{i,k})

where N, C, J, and R denote NIS, CUSUM, Jacobian-precursor, and temporal-risk channels.

## Channel normalization
For channel j with positive threshold h_j:

d^j_{i,k} = clip(max(s^j_{i,k},0)/h_j, 0, 1).

The threshold is a detector-level configuration parameter. It is not chosen from a desired final consensus result.

## Evidence aggregation
Let omega_j >= 0 and sum_j omega_j = 1. Then

e_{i,k} = clip(sum_j omega_j d^j_{i,k}, 0, 1).

Reference weights are equal by default (1/4 each) until a data-driven calibration protocol is explicitly justified. Equal weights are not claimed to be optimal.

## Determinism contract
Given the same detector vector, thresholds, and weights, the output e_{i,k} must be identical. The mapping contains no random number generation, hidden state, attack generation, or stochastic detector model.

## Separation of variables
The following must not be conflated:

- raw detector statistic s;
- normalized detector score d;
- aggregate evidence e;
- predictive risk R;
- trust tau;
- governance influence G;
- quorum q.

## Current implementation
`detector_evidence.py` is the reference implementation. `test_detector_evidence.py` checks bounds, zero/full response, explicit weights, deterministic validator ordering, and invalid-weight rejection.

## Theorem consequence
If detector evidence is stochastic in the experimental model, deterministic trust-equilibrium statements apply only conditionally on a stationary realization or must be replaced by an appropriate stochastic-stability statement. This is a mandatory proof gate, not an optional caveat.
