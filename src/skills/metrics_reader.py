# -*- coding: utf-8 -*-
"""
Hermes Chief Skill: channel-metrics-reader
Reads YouTube Studio metrics (CSV, JSON, or direct summaries).
Computes moving averages, identifies 2-sigma outliers, and detects trajectory trends.
"""

import json
import csv
import math
from pathlib import Path
from typing import Dict, List, Any, Optional, Union

class ChannelMetricsReader:
    """Ingests and calculates quantitative indicators from YouTube Studio metrics."""

    def __init__(self, baseline_dir: Optional[Path] = None):
        self.baseline_dir = baseline_dir or (Path(__file__).resolve().parent.parent.parent / "data" / "channels")

    def load_from_json(self, json_path: Union[str, Path]) -> Dict[str, Any]:
        with open(json_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def load_from_csv(self, csv_path: Union[str, Path]) -> List[Dict[str, Any]]:
        rows = []
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for r in reader:
                rows.append(dict(r))
        return rows

    def analyze_channel(self, raw_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Processes videos array from a channel data packet.
        Computes rolling averages, outliers, and macro performance indicators.
        """
        videos = raw_data.get("videos", [])
        if not videos:
            return {
                "channel_id": raw_data.get("channel_id", "unknown"),
                "channel_name": raw_data.get("channel_name", "unknown"),
                "total_videos": 0,
                "error": "No videos found in dataset"
            }

        # Segregate long-form and shorts
        long_videos = [v for v in videos if v.get("format", "long") == "long"]
        shorts = [v for v in videos if v.get("format", "long") == "short"]

        def calc_stats(v_list: List[Dict[str, Any]], format_name: str) -> Dict[str, Any]:
            if not v_list:
                return {"count": 0, "avg_views": 0, "avg_ctr": 0.0, "avg_retention_30s": 0.0}

            views_list = [float(v.get("views", 0)) for v in v_list]
            ctr_list = [float(v.get("ctr", 0.0)) for v in v_list]
            ret30_list = [float(v.get("retention_30s", 0.0)) for v in v_list]
            avd_list = [float(v.get("avd_pct", 0.0)) for v in v_list]

            n = len(views_list)
            mean_views = sum(views_list) / n
            mean_ctr = sum(ctr_list) / n if n else 0.0
            mean_ret30 = sum(ret30_list) / n if n else 0.0
            mean_avd = sum(avd_list) / n if n else 0.0

            # Standard deviation for views
            variance = sum((x - mean_views) ** 2 for x in views_list) / n if n > 1 else 0
            std_dev_views = math.sqrt(variance)

            # Detect outliers (> 2 sigma)
            outliers = []
            for v in v_list:
                val = float(v.get("views", 0))
                if std_dev_views > 0 and (val - mean_views) > 1.8 * std_dev_views:
                    outliers.append({
                        "id": v.get("id"),
                        "title": v.get("title"),
                        "views": val,
                        "sigma": round((val - mean_views) / std_dev_views, 2),
                        "type": "HIGH_OUTLIER"
                    })
                elif val == 0:
                    outliers.append({
                        "id": v.get("id"),
                        "title": v.get("title"),
                        "views": 0,
                        "type": "ZERO_VIEW_STALL"
                    })

            # Rolling averages (3-video and 7-video)
            rolling_3 = []
            for i in range(len(v_list)):
                window = v_list[max(0, i - 2):i + 1]
                avg_3 = sum(float(x.get("views", 0)) for x in window) / len(window)
                rolling_3.append(round(avg_3, 1))

            rolling_7 = []
            for i in range(len(v_list)):
                window = v_list[max(0, i - 6):i + 1]
                avg_7 = sum(float(x.get("views", 0)) for x in window) / len(window)
                rolling_7.append(round(avg_7, 1))

            # Macro Trend
            if len(rolling_3) >= 3:
                recent_avg = rolling_3[-1]
                prev_avg = rolling_3[0]
                if recent_avg > prev_avg * 1.3:
                    trend = "ACCELERATING"
                elif recent_avg < prev_avg * 0.7:
                    trend = "DECELERATING"
                else:
                    trend = "STABLE"
            else:
                trend = "INSUFFICIENT_DATA"

            return {
                "count": n,
                "mean_views": round(mean_views, 1),
                "std_dev_views": round(std_dev_views, 1),
                "mean_ctr": round(mean_ctr, 2),
                "mean_retention_30s": round(mean_ret30, 2),
                "mean_avd_pct": round(mean_avd, 2),
                "trend": trend,
                "outliers": outliers,
                "rolling_avg_3_latest": rolling_3[-1] if rolling_3 else 0,
                "rolling_avg_7_latest": rolling_7[-1] if rolling_7 else 0
            }

        long_stats = calc_stats(long_videos, "long")
        short_stats = calc_stats(shorts, "short")

        # Global conversion metric: Shorts views to Long views ratio
        total_short_views = sum(float(v.get("views", 0)) for v in shorts)
        total_long_views = sum(float(v.get("views", 0)) for v in long_videos)
        ratio = round(total_long_views / total_short_views, 3) if total_short_views > 0 else 0.0

        return {
            "channel_id": raw_data.get("channel_id"),
            "channel_name": raw_data.get("channel_name"),
            "subscribers": raw_data.get("subscribers", 0),
            "total_videos_analyzed": len(videos),
            "long_form_summary": long_stats,
            "shorts_summary": short_stats,
            "shorts_to_long_ratio": ratio,
            "traffic_sources_dominant": raw_data.get("dominant_traffic_sources", ["Browse Features", "YouTube Search", "Shorts Feed"])
        }

metrics_reader = ChannelMetricsReader()
