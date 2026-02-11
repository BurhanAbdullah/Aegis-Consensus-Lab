#!/usr/bin/env bash
set -euo pipefail

LEDGER="ledger/chain.log"

PREV_HASH="GENESIS"
mapfile -t LINES < "$LEDGER"

for ((i=1; i<${#LINES[@]}; i++)); do
  IFS='|' read -r P TS AGENT TYPE PAYLOAD HASH SIG <<< "${LINES[$i]}"

  # --- 1) chain integrity ---
  if [ "$P" != "$PREV_HASH" ]; then
    echo "[FAIL] broken chain at line $i"
    exit 1
  fi

  # --- 2) hash correctness ---
  DATA="$P|$TS|$AGENT|$TYPE|$PAYLOAD"
  CALC_HASH=$(printf "%s" "$DATA" | sha256sum | awk '{print $1}')

  if [ "$CALC_HASH" != "$HASH" ]; then
    echo "[FAIL] hash mismatch at line $i"
    exit 1
  fi

  # --- 3) signature verification ---
  PUBKEY="keys/$AGENT.pub"
  if [ ! -f "$PUBKEY" ]; then
    echo "[FAIL] missing public key for $AGENT"
    exit 1
  fi

  printf "%s" "$SIG" | base64 -d > /tmp/sig.bin
  printf "%s" "$HASH" | \
    openssl dgst -sha256 -verify "$PUBKEY" -signature /tmp/sig.bin \
    > /dev/null 2>&1 || {
      echo "[FAIL] bad signature at line $i (agent=$AGENT)"
      exit 1
    }

  PREV_HASH="$HASH"
done

echo "[OK] ledger verified (chain + hash + signature)"
