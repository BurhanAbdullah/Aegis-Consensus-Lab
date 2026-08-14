# Detector Evidence Schema v1 — tag4 canonical

## Purpose
Define the deterministic, observable interface between detector outputs and the trust/risk dynamics.

## Per-validator detector vector
For validator i and round k:

`D^{raw}_{i,k}=(s^N_{i,k},s^C_{i,k},s^J_{i,k},s^R_{i,k})`,

where N, C, J, and R denote NIS, CUSUM, Jacobian-precursor, and temporal-risk channels.

## Channel normalization
For channel j with positive detector threshold h_j:

`d^j_{i,k}=clip(max(s^j_{i,k},0)/h_j,0,1)`.

The threshold is a detector-level configuration parameter. It is not selected from a desired consensus result.

## Evidence aggregation
Let omega_j >= 0 and sum_j omega_j=1. Then

`E_{i,k}=clip(sum_j omega_j d^j_{i,k},0,1)`.

Reference weights are equal by default (1/4 each) until a data-driven calibration protocol is justified. Equal weights are not claimed to be optimal.

## Canonical observable temporal drift
The normalized detector-score vector is

`d_{i,k}=(d^N_{i,k},d^C_{i,k},d^J_{i,k},d^R_{i,k})`.

For k>=1, the risk input is

`D_{i,k}=clip(||d_{i,k}-d_{i,k-1}||_2/2,0,1)`.

The factor 2 is `sqrt(4)`, the maximum Euclidean distance in the unit 4-cube. For the first round, `D_{i,0}=0` unless a prior detector vector is explicitly supplied. This definition uses only observable detector traces and never uses attack labels.

## Determinism contract
Given the same raw detector vector, thresholds, weights, and previous normalized detector vector, the output `(d,E,D)` is identical. The mapping contains no random number generation, hidden state, attack generation, or stochastic detector model.

## Separation of variables
Do not conflate:

- raw detector statistic `s`;
- normalized detector score `d`;
- aggregate evidence `E`;
- observable temporal drift `D`;
- predictive risk `R`;
- trust `tau`;
- governance influence `G`;
- quorum `q`.

## Implementation contract
`detector_evidence.py` implements the normalization and evidence aggregation. The temporal-drift function must be the only canonical construction of `D` used by the risk update. Tests must verify bounds, first-round behavior, exact zero drift, maximum-distance normalization, and deterministic repeatability.

## Theorem consequence
If detector evidence or drift is stochastic in an experimental model, deterministic equilibrium statements apply conditionally on the realized detector inputs. A stochastic convergence claim requires a separate stochastic-stability argument.
