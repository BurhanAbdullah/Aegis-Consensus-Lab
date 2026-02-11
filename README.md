Perfect. Below is a clean, two-page professional README version — concise, research-grade, and publication-ready.

You can paste this directly into README.md.

🛡 Aegis Consensus Lab
AT-PBFT: Adaptive Trust Byzantine Fault Tolerance

Aegis Consensus Lab is a research framework implementing Adaptive-Trust Practical Byzantine Fault Tolerance (AT-PBFT) for cyber-physical and critical infrastructure systems.

It extends classical PBFT by introducing:

Dynamic trust scoring

Weighted quorum

Adaptive primary selection

Slashing & recovery

Cryptographic block validation

View change under primary failure

Cyber-physical simulation integration

Aegis is designed for experimentation, adversarial testing, and resilience modeling in distributed systems operating under partial compromise.

1. System Overview

1.1 Motivation

Classical PBFT assumes:

Static validator set

Binary trust model (honest vs faulty)

Fixed quorum (2f + 1)

Modern infrastructure environments require:

Gradual trust degradation

Partial compromise tolerance

Dynamic leadership

Replay resistance

Action irreversibility safeguards

AT-PBFT addresses these requirements.

1.2 Core Architecture
agents/        Validator nodes
core/          Consensus engine
consensus/     Propose & decision logic
ledger/        Block append & verification
state/         Runtime state (view, trust)
metrics/       Agreement & safety metrics
policies/      Governance & safety constraints
attacks/       Adversarial simulations
simulator/     Cyber-physical integration

