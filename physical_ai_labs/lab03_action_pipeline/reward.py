from __future__ import annotations
import math
import numpy as np
from kinematics import forward_kinematics


def point_segment_distance(p, a, b):
    p=np.asarray(p,float); a=np.asarray(a,float); b=np.asarray(b,float)
    ab=b-a
    denom=float(np.dot(ab,ab))
    if denom == 0:
        return float(np.linalg.norm(p-a))
    u=float(np.clip(np.dot(p-a,ab)/denom,0,1))
    return float(np.linalg.norm(p-(a+u*ab)))


def evaluate(t, q, links, target, obstacle, safety_margin):
    l1,l2=links
    ee=[]; min_clear=float('inf')
    center=np.asarray(obstacle['center'],float); radius=float(obstacle['radius'])
    for a1,a2 in q:
        elbow, end=forward_kinematics(a1,a2,l1,l2)
        ee.append(end)
        d1=point_segment_distance(center,(0,0),elbow)-radius
        d2=point_segment_distance(center,elbow,end)-radius
        min_clear=min(min_clear,d1,d2)
    ee=np.asarray(ee)
    goal_error=float(np.linalg.norm(ee[-1]-np.asarray(target,float)))
    dq=np.gradient(q,t,axis=0)
    ddq=np.gradient(dq,t,axis=0)
    smoothness=float(np.mean(np.linalg.norm(ddq,axis=1)))
    safety_violation=max(0.0,safety_margin-min_clear)
    reward=100.0 - 600*goal_error - 12*smoothness - 800*safety_violation
    return {
        'goal_error_m':goal_error,
        'minimum_clearance_m':min_clear,
        'safety_margin_m':safety_margin,
        'safety_violation_m':safety_violation,
        'smoothness_cost':smoothness,
        'reward':reward,
        'pass': goal_error < 0.015 and safety_violation <= 0
    }, ee
