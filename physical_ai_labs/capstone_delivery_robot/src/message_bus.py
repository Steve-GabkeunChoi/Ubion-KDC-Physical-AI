from __future__ import annotations
import json
from pathlib import Path

class MessageBus:
    def __init__(self, log_dir='results/bus'):
        self.log_dir=Path(log_dir); self.log_dir.mkdir(parents=True,exist_ok=True)
        self.seq=0
    def publish(self, topic, payload):
        self.seq += 1
        rec={'seq':self.seq,'topic':topic,'payload':payload}
        p=self.log_dir/f'{self.seq:04d}_{topic.strip("/").replace("/","__")}.json'
        p.write_text(json.dumps(rec,ensure_ascii=False,indent=2),encoding='utf-8')
        return rec
