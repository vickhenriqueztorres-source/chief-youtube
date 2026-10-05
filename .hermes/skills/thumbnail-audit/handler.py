# -*- coding: utf-8 -*-
import sys
import json
from pathlib import Path

root_dir = Path(__file__).resolve().parent.parent.parent.parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

from src.skills.thumb_audit import thumbnail_auditor

def handle(channel_slug, title, thumb_desc, thumb_text=""):
    return thumbnail_auditor.audit(channel_slug, title, thumb_desc, thumb_text)

if __name__ == "__main__":
    if len(sys.argv) > 3:
        txt = sys.argv[4] if len(sys.argv) > 4 else ""
        res = handle(sys.argv[1], sys.argv[2], sys.argv[3], txt)
        print(json.dumps(res, indent=2, ensure_ascii=False))
