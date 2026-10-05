# -*- coding: utf-8 -*-
"""
Hermes Chief Trading Skill: trading-metrics-reader
Extracts, aggregates, and computes statistical diagnostics (means, medians, Z-scores, ratios)
for YouTube Trading Channels.
"""

import json
import math
from pathlib import Path
from typing import Dict, Any, List, Optional

class TradingMetricsReader:
    """Reads and calculates statistical baselines for trading channels."""

    def load_from_json(self, file_path: Path) -> Dict[str, Any]:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def analyze_channel(self, raw_data: Dict[str, Any]) -> Dict[str, Any]:
        videos = raw_data.get("videos", [])
        subs = raw_data.get("subscribers", 0)

        long_vids = [v for v in videos if v.get("format") == "long"]
        short_vids = [v for v in videos if v.get("format") == "short"]

        def calc_stats(v_list: List[Dict[str, Any]]) -> Dict[str, Any]:
            if not v_list:
                return {
                    "count": 0, "mean_views": 0.0, "median_views": 0.0, "std_views": 0.0,
                    "mean_ctr": 0.0, "mean_avd_pct": 0.0, "mean_retention_30s": 0.0,
                    "trend": "ESTAGNADO", "rolling_avg_3_latest": 0.0, "outliers": []
                }

            views = [v.get("views", 0) for v in v_list]
            ctrs = [v.get("ctr", 0.0) for v in v_list if v.get("ctr") is not None]
            avds = [v.get("avd_pct", 0.0) for v in v_list if v.get("avd_pct") is not None]
            ret30s = [v.get("retention_30s", 0.0) for v in v_list if v.get("retention_30s") is not None]

            n = len(views)
            mean_v = sum(views) / n
            sorted_v = sorted(views)
            median_v = sorted_v[n // 2] if n % 2 != 0 else (sorted_v[n // 2 - 1] + sorted_v[n // 2]) / 2.0

            var = sum((x - mean_v) ** 2 for x in views) / n if n > 1 else 0.0
            std_v = math.sqrt(var)

            # Z-Score Outlier Detection (Z >= 1.5)
            outliers = []
            for v in v_list:
                v_views = v.get("views", 0)
                z = (v_views - mean_v) / std_v if std_v > 0 else 0.0
                if z >= 1.2 or (subs > 0 and v_views / max(1, subs) >= 5.0):
                    outliers.append({
                        "id": v.get("id", v.get("youtube_id", "")),
                        "title": v.get("title", ""),
                        "views": v_views,
                        "z_score": round(z, 2),
                        "multiplier_vs_subs": round(v_views / max(1, subs), 1) if subs > 0 else 0.0
                    })

            # Trend & Rolling Avg (latest 3)
            latest_3 = views[:3]
            rolling_3 = sum(latest_3) / len(latest_3) if latest_3 else 0.0
            trend = "NEUTRO"
            if len(views) >= 3:
                if rolling_3 > mean_v * 1.15:
                    trend = "CRESCIMENTO"
                elif rolling_3 < mean_v * 0.85:
                    trend = "QUEDA"

            return {
                "count": n,
                "mean_views": round(mean_v, 1),
                "median_views": round(median_v, 1),
                "std_views": round(std_v, 1),
                "mean_ctr": round(sum(ctrs) / len(ctrs), 2) if ctrs else 0.0,
                "mean_avd_pct": round(sum(avds) / len(avds), 1) if avds else 0.0,
                "mean_retention_30s": round(sum(ret30s) / len(ret30s), 1) if ret30s else 0.0,
                "trend": trend,
                "rolling_avg_3_latest": round(rolling_3, 1),
                "outliers": outliers
            }

        long_stats = calc_stats(long_vids)
        short_stats = calc_stats(short_vids)
        ratio = f"{short_stats['count']}:{long_stats['count']}" if long_stats['count'] > 0 else f"{short_stats['count']}:0"

        return {
            "channel_slug": raw_data.get("channel_slug", "el_profe_de_velas"),
            "channel_name": raw_data.get("channel_name", "El Profe de Velas"),
            "handle": raw_data.get("handle", "@ElProfdelLasVelas"),
            "subscribers": subs,
            "total_videos_analyzed": len(videos),
            "shorts_to_long_ratio": ratio,
            "long_form_summary": long_stats,
            "shorts_summary": short_stats,
            "traffic_sources": raw_data.get("dominant_traffic_sources", [])
        }

trading_metrics_reader = TradingMetricsReader()
