#!/usr/bin/env bash

set -euo pipefail

# =====================================================
# AEGIS v5
# Predictive Epistemic Adaptive Consensus
# =====================================================

STATE_DIR="state"
TRUST_FILE="$STATE_DIR/trust_v5.db"

mkdir -p "$STATE_DIR"
mkdir -p metrics
mkdir -p attacks
mkdir -p history

VALIDATORS=("A" "B" "C" "D")

# =====================================================
# PARAMETERS
# =====================================================

ALPHA=80

MIN_TRUST=25
MAX_TRUST=100

SLASH=35
RECOVER=6

PREPARE_THRESHOLD=55
COMMIT_THRESHOLD=52

JOIN_THRESHOLD=50
STAY_THRESHOLD=52

FAILED=0

# =====================================================
# INIT DATABASE
# =====================================================

if [ ! -f "$TRUST_FILE" ]; then

cat > "$TRUST_FILE" <<DBEOF
A|90|95|92|91
B|88|90|85|87
C|30|20|25|30
D|25|15|20|25
DBEOF

fi

# =====================================================
# LOAD TRUST
# =====================================================

declare -A CRYPTO
declare -A BEHAVIOR
declare -A LATENCY
declare -A SENSOR

declare -A EFFECTIVE
declare -A CONFIDENCE
declare -A PARTICIPATING

declare -A RISK
declare -A PREV_CONFIDENCE
declare -A OSCILLATION

while IFS='|' read -r V C B L S; do

    CRYPTO[$V]=$C
    BEHAVIOR[$V]=$B
    LATENCY[$V]=$L
    SENSOR[$V]=$S

done < "$TRUST_FILE"

# =====================================================
# LATENCY DRIFT
# =====================================================

for V in "${VALIDATORS[@]}"; do

    LATENCY[$V]=$(( ${LATENCY[$V]} + RANDOM % 10 - 5 ))

    if [ "${LATENCY[$V]}" -lt 0 ]; then
        LATENCY[$V]=0
    fi

    if [ "${LATENCY[$V]}" -gt 100 ]; then
        LATENCY[$V]=100
    fi

done

# =====================================================
# BYZANTINE EVENTS
# =====================================================

for V in "${VALIDATORS[@]}"; do

    if (( RANDOM % 4 == 0 )); then

        echo "[BYZANTINE EVENT] $V equivocation"

        BEHAVIOR[$V]=$(( ${BEHAVIOR[$V]} - SLASH ))

    fi

done

# =====================================================
# EFFECTIVE TRUST + PREDICTIVE RISK
# =====================================================

TOTAL_WEIGHT=0

for V in "${VALIDATORS[@]}"; do

    # ============================================
    # BASE EFFECTIVE TRUST
    # ============================================

    EFFECTIVE[$V]=$(( (
        40 * ${CRYPTO[$V]} +
        30 * ${BEHAVIOR[$V]} +
        15 * ${LATENCY[$V]} +
        15 * ${SENSOR[$V]}
    ) / 100 ))

    if [ "${EFFECTIVE[$V]}" -lt 0 ]; then
        EFFECTIVE[$V]=0
    fi

    # ============================================
    # CONFIDENCE
    # ============================================

    CONFIDENCE[$V]=$(( (
        ${CRYPTO[$V]} +
        ${BEHAVIOR[$V]} +
        ${LATENCY[$V]} +
        ${SENSOR[$V]}
    ) / 4 ))

    if [ "${CONFIDENCE[$V]}" -lt 0 ]; then
        CONFIDENCE[$V]=0
    fi

    # ============================================
    # PREDICTIVE EPISTEMIC RISK
    # ============================================

    PREV=${PREV_CONFIDENCE[$V]:-50}

    DELTA=$(( CONFIDENCE[$V] - PREV ))

    if [ "$DELTA" -lt 0 ]; then
        DELTA=$(( -DELTA ))
    fi

    # ============================================
    # PARTICIPATION STATE
    # ============================================

    if [ "${PARTICIPATING[$V]:-0}" -eq 1 ]; then
        CURRENT_STATE=1
    else
        CURRENT_STATE=0
    fi

    # ============================================
    # OSCILLATION MEMORY
    # ============================================

    PREV_STATE=${OSCILLATION[$V]:-0}

    if [ "$CURRENT_STATE" -ne "$PREV_STATE" ]; then

        OSCILLATION[$V]=$(( ${OSCILLATION[$V]:-0} + 1 ))

    else

        OSCILLATION[$V]=${OSCILLATION[$V]:-0}

    fi

    # ============================================
    # RISK COMPUTATION
    # ============================================

    RISK[$V]=$(( (
        2 * DELTA +
        ${OSCILLATION[$V]:-0} +
        (100 - ${LATENCY[$V]}) / 5
    ) / 4 ))

    PREV_CONFIDENCE[$V]=${CONFIDENCE[$V]}
    # ============================================
    # ANTICIPATORY CONTAINMENT
    # ============================================

    if [ "${RISK[$V]}" -gt 15 ]; then

        EFFECTIVE[$V]=$(( EFFECTIVE[$V] * 85 / 100 ))

    fi

    # ============================================
    # TOTAL ACTIVE WEIGHT
    # ============================================

    if [ "${EFFECTIVE[$V]}" -ge "$MIN_TRUST" ]; then

        TOTAL_WEIGHT=$(( TOTAL_WEIGHT + ${EFFECTIVE[$V]} ))

    fi

