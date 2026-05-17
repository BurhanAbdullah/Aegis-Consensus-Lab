#!/usr/bin/env bash

mkdir -p experiments

OUTPUT="experiments/phase_space.csv"

echo "slash,recover,successes" > "$OUTPUT"

for SLASH in 10 15 20 25 30 35; do

    for RECOVER in 1 2 3 4 5 6; do

        sed -i "s/^SLASH=.*/SLASH=$SLASH/" core/consensus_v4.sh
        sed -i "s/^RECOVER=.*/RECOVER=$RECOVER/" core/consensus_v4.sh

        rm -f metrics/results.csv
        rm -f history/trust.csv
        rm -f state/trust_v4.db

        ./simulator/rounds.sh 200 > /dev/null 2>&1

        SUCCESS=$(grep ",success" metrics/results.csv | wc -l)

        echo "$SLASH,$RECOVER,$SUCCESS" \
        | tee -a "$OUTPUT"

        echo "SLASH=$SLASH RECOVER=$RECOVER SUCCESS=$SUCCESS"

    done

done
