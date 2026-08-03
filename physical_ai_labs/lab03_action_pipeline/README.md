# 실습 3 — 명령에서 로봇 행동까지

## 목표
- 구조화된 명령 JSON을 읽는다.
- 2링크 로봇 팔의 역기구학 해를 구한다.
- 관절 궤적을 생성하고 목표 오차·안전거리·보상을 평가한다.

## Colab 터미널 실행
```bash
unzip lab03_action_pipeline.zip
cd lab03_action_pipeline
cat command.json
bash run_action.sh
cat results/reward_result.txt
head results/trajectory.csv
```

## 수정 과제
```bash
nano command.json
```
- `target`, `speed`, `safety_margin`을 바꾸고 결과를 비교한다.
- 도달 불가능한 target을 넣어 오류 처리를 확인한다.

## 산출물
- `results/joint_angles.csv`
- `results/trajectory.csv`
- `results/reward_result.txt`
- `results/arm_motion.png`
