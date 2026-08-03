#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
for d in lab01_rgbd_pipeline lab02_digital_twin lab03_action_pipeline capstone_delivery_robot; do
  echo "===== $d ====="
  case "$d" in
    lab01_rgbd_pipeline) (cd "$d" && bash run_pipeline.sh) ;;
    lab02_digital_twin) (cd "$d" && bash run_experiment.sh) ;;
    lab03_action_pipeline) (cd "$d" && bash run_action.sh) ;;
    capstone_delivery_robot) (cd "$d" && bash run_capstone.sh) ;;
  esac
done
echo "모든 패키지 실행 완료"
