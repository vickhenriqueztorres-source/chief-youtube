# -*- coding: utf-8 -*-
"""
Hermes Chief Trading - Central Agent Brain
Orchestrates trading skills, isolated SQLite FTS5 memory (chief_trading_memory.db),
personality frameworks, and strategic decision loops for YouTube Trading Channels.
"""

import json
import subprocess
from pathlib import Path
from typing import Dict, Any, List, Optional

from src.core.trading_memory import ChiefTradingMemory, trading_memory
from src.core.trading_personality import CHIEF_TRADING_SYSTEM_PROMPT, TRADING_CHANNEL_CONFIGS
from src.skills.trading_metrics_reader import TradingMetricsReader, trading_metrics_reader
from src.skills.trading_diagnostic import TradingDiagnostic, trading_diagnostic
from src.skills.trading_thumb_audit import TradingThumbnailAuditor, trading_thumbnail_auditor
from src.skills.trading_theme_decider import TradingThemeDecider, trading_theme_decider
from src.skills.trading_squad_briefing import TradingSquadBriefingGenerator, trading_squad_briefing_gen
from src.skills.trading_discovery_engine import TradingDiscoveryEngine, trading_discovery_engine

class ChiefTradingAgent:
    """The Autonomous Chief Analyst Agent for YouTube Trading & Candlestick Channels."""

    def __init__(self, memory_instance: Optional[ChiefTradingMemory] = None):
        self.memory = memory_instance or trading_memory
        self.metrics_reader = trading_metrics_reader
        self.diagnostic = trading_diagnostic
        self.auditor = trading_thumbnail_auditor
        self.theme_decider = trading_theme_decider
        self.briefing_gen = trading_squad_briefing_gen
        self.discovery = trading_discovery_engine
        self.configs = TRADING_CHANNEL_CONFIGS
        self.base_data_dir = Path(__file__).resolve().parent.parent.parent / "data" / "trading_channels"
        self.base_data_dir.mkdir(parents=True, exist_ok=True)

    def get_channel_data(self, channel_slug: str) -> Dict[str, Any]:
        slug = channel_slug.lower()
        if "profe" in slug or "vela" in slug:
            p = self.base_data_dir / "el_profe_de_velas_baseline.json"
        elif any(k in slug for k in ["cazador", "caza", "wins"]):
            p = self.base_data_dir / "el_cazador_del_wins_baseline.json"
        elif any(k in slug for k in ["miguel", "restrepo", "quant", "million"]):
            p = self.base_data_dir / "miguel_trader_baseline.json"
        elif "canal_02" in slug:
            p = self.base_data_dir / "el_cazador_del_wins_baseline.json"
        else:
            p = self.base_data_dir / f"{slug}_baseline.json"

        if p.exists():
            return self.metrics_reader.load_from_json(p)
        raise FileNotFoundError(f"Dados do canal de trading '{channel_slug}' não encontrados em {p}")

    def audit_channel(self, channel_slug: str) -> Dict[str, Any]:
        """Runs end-to-end quant audit: metrics -> diagnosis -> top themes -> persistent memory update."""
        raw_data = self.get_channel_data(channel_slug)
        metrics_summary = self.metrics_reader.analyze_channel(raw_data)
        diag_result = self.diagnostic.diagnose(channel_slug, metrics_summary)
        themes_result = self.theme_decider.evaluate_themes(channel_slug)

        # Record insight in isolated trading FTS5 memory automatically
        bottleneck_name = diag_result["primary_bottleneck"]["name"]
        self.memory.record_learning(
            channel=channel_slug,
            category="diagnostic",
            insight=f"Gargalo primário detectado: {bottleneck_name}",
            evidence=f"Inscritos: {metrics_summary.get('subscribers')} | Longos: {metrics_summary.get('long_form_summary', {}).get('mean_views')} views | Shorts: {metrics_summary.get('shorts_summary', {}).get('mean_views')} views",
            action_taken=diag_result["proposed_experiment"]["hypothesis"][:140] + "..."
        )

        return {
            "channel_slug": channel_slug,
            "metrics": metrics_summary,
            "diagnosis": diag_result,
            "top_themes": themes_result["top_themes"][:3],
            "duplicates_blocked": themes_result["duplicates_blocked"],
            "total_virgin_themes_available": themes_result["approved_virgin_themes"]
        }

    def audit_thumbnail(self, channel_slug: str, title: str, thumb_desc: str, thumb_text: str = "") -> Dict[str, Any]:
        """Audits packaging (title + thumbnail) for trading channels."""
        return self.auditor.audit(channel_slug, title, thumb_desc, thumb_text)

    def evaluate_themes(self, channel_slug: str) -> Dict[str, Any]:
        """Scores and filters themes using P-Score and Anti-Duplication Guardian."""
        return self.theme_decider.evaluate_themes(channel_slug)

    def generate_briefing(self, channel_slug: str, episode_id: str, topic_override: str = "") -> Dict[str, Any]:
        """Emits typed production briefing for editing squad."""
        return self.briefing_gen.generate_briefing(channel_slug, episode_id, topic_override)

    def plan_discovery_ecosystem(self, channel_slug: str, topic: str) -> Dict[str, Any]:
        """Projects 7-piece multi-front discovery ecosystem."""
        return self.discovery.plan_ecosystem(channel_slug, topic)

    def live_sync(self, channel_slug: str) -> Dict[str, Any]:
        """Scrapes YouTube in real-time via yt-dlp to update metrics and video history."""
        config = self.configs.get(channel_slug.lower(), self.configs.get("el_profe_de_velas", {}))
        channel_url = config.get("url", "https://www.youtube.com/@ElProfdelLasVelas")

        try:
            # Query Long videos
            cmd_longs = ["yt-dlp", "--flat-playlist", "--dump-single-json", f"{channel_url}/videos"]
            res_longs = subprocess.run(cmd_longs, capture_output=True, text=True, check=True)
            data_longs = json.loads(res_longs.stdout)

            # Query Shorts
            cmd_shorts = ["yt-dlp", "--flat-playlist", "--dump-single-json", f"{channel_url}/shorts"]
            res_shorts = subprocess.run(cmd_shorts, capture_output=True, text=True, check=True)
            data_shorts = json.loads(res_shorts.stdout)

            subs = data_longs.get("channel_follower_count", config.get("subscribers", 4))
            
            videos = []
            for i, entry in enumerate(data_longs.get("entries", []), 1):
                videos.append({
                    "id": f"LIVE-L{i:02d}",
                    "youtube_id": entry.get("id"),
                    "title": entry.get("title"),
                    "format": "long",
                    "views": entry.get("view_count", 0) or 0,
                    "duration_seconds": entry.get("duration", 0) or 0
                })
            
            for i, entry in enumerate(data_shorts.get("entries", []), 1):
                videos.append({
                    "id": f"LIVE-S{i:02d}",
                    "youtube_id": entry.get("id"),
                    "title": entry.get("title"),
                    "format": "short",
                    "views": entry.get("view_count", 0) or 0
                })

            baseline_payload = {
                "channel_id": data_longs.get("channel_id", config.get("id")),
                "channel_slug": channel_slug,
                "channel_name": config.get("name"),
                "handle": config.get("handle"),
                "url": channel_url,
                "language": config.get("language"),
                "subscribers": subs,
                "genre": config.get("genre"),
                "archetype": config.get("archetype"),
                "videos": videos
            }

            # Save updated baseline
            baseline_path = self.base_data_dir / f"{channel_slug}_baseline.json"
            with open(baseline_path, "w", encoding="utf-8") as f:
                json.dump(baseline_payload, f, indent=2, ensure_ascii=False)

            # Update memory with live videos
            for v in videos:
                self.memory.record_video(
                    channel=channel_slug,
                    title=v["title"],
                    video_id=v.get("youtube_id"),
                    format=v["format"],
                    views=v["views"]
                )

            return {
                "status": "LIVE_SYNC_SUCCESS",
                "subscribers": subs,
                "total_videos_found": len(videos),
                "long_videos_count": len(data_longs.get("entries", [])),
                "shorts_count": len(data_shorts.get("entries", []))
            }
        except Exception as e:
            return {"status": "LIVE_SYNC_FAILED", "error": str(e)}

    def register_channel_02(self, channel_data: Dict[str, Any]) -> Dict[str, Any]:
        """Registers Channel 2 dynamically when the user provides the identity/data."""
        slug = channel_data.get("slug", "canal_02_trading").lower()
        self.configs[slug] = channel_data
        
        # Save baseline file
        p = self.base_data_dir / f"{slug}_baseline.json"
        with open(p, "w", encoding="utf-8") as f:
            json.dump(channel_data, f, indent=2, ensure_ascii=False)
            
        return {"status": "CHANNEL_02_REGISTERED", "channel_slug": slug}

chief_trading_agent = ChiefTradingAgent()
