# AEGIS Expert Validation Harness

This directory is an evidence-first validation layer for the AEGIS research repository.

It deliberately separates:

1. historical reproducibility checks;
2. independent statistical analysis;
3. blind mathematical tests;
4. external power-flow validation;
5. publication figure generation.

The harness must never rewrite historical results. A result is classified as `VERIFIED`, `PARTIALLY_VERIFIED`, `NOT_VERIFIED`, or `CONTRADICTED` rather than being forced into a positive outcome.

Run locally:

```bash
python research_validation/audit.py --output research_validation/results
```

The GitHub Actions workflow additionally installs `pandapower`, `pypsa`, `matplotlib`, `pandas`, `numpy`, and `scipy` and executes the reproducibility and independent solver checks.

Important: the public repository's historical v4 implementation is stochastic and four-validator. The harness therefore does not treat old stochastic outputs as deterministic unless the original experiment actually recorded sufficient seed/state information.
