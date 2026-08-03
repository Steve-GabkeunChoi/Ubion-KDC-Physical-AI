from __future__ import annotations
import math

def observe(robot_xy, obstacle_xy, obstacle_radius, dropout=False):
    if dropout:
        return {'valid':False,'distance_m':None,'bearing_rad':None}
    dx=obstacle_xy[0]-robot_xy[0]; dy=obstacle_xy[1]-robot_xy[1]
    d=max(0.0,math.hypot(dx,dy)-obstacle_radius)
    return {'valid':True,'distance_m':d,'bearing_rad':math.atan2(dy,dx)}
