#!/usr/bin/env bash
set -euo pipefail

LEDGER="ledger/chain.log"
RISK="state/risk.conf"
# --- current epoch ---
EPOCH=$(grep '|observation|reset_epoch' "$LEDGER" | wc -l)

VOTES=$(awk -F'|' -v epoch="$EPOCH" '
  BEGIN { e=0 }
  $4=="observation" && $5=="reset_epoch" { e++ }
  e==epoch && $4=="proposal" { print }
' "$LEDGER")
