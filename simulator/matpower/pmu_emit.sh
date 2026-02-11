#!/usr/bin/env bash
set -euo pipefail

PF="matpower/run/last_pf.txt"

[ -f "$PF" ] || { echo "[FAIL] no PF data"; exit 1; }

while IFS= read -r line; do
  ledger/append_block.sh agent_A observation "$line"
  sleep 0.2
done < "$PF"
