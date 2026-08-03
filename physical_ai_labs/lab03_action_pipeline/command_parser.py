from __future__ import annotations
import json
from pathlib import Path


def load_command(path='command.json'):
    cmd = json.loads(Path(path).read_text(encoding='utf-8'))
    required = ['task','target','speed','safety_margin','links','start_joint_deg','joint_limits_deg']
    missing = [k for k in required if k not in cmd]
    if missing:
        raise ValueError(f'누락 필드: {missing}')
    if cmd['task'] != 'reach':
        raise ValueError('이 실습은 reach task만 지원합니다.')
    if len(cmd['target']) != 2 or len(cmd['links']) != 2:
        raise ValueError('target과 links는 길이 2여야 합니다.')
    if not (0 < cmd['speed'] <= 1.0):
        raise ValueError('speed는 0~1 범위여야 합니다.')
    return cmd
