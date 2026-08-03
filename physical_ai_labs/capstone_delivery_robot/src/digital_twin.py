from __future__ import annotations

def effective_speed(command_speed, friction, latency_s, extra_latency_s):
    friction_scale=max(0.5,1.0-0.22*(friction-0.55))
    latency_scale=max(0.55,1.0-0.15*(latency_s+extra_latency_s))
    return command_speed*friction_scale*latency_scale
