#!/usr/bin/env bash
set -euo pipefail

LEDGER="ledger/chain.log"

LINE=$(grep '|proposal|' "$LEDGER" | head -n 1)
[ -z "$LINE" ] && { echo "[ATTACK] no proposal to replay"; exit 0; }

echo "[ATTACK] replaying old signed block"
echo "$LINE" >> "$LEDGER"
