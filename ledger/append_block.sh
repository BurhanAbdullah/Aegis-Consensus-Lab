#!/usr/bin/env bash
set -euo pipefail

AGENT="$1"
TYPE="$2"
PAYLOAD="$3"
# ---- quorum enforcement for proposals ----
if [ "$TYPE" = "proposal" ]; then
  ACTION="$PAYLOAD"
  REQUIRED=$(grep "^$ACTION=" state/action_quorum.conf | cut -d= -f2)
  REQUIRED=${REQUIRED:-1}

  COUNT=$(tail -n 50 "$LEDGER" | \
    awk -F'|' -v act="$ACTION" '$4=="proposal" && $5==act {print $3}' | \
    sort -u | wc -l)

  if [ "$COUNT" -lt "$REQUIRED" ]; then
    echo "[REJECTED] quorum not met for $ACTION ($COUNT/$REQUIRED)"
    exit 1
  fi
fi

KEY="keys/$AGENT.pem"
LEDGER="ledger/chain.log"
LOCK="ledger/.chain.lock"

[ -f "$KEY" ] || { echo "[FAIL] missing key $KEY"; exit 1; }

# ---- acquire exclusive lock ----
exec 9>"$LOCK"
flock -x 9

TS=$(date -u +%s)
PREV_HASH=$(tail -n 1 "$LEDGER" | awk -F'|' '{print $6}')

DATA="$PREV_HASH|$TS|$AGENT|$TYPE|$PAYLOAD"
HASH=$(printf "%s" "$DATA" | sha256sum | awk '{print $1}')

SIG=$(printf "%s" "$HASH" | \
  openssl dgst -sha256 -sign "$KEY" | base64 -w0)

echo "$PREV_HASH|$TS|$AGENT|$TYPE|$PAYLOAD|$HASH|$SIG" >> "$LEDGER"

echo "[OK] block appended by $AGENT"
LAST_TYPE=$(tail -n 1 "$LEDGER" | awk -F'|' '{print $4}')

# ---- finality rule ----
if [ "$LAST_TYPE" = "verdict" ] && [ "$TYPE" != "observation" ]; then
  echo "[REJECTED] verdict is final — new observation required"
  exit 1
fi
