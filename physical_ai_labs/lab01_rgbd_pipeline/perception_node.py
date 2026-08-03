from __future__ import annotations
import argparse
import json
from pathlib import Path
import numpy as np
from message_bus import FileMessageBus


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument('--results-dir', default='results')
    args = ap.parse_args()
    results = Path(args.results_dir)
    results.mkdir(parents=True, exist_ok=True)

    bus = FileMessageBus('bus')
    msg = bus.read('/camera/rgbd_frame')
    depth = np.loadtxt(msg['depth']['path'], delimiter=',')
    cfg = msg['camera_info']
    valid = (depth >= cfg['valid_min_m']) & (depth <= cfg['valid_max_m'])

    cy, cx = depth.shape[0] // 2, depth.shape[1] // 2
    window = depth[max(0,cy-2):cy+3, max(0,cx-2):cx+3]
    window = window[(window >= cfg['valid_min_m']) & (window <= cfg['valid_max_m'])]
    center_m = float(np.median(window))

    nearest_idx = np.argwhere(np.where(valid, depth, np.inf) == np.where(valid, depth, np.inf).min())[0]
    v, u = map(int, nearest_idx)
    z = float(depth[v, u])
    x = (u - cfg['cx']) * z / cfg['fx']
    y = (v - cfg['cy']) * z / cfg['fy']

    result = {
        'topic': '/perception/nearest_obstacle',
        'frame_id': msg['frame_id'],
        'source_stamp_utc': msg['stamp_utc'],
        'center_distance_m': center_m,
        'nearest_pixel_uv': [u, v],
        'nearest_point_xyz_m': [float(x), float(y), z],
        'valid_depth_ratio': float(valid.mean()),
        'diagnosis': '정상' if valid.mean() > 0.95 else '유효 깊이값 비율 점검 필요'
    }
    bus.publish('/perception/nearest_obstacle', result)
    out = results / 'perception_result.json'
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
    print(f"[perception_node] center={center_m:.3f} m, nearest={z:.3f} m at (u={u}, v={v})")

if __name__ == '__main__':
    main()
