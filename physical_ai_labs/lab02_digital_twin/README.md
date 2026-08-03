# 실습 2 — 경량 Digital Twin과 Reality Gap 분석

## 목표
- 시뮬레이션과 현실 측정 궤적의 차이를 수치화한다.
- 마찰계수와 지연시간을 탐색해 Twin 파라미터를 보정한다.
- 보정 전·후 RMSE를 비교한다.

## Colab 터미널 실행
```bash
unzip lab02_digital_twin.zip
cd lab02_digital_twin
bash run_experiment.sh
cat results/error_report.txt
cat results/best_parameters.yaml
```

## 수정 과제
```bash
nano parameters.yaml
```
- 탐색 범위를 넓히거나 step을 변경한다.
- `real_result.csv`에 추가 노이즈를 넣고 보정 결과를 비교한다.

## 산출물
- `results/best_parameters.yaml`
- `results/calibration_grid.csv`
- `results/comparison.csv`
- `results/error_report.txt`
- `results/comparison.png`
