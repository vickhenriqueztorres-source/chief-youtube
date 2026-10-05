# -*- coding: utf-8 -*-
import sys
import json
from pathlib import Path

workspace_candidates = [
    Path(__file__).resolve().parent.parent.parent.parent,
    Path("D:/CHIEF YOUTUBE"),
    Path.cwd()
]
for candidate in workspace_candidates:
    if (candidate / "src" / "skills").exists() and str(candidate) not in sys.path:
        sys.path.insert(0, str(candidate))
        break

from src.skills.channel_reverse_engineer import channel_reverse_engineer

def handle(region_focus="BR+GLOBAL", discovery_method="all", custom_channels=None, output_format="json"):
    if custom_channels and isinstance(custom_channels, str):
        p = Path(custom_channels)
        if p.exists():
            with open(p, 'r', encoding='utf-8') as f:
                custom_channels = json.load(f)
        else:
            try:
                custom_channels = json.loads(custom_channels)
            except Exception:
                custom_channels = None

    raw_results = channel_reverse_engineer.reverse_engineer(
        region_focus=region_focus,
        discovery_method=discovery_method,
        custom_channels=custom_channels
    )

    if output_format.lower() in ["html", "--html"]:
        html_path = channel_reverse_engineer.generate_html_report(raw_results)
        return {
            "status": "HTML_GENERATED",
            "html_path": html_path,
            "raw_output": raw_results
        }

    return raw_results

if __name__ == "__main__":
    is_html = any(arg.lower() in ["--html", "html"] for arg in sys.argv)
    
    # Extract --method or -m
    discovery_method = "all"
    for idx, arg in enumerate(sys.argv):
        if arg.lower() in ["--method", "-m"] and idx + 1 < len(sys.argv):
            discovery_method = sys.argv[idx + 1]

    clean_args = [a for a in sys.argv[1:] if a.lower() not in ["--html", "html", "--method", "-m", discovery_method]]

    region = clean_args[0] if len(clean_args) > 0 else "BR+GLOBAL"
    custom_ch = clean_args[1] if len(clean_args) > 1 else None
    fmt = "html" if is_html else "json"

    res = handle(region_focus=region, discovery_method=discovery_method, custom_channels=custom_ch, output_format=fmt)
    if fmt == "html":
        print(f"📊 Relatório HTML gerado com sucesso: {res['html_path']}")
    else:
        print(json.dumps(res, indent=2, ensure_ascii=False))
