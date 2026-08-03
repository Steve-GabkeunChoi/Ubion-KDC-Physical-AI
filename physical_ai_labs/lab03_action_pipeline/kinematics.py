from __future__ import annotations
import math


def forward_kinematics(theta1, theta2, l1, l2):
    x1 = l1 * math.cos(theta1)
    y1 = l1 * math.sin(theta1)
    x2 = x1 + l2 * math.cos(theta1 + theta2)
    y2 = y1 + l2 * math.sin(theta1 + theta2)
    return (x1, y1), (x2, y2)


def inverse_kinematics(x, y, l1, l2):
    r2 = x*x + y*y
    c2 = (r2 - l1*l1 - l2*l2) / (2*l1*l2)
    if c2 < -1.0 or c2 > 1.0:
        return []
    c2 = max(-1.0, min(1.0, c2))
    s2_abs = math.sqrt(max(0.0, 1.0 - c2*c2))
    sols = []
    for s2 in (s2_abs, -s2_abs):
        t2 = math.atan2(s2, c2)
        t1 = math.atan2(y, x) - math.atan2(l2*s2, l1+l2*c2)
        sols.append((t1,t2))
    return sols


def within_limits(sol, limits_deg):
    deg = [math.degrees(a) for a in sol]
    return all(lo <= a <= hi for a,(lo,hi) in zip(deg, limits_deg))
