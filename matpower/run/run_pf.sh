#!/usr/bin/env bash
set -euo pipefail

CASE="$1"
OUT="matpower/run/last_pf.txt"

octave --quiet --eval "
mpc = loadcase('$CASE');
r = runpf(mpc);
f = r.bus(:,8);     % voltage magnitude
a = r.bus(:,9);     % voltage angle
for i=1:length(f)
  printf('%d,%.4f,%.4f\n', i, f(i), a(i));
end
" > "$OUT"

echo "[OK] power flow executed"
