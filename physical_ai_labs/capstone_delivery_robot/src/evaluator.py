from __future__ import annotations
import math

def evaluate(goal,final_xy,logs,reached,stopped):
    goal_error=math.dist(goal,final_xy)
    min_distance=min((r[6] for r in logs if r[6] is not None),default=float('nan'))
    elapsed=logs[-1][1] if logs else 0.0
    path_len=0.0
    for a,b in zip(logs,logs[1:]): path_len += math.dist((a[2],a[3]),(b[2],b[3]))
    return {
        'reached':reached,'emergency_stopped':stopped,'goal_error_m':goal_error,
        'minimum_obstacle_distance_m':min_distance,'elapsed_s':elapsed,'path_length_m':path_len,
        'pass': reached and not stopped and goal_error<0.15
    }
