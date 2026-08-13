# tag4 end-to-end harness

The harness composes the canonical detector-evidence interface with the deterministic trust/risk/governance kernel.

Pipeline:

`detector observations -> normalized evidence -> trust/risk update -> governance influence -> adaptive quorum -> certificate decision`

The harness does not generate attacks, noise, or labels. Those are supplied by the scenario layer, preserving causal separation and deterministic replay.

## Limitation
This is an integration harness, not the final benchmark runner. It must still be connected to the repository's validated NIS/CUSUM/Jacobian implementations and the final authenticated PBFT certificate layer before production results are generated.
