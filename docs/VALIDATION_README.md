# Validation run

From repository root:

```bash
PYTHONPATH=research:research/transactions_rebuild:research/transactions_rebuild/kernel python -m pytest -q research/transactions_rebuild
PYTHONPATH=research:research/transactions_rebuild:research/transactions_rebuild/kernel python -m research.transactions_rebuild.benchmarks.canonical_scenarios
PYTHONPATH=research:research/transactions_rebuild:research/transactions_rebuild/kernel python -m research.transactions_rebuild.benchmarks.comparative_reference
```

The CI workflow repeats the test suite and canonical benchmark and requires identical repeated benchmark output.