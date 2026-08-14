# Canonical benchmark

`canonical_scenarios.py` is the reproducible six-scenario benchmark for the tag4 reference kernel.

- Scenarios: clean, burst, slow drift, stealth, equivocation, mixed.
- Seeds: 10 frozen integer seeds.
- Horizon: 30 rounds per scenario/seed.
- Attack generation: deterministic scenario schedule.
- Detector perturbation: seeded and reproducible.
- Repeated identical seed: identical trace.

`comparative_reference.py` is a fixed weighted-quorum reference comparator. It is not a PBFT or HotStuff implementation.
