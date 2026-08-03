from __future__ import annotations
import numpy as np


def smoothstep(s):
    return 3*s**2 - 2*s**3


def generate_joint_trajectory(start, goal, speed, dt=0.05):
    start = np.asarray(start, dtype=float)
    goal = np.asarray(goal, dtype=float)
    max_delta = float(np.max(np.abs(goal-start)))
    duration = max(1.0, max_delta / max(0.1, speed))
    n = int(np.ceil(duration/dt)) + 1
    t = np.linspace(0, duration, n)
    s = smoothstep(t/duration)
    q = start[None,:] + s[:,None]*(goal-start)[None,:]
    return t, q
