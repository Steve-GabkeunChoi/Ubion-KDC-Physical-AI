#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
rm -rf results
mkdir -p results
python3 run_capstone.py
printf '\n[완료] 주요 결과\n'
cat results/evaluation_report.txt
ls -lh results
