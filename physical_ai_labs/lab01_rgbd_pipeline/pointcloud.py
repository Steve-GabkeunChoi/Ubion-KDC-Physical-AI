from __future__ import annotations
import argparse
import csv
import json
from pathlib import Path
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument('--data-dir', default='data')
    ap.add_argument('--results-dir', default='results')
    args = ap.parse_args()
    data = Path(args.data_dir)
    results = Path(args.results_dir)
    results.mkdir(parents=True, exist_ok=True)

    cfg = json.loads((data / 'camera_config.json').read_text(encoding='utf-8'))
    depth = np.loadtxt(data / 'depth.csv', delimiter=',')
    rgb = Image.open(data / 'rgb.png').resize((cfg['width'], cfg['height']))
    rgb_arr = np.asarray(rgb)
    stride = int(cfg.get('point_stride', 2))

    rows = []
    for v in range(0, cfg['height'], stride):
        for u in range(0, cfg['width'], stride):
            z = float(depth[v, u])
            if not (cfg['valid_min_m'] <= z <= cfg['valid_max_m']):
                continue
            x = (u - cfg['cx']) * z / cfg['fx']
            y = (v - cfg['cy']) * z / cfg['fy']
            r, g, b = map(int, rgb_arr[v, u])
            rows.append((x, y, z, r, g, b, u, v))

    out_csv = results / 'point_cloud.csv'
    with out_csv.open('w', newline='', encoding='utf-8') as f:
        w = csv.writer(f)
        w.writerow(['x_m','y_m','z_m','r','g','b','u','v'])
        w.writerows(rows)

    valid = np.where((depth >= cfg['valid_min_m']) & (depth <= cfg['valid_max_m']), depth, np.nan)
    fig, ax = plt.subplots(figsize=(8, 4.8))
    im = ax.imshow(valid, cmap='turbo')
    ax.set_title('Depth Preview (meter)')
    ax.set_xlabel('u pixel')
    ax.set_ylabel('v pixel')
    fig.colorbar(im, ax=ax, label='m')
    fig.tight_layout()
    fig.savefig(results / 'depth_preview.png', dpi=150)
    plt.close(fig)

    print(f'[pointcloud] points={len(rows)}')
    print(f'[pointcloud] result={out_csv}')

if __name__ == '__main__':
    main()
