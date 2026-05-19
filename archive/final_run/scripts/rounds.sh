#!/usr/bin/env bash

set +e

ROUNDS="${1:-100}"

mkdir -p metrics
mkdir -p attacks

RESULTS="metrics/results.csv"

# =====================================================
# RESULTS HEADER
# =====================================================

echo "round,total_weight,quorum,safety,prepare_weight,commit_weight,primary,status" \
> "$RESULTS"

# =====================================================
# RUN SIMULATION
# =====================================================

for ((ROUND=1; ROUND<=ROUNDS; ROUND++)); do

    echo
    echo "======================================="
    echo "ROUND $ROUND"
    echo "======================================="

    export ROUND_NUMBER="$ROUND"

    OUT=$(bash core/consensus_v4.sh 2>&1)

    EXIT_CODE=$?

    echo "$OUT"

    # =================================================
    # STATUS
    # =================================================

    if [ "$EXIT_CODE" -eq 0 ]; then

        STATUS="success"

    else

        STATUS="fail"

    fi

    # =================================================
    # METRICS EXTRACTION
    # =================================================

    TOTAL_WEIGHT=$(echo "$OUT" \
        | grep "Total trust weight" \
        | awk '{print $5}' \
        | tail -1)

    QUORUM=$(echo "$OUT" \
        | grep "Adaptive quorum" \
        | awk '{print $4}' \
        | tail -1)

    SAFETY=$(echo "$OUT" \
        | grep "Safety envelope" \
        | awk '{print $4}' \
        | tr -d '%' \
        | tail -1)

    PREPARE_WEIGHT=$(echo "$OUT" \
        | grep "Prepare weight" \
        | awk '{print $4}' \
        | tail -1)

    COMMIT_WEIGHT=$(echo "$OUT" \
        | grep "Commit weight" \
        | awk '{print $4}' \
        | tail -1)

    PRIMARY=$(echo "$OUT" \
        | grep "Primary selected" \
        | awk '{print $4}' \
        | tail -1)

    # =================================================
    # FALLBACKS
    # =================================================

    TOTAL_WEIGHT=${TOTAL_WEIGHT:-0}
    QUORUM=${QUORUM:-0}
    SAFETY=${SAFETY:-0}
    PREPARE_WEIGHT=${PREPARE_WEIGHT:-0}
    COMMIT_WEIGHT=${COMMIT_WEIGHT:-0}
    PRIMARY=${PRIMARY:-none}

    # =================================================
    # SAVE RESULTS
    # =================================================

    echo "$ROUND,$TOTAL_WEIGHT,$QUORUM,$SAFETY,$PREPARE_WEIGHT,$COMMIT_WEIGHT,$PRIMARY,$STATUS" \
    >> "$RESULTS"

done

echo
echo "======================================="
echo "SIMULATION COMPLETE"
echo "======================================="

echo
echo "Results:"
echo "  metrics/results.csv"
echo "  history/trust.csv"
