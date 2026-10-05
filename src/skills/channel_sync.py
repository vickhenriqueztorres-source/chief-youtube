# -*- coding: utf-8 -*-
"""
Hermes Chief Skill: channel-sync
Performs live extraction and continuous synchronization of YouTube channel data.
Ingests real-time video counts, views, durations, and formats (Longs vs Shorts)
via yt-dlp flat-playlist extraction, and merges them into data/channels/*.json baselines.
Optionally integrates YouTube Studio CSV analytics exports for exact CTR and retention curves.
"""

import sys
import os
import json
import csv
import re
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple

# Safe UTF-8 output on Windows consoles
try:
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    if hasattr(sys.stderr, 'reconfigure'):
        sys.stderr.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass

class ChannelDataSynchronizer:
    """Synchronizes live YouTube channel performance metrics with Chief baseline databases."""

    CHANNEL_TARGETS = {
        "o_outro_lado": {
            "handle": "@outroladodetudo",
            "file": "outro_lado_baseline.json",
            "name": "O Outro Lado",
            "id": "UCf6Ox9rzQbIkDeE94to9AEQ",
            "id_prefix_long": "OOL-",
            "id_prefix_short": "OOL-S"
        },
        "hidden_systems_lab": {
            "handle": "@HiddenSystemslabss",
            "file": "hsl_baseline.json",
            "name": "Hidden Systems Lab (HSL)",
            "id": "UC-HiddenSystemsLab",
            "id_prefix_long": "HSL-",
            "id_prefix_short": "HSL-S"
        },
        "brecha": {
            "handle": "@brechadocs",
            "file": "brecha_baseline.json",
            "name": "Brecha",
            "id": "UC-CanalBrecha",
            "id_prefix_long": "BRC-",
            "id_prefix_short": "BRC-S"
        }
    }

    def __init__(self, data_dir: Optional[Path] = None):
        self.data_dir = data_dir or (Path(__file__).resolve().parent.parent.parent / "data" / "channels")
        self.data_dir.mkdir(parents=True, exist_ok=True)

    def normalize_slug(self, raw_slug: str) -> str:
        s = raw_slug.strip().lower()
        if s in ["outro_lado", "ool", "o_outro_lado"]:
            return "o_outro_lado"
        elif s in ["hsl", "hidden", "hidden_systems_lab"]:
            return "hidden_systems_lab"
        elif s in ["brecha", "brc"]:
            return "brecha"
        return s

    def fetch_channel_videos_live(self, handle: str) -> List[Dict[str, Any]]:
        """
        Fetches live videos and shorts list from YouTube using yt-dlp flat extraction.
        Returns a list of normalized video dicts.
        """
        try:
            import yt_dlp
        except ImportError:
            raise RuntimeError("A biblioteca 'yt-dlp' é necessária para sincronização automática. Instale via pip install yt-dlp")

        ydl_opts = {
            'extract_flat': True,
            'quiet': True,
            'no_warnings': True,
            'skip_download': True,
            'ignoreerrors': True,
        }

        extracted_videos: List[Dict[str, Any]] = []
        clean_handle = handle if handle.startswith("@") else f"@{handle}"

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # 1. Fetch Long-form videos tab
            videos_url = f"https://www.youtube.com/{clean_handle}/videos"
            try:
                v_info = ydl.extract_info(videos_url, download=False)
                if v_info and "entries" in v_info:
                    for entry in v_info["entries"]:
                        if not entry:
                            continue
                        dur = entry.get("duration") or 0
                        extracted_videos.append({
                            "youtube_id": entry.get("id"),
                            "title": entry.get("title", "").strip(),
                            "views": int(entry.get("view_count") or 0),
                            "duration": int(dur),
                            "format": "short" if dur and dur <= 60 else "long",
                            "url": entry.get("url") or f"https://www.youtube.com/watch?v={entry.get('id')}",
                            "source_tab": "videos"
                        })
            except Exception as e:
                print(f"⚠️ Aviso ao buscar vídeos longos para {clean_handle}: {e}", file=sys.stderr)

            # 2. Fetch Shorts tab
            shorts_url = f"https://www.youtube.com/{clean_handle}/shorts"
            try:
                s_info = ydl.extract_info(shorts_url, download=False)
                if s_info and "entries" in s_info:
                    existing_ids = {v["youtube_id"] for v in extracted_videos if v.get("youtube_id")}
                    for entry in s_info["entries"]:
                        if not entry:
                            continue
                        yt_id = entry.get("id")
                        if yt_id in existing_ids:
                            # Already captured; ensure marked as short if in shorts tab
                            for v in extracted_videos:
                                if v.get("youtube_id") == yt_id:
                                    v["format"] = "short"
                            continue
                        
                        dur = entry.get("duration") or 0
                        extracted_videos.append({
                            "youtube_id": yt_id,
                            "title": entry.get("title", "").strip(),
                            "views": int(entry.get("view_count") or 0),
                            "duration": int(dur),
                            "format": "short",
                            "url": entry.get("url") or f"https://www.youtube.com/shorts/{yt_id}",
                            "source_tab": "shorts"
                        })
            except Exception as e:
                print(f"⚠️ Aviso ao buscar shorts para {clean_handle}: {e}", file=sys.stderr)

        return extracted_videos

    def _clean_title_for_matching(self, title: str) -> str:
        """Removes punctuation and normalizes casing for fuzzy title comparison."""
        t = re.sub(r'[^\w\s]', '', title).lower()
        return re.sub(r'\s+', ' ', t).strip()

    def merge_with_baseline(
        self,
        channel_slug: str,
        live_videos: List[Dict[str, Any]],
        csv_path: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Merges freshly extracted live YouTube data into the channel baseline file.
        Preserves historical CTR/Retention, updates view counts, and integrates new uploads.
        """
        slug = self.normalize_slug(channel_slug)
        cfg = self.CHANNEL_TARGETS.get(slug)
        if not cfg:
            raise ValueError(f"Canal '{channel_slug}' não configurado em CHANNEL_TARGETS.")

        baseline_file = self.data_dir / cfg["file"]
        if baseline_file.exists():
            with open(baseline_file, 'r', encoding='utf-8') as f:
                baseline_data = json.load(f)
        else:
            baseline_data = {
                "channel_id": cfg["id"],
                "channel_slug": slug,
                "channel_name": cfg["name"],
                "handle": cfg["handle"],
                "subscribers": 0,
                "dominant_traffic_sources": ["Recursos de Navegação (Browse)", "Pesquisa do YouTube", "Feed dos Shorts"],
                "videos": []
            }

        existing_videos = baseline_data.get("videos", [])

        # Build index for fast matching
        # 1. Matching by cleaned title
        title_map: Dict[str, Dict[str, Any]] = {}
        # 2. Matching by youtube_id if present
        ytid_map: Dict[str, Dict[str, Any]] = {}

        for v in existing_videos:
            clean_t = self._clean_title_for_matching(v.get("title", ""))
            title_map[clean_t] = v
            if "youtube_id" in v:
                ytid_map[v["youtube_id"]] = v

        # Calculate current channel averages for priors
        long_ctrs = [v.get("ctr", 0.0) for v in existing_videos if v.get("format") == "long" and v.get("ctr")]
        long_ret30 = [v.get("retention_30s", 0.0) for v in existing_videos if v.get("format") == "long" and v.get("retention_30s")]
        long_avd = [v.get("avd_pct", 0.0) for v in existing_videos if v.get("format") == "long" and v.get("avd_pct")]

        short_ctrs = [v.get("ctr", 0.0) for v in existing_videos if v.get("format") == "short" and v.get("ctr")]
        short_ret30 = [v.get("retention_30s", 0.0) for v in existing_videos if v.get("format") == "short" and v.get("retention_30s")]
        short_avd = [v.get("avd_pct", 0.0) for v in existing_videos if v.get("format") == "short" and v.get("avd_pct")]

        prior_long_ctr = round(sum(long_ctrs) / len(long_ctrs), 2) if long_ctrs else 4.0
        prior_long_ret30 = round(sum(long_ret30) / len(long_ret30), 2) if long_ret30 else 50.0
        prior_long_avd = round(sum(long_avd) / len(long_avd), 2) if long_avd else 40.0

        prior_short_ctr = round(sum(short_ctrs) / len(short_ctrs), 2) if short_ctrs else 6.5
        prior_short_ret30 = round(sum(short_ret30) / len(short_ret30), 2) if short_ret30 else 70.0
        prior_short_avd = round(sum(short_avd) / len(short_avd), 2) if short_avd else 60.0

        updated_count = 0
        inserted_count = 0

        # Determine next ID counters
        next_long_idx = len([v for v in existing_videos if v.get("format") == "long"]) + 1
        next_short_idx = len([v for v in existing_videos if v.get("format") == "short"]) + 1

        for live in live_videos:
            yt_id = live.get("youtube_id")
            live_title = live.get("title", "")
            clean_live_t = self._clean_title_for_matching(live_title)

            match = None
            if yt_id and yt_id in ytid_map:
                match = ytid_map[yt_id]
            elif clean_live_t in title_map:
                match = title_map[clean_live_t]
            else:
                # Fuzzy fallback: check if title is substring
                for existing_t, v in title_map.items():
                    if len(existing_t) > 10 and (existing_t in clean_live_t or clean_live_t in existing_t):
                        match = v
                        break

            if match:
                # Update existing video
                match["views"] = live["views"]
                if yt_id:
                    match["youtube_id"] = yt_id
                if "duration" in live and live["duration"] > 0:
                    match["duration_seconds"] = live["duration"]
                updated_count += 1
            else:
                # New video discovered on YouTube
                fmt = live.get("format", "long")
                if fmt == "long":
                    new_id = f"{cfg['id_prefix_long']}{next_long_idx:02d}"
                    next_long_idx += 1
                    ctr_val = prior_long_ctr
                    ret30_val = prior_long_ret30
                    avd_val = prior_long_avd
                else:
                    new_id = f"{cfg['id_prefix_short']}{next_short_idx:02d}"
                    next_short_idx += 1
                    ctr_val = prior_short_ctr
                    ret30_val = prior_short_ret30
                    avd_val = prior_short_avd

                new_record = {
                    "id": new_id,
                    "youtube_id": yt_id,
                    "title": live_title,
                    "format": fmt,
                    "views": live["views"],
                    "ctr": ctr_val,
                    "avd_pct": avd_val,
                    "retention_30s": ret30_val,
                    "duration_seconds": live.get("duration", 0),
                    "auto_ingested": True
                }
                existing_videos.append(new_record)
                title_map[clean_live_t] = new_record
                if yt_id:
                    ytid_map[yt_id] = new_record
                inserted_count += 1

        # Optional: Ingest and merge Studio CSV
        csv_updated = 0
        if csv_path and os.path.exists(csv_path):
            csv_updated = self._merge_studio_csv(existing_videos, csv_path)

        baseline_data["videos"] = existing_videos

        # Save to disk
        with open(baseline_file, 'w', encoding='utf-8') as f:
            json.dump(baseline_data, f, ensure_ascii=False, indent=2)

        return {
            "channel_slug": slug,
            "channel_name": cfg["name"],
            "total_videos_catalog": len(existing_videos),
            "updated_views_count": updated_count,
            "new_videos_inserted": inserted_count,
            "csv_records_merged": csv_updated,
            "baseline_path": str(baseline_file)
        }

    def _merge_studio_csv(self, videos: List[Dict[str, Any]], csv_path: str) -> int:
        """Parses a YouTube Studio Analytics export CSV and updates exact CTR and retention."""
        updated = 0
        try:
            with open(csv_path, 'r', encoding='utf-8-sig', errors='replace') as f:
                reader = csv.DictReader(f)
                rows = list(reader)

            for r in rows:
                t_cand = r.get("Título do vídeo") or r.get("Video title") or r.get("Content") or ""
                if not t_cand:
                    continue
                clean_csv_t = self._clean_title_for_matching(t_cand)

                for v in videos:
                    clean_v_t = self._clean_title_for_matching(v.get("title", ""))
                    if clean_csv_t == clean_v_t or (len(clean_csv_t) > 10 and clean_csv_t in clean_v_t):
                        # CTR
                        ctr_str = r.get("Taxa de cliques nas impressões (%)") or r.get("Impressions click-through rate (%)") or ""
                        if ctr_str:
                            try:
                                v["ctr"] = float(ctr_str.replace("%", "").replace(",", ".").strip())
                            except ValueError:
                                pass
                        
                        # Retenção / AVD
                        avd_str = r.get("Duração média da visualização (%)") or r.get("Average percentage viewed (%)") or ""
                        if avd_str:
                            try:
                                v["avd_pct"] = float(avd_str.replace("%", "").replace(",", ".").strip())
                            except ValueError:
                                pass

                        updated += 1
                        break
        except Exception as e:
            print(f"⚠️ Erro ao processar CSV do Studio ({csv_path}): {e}", file=sys.stderr)

        return updated

    def sync_channel(self, channel_slug: str, csv_path: Optional[str] = None) -> Dict[str, Any]:
        """Runs full live synchronization for a single channel."""
        slug = self.normalize_slug(channel_slug)
        cfg = self.CHANNEL_TARGETS.get(slug)
        if not cfg:
            raise ValueError(f"Canal '{channel_slug}' inválido. Escolha entre: {list(self.CHANNEL_TARGETS.keys())}")

        print(f"📡 Conectando ao YouTube para sincronizar {cfg['name']} ({cfg['handle']})...", file=sys.stderr)
        live_data = self.fetch_channel_videos_live(cfg["handle"])
        res = self.merge_with_baseline(slug, live_data, csv_path)
        return res

    def sync_all(self, csv_dir: Optional[str] = None) -> Dict[str, Any]:
        """Synchronizes all 3 channels in sequence."""
        results = {}
        for slug in self.CHANNEL_TARGETS.keys():
            res = self.sync_channel(slug)
            results[slug] = res
        return results

# Singleton instance
channel_synchronizer = ChannelDataSynchronizer()
