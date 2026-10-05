# -*- coding: utf-8 -*-
import sys
import json
from pathlib import Path

root_dir = Path(__file__).resolve().parent.parent.parent.parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

from src.skills.theme_decider import theme_decider

def handle(channel_slug, custom_ideas=None):
    if custom_ideas and isinstance(custom_ideas, str):
        p = Path(custom_ideas)
        if p.exists():
            with open(p, 'r', encoding='utf-8') as f:
                custom_ideas = json.load(f)
        else:
            custom_ideas = json.loads(custom_ideas)
    return theme_decider.evaluate_themes(channel_slug, custom_ideas)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        ideas = sys.argv[2] if len(sys.argv) > 2 else None
        res = handle(sys.argv[1], ideas)
        print(json.dumps(res, indent=2, ensure_ascii=False))
