from __future__ import annotations
from pathlib import Path
import csv
import re
import numpy as np
import matplotlib.pyplot as plt
from twin_model import predict_real_from_sim, rmse


def load(path):
    return np.genfromtxt(path, delimiter=',', names=True)


def read_best(path):
    vals = {}
    for line in Path(path).read_text(encoding='utf-8').splitlines():
        m = re.match(r'\s*([a-zA-Z0-9_]+):\s*([-+0-9.eE]+)', line)
        if m:
            vals[m.group(1)] = float(m.group(2))
    return vals


def main() -> None:
    sim = load('data/simulation_result.csv')
    real = load('data/real_result.csv')
    best = read_best('results/best_parameters.yaml')
    px, py = predict_real_from_sim(sim['time_s'], sim['x_m'], sim['y_m'], best['friction'], best['latency_s'])
    px += best['bias_x_m']
    py += best['bias_y_m']

    baseline = float(np.sqrt((rmse(real['x_m'], sim['x_m'])**2 + rmse(real['y_m'], sim['y_m'])**2)/2))
    calibrated = float(np.sqrt((rmse(real['x_m'], px)**2 + rmse(real['y_m'], py)**2)/2))
    improvement = 100.0 * (baseline - calibrated) / baseline

    with open('results/comparison.csv','w',newline='',encoding='utf-8') as f:
        w = csv.writer(f)
        w.writerow(['time_s','sim_x','sim_y','real_x','real_y','calibrated_x','calibrated_y','position_error_m'])
        for i in range(len(sim)):
            err = float(np.hypot(real['x_m'][i]-px[i], real['y_m'][i]-py[i]))
            w.writerow([sim['time_s'][i], sim['x_m'][i], sim['y_m'][i], real['x_m'][i], real['y_m'][i], px[i], py[i], err])

    report = f"""Digital Twin Calibration Report\n================================\nBaseline combined RMSE : {baseline:.5f} m\nCalibrated combined RMSE: {calibrated:.5f} m\nImprovement             : {improvement:.2f} %\nBest friction           : {best['friction']:.3f}\nBest latency            : {best['latency_s']:.3f} s\nEstimated sensor noise  : {best['residual_noise_std_m']:.5f} m\n\n판정: {'보정 성공' if improvement > 50 else '추가 모델 개선 필요'}\n"""
    Path('results/error_report.txt').write_text(report, encoding='utf-8')

    fig, ax = plt.subplots(figsize=(8,5))
    ax.plot(sim['x_m'], sim['y_m'], '--', label='simulation baseline')
    ax.plot(real['x_m'], real['y_m'], label='real measurement')
    ax.plot(px, py, label='calibrated twin')
    ax.set_aspect('equal', adjustable='box')
    ax.set_xlabel('x [m]'); ax.set_ylabel('y [m]')
    ax.grid(True, alpha=0.3); ax.legend(); fig.tight_layout()
    fig.savefig('results/comparison.png', dpi=160)
    plt.close(fig)
    print(report)

if __name__ == '__main__':
    main()
