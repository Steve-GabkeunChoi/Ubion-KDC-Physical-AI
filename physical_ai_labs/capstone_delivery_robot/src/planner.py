from __future__ import annotations
import math
import numpy as np

def segment_distance_to_point(a,b,p):
    a=np.asarray(a,float); b=np.asarray(b,float); p=np.asarray(p,float)
    ab=b-a; den=float(np.dot(ab,ab))
    if den==0: return float(np.linalg.norm(p-a))
    u=float(np.clip(np.dot(p-a,ab)/den,0,1))
    return float(np.linalg.norm(p-(a+u*ab)))

def plan(start,goal,obstacle,radius,margin):
    safe_r=radius+margin
    if segment_distance_to_point(start,goal,obstacle) > safe_r:
        return [tuple(start),tuple(goal)], 'DIRECT'
    # choose detour waypoint perpendicular to path on safer side
    sx,sy=start; gx,gy=goal; ox,oy=obstacle
    dx,dy=gx-sx,gy-sy; norm=max(1e-9,math.hypot(dx,dy))
    nx,ny=-dy/norm,dx/norm
    w1=(ox+nx*(safe_r+0.35),oy+ny*(safe_r+0.35))
    w2=(ox-nx*(safe_r+0.35),oy-ny*(safe_r+0.35))
    def length(w): return math.dist(start,w)+math.dist(w,goal)
    wp=w1 if length(w1)<=length(w2) else w2
    return [tuple(start),wp,tuple(goal)], 'DETOUR'
