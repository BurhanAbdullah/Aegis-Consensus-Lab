# Runtime Verification Status — tag4

## CI gate
A GitHub Actions workflow has been added at `.github/workflows/tag4-validation.yml` to execute the tag4 pytest suite on pushes and pull requests targeting `tag4`.

## Current status
- Workflow definition: IMPLEMENTED
- Runtime execution observed for current workflow commit: NOT YET OBSERVED
- Test pass/fail claim: NOT YET MADE

## Scientific rule
A theorem or implementation item is not marked empirically verified merely because a test file exists. It becomes verified only after a recorded runtime execution passes.

## Required next evidence
1. Successful tag4 CI run.
2. Full test output archived or linked.
3. Any failures fixed before experiments begin.
4. Reference-model vs production-kernel regression pass.
