#!/usr/bin/env bash
set -euo pipefail

AGENT="$1"
TYPE="$2"
PAYLOAD="$3"

KEY="keys/$AGENT.pem"
STATE="state/replay/$AGENT.last"

[ -f "$KEY" ] || { echo "[FAIL] missing key $KEY"; exit 1; }

TS=$(date -u +%s)

# --- anti-replay (monotonic per agent) ---
LAST_TS=0
[ -f "$STATE" ] && LAST_TS=$(cat "$STATE")

if [ "$TS" -le "$LAST_TS" ]; then
  echo "[DROP] replay detected from $AGENT"
  exit 1
fi

echo "$TS" > "$STATE"

PREV=$(tail -n 1 ledger/chain.log | awk -F'|' '{print $6}')

DATA="$PREV|$TS|$AGENT|$TYPE|$PAYLOAD"
HASH=$(printf "%s" "$DATA" | sha256sum | awk '{print $1}')

SIG=$(printf "%s" "$HASH" | \
  openssl dgst -sha256 -sign "$KEY" | base64 -w0)

printf "%s|%s|%s|%s|%s|%s|%s\n" \
  "$PREV" "$TS" "$AGENT" "$TYPE" "$PAYLOAD" "$HASH" "$SIG" \
  >> ledger/chain.log

echo "[OK] block appended by $AGENT"
