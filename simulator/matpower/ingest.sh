#!/usr/bin/env bash
FILE="$1"

[ ! -f "$FILE" ] && { echo "file not found"; exit 1; }

while read -r line; do
  ledger/append_block.sh agent_A observation "$line"
  sleep 0.5
done < "$FILE"
