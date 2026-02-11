#!/usr/bin/env bash
set -euo pipefail

AGENT="$1"
TYPE="$2"
PAYLOAD="$3"

KEY="keys/$AGENT.pem"
STATE="state/replay/$AGENT.last"

[ -f "$KEY" ] || { echo "[FAIL] missing key $KEY"; exit 1; }

TS=$(date -u +%s)

# --- anti-replay: monotonic timestamp per agent ---
LAST_TS=0
[ -f "$STATE" ] && LAST_TS=$(cat "$STATE")

if [ "$TS" -le "$LAST_TS" ]; then
  echo "[REPLAY BLOCKED] $AGENT timestamp $TS <= $LAST_TS"
  exit 1
fi

PREV_HASH=$(tail -n 1 ledger/chain.log | awk -F'|' '{print $6}')

DATA="$PREV_HASH|$TS|$AGENT|$TYPE|$PAYLOAD"
HASH=$(printf "%s" "$DATA" | sha256sum | awk '{print $1}')

SIG=$(printf "%s" "$HASH" | \
  openssl dgst -sha256 -sign "$KEY" | base64 -w0)

echo "$DATA|$HASH|$SIG" >> ledger/chain.log
echo "$TS" > "$STATE"

echo "[OK] block appended by $AGENT"
