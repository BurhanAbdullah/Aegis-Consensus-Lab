#!/usr/bin/env bash
OBS="$1"

BUS=$(echo "$OBS" | cut -d, -f1)
VMAG=$(echo "$OBS" | cut -d, -f2)

awk -v v="$VMAG" '
  v < 0.90 { print "load_shed" }
  v < 0.85 { print "isolate_bus" }
  v >= 0.90 { print "no_action" }
'
