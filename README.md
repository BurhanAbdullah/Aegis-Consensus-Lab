🛡 Aegis Consensus Lab
Adaptive-Trust PBFT (AT-PBFT)

Aegis Consensus Lab is a research framework for adaptive Byzantine fault tolerance in distributed and cyber-physical systems.

It extends Practical Byzantine Fault Tolerance (PBFT) with:

Adaptive trust scoring

Weighted quorum formation

Dynamic primary rotation

Slashing & recovery

Cryptographic block sealing

View change under failure

Adversarial simulation support

Aegis is built for experimentation, resilience modeling, and security research — not cryptocurrency.

Why Aegis?

Classical PBFT assumes:

Static validator trust

Binary fault model (honest or Byzantine)

Fixed quorum (2f + 1)

Real-world infrastructure does not behave this way.

Nodes degrade.
Trust erodes gradually.
Partial compromise happens.
Leaders fail intermittently.

AT-PBFT introduces continuous trust adaptation and weighted consensus to better model modern distributed environments.

Architecture
agents/        Validator nodes
core/          Consensus engine
consensus/     Proposal & decision logic
ledger/        Block append & verification
state/         Runtime state (view, trust)
policies/      Governance & safety constraints
metrics/       Agreement & safety evaluation
attacks/       Adversarial scenarios
simulator/     Cyber-physical integration


The system is modular and shell-based for transparency and auditability.
