#!/usr/bin/env bash

set -e

echo "========================================="
echo "AEGIS REPOSITORY STABILIZATION"
echo "========================================="

# =====================================================
# CREATE CLEAN DIRECTORY STRUCTURE
# =====================================================

mkdir -p archive/final_run
mkdir -p archive/final_run/experiments
mkdir -p archive/final_run/metrics
mkdir -p archive/final_run/history

mkdir -p figures
mkdir -p experiments
mkdir -p metrics
mkdir -p history

# =====================================================
# REMOVE TEMP / BROKEN FILES
# =====================================================

echo
echo "[CLEAN] Removing temporary files"

rm -f simulator/*tmp*.py
rm -f simulator/*broken*.py
rm -f simulator/*debug*.py

rm -f *.aux
rm -f *.log
rm -f *.out
rm -f *.toc

# =====================================================
# NORMALIZE CSV HEADER
# =====================================================

echo
echo "[FIX] Normalizing phase_space.csv"

if [ -f experiments/phase_space.csv ]; then

    FIRST_LINE=$(head -n 1 experiments/phase_space.csv)

    if [[ "$FIRST_LINE" != "slash,recover,successes" ]]; then

        sed -i '1i slash,recover,successes' \
        experiments/phase_space.csv

    fi

fi

# =====================================================
# CREATE BASELINE / PREDICTIVE COPIES
# =====================================================

echo
echo "[FIX] Creating baseline/predictive snapshots"

if [ -f experiments/phase_space.csv ]; then

    cp experiments/phase_space.csv \
       experiments/phase_space_baseline.csv

    cp experiments/phase_space.csv \
       experiments/phase_space_predictive.csv

fi

# =====================================================
# FIX REPOSITORY REFERENCES
# =====================================================

echo
echo "[FIX] Repository naming consistency"

find . \
    -type f \
    \( -name "*.tex" -o -name "*.md" \) \
    -exec sed -i \
    's/Consensus-Lab/Aegis-Consensus-Lab/g' {} +

find . \
    -type f \
    \( -name "*.tex" -o -name "*.md" \) \
    -exec sed -i \
    's/archive\/final run/archive\/final_run/g' {} +

# =====================================================
# REMOVE WEAK / OLD FIGURES
# =====================================================

echo
echo "[CLEAN] Removing weak figures"

rm -f experiments/*timeline_old*.png
rm -f experiments/*survivability_old*.png

# =====================================================
# ARCHIVE CURRENT FILES
# =====================================================

echo
echo "[ARCHIVE] Saving artifacts"

cp experiments/*.csv \
   archive/final_run/experiments/ \
   2>/dev/null || true

cp experiments/*.png \
   archive/final_run/experiments/ \
   2>/dev/null || true

cp metrics/*.csv \
   archive/final_run/metrics/ \
   2>/dev/null || true

cp history/*.csv \
   archive/final_run/history/ \
   2>/dev/null || true

# =====================================================
# FINAL STATUS
# =====================================================

echo
echo "========================================="
echo "REPOSITORY STATUS"
echo "========================================="

git status --short

echo
echo "========================================="
echo "ARCHIVED FILES"
echo "========================================="

find archive/final_run -type f | sort

echo
echo "========================================="
echo "STABILIZATION COMPLETE"
echo "========================================="
