#!/usr/bin/env bash
set -euo pipefail

LEDGER="ledger/ledger.log"

PREV_HASH="GENESIS"
LINE_NUM=0

while IFS="|" read -r INDEX TIMESTAMP ID PROPOSAL_HASH STORED_PREV_HASH HASH BLOCK_SIG; do

  DATA="${INDEX}|${TIMESTAMP}|${ID}|${PROPOSAL_HASH}|${STORED_PREV_HASH}"
  CALC_HASH=$(printf "%s" "$DATA" | sha256sum | awk '{print $1}')

  if [ "$STORED_PREV_HASH" != "$PREV_HASH" ]; then
    echo "Chain broken at block $LINE_NUM (prev hash mismatch)"
    exit 1
  fi

  if [ "$CALC_HASH" != "$HASH" ]; then
    echo "Invalid hash at block $LINE_NUM"
    exit 1
  fi

  SIG_FILE=$(mktemp)
  HASH_FILE=$(mktemp)

  echo "$BLOCK_SIG" | base64 -d > "$SIG_FILE"
  printf "%s" "$HASH" > "$HASH_FILE"

  if ! openssl dgst -sha256 -verify keys/consensus.pub \
      -signature "$SIG_FILE" "$HASH_FILE" > /dev/null 2>&1; then
    echo "Invalid block signature at block $LINE_NUM"
    rm -f "$SIG_FILE" "$HASH_FILE"
    exit 1
  fi

  rm -f "$SIG_FILE" "$HASH_FILE"

  PREV_HASH="$HASH"
  LINE_NUM=$((LINE_NUM + 1))

done < "$LEDGER"

echo "Chain and block signatures verified successfully."
