#!/usr/bin/env bash
set -euo pipefail

LEDGER="ledger/chain.log"

PREV_HASH="GENESIS"

mapfile -t LINES < "$LEDGER"

for ((i=1; i<${#LINES[@]}; i++)); do
  IFS='|' read -r P TS AGENT TYPE PAYLOAD HASH SIG <<< "${LINES[$i]}"

  if [ "$P" != "$PREV_HASH" ]; then
    echo "[FAIL] broken chain at line $i"
    exit 1
  fi

  PREV_HASH="$HASH"
done

echo "[OK] ledger verified"
