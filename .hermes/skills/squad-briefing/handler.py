# -*- coding: utf-8 -*-
import sys
import json
from pathlib import Path

root_dir = Path(__file__).resolve().parent.parent.parent.parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

from src.skills.squad_briefing import squad_briefing_gen

def handle(channel_slug, episode_id, custom_params=None):
    if custom_params and isinstance(custom_params, str):
        p = Path(custom_params)
        if p.exists():
            with open(p, 'r', encoding='utf-8') as f:
                custom_params = json.load(f)
        else:
            custom_params = json.loads(custom_params)
    return squad_briefing_gen.generate_briefing(channel_slug, episode_id, custom_params)

if __name__ == "__main__":
    if len(sys.argv) > 2:
        params = sys.argv[3] if len(sys.argv) > 3 else None
        res = handle(sys.argv[1], sys.argv[2], params)
        print(json.dumps(res, indent=2, ensure_ascii=False))
