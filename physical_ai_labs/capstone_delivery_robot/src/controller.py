from __future__ import annotations
import math

def follow_path(path,max_speed,dt,effective_speed,perception_fn,max_steps=3000):
    x,y=path[0]; logs=[]; wp_idx=1; stopped=False
    for step in range(max_steps):
        if wp_idx>=len(path): break
        obs,per=perception_fn((x,y))
        if per['stop']:
            stopped=True
            logs.append((step,step*dt,x,y,0.0,wp_idx,obs['distance_m'],per['status']))
            break
        tx,ty=path[wp_idx]; dx,dy=tx-x,ty-y; dist=math.hypot(dx,dy)
        if dist<0.10:
            wp_idx+=1; continue
        speed=min(max_speed,effective_speed,dist/dt)
        x += speed*dt*dx/dist; y += speed*dt*dy/dist
        logs.append((step,step*dt,x,y,speed,wp_idx,obs['distance_m'],per['status']))
    reached=wp_idx>=len(path)
    return logs, reached, stopped, (x,y)
