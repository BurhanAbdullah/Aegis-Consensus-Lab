#!/usr/bin/env bash

TOTAL="$1"
shift

H=0

for W in "$@"; do

  P=$(awk "BEGIN {print $W/$TOTAL}")

  if awk "BEGIN {exit !($P > 0)}"; then

    TERM=$(awk "BEGIN {print -1 * $P * log($P)}")

    H=$(awk "BEGIN {print $H + $TERM}")

  fi

done

echo "$H"
