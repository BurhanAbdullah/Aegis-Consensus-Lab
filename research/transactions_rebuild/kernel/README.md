# tag4 deterministic kernel

This directory contains the first production-style deterministic kernel for the Transactions rebuild.

## Files
- `tag4_kernel.py`: trust, risk, governance influence, adaptive quorum, and certificate-weight accounting.
- `test_tag4_kernel.py`: domain, deterministic replay, and equation regression tests.

## Important limitation
This is a reference protocol kernel, not yet the final PBFT implementation. Certificate authentication, equivocation handling, proposal identity, view/height semantics, and adversarial scheduling must be integrated before safety claims are accepted.

The kernel deliberately does not generate attacks or random noise internally.
