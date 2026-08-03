#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
mkdir -p results bus
rm -f results/* bus/*
python3 sensor_node.py
python3 perception_node.py
python3 pointcloud.py
printf '\n[완료] 생성 결과\n'
ls -lh results
