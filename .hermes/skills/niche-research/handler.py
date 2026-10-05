# -*- coding: utf-8 -*-
import sys
import json
from pathlib import Path

root_dir = Path(__file__).resolve().parent.parent.parent.parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

from src.skills.niche_researcher import niche_researcher

def handle(region="BR+US", territory_filter=None, custom_seeds=None, output_format="json"):
    if custom_seeds and isinstance(custom_seeds, str):
        p = Path(custom_seeds)
        if p.exists():
            with open(p, 'r', encoding='utf-8') as f:
                custom_seeds = json.load(f)
        else:
            try:
                custom_seeds = json.loads(custom_seeds)
            except Exception:
                custom_seeds = None

    raw_results = niche_researcher.research_niches(
        region=region,
        territory_filter=territory_filter,
        custom_seeds=custom_seeds
    )

    if output_format.lower() in ["html", "--html"]:
        html_path = niche_researcher.generate_html_report(raw_results)
        return {
            "status": "HTML_GENERATED",
            "html_path": html_path,
            "raw_output": raw_results
        }

    return raw_results

if __name__ == "__main__":
    is_html = any(arg.lower() in ["--html", "html"] for arg in sys.argv)
    clean_args = [a for a in sys.argv[1:] if a.lower() not in ["--html", "html"]]

    region = clean_args[0] if len(clean_args) > 0 else "BR+US"
    territory = clean_args[1] if len(clean_args) > 1 else None
    seeds = clean_args[2] if len(clean_args) > 2 else None
    fmt = "html" if is_html else "json"

    res = handle(region, territory, seeds, output_format=fmt)
    if fmt == "html":
        print(f"📊 Relatório HTML gerado com sucesso: {res['html_path']}")
    else:
        print(json.dumps(res, indent=2, ensure_ascii=False))
