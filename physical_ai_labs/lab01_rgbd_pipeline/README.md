# 실습 1 — 센서 데이터에서 3D 인지까지

## 목표
- RGB·Depth 데이터를 파일 기반 센서 메시지로 구성한다.
- `Node → Message → Node` 구조를 ROS 2 없이 모사한다.
- Depth 픽셀을 카메라 좌표계의 3D 점으로 변환한다.

## Colab 터미널 실행
```bash
unzip lab01_rgbd_pipeline.zip
cd lab01_rgbd_pipeline
bash run_pipeline.sh
cat results/sensor_message.json
cat results/perception_result.json
head results/point_cloud.csv
```

## 수정 과제
```bash
nano data/camera_config.json
nano perception_node.py
```
- `point_stride`를 1, 2, 4로 변경하고 포인트 수를 비교한다.
- 유효 깊이 범위를 변경하고 `valid_depth_ratio` 변화를 확인한다.

## 주요 산출물
- `results/sensor_message.json`
- `results/perception_result.json`
- `results/point_cloud.csv`
- `results/depth_preview.png`
