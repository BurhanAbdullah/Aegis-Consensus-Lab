🛡 Aegis Consensus Lab
AT-PBFT: Adaptive Trust Byzantine Fault Tolerance

Aegis Consensus Lab is a research framework implementing Adaptive-Trust Practical Byzantine Fault Tolerance (AT-PBFT) for resilient distributed and cyber-physical systems.

AT-PBFT extends classical PBFT by introducing:

Dynamic trust scoring

Weighted quorum

Adaptive primary selection

Slashing and recovery mechanisms

Cryptographic block verification

Automatic view change

Adversarial scenario simulation

This repository is intended for resilience research, distributed systems experimentation, and security modeling.

1. Motivation

Traditional PBFT assumes:

Static validator set

Binary trust model (honest vs faulty)

Fixed quorum (2f + 1)

Modern infrastructure systems require:

Gradual trust degradation

Partial compromise tolerance

Dynamic leadership rotation

Replay resistance

Irreversibility safeguards

AT-PBFT introduces adaptive trust and weighted consensus to address these challenges.

2. Core Architecture
agents/        Validator nodes
core/          Consensus engine
consensus/     Propose & decision logic
ledger/        Block append & verification
state/         Runtime state (view, trust)
metrics/       Agreement & safety metrics
policies/      Governance rules
attacks/       Adversarial simulations
simulator/     Cyber-physical integration

3. Strict PBFT (v3 Base)

Implements full PBFT lifecycle:

preprepare

prepare

commit

Consensus rule:

f = floor((n - 1) / 3)
threshold = 2f + 1


Block format:

INDEX | TIMESTAMP | PROPOSAL_ID | PROPOSAL_HASH | PREV_HASH | HASH | BLOCK_SIGNATURE


Ledger verification:

./ledger/verify_chain.sh

4. Adaptive Trust Model (v4)

Trust database:

state/trust.db


Example:

agent_A|1.0
agent_B|1.0
agent_C|1.0
agent_D|1.0


Properties:

Range: 0.0 – 2.0

Default: 1.0

Increased on correct participation

Decreased on detected misbehavior

Influences quorum weight

Influences primary selection

5. Weighted Quorum

Instead of counting validators:

Σ trust(yes voters) ≥ threshold_weight


Benefits:

Gradual resilience

Reduced sensitivity to single-node compromise

Adaptive tolerance under attack

6. View Change

If quorum is not reached:

Primary failed. Initiating view change...
View changed to X


Primary rotates using:

primary = validators[ view % N ]


State stored in:

state/view.txt

7. Security Features

Full signature verification (OpenSSL)

Block-level cryptographic sealing

Replay protection

Slashing model

Trust recovery

Policy-based action irreversibility

8. Cyber-Physical Simulation

Includes:

MATPOWER integration

PMU data ingestion

Scenario-based stress testing

Delayed sensor simulation

Irreversible minority attack modeling

Designed for experimentation in critical infrastructure environments.

9. Version History

v1 – Basic chain hashing
v2 – Signature verification
v3.0.0 – Strict PBFT + View Change
v4 (in progress) – Adaptive Trust + Weighted Quorum

10. Quick Start

Initialize trust:

mkdir -p state
cat > state/trust.db << EOF
agent_A|1.0
agent_B|1.0
agent_C|1.0
agent_D|1.0
EOF


Run consensus:

./core/consensus.sh 9000


Verify ledger:

./ledger/verify_chain.sh

11. Research Direction

AT-PBFT explores:

Adaptive Byzantine tolerance

Continuous trust modeling

Trust-weighted consensus

Cyber-physical resilience

Dynamic leader selection

This is a research system — not a cryptocurrency implementation.

12. License

MIT License
