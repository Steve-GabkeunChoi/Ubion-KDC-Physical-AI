from __future__ import annotations
import json
from pathlib import Path
from typing import Any, Dict

class FileMessageBus:
    """ROS2 topic을 단순 파일 기반 메시지로 모사하는 교육용 버스."""
    def __init__(self, root: str = 'bus') -> None:
        self.root = Path(root)
        self.root.mkdir(parents=True, exist_ok=True)

    def publish(self, topic: str, message: Dict[str, Any]) -> Path:
        safe = topic.strip('/').replace('/', '__') or 'root'
        path = self.root / f'{safe}.json'
        path.write_text(json.dumps(message, ensure_ascii=False, indent=2), encoding='utf-8')
        return path

    def read(self, topic: str) -> Dict[str, Any]:
        safe = topic.strip('/').replace('/', '__') or 'root'
        path = self.root / f'{safe}.json'
        if not path.exists():
            raise FileNotFoundError(f'메시지 없음: {topic} -> {path}')
        return json.loads(path.read_text(encoding='utf-8'))