done

# =====================================================
# SAFETY
# =====================================================

HONEST_ESTIMATE=0

for V in "${VALIDATORS[@]}"; do

    if [ "${CONFIDENCE[$V]}" -ge 55 ]; then

        HONEST_ESTIMATE=$(( HONEST_ESTIMATE + ${EFFECTIVE[$V]} ))

    fi

done

if [ "$TOTAL_WEIGHT" -gt 0 ]; then

    SAFETY=$(( 100 * HONEST_ESTIMATE / TOTAL_WEIGHT ))

else

    SAFETY=0

fi

# =====================================================
# ADAPTIVE QUORUM
# =====================================================

QUORUM_PERCENT=$(( 50 + ((100 - SAFETY) / 5) ))

if [ "$QUORUM_PERCENT" -gt 66 ]; then
    QUORUM_PERCENT=66
fi

if [ "$QUORUM_PERCENT" -lt 50 ]; then
    QUORUM_PERCENT=50
fi

QUORUM=$(( QUORUM_PERCENT * TOTAL_WEIGHT / 100 ))

# =====================================================
# PRIMARY SELECTION
# =====================================================

PRIMARY=""
BEST=0

for V in "${VALIDATORS[@]}"; do

    if [ "${EFFECTIVE[$V]}" -gt "$BEST" ]; then

        BEST=${EFFECTIVE[$V]}
        PRIMARY=$V

    fi

done

# =====================================================
# OUTPUT
# =====================================================

echo "================================="
echo "AEGIS v5"
echo "================================="
echo "Total trust weight : $TOTAL_WEIGHT"
echo "Adaptive quorum    : $QUORUM"

echo
echo "Safety envelope : ${SAFETY}%"

echo
echo "Primary selected : $PRIMARY"
echo "Primary trust    : $BEST"

# =====================================================
# PREPARE PHASE
# =====================================================

PREPARE_WEIGHT=0

echo
echo "----- PREPARE PHASE -----"

for V in "${VALIDATORS[@]}"; do

    W=${EFFECTIVE[$V]}
    CONF=${CONFIDENCE[$V]}
    R=${RISK[$V]}

    if [ "${PARTICIPATING[$V]:-0}" -eq 1 ]; then
        THRESHOLD=$STAY_THRESHOLD
    else
        THRESHOLD=$JOIN_THRESHOLD
    fi

    if [ "$CONF" -ge "$THRESHOLD" ]; then

        PARTICIPATING[$V]=1

        PREPARE_WEIGHT=$(( PREPARE_WEIGHT + W ))

        echo "$V PREPARE yes weight=$W confidence=$CONF risk=$R threshold=$THRESHOLD"

    else

        PARTICIPATING[$V]=0

        echo "$V PREPARE abstain confidence=$CONF risk=$R threshold=$THRESHOLD"

    fi

