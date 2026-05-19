#!/usr/bin/env bash

set +e

echo "========================================="
echo "AEGIS TRUE COMPARATIVE EXPERIMENT"
echo "========================================="

mkdir -p experiments
mkdir -p archive/final_run/experiments

# =====================================================
# CLEAN OLD FILES
# =====================================================

rm -f experiments/phase_space_baseline.csv
rm -f experiments/phase_space_predictive.csv

# =====================================================
# BASELINE REGIME
# =====================================================

echo
echo "========================================="
echo "RUNNING BASELINE REGIME"
echo "========================================="

export PREDICTIVE_MODE=0

echo "slash,recover,successes" \
> experiments/phase_space_baseline.csv

for SLASH in 10 15 20 25 30 35; do

    for RECOVER in 1 2 3 4 5 6; do

        SUCCESS=0

        for ROUND in $(seq 1 200); do

            OUTPUT=$(
                SLASH=$SLASH \
                RECOVER=$RECOVER \
                PREDICTIVE_MODE=0 \
                ./core/consensus_v4.sh 2>/dev/null || true
            )

            if echo "$OUTPUT" | grep -q "\[SUCCESS\]"; then

                SUCCESS=$(( SUCCESS + 1 ))

            fi

        done

        echo "$SLASH,$RECOVER,$SUCCESS" \
        >> experiments/phase_space_baseline.csv

        echo "BASELINE: SLASH=$SLASH RECOVER=$RECOVER SUCCESS=$SUCCESS"

    done

done

# =====================================================
# PREDICTIVE REGIME
# =====================================================

echo
echo "========================================="
echo "RUNNING PREDICTIVE REGIME"
echo "========================================="

export PREDICTIVE_MODE=1

echo "slash,recover,successes" \
> experiments/phase_space_predictive.csv

for SLASH in 10 15 20 25 30 35; do

    for RECOVER in 1 2 3 4 5 6; do

        SUCCESS=0

        for ROUND in $(seq 1 200); do

            OUTPUT=$(
                SLASH=$SLASH \
                RECOVER=$RECOVER \
                PREDICTIVE_MODE=1 \
                ./core/consensus_v4.sh 2>/dev/null || true
            )

            if echo "$OUTPUT" | grep -q "\[SUCCESS\]"; then

                SUCCESS=$(( SUCCESS + 1 ))

            fi

        done

        echo "$SLASH,$RECOVER,$SUCCESS" \
        >> experiments/phase_space_predictive.csv

        echo "PREDICTIVE: SLASH=$SLASH RECOVER=$RECOVER SUCCESS=$SUCCESS"

    done

done

# =====================================================
# ARCHIVE RESULTS
# =====================================================

cp experiments/phase_space_baseline.csv \
   archive/final_run/experiments/

cp experiments/phase_space_predictive.csv \
   archive/final_run/experiments/

# =====================================================
# FINAL STATUS
# =====================================================

echo
echo "========================================="
echo "TRUE COMPARATIVE DATA GENERATED"
echo "========================================="

echo
echo "Generated files:"

ls experiments/*baseline.csv
ls experiments/*predictive.csv

echo
echo "========================================="
echo "DONE"
echo "========================================="
