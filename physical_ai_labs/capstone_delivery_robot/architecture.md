# 실내 배송 로봇 Physical AI Mini Stack

```text
Scenario / Sensor
      ↓
File Message Bus
      ↓
Perception & Safety Classification
      ↓
Planner (Direct / Detour)
      ↓
Digital Twin Speed Model
      ↓
Waypoint Controller
      ↓
Integrated Log & Evaluator
```

## 모듈별 입출력
| 모듈 | 입력 | 출력 |
|---|---|---|
| sensor | robot pose, obstacle | distance, bearing, valid |
| perception | observation | CLEAR / CAUTION / EMERGENCY / SENSOR_FAULT |
| planner | start, goal, obstacle | waypoint path |
| digital_twin | command speed, friction, latency | effective speed |
| controller | path, speed, safety callback | executed trajectory |
| evaluator | goal, logs | pass/fail and metrics |