done

echo
echo "Prepare weight = $PREPARE_WEIGHT"

if [ "$PREPARE_WEIGHT" -lt "$QUORUM" ]; then

    echo "[FAIL] prepare quorum"

    FAILED=1

fi

# =====================================================
# COMMIT PHASE
# =====================================================

COMMIT_WEIGHT=0

echo
echo "----- COMMIT PHASE -----"

for V in "${VALIDATORS[@]}"; do

    W=${EFFECTIVE[$V]}
    CONF=${CONFIDENCE[$V]}

    if [ "$CONF" -ge "$COMMIT_THRESHOLD" ]; then

        COMMIT_WEIGHT=$(( COMMIT_WEIGHT + W ))

        echo "$V COMMIT yes weight=$W"

    else

        echo "$V COMMIT abstain"

    fi

done

echo
echo "Commit weight = $COMMIT_WEIGHT"

if [ "$COMMIT_WEIGHT" -lt "$QUORUM" ]; then

    echo "[FAIL] commit quorum"

    FAILED=1

fi

echo

if [ "$FAILED" -eq 0 ]; then

    echo "[SUCCESS] consensus finalized"

fi

# =====================================================
# TRUST UPDATE
# =====================================================

TMP=$(mktemp)

ROUND_NUMBER="${ROUND_NUMBER:-0}"

if [ ! -f history/trust.csv ]; then

    echo "round,validator,crypto,behavior,latency,sensor,effective" \
    > history/trust.csv

fi

for V in "${VALIDATORS[@]}"; do

    NEW_CRYPTO=${CRYPTO[$V]}
    NEW_BEHAVIOR=${BEHAVIOR[$V]}
    NEW_LATENCY=${LATENCY[$V]}
    NEW_SENSOR=${SENSOR[$V]}

    if (( RANDOM % 40 == 0 )); then
        NEW_CRYPTO=$(( NEW_CRYPTO - 15 ))
    else
        NEW_CRYPTO=$(( NEW_CRYPTO + 1 ))
    fi

    if [ "$NEW_BEHAVIOR" -lt 100 ]; then
        NEW_BEHAVIOR=$(( NEW_BEHAVIOR + RECOVER ))
    fi

    LATENCY_DRIFT=$(( RANDOM % 11 - 5 ))
    NEW_LATENCY=$(( NEW_LATENCY + LATENCY_DRIFT ))

    if (( RANDOM % 25 == 0 )); then
        NEW_SENSOR=$(( NEW_SENSOR - 10 ))
    else
        NEW_SENSOR=$(( NEW_SENSOR + 1 ))
    fi

    for FIELD in \
        NEW_CRYPTO \
        NEW_BEHAVIOR \
        NEW_LATENCY \
        NEW_SENSOR
    do

        VALUE=${!FIELD}

        if [ "$VALUE" -gt 100 ]; then
            VALUE=100
        fi

        if [ "$VALUE" -lt 0 ]; then
            VALUE=0
        fi

        printf -v "$FIELD" "%s" "$VALUE"

    done

    EFFECTIVE_NEW=$(( (
        40 * NEW_CRYPTO +
        30 * NEW_BEHAVIOR +
        15 * NEW_LATENCY +
        15 * NEW_SENSOR
    ) / 100 ))

    echo "$V|$NEW_CRYPTO|$NEW_BEHAVIOR|$NEW_LATENCY|$NEW_SENSOR" \
    >> "$TMP"

    printf "%s,%s,%s,%s,%s,%s,%s\n" \
        "$ROUND_NUMBER" \
        "$V" \
        "$NEW_CRYPTO" \
        "$NEW_BEHAVIOR" \
        "$NEW_LATENCY" \
        "$NEW_SENSOR" \
        "$EFFECTIVE_NEW" \
    >> history/trust.csv

done

mv "$TMP" "$TRUST_FILE"

echo
echo "================================="
echo "AEGIS v5 completed"
echo "================================="

if [ "$FAILED" -eq 1 ]; then
    exit 1
fi
