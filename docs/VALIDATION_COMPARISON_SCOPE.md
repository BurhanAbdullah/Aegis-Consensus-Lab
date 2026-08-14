# Validation and comparison scope

## Canonical benchmark
The canonical benchmark is generated from `research/transactions_rebuild/kernel/tag4_kernel.py` and the explicit six-scenario input generator. It uses ten frozen seeds and thirty rounds per scenario/seed.

## Metrics
The benchmark records finalization, quorum margin, detector evidence, detector drift, attack-active state, detection and recovery markers, and adaptive quorum fraction. Per-seed finalization rates are summarized with 95% confidence intervals.

## Comparator
The repository contains a fixed weighted-quorum reference at `q=0.67` using exactly the same scenario traces, validators, rounds and seeds. This is an analytical/reference comparator only.

It is **not** PBFT, HotStuff, or another named production consensus implementation. No performance claim against PBFT or HotStuff is permitted until those protocols are implemented or independently benchmarked under the same conditions.

## Physical-system evidence
The previously reported 9,450-case physical-system result is excluded from the submission evidence set. It is not regenerated or inferred. It can only be reinstated when raw case-level inputs, controller/network mapping, execution artifacts and provenance are available.
