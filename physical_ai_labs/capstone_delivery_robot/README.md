# 캡스톤 — 실내 배송 로봇 Physical AI Mini Stack

## 목표
앞선 실습의 개념을 센서→인지→계획→Twin→제어→평가 구조로 통합한다.

## Colab 터미널 실행
```bash
unzip capstone_delivery_robot.zip
cd capstone_delivery_robot
bash run_capstone.sh
cat results/scenario_summary.csv
cat results/evaluation_report.txt
```

## 수정 과제
```bash
nano config.yaml
nano tests/scenarios.csv
nano src/planner.py
```
- 장애물 위치와 크기를 변경한다.
- 마찰·지연 파라미터를 변경하고 도착시간을 비교한다.
- 새로운 시나리오를 추가하고 pass/fail 기준을 설명한다.

## 산출물
- `results/scenario_summary.csv`
- `results/evaluation_report.txt`
- `results/capstone_paths.png`
- 시나리오별 `integrated_log.csv`, `evaluation.json`, 메시지 로그
