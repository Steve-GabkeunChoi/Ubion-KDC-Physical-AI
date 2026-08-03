#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
mkdir -p results
rm -f results/*
python3 calibrate.py
python3 compare_results.py
printf '\n[완료] 생성 결과\n'
ls -lh results
