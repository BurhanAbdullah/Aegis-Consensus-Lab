#!/usr/bin/env bash
set -euo pipefail

OBS=$(tail -n 1 ledger/chain.log | grep '|observation|' | tail -n1 | awk -F'|' '{print $5}')
[ -z "$OBS" ] && exit 0

ACTION=$(agents/freq_guard.sh "$OBS")
ledger/append_block.sh agent_B proposal "$ACTION"
