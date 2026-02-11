#!/usr/bin/env bash
set -euo pipefail

LEDGER="ledger/chain.log"

PREV_HASH="GENESIS"

mapfile -t LINES < "$LEDGER"

for ((i=1; i<${#LINES[@]}; i++)); do
  IFS='|' read -r P TS AGENT TYPE PAYLOAD HASH SIG <<< "${LINES[$i]}"

  # 1) chain integrity
  if [ "$P" != "$PREV_HASH" ]; then
    echo "[FAIL] broken chain at line $i"
    exit 1
  fi

  # 2) hash correctness
  DATA="$P|$TS|$AGENT|$TYPE|$PAYLOAD"
  CALC_HASH=$(printf "%s" "$DATA" | sha256sum | awk '{print $1}')

  if [ "$CALC_HASH" != "$HASH" ]; then
    echo "[FAIL] hash mismatch at line $i"
    echo " expected: $HASH"
    echo " computed: $CALC_HASH"
    exit 1
  fi

  PREV_HASH="$HASH"
done

echo "[OK] ledger verified (chain + hash)"
