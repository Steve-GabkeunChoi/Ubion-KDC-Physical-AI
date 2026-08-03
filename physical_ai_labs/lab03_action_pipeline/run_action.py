from __future__ import annotations
import csv
import json
import math
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from command_parser import load_command
from kinematics import inverse_kinematics, within_limits
from trajectory import generate_joint_trajectory
from reward import evaluate


def choose_solution(solutions, start_rad):
    return min(solutions, key=lambda s: float(np.linalg.norm(np.asarray(s)-np.asarray(start_rad))))


def main():
    cmd=load_command('command.json')
    l1,l2=map(float,cmd['links'])
    start=np.radians(np.asarray(cmd['start_joint_deg'],float))
    sols=[s for s in inverse_kinematics(*cmd['target'],l1,l2) if within_limits(s,cmd['joint_limits_deg'])]
    if not sols:
        raise RuntimeError('도달 가능한 IK 해가 없습니다. target 또는 joint limit을 수정하세요.')
    goal=np.asarray(choose_solution(sols,start),float)
    t,q=generate_joint_trajectory(start,goal,float(cmd['speed']))
    metrics,ee=evaluate(t,q,cmd['links'],cmd['target'],cmd.get('obstacle',{'center':[9,9],'radius':0}),float(cmd['safety_margin']))

    out=Path('results'); out.mkdir(exist_ok=True)
    with (out/'joint_angles.csv').open('w',newline='',encoding='utf-8') as f:
        w=csv.writer(f); w.writerow(['solution','theta1_deg','theta2_deg','selected'])
        for i,s in enumerate(sols):
            w.writerow([i+1,math.degrees(s[0]),math.degrees(s[1]),np.allclose(s,goal)])
    with (out/'trajectory.csv').open('w',newline='',encoding='utf-8') as f:
        w=csv.writer(f); w.writerow(['time_s','theta1_deg','theta2_deg','ee_x_m','ee_y_m'])
        for ti,qi,pi in zip(t,q,ee):
            w.writerow([ti,math.degrees(qi[0]),math.degrees(qi[1]),pi[0],pi[1]])

    report='\n'.join([
        'Action Pipeline Evaluation',
        '==========================',
        f"Target                 : {cmd['target']}",
        f"Selected joint angles  : [{math.degrees(goal[0]):.3f}, {math.degrees(goal[1]):.3f}] deg",
        f"Goal error             : {metrics['goal_error_m']:.6f} m",
        f"Minimum clearance      : {metrics['minimum_clearance_m']:.6f} m",
        f"Safety margin          : {metrics['safety_margin_m']:.6f} m",
        f"Smoothness cost        : {metrics['smoothness_cost']:.6f}",
        f"Reward                 : {metrics['reward']:.3f}",
        f"PASS                    : {metrics['pass']}",
    ])+'\n'
    (out/'reward_result.txt').write_text(report,encoding='utf-8')

    fig,ax=plt.subplots(figsize=(7,6))
    ax.plot(ee[:,0],ee[:,1],label='end-effector path')
    ax.scatter([cmd['target'][0]],[cmd['target'][1]],marker='*',s=180,label='target')
    obs=cmd['obstacle']; circle=plt.Circle(obs['center'],obs['radius'],color='r',alpha=.25,label='obstacle')
    safe=plt.Circle(obs['center'],obs['radius']+cmd['safety_margin'],color='r',fill=False,linestyle='--',label='safety boundary')
    ax.add_patch(circle); ax.add_patch(safe)
    ax.set_aspect('equal',adjustable='box'); ax.grid(True,alpha=.3); ax.legend(); ax.set_xlabel('x [m]'); ax.set_ylabel('y [m]')
    fig.tight_layout(); fig.savefig(out/'arm_motion.png',dpi=160); plt.close(fig)
    print(report)

if __name__=='__main__':
    main()
