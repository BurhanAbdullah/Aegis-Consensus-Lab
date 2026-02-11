#!/usr/bin/env bash
set -euo pipefail

LEDGER="ledger/ledger.log"
VOTES="logs/votes.log"
VALIDATORS="validators/list.txt"
TRUST_FILE="state/trust.txt"
VIEW_FILE="state/view.txt"

SLASH_AMOUNT=20
RECOVERY_RATE=2
DECAY_RATE=1
MIN_TRUST=30
MAX_TRUST=150

ID="${1:-}"

if [ -z "$ID" ]; then
  echo "Usage: consensus.sh <proposal_id>"
  exit 1
fi

mkdir -p ledger logs state
touch "$LEDGER" "$VOTES"

# -------- INIT TRUST --------
if [ ! -f "$TRUST_FILE" ]; then
  while read -r V; do
    echo "${V}:100" >> "$TRUST_FILE"
  done < "$VALIDATORS"
fi

# -------- LOAD TRUST --------
declare -A TRUST
declare -A ACTIVE
TOTAL_TRUST=0

while IFS=':' read -r V T; do
  TRUST[$V]=$T
done < "$TRUST_FILE"

# -------- TRUST DECAY (inactive penalty) --------
for V in "${!TRUST[@]}"; do
  TRUST[$V]=$(( TRUST[$V] - DECAY_RATE ))
  if [ "${TRUST[$V]}" -lt 0 ]; then TRUST[$V]=0; fi
done

# -------- SELECT PRIMARY (highest trust) --------
PRIMARY=""
HIGHEST=0

for V in "${!TRUST[@]}"; do
  if [ "${TRUST[$V]}" -gt "$HIGHEST" ]; then
    HIGHEST=${TRUST[$V]}
    PRIMARY=$V
  fi
done

echo "Dynamic Primary: $PRIMARY (trust=$HIGHEST)"

# -------- CALCULATE ACTIVE TRUST --------
for V in "${!TRUST[@]}"; do
  if [ "${TRUST[$V]}" -ge "$MIN_TRUST" ]; then
    ACTIVE[$V]=1
    TOTAL_TRUST=$((TOTAL_TRUST + TRUST[$V]))
  fi
done

QUORUM=$(( (2 * TOTAL_TRUST) / 3 ))

PREPREPARE_OK=0
PREPARE_WEIGHT=0
COMMIT_WEIGHT=0

declare -A PREPARE_SEEN
declare -A COMMIT_SEEN
declare -A PHASE_TRACK

# -------- PROCESS VOTES --------
while IFS='|' read -r PID PHASE VALIDATOR VOTE SIG; do

  [ "$PID" != "$ID" ] && continue
  grep -qx "$VALIDATOR" "$VALIDATORS" || continue

  MSG="${PID}|${PHASE}|${VALIDATOR}|${VOTE}"

  SIG_FILE=$(mktemp)
  MSG_FILE=$(mktemp)

  echo "$SIG" | base64 -d > "$SIG_FILE" 2>/dev/null || { rm -f "$SIG_FILE" "$MSG_FILE"; continue; }
  printf "%s" "$MSG" > "$MSG_FILE"

  if ! openssl dgst -sha256 -verify "keys/${VALIDATOR}.pub" \
        -signature "$SIG_FILE" "$MSG_FILE" > /dev/null 2>&1; then
      echo "Invalid signature by $VALIDATOR — slashing."
      TRUST[$VALIDATOR]=$(( TRUST[$VALIDATOR] - SLASH_AMOUNT ))
      rm -f "$SIG_FILE" "$MSG_FILE"
      continue
  fi

  rm -f "$SIG_FILE" "$MSG_FILE"

  # Equivocation detection
  KEY="${VALIDATOR}_${PHASE}"
  if [ -n "${PHASE_TRACK[$KEY]+x}" ] && [ "${PHASE_TRACK[$KEY]}" != "$VOTE" ]; then
      echo "Equivocation by $VALIDATOR — slashing."
      TRUST[$VALIDATOR]=$(( TRUST[$VALIDATOR] - SLASH_AMOUNT ))
      continue
  fi
  PHASE_TRACK[$KEY]="$VOTE"

  # Skip suspended
  if [ "${TRUST[$VALIDATOR]}" -lt "$MIN_TRUST" ]; then
    continue
  fi

  WEIGHT=${TRUST[$VALIDATOR]}

  if [ "$PHASE" = "preprepare" ] && [ "$VALIDATOR" = "$PRIMARY" ]; then
      PREPREPARE_OK=1
  fi

  if [ "$PHASE" = "prepare" ] && [ "$VOTE" = "yes" ]; then
      if [ -z "${PREPARE_SEEN[$VALIDATOR]+x}" ]; then
          PREPARE_SEEN[$VALIDATOR]=1
          PREPARE_WEIGHT=$((PREPARE_WEIGHT + WEIGHT))
      fi
  fi

  if [ "$PHASE" = "commit" ] && [ "$VOTE" = "yes" ]; then
      if [ -z "${COMMIT_SEEN[$VALIDATOR]+x}" ]; then
          COMMIT_SEEN[$VALIDATOR]=1
          COMMIT_WEIGHT=$((COMMIT_WEIGHT + WEIGHT))
      fi
  fi

  # Recovery bonus for honest participation
  TRUST[$VALIDATOR]=$(( TRUST[$VALIDATOR] + RECOVERY_RATE ))
  if [ "${TRUST[$VALIDATOR]}" -gt "$MAX_TRUST" ]; then
    TRUST[$VALIDATOR]=$MAX_TRUST
  fi

done < "$VOTES"

echo "Total active trust: $TOTAL_TRUST"
echo "Quorum threshold: $QUORUM"
echo "Prepare weight: $PREPARE_WEIGHT"
echo "Commit weight: $COMMIT_WEIGHT"

if [ "$PREPREPARE_OK" -ne 1 ]; then
  echo "Primary failed."
  exit 0
fi

if [ "$PREPARE_WEIGHT" -lt "$QUORUM" ]; then
  echo "Prepare quorum not reached."
  exit 0
fi

if [ "$COMMIT_WEIGHT" -lt "$QUORUM" ]; then
  echo "Commit quorum not reached."
  exit 0
fi

# -------- SAVE TRUST --------
> "$TRUST_FILE"
for V in "${!TRUST[@]}"; do
  echo "${V}:${TRUST[$V]}" >> "$TRUST_FILE"
done

# -------- FINALIZE BLOCK --------
INDEX=$(wc -l < "$LEDGER")
TIMESTAMP=$(date +%s)

PREV_HASH=$(tail -n 1 "$LEDGER" 2>/dev/null | awk -F'|' '{print $6}')
[ -z "$PREV_HASH" ] && PREV_HASH="GENESIS"

if [ -f "proposals/${ID}.txt" ]; then
  PROPOSAL_HASH=$(sha256sum "proposals/${ID}.txt" | awk '{print $1}')
else
  PROPOSAL_HASH="NO_PROPOSAL_FILE"
fi

DATA="${INDEX}|${TIMESTAMP}|${ID}|${PROPOSAL_HASH}|${PREV_HASH}"
HASH=$(printf "%s" "$DATA" | sha256sum | awk '{print $1}')

BLOCK_SIG=$(printf "%s" "$HASH" | \
  openssl dgst -sha256 -sign keys/consensus.pem | \
  base64 -w 0)

echo "${DATA}|${HASH}|${BLOCK_SIG}" >> "$LEDGER"

echo "Consensus reached under AT-PBFT v3 (self-healing trust consensus)."

