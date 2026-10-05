# -*- coding: utf-8 -*-
"""
Hermes Chief Skill: live-channel-crawler & quant-intelligence
Performs real-time live extraction of YouTube channels, executes statistical analysis
(Z-score viral outliers, views velocity, cadence, format ratio, tag clusters),
and prepares actionable intelligence dossiers for the Chief Analyst Agent.
"""

import sys
import os
import json
import re
import math
from datetime import datetime, date
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

class LiveChannelCrawler:
    """Connects to live YouTube channels, extracts all videos and computes quant metrics."""

    CHANNEL_MAP = {
        "o_outro_lado": {
            "handle": "@outroladodetudo",
            "name": "O Outro Lado",
            "file": "outro_lado_baseline.json",
            "default_id": "UCf6Ox9rzQbIkDeE94to9AEQ",
            "prefix_long": "OOL-",
            "prefix_short": "OOL-S"
        },
        "hidden_systems_lab": {
            "handle": "@HiddenSystemslabss",
            "name": "Hidden Systems Lab (HSL)",
            "file": "hsl_baseline.json",
            "default_id": "UC-HiddenSystemsLab",
            "prefix_long": "HSL-",
            "prefix_short": "HSL-S"
        },
        "brecha": {
            "handle": "@brechadocs",
            "name": "Brecha",
            "file": "brecha_baseline.json",
            "default_id": "UC-CanalBrecha",
            "prefix_long": "BRC-",
            "prefix_short": "BRC-S"
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

    def _get_ydl(self, extract_flat: bool = True):
        try:
            import yt_dlp
        except ImportError:
            raise RuntimeError("A biblioteca 'yt-dlp' é necessária para a inteligência ao vivo. Instale com 'pip install yt-dlp'.")

        opts = {
            'quiet': True,
            'no_warnings': True,
            'skip_download': True,
            'ignoreerrors': True,
            'extract_flat': extract_flat,
        }
        return yt_dlp.YoutubeDL(opts)

    def fetch_channel_overview_live(self, handle: str) -> Dict[str, Any]:
        """Fetches channel-level metadata (live subscribers, total video count, channel ID, description)."""
        clean_handle = handle if handle.startswith("@") else f"@{handle}"
        url = f"https://www.youtube.com/{clean_handle}"

        with self._get_ydl(extract_flat=True) as ydl:
            try:
                info = ydl.extract_info(url, download=False)
                if not info:
                    return {}
                return {
                    "channel_title": info.get("channel") or info.get("title") or clean_handle,
                    "channel_id": info.get("channel_id") or "",
                    "subscribers": info.get("channel_follower_count") or 0,
                    "description": info.get("description") or "",
                    "uploader_id": info.get("uploader_id") or clean_handle
                }
            except Exception as e:
                print(f"⚠️ Erro ao obter visão geral do canal {clean_handle}: {e}", file=sys.stderr)
                return {}

    def fetch_all_videos_live(self, handle: str) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
        """
        Extracts all long-form videos and shorts with full available metadata.
        Returns: (long_videos_list, shorts_list)
        """
        clean_handle = handle if handle.startswith("@") else f"@{handle}"
        long_videos: List[Dict[str, Any]] = []
        shorts_videos: List[Dict[str, Any]] = []

        with self._get_ydl(extract_flat=True) as ydl:
            # 1. Long videos (/videos)
            videos_url = f"https://www.youtube.com/{clean_handle}/videos"
            try:
                v_res = ydl.extract_info(videos_url, download=False)
                if v_res and "entries" in v_res:
                    for e in v_res["entries"]:
                        if not e:
                            continue
                        dur = int(e.get("duration") or 0)
                        views = int(e.get("view_count") or 0)
                        long_videos.append({
                            "youtube_id": e.get("id"),
                            "title": (e.get("title") or "").strip(),
                            "views": views,
                            "duration_seconds": dur,
                            "format": "long",
                            "upload_date": e.get("upload_date"), # YYYYMMDD if present
                            "timestamp": e.get("timestamp"),
                            "url": e.get("url") or f"https://www.youtube.com/watch?v={e.get('id')}",
                            "source_tab": "videos"
                        })
            except Exception as e:
                print(f"⚠️ Erro ao buscar vídeos longos de {clean_handle}: {e}", file=sys.stderr)

            # 2. Shorts (/shorts)
            shorts_url = f"https://www.youtube.com/{clean_handle}/shorts"
            try:
                s_res = ydl.extract_info(shorts_url, download=False)
                if s_res and "entries" in s_res:
                    seen_ids = {v["youtube_id"] for v in long_videos if v.get("youtube_id")}
                    for e in s_res["entries"]:
                        if not e:
                            continue
                        yt_id = e.get("id")
                        dur = int(e.get("duration") or 0)
                        views = int(e.get("view_count") or 0)

                        if yt_id in seen_ids:
                            # Reclassify from long to short if YouTube placed in /shorts
                            long_videos = [v for v in long_videos if v.get("youtube_id") != yt_id]

                        shorts_videos.append({
                            "youtube_id": yt_id,
                            "title": (e.get("title") or "").strip(),
                            "views": views,
                            "duration_seconds": dur,
                            "format": "short",
                            "upload_date": e.get("upload_date"),
                            "timestamp": e.get("timestamp"),
                            "url": e.get("url") or f"https://www.youtube.com/shorts/{yt_id}",
                            "source_tab": "shorts"
                        })
            except Exception as e:
                print(f"⚠️ Erro ao buscar shorts de {clean_handle}: {e}", file=sys.stderr)

        return long_videos, shorts_videos

    def _compute_stats(self, items: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Calculates statistical indicators (mean, median, std dev, z-scores, outliers)."""
        if not items:
            return {
                "count": 0,
                "total_views": 0,
                "mean_views": 0.0,
                "median_views": 0.0,
                "std_dev_views": 0.0,
                "viral_outliers": [],
                "stalled_videos": []
            }

        views_list = [float(v.get("views", 0)) for v in items]
        n = len(views_list)
        total_views = sum(views_list)
        mean_v = total_views / n

        sorted_v = sorted(views_list)
        if n % 2 == 1:
            median_v = sorted_v[n // 2]
        else:
            median_v = (sorted_v[n // 2 - 1] + sorted_v[n // 2]) / 2.0

        variance = sum((x - mean_v) ** 2 for x in views_list) / n if n > 1 else 0.0
        std_dev = math.sqrt(variance)

        viral_outliers = []
        stalled_videos = []

        for v in items:
            views = float(v.get("views", 0))
            z = round((views - mean_v) / std_dev, 2) if std_dev > 0 else 0.0
            v["z_score"] = z

            if std_dev > 0 and z >= 1.5:
                viral_outliers.append({
                    "id": v.get("youtube_id"),
                    "title": v.get("title"),
                    "views": int(views),
                    "z_score": z,
                    "format": v.get("format")
                })
            elif views <= 5:
                stalled_videos.append({
                    "id": v.get("youtube_id"),
                    "title": v.get("title"),
                    "views": int(views),
                    "z_score": z,
                    "format": v.get("format")
                })

        return {
            "count": n,
            "total_views": int(total_views),
            "mean_views": round(mean_v, 1),
            "median_views": round(median_v, 1),
            "std_dev_views": round(std_dev, 1),
            "viral_outliers": viral_outliers,
            "stalled_videos": stalled_videos
        }

    def _extract_keyword_clusters(self, videos: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Identifies recurring themes/keywords and correlates them with average views."""
        stopwords = {
            "de", "a", "o", "que", "e", "do", "da", "em", "um", "para", "é", "com", "não", "uma", "os", "no", "se", "na",
            "por", "mais", "as", "dos", "como", "mas", "foi", "ao", "ele", "das", "tem", "à", "seu", "sua", "ou", "ser",
            "quando", "muito", "há", "nos", "já", "está", "eu", "também", "só", "pelo", "pela", "até", "isso", "ela", "entre",
            "era", "depois", "sem", "mesmo", "aos", "ter", "seus", "quem", "nas", "me", "esse", "eles", "estão", "você", "tinha",
            "foram", "essa", "num", "nem", "suas", "meu", "às", "minha", "têm", "numa", "pelos", "elas", "havia", "seja",
            "the", "of", "and", "to", "in", "a", "is", "that", "for", "it", "as", "was", "with", "on", "at", "by", "this", "from"
        }

        word_views: Dict[str, List[int]] = {}
        for v in videos:
            t = (v.get("title") or "").lower()
            words = re.findall(r'\b[a-záéíóúãõâêîôûç]{4,}\b', t)
            views = int(v.get("views") or 0)
            seen_in_title = set()
            for w in words:
                if w not in stopwords and w not in seen_in_title:
                    word_views.setdefault(w, []).append(views)
                    seen_in_title.add(w)

        clusters = []
        for word, v_list in word_views.items():
            if len(v_list) >= 2: # Appears in at least 2 titles
                clusters.append({
                    "keyword": word,
                    "frequency": len(v_list),
                    "mean_views": round(sum(v_list) / len(v_list), 1),
                    "max_views": max(v_list)
                })

        clusters.sort(key=lambda x: (x["mean_views"], x["frequency"]), reverse=True)
        return clusters[:8]

    def _find_shorts_bridges(self, long_videos: List[Dict[str, Any]], shorts_videos: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Finds high-performing shorts that should bridge audience to long-form videos."""
        bridges = []
        # Filter shorts with substantial views
        top_shorts = [s for s in shorts_videos if int(s.get("views") or 0) >= 100]
        top_shorts.sort(key=lambda s: int(s.get("views") or 0), reverse=True)

        for s in top_shorts:
            s_title = s.get("title", "").lower()
            # Try to match with long-form
            best_match = None
            max_common_words = 0

            s_words = set(re.findall(r'\b\w{4,}\b', s_title))
            for l in long_videos:
                l_title = l.get("title", "").lower()
                l_words = set(re.findall(r'\b\w{4,}\b', l_title))
                common = len(s_words.intersection(l_words))
                if common > max_common_words:
                    max_common_words = common
                    best_match = l

            bridges.append({
                "short_title": s.get("title"),
                "short_views": s.get("views"),
                "short_url": s.get("url"),
                "recommended_master_video": best_match.get("title") if best_match else "Produzir documentário longo correspondente",
                "recommended_master_id": best_match.get("youtube_id") if best_match else None,
                "urgency": "ALTA" if int(s.get("views") or 0) >= 1000 else "MÉDIA"
            })

        return bridges[:5]

    def analyze_live_channel(self, channel_slug: str) -> Dict[str, Any]:
        """
        Executes end-to-end real-time quantitative analysis for a channel.
        Crawls channel info, all videos, calculates indicators, generates insights,
        and saves updated snapshot to data/channels/.
        """
        slug = self.normalize_slug(channel_slug)
        cfg = self.CHANNEL_MAP.get(slug)
        if not cfg:
            raise ValueError(f"Canal '{channel_slug}' não encontrado. Opções válidas: {list(self.CHANNEL_MAP.keys())}")

        handle = cfg["handle"]
        print(f"🛰️ Conectando ao vivo ao YouTube: {cfg['name']} ({handle})...", file=sys.stderr)

        # 1. Fetch channel overview
        overview = self.fetch_channel_overview_live(handle)
        live_subs = overview.get("subscribers") or 0

        # 2. Fetch all videos & shorts
        long_v, short_v = self.fetch_all_videos_live(handle)
        all_videos = long_v + short_v

        # 3. Compute stats
        long_stats = self._compute_stats(long_v)
        short_stats = self._compute_stats(short_v)

        total_catalog_views = long_stats["total_views"] + short_stats["total_views"]
        total_videos = len(all_videos)
        ratio = round(short_stats["mean_views"] / (long_stats["mean_views"] or 1.0), 2)

        # 4. Keyword clusters
        keyword_clusters = self._extract_keyword_clusters(all_videos)

        # 5. Bridge opportunities
        bridges = self._find_shorts_bridges(long_v, short_v)

        # 6. Primary Bottleneck Diagnosis
        if live_subs < 50 and long_stats["mean_views"] < 35:
            primary_bottleneck = {
                "type": "COLD_START",
                "name": "Gargalo de Descoberta // Cold Start Algorítmico",
                "symptom": f"Poucos inscritos ({live_subs}) e views médias em longos baixas ({long_stats['mean_views']}).",
                "root_cause": "Canal novo sem base semente; algoritmo ainda mapeando o público-alvo.",
                "action": "Vincular Shorts virais aos vídeos longos no YouTube Studio e concentrar pautas em temas com alto volume de busca."
            }
        elif ratio > 10.0:
            primary_bottleneck = {
                "type": "SHORTS_DISCONNECT",
                "name": "Desconexão de Tráfego entre Shorts e Longos",
                "symptom": f"Shorts têm média de views {ratio}x maior que os longos ({short_stats['mean_views']} vs {long_stats['mean_views']}).",
                "root_cause": "Visualizações de Shorts não convertem para longos por falta de call-to-action e link de vídeo relacionado.",
                "action": "Configurar o botão 'Vídeo Relacionado' em todos os Shorts com mais de 500 visualizações."
            }
        elif live_subs > 500 and long_stats["mean_views"] < 50:
            primary_bottleneck = {
                "type": "GHOST_AUDIENCE",
                "name": "Audiência Fantasma // Inscritos Inativos",
                "symptom": f"Base de {live_subs} inscritos mas média de apenas {long_stats['mean_views']} views por vídeo longo.",
                "root_cause": "Inscritos antigos não clicam nas novas publicações, derrubando o CTR inicial de navegação.",
                "action": "Reformular a embalagem (título + thumb) para atrair tráfego externo via Browse/Pesquisa em vez de depender de inscritos."
            }
        else:
            primary_bottleneck = {
                "type": "PACKAGING_CTR",
                "name": "Gargalo de Embalagem // Baixa Taxa de Clique",
                "symptom": f"Média de visualizações em longos ({long_stats['mean_views']}) estagnada.",
                "root_cause": "Promessa da thumbnail ou título não gera curiosidade suficiente (curiosity gap fraca).",
                "action": "Aplicar a regra dos 3 elementos focais na thumbnail e títulos no formato 'O Mecanismo Oculto'."
            }

        # 7. Update Baseline File with live figures
        baseline_file = self.data_dir / cfg["file"]
        existing_data = {}
        if baseline_file.exists():
            try:
                with open(baseline_file, 'r', encoding='utf-8') as f:
                    existing_data = json.load(f)
            except Exception:
                pass

        # Merge with existing metrics
        existing_v_map = {v.get("youtube_id") or v.get("id"): v for v in existing_data.get("videos", [])}

        merged_catalog = []
        for v in all_videos:
            yt_id = v.get("youtube_id")
            old = existing_v_map.get(yt_id)
            if old:
                record = dict(old)
                record["views"] = v["views"]
                record["youtube_id"] = yt_id
                record["duration_seconds"] = v.get("duration_seconds", 0)
            else:
                # Newly discovered
                record = {
                    "id": f"{cfg['prefix_long' if v['format'] == 'long' else 'prefix_short']}{len(merged_catalog) + 1:02d}",
                    "youtube_id": yt_id,
                    "title": v["title"],
                    "format": v["format"],
                    "views": v["views"],
                    "ctr": 3.8 if v["format"] == "long" else 6.5,
                    "avd_pct": 40.0 if v["format"] == "long" else 65.0,
                    "retention_30s": 50.0 if v["format"] == "long" else 75.0,
                    "duration_seconds": v.get("duration_seconds", 0),
                    "auto_ingested": True
                }
            merged_catalog.append(record)

        updated_payload = {
            "channel_id": overview.get("channel_id") or cfg["default_id"],
            "channel_slug": slug,
            "channel_name": cfg["name"],
            "handle": handle,
            "subscribers": live_subs,
            "last_synced_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "dominant_traffic_sources": existing_data.get("dominant_traffic_sources", ["Recursos de Navegação (Browse)", "Pesquisa do YouTube", "Feed dos Shorts"]),
            "videos": merged_catalog
        }

        with open(baseline_file, 'w', encoding='utf-8') as f:
            json.dump(updated_payload, f, ensure_ascii=False, indent=2)

        # 8. Automatically register all discovered videos into ChiefMemory covered_themes
        try:
            from src.core.memory import chief_memory
            for v in all_videos:
                chief_memory.register_covered_theme(
                    channel=slug,
                    core_topic=v["title"],
                    title_reference=v["title"],
                    status="PUBLISHED",
                    format=v.get("format", "long"),
                    video_id=v.get("youtube_id", ""),
                    views=int(v.get("views") or 0)
                )
            chief_memory.export_covered_themes_catalog(self.data_dir)
        except Exception:
            pass

        return {
            "status": "LIVE_ANALYSIS_COMPLETED",
            "channel_slug": slug,
            "channel_name": cfg["name"],
            "handle": handle,
            "live_subscribers": live_subs,
            "total_videos_analyzed": total_videos,
            "total_catalog_views": total_catalog_views,
            "long_videos": long_stats,
            "shorts_videos": short_stats,
            "shorts_to_long_ratio": ratio,
            "keyword_clusters": keyword_clusters,
            "bridge_opportunities": bridges,
            "primary_bottleneck": primary_bottleneck,
            "analyzed_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "baseline_updated": str(baseline_file)
        }

# Singleton instance
live_channel_crawler = LiveChannelCrawler()
