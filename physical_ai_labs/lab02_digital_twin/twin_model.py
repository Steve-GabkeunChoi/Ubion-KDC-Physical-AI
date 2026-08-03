from __future__ import annotations
import numpy as np


def predict_real_from_sim(t, sim_x, sim_y, friction: float, latency_s: float):
    """단순 교육용 twin: 시간 지연 + 마찰에 따른 이동 스케일을 적용."""
    shifted_t = np.clip(t - latency_s, t[0], t[-1])
    scale = 1.0 - 0.22 * (friction - 0.55)
    x = np.interp(shifted_t, t, sim_x) * scale
    y = np.interp(shifted_t, t, sim_y) * (0.96 * scale)
    return x, y


def rmse(a, b) -> float:
    a = np.asarray(a, dtype=float)
    b = np.asarray(b, dtype=float)
    return float(np.sqrt(np.mean((a - b) ** 2)))
