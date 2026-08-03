from __future__ import annotations
import csv
from pathlib import Path
import numpy as np
from twin_model import predict_real_from_sim, rmse


def load_csv(path: str):
    arr = np.genfromtxt(path, delimiter=',', names=True)
    return arr


def parse_simple_yaml(path: str):
    values = {}
    section = None
    for raw in Path(path).read_text(encoding='utf-8').splitlines():
        line = raw.strip()
        if not line or line.startswith('#'):
            continue
        if line.endswith(':'):
            section = line[:-1]
            continue
        key, val = [x.strip() for x in line.split(':', 1)]
        values[f'{section}.{key}'] = float(val)
    return values


def main() -> None:
    sim = load_csv('data/simulation_result.csv')
    real = load_csv('data/real_result.csv')
    p = parse_simple_yaml('parameters.yaml')

    frictions = np.arange(p['search.friction_min'], p['search.friction_max'] + 1e-9, p['search.friction_step'])
    latencies = np.arange(p['search.latency_min_s'], p['search.latency_max_s'] + 1e-9, p['search.latency_step_s'])

    best = None
    rows = []
    for friction in frictions:
        for latency in latencies:
            px, py = predict_real_from_sim(sim['time_s'], sim['x_m'], sim['y_m'], friction, latency)
            # constant sensor bias is estimated from residual mean
            bx = float(np.mean(real['x_m'] - px))
            by = float(np.mean(real['y_m'] - py))
            px2, py2 = px + bx, py + by
            ex = rmse(real['x_m'], px2)
            ey = rmse(real['y_m'], py2)
            score = float(np.sqrt((ex**2 + ey**2)/2))
            noise = float(np.std(np.hypot(real['x_m']-px2, real['y_m']-py2)))
            row = (float(friction), float(latency), bx, by, ex, ey, score, noise)
            rows.append(row)
            if best is None or score < best[-2]:
                best = row

    Path('results').mkdir(exist_ok=True)
    with open('results/calibration_grid.csv','w',newline='',encoding='utf-8') as f:
        w = csv.writer(f)
        w.writerow(['friction','latency_s','bias_x_m','bias_y_m','rmse_x_m','rmse_y_m','score_m','residual_noise_std_m'])
        w.writerows(rows)

    friction, latency, bx, by, ex, ey, score, noise = best
    text = f"""best_parameters:\n  friction: {friction:.3f}\n  latency_s: {latency:.3f}\n  bias_x_m: {bx:.5f}\n  bias_y_m: {by:.5f}\n  residual_noise_std_m: {noise:.5f}\nmetrics:\n  rmse_x_m: {ex:.5f}\n  rmse_y_m: {ey:.5f}\n  combined_score_m: {score:.5f}\n"""
    Path('results/best_parameters.yaml').write_text(text, encoding='utf-8')
    print(text)

if __name__ == '__main__':
    main()
