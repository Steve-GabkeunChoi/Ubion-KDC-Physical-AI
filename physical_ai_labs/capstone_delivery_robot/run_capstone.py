from __future__ import annotations
import csv
import json
import re
import sys
from pathlib import Path
import matplotlib.pyplot as plt
sys.path.insert(0,'src')
from message_bus import MessageBus
from sensor import observe
from perception import classify_obstacle
from digital_twin import effective_speed
from planner import plan
from controller import follow_path
from evaluator import evaluate


def parse_yaml(path):
    vals={}; section=None
    for raw in Path(path).read_text(encoding='utf-8').splitlines():
        line=raw.strip()
        if not line: continue
        if line.endswith(':'): section=line[:-1]; continue
        k,v=[x.strip() for x in line.split(':',1)]
        vals[f'{section}.{k}']=float(v)
    return vals

def load_scenarios(path):
    with open(path,newline='',encoding='utf-8') as f:
        return list(csv.DictReader(f))

def run_one(sc,cfg,out_dir):
    name=sc['scenario']; start=(float(sc['start_x']),float(sc['start_y'])); goal=(float(sc['goal_x']),float(sc['goal_y']))
    obstacle=(float(sc['obstacle_x']),float(sc['obstacle_y'])); radius=float(sc['obstacle_radius'])
    dropout=sc['sensor_dropout']=='1'; extra_latency=float(sc['extra_latency_s'])
    bus=MessageBus(out_dir/'bus')
    path,mode=plan(start,goal,obstacle,radius,cfg['safety.obstacle_margin_m'])
    bus.publish('/planner/path',{'scenario':name,'mode':mode,'path':path})
    eff=effective_speed(cfg['robot.max_speed_mps'],cfg['digital_twin.friction'],cfg['digital_twin.latency_s'],extra_latency)
    def perception_fn(xy):
        obs=observe(xy,obstacle,radius,dropout)
        per=classify_obstacle(obs,cfg['safety.emergency_stop_distance_m'],cfg['safety.obstacle_margin_m'])
        return obs,per
    logs,reached,stopped,final_xy=follow_path(path,cfg['robot.max_speed_mps'],cfg['robot.control_dt_s'],eff,perception_fn)
    metrics=evaluate(goal,final_xy,logs,reached,stopped)
    bus.publish('/evaluation/metrics',metrics)
    return path,logs,metrics,obstacle,radius,goal

def main():
    cfg=parse_yaml('config.yaml'); root=Path('results'); root.mkdir(exist_ok=True)
    summary=[]
    fig,axes=plt.subplots(2,2,figsize=(10,8)); axes=axes.ravel()
    for ax,sc in zip(axes,load_scenarios('tests/scenarios.csv')):
        out=root/sc['scenario']; out.mkdir(parents=True,exist_ok=True)
        path,logs,m,obs,radius,goal=run_one(sc,cfg,out)
        with (out/'integrated_log.csv').open('w',newline='',encoding='utf-8') as f:
            w=csv.writer(f); w.writerow(['step','time_s','x_m','y_m','speed_mps','waypoint_index','obstacle_distance_m','status']); w.writerows(logs)
        (out/'evaluation.json').write_text(json.dumps(m,ensure_ascii=False,indent=2),encoding='utf-8')
        summary.append([sc['scenario'],m['reached'],m['emergency_stopped'],m['goal_error_m'],m['minimum_obstacle_distance_m'],m['elapsed_s'],m['path_length_m'],m['pass']])
        px=[p[0] for p in path]; py=[p[1] for p in path]; ax.plot(px,py,'--',label='planned')
        if logs: ax.plot([r[2] for r in logs],[r[3] for r in logs],label='executed')
        ax.scatter([goal[0]],[goal[1]],marker='*',s=100,label='goal'); ax.add_patch(plt.Circle(obs,radius,color='r',alpha=.25))
        ax.set_title(sc['scenario']); ax.set_aspect('equal',adjustable='box'); ax.grid(True,alpha=.3)
    fig.tight_layout(); fig.savefig(root/'capstone_paths.png',dpi=160); plt.close(fig)
    with (root/'scenario_summary.csv').open('w',newline='',encoding='utf-8') as f:
        w=csv.writer(f); w.writerow(['scenario','reached','emergency_stopped','goal_error_m','minimum_obstacle_distance_m','elapsed_s','path_length_m','pass']); w.writerows(summary)
    passed=sum(bool(r[-1]) for r in summary)
    report=f"""Physical AI Capstone Evaluation\n===============================\nScenarios: {len(summary)}\nPassed   : {passed}\nFailed   : {len(summary)-passed}\n\n평가 기준\n- 정상 시나리오에서 목표 도달\n- 센서 결함 시 안전 정지\n- 장애물 회피 경로 생성\n- 지연 증가에 따른 성능 저하 관찰\n"""
    (root/'evaluation_report.txt').write_text(report,encoding='utf-8')
    print(report)

if __name__=='__main__': main()
