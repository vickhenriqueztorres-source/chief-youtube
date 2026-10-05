# -*- coding: utf-8 -*-
import sys
import json
from pathlib import Path

root_dir = Path(__file__).resolve().parent.parent.parent.parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

from src.skills.diagnostic import channel_diagnostic

def handle(channel_slug, metrics_summary):
    if isinstance(metrics_summary, str):
        p = Path(metrics_summary)
        if p.exists():
            with open(p, 'r', encoding='utf-8') as f:
                metrics_summary = json.load(f)
        else:
            metrics_summary = json.loads(metrics_summary)
    return channel_diagnostic.diagnose(channel_slug, metrics_summary)

if __name__ == "__main__":
    if len(sys.argv) > 2:
        res = handle(sys.argv[1], sys.argv[2])
        print(json.dumps(res, indent=2, ensure_ascii=False))
