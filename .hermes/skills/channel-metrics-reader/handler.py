# -*- coding: utf-8 -*-
import sys
import json
from pathlib import Path

# Add src to sys.path
root_dir = Path(__file__).resolve().parent.parent.parent.parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

from src.skills.metrics_reader import metrics_reader

def handle(input_data):
    if isinstance(input_data, str):
        path = Path(input_data)
        if path.exists():
            input_data = metrics_reader.load_from_json(path)
        else:
            input_data = json.loads(input_data)
    return metrics_reader.analyze_channel(input_data)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        result = handle(sys.argv[1])
        print(json.dumps(result, indent=2, ensure_ascii=False))
