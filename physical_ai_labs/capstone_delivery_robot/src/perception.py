from __future__ import annotations

def classify_obstacle(observation, emergency_stop_distance, safety_margin):
    if not observation['valid']:
        return {'status':'SENSOR_FAULT','stop':True,'caution':True}
    d=observation['distance_m']
    return {
        'status':'EMERGENCY' if d < emergency_stop_distance else ('CAUTION' if d < safety_margin else 'CLEAR'),
        'stop': d < emergency_stop_distance,
        'caution': d < safety_margin
    }
