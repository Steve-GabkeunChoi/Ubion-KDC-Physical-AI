from __future__ import annotations
import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
import numpy as np
from PIL import Image
from message_bus import FileMessageBus


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument('--data-dir', default='data')
    ap.add_argument('--results-dir', default='results')
    args = ap.parse_args()

    data = Path(args.data_dir)
    results = Path(args.results_dir)
    results.mkdir(parents=True, exist_ok=True)

    config = json.loads((data / 'camera_config.json').read_text(encoding='utf-8'))
    depth = np.loadtxt(data / 'depth.csv', delimiter=',')
    rgb = Image.open(data / 'rgb.png')
    if depth.shape != (config['height'], config['width']):
        raise ValueError(f"depth shape {depth.shape} != config {(config['height'], config['width'])}")

    valid = (depth >= config['valid_min_m']) & (depth <= config['valid_max_m'])
    message = {
        'topic': '/camera/rgbd_frame',
        'frame_id': 'camera_link',
        'stamp_utc': datetime.now(timezone.utc).isoformat(),
        'rgb': {'path': str(data / 'rgb.png'), 'width': rgb.width, 'height': rgb.height},
        'depth': {
            'path': str(data / 'depth.csv'),
            'width': int(depth.shape[1]),
            'height': int(depth.shape[0]),
            'unit': config['depth_unit'],
            'valid_ratio': float(valid.mean()),
            'min_m': float(depth[valid].min()),
            'max_m': float(depth[valid].max())
        },
        'camera_info': config
    }
    bus = FileMessageBus('bus')
    bus_path = bus.publish('/camera/rgbd_frame', message)
    out = results / 'sensor_message.json'
    out.write_text(json.dumps(message, ensure_ascii=False, indent=2), encoding='utf-8')
    print(f'[sensor_node] publish: {bus_path}')
    print(f'[sensor_node] result : {out}')

if __name__ == '__main__':
    main()
