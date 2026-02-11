#!/usr/bin/env bash
set -euo pipefail

LEDGER="ledger/chain.log"

declare -A SEEN_HASH

PREV_HASH="GENESIS"
PREV_TS=0

tail -n +2 "$LEDGER" | while IFS='|' read -r P TS AGENT TYPE PAYLOAD HASH SIG; do

  # 1. Strict hash chaining
  if [ "$P" != "$PREV_HASH" ]; then
    echo "[FAIL] broken chain (prev hash mismatch)"
    exit 1
  fi

  # 2. Time must move forward
  if [ "$TS" -lt "$PREV_TS" ]; then
    echo "[FAIL] time went backwards (replay detected)"
    exit 1
  fi

  # 3. Hash correctness
  DATA="$P|$TS|$AGENT|$TYPE|$PAYLOAD"
  CHECK=$(printf "%s" "$DATA" | sha256sum | awk '{print $1}')
  if [ "$CHECK" != "$HASH" ]; then
    echo "[FAIL] hash mismatch"
    exit 1
  fi

  # 4. No duplicate blocks (anti-replay)
  if [[ -n "${SEEN_HASH[$HASH]:-}" ]]; then
    echo "[FAIL] replayed block detected"
    exit 1
  fi
  SEEN_HASH["$HASH"]=1

  # 5. Signature verification
  printf "%s" "$SIG" | base64 -d > /tmp/sig.bin
  printf "%s" "$HASH" | \
    openssl dgst -sha256 -verify "keys/$AGENT.pub" -signature /tmp/sig.bin \
    >/dev/null || { echo "[FAIL] bad signature ($AGENT)"; exit 1; }

  PREV_HASH="$HASH"
  PREV_TS="$TS"

done

echo "[OK] ledger verified"
