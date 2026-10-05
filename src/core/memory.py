# -*- coding: utf-8 -*-
"""
Hermes Chief - SQLite FTS5 Persistent Memory Engine
Manages tactical memory, learned lessons, validated hypotheses, and video track records.
"""

import sqlite3
import os
import json
import re
import unicodedata
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any, Optional, Set, Tuple

# Predefined Stopwords for Portuguese and English to isolate core topical entities
STOPWORDS = {
    # Portuguese
    "de", "a", "o", "que", "e", "do", "da", "em", "um", "para", "com", "nao", "uma", "os", "no", "se", "na",
    "por", "mais", "as", "dos", "como", "mas", "foi", "ao", "ele", "das", "tem", "seu", "sua", "ou", "ser",
    "quando", "muito", "nos", "esta", "eu", "tambem", "so", "pelo", "pela", "ate", "isso", "ela", "entre",
    "era", "depois", "sem", "mesmo", "aos", "ter", "seus", "quem", "nas", "me", "esse", "eles", "estao", "voce",
    "tinha", "foram", "essa", "num", "nem", "suas", "meu", "minha", "pelos", "onde", "qual", "como",
    "funciona", "veja", "porque", "por que", "fazem", "fazer", "pode", "duas", "vezes", "segundos", "minutos",
    "horas", "dias", "anos", "primeiros", "falha", "invisivel", "revelado", "segredo", "verdade", "canal",
    # English
    "the", "of", "and", "to", "in", "is", "that", "for", "it", "as", "was", "with", "on", "at", "by", "this",
    "from", "they", "we", "say", "her", "she", "or", "an", "will", "my", "one", "all", "would", "there", "their",
    "what", "so", "up", "out", "if", "about", "who", "get", "which", "go", "me", "when", "make", "can", "like",
    "time", "no", "just", "him", "know", "take", "people", "into", "year", "your", "good", "some", "could", "them",
    "see", "other", "than", "then", "now", "look", "only", "come", "its", "over", "think", "also", "back", "after",
    "use", "two", "how", "why", "stop", "cannot"
}

def normalize_text(text: str) -> str:
    """Removes accents, lowercase, removes special characters."""
    if not text:
        return ""
    nfkd = unicodedata.normalize('NFKD', text)
    no_accents = ''.join([c for c in nfkd if not unicodedata.combining(c)])
    cleaned = re.sub(r'[^a-zA-Z0-9\s]', ' ', no_accents.lower())
    return ' '.join(cleaned.split())

def stem_token(word: str) -> str:
    """Lightweight suffix normalizer for Portuguese & English singular/plural and verb forms."""
    w = word.lower()
    if len(w) <= 3:
        return w
    if w.endswith('ores') and len(w) > 5:
        return w[:-4] + 'or'
    if w.endswith('dores') and len(w) > 6:
        return w[:-5] + 'dor'
    if w.endswith('oes') and len(w) > 4:
        return w[:-3] + 'ao'
    if w.endswith('ais') and len(w) > 4:
        return w[:-3] + 'al'
    if w.endswith('eis') and len(w) > 4:
        return w[:-3] + 'el'
    if w.endswith('ados') or w.endswith('adas'):
        return w[:-2]
    if w.endswith('ado') or w.endswith('ada'):
        return w[:-1]
    if w.endswith('idos') or w.endswith('idas'):
        return w[:-2]
    if w.endswith('ido') or w.endswith('ida'):
        return w[:-1]
    if w.endswith('ies') and len(w) > 4:
        return w[:-3] + 'y'
    if w.endswith('es') and len(w) > 4:
        return w[:-2]
    if w.endswith('s') and not w.endswith('ss') and len(w) > 3:
        return w[:-1]
    return w

# Core technical synonym expansion
SYNONYM_EXPANSIONS = {
    "jammer": ["bloqueador", "rastreador", "gps", "interferencia", "frequencia"],
    "rastreador": ["jammer", "bloqueador", "gps", "veiculo", "caminhao"],
    "spoofing": ["ura", "falsa", "banco", "ligacao", "central", "telefone"],
    "ura": ["spoofing", "ligacao", "central", "banco", "telefone"],
    "sim": ["swap", "chip", "portabilidade", "operadora", "clonagem"],
    "swap": ["sim", "chip", "portabilidade", "operadora"],
    "maquininha": ["pos", "chupa", "cabra", "cartao", "senha"],
    "chupacabra": ["maquininha", "pos", "cartao", "senha", "golpe"],
    "pix": ["devolucao", "med", "estorno", "transferencia", "banco"],
    "deepfake": ["clonagem", "voz", "audio", "ia", "inteligencia"],
    "blackstart": ["grid", "apaga", "blecaute", "reiniciar", "gerador"],
    "waterhammer": ["shockwave", "golpe", "ariete", "valvula", "pressao"]
}

def extract_core_tokens(text: str) -> Set[str]:
    """Extracts significant stemmed keywords and synonyms for semantic deduplication."""
    norm = normalize_text(text)
    words = norm.split()
    tokens = set()
    for w in words:
        if len(w) >= 3 and w not in STOPWORDS:
            st = stem_token(w)
            tokens.add(st)
            # Add technical synonyms if applicable
            if st in SYNONYM_EXPANSIONS:
                for syn in SYNONYM_EXPANSIONS[st]:
                    tokens.add(stem_token(syn))
    return tokens

def generate_topic_slug(text: str) -> str:
    """Generates an alphanumeric slug from the most significant tokens."""
    tokens = sorted(list(extract_core_tokens(text)))
    if tokens:
        return '_'.join(tokens[:5])
    norm = normalize_text(text)
    return re.sub(r'[^a-z0-9]+', '_', norm).strip('_')[:50]

def get_db_path() -> Path:
    """Returns local project memory path or fallback to user home directory."""
    local_dir = Path(__file__).resolve().parent.parent.parent / ".hermes" / "memory"
    if local_dir.exists():
        return local_dir / "chief_memory.db"
    
    home_dir = Path.home() / ".hermes" / "memory"
    home_dir.mkdir(parents=True, exist_ok=True)
    return home_dir / "chief_memory.db"

class ChiefMemory:
    def __init__(self, db_path: Optional[Path] = None):
        self.db_path = db_path or get_db_path()
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_db()

    def _get_connection(self) -> sqlite3.Connection:
        con = sqlite3.connect(str(self.db_path))
        con.row_factory = sqlite3.Row
        return con

    def _init_db(self):
        with self._get_connection() as con:
            cur = con.cursor()
            
            # Base table: learnings
            cur.execute("""
            CREATE TABLE IF NOT EXISTS learnings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                channel TEXT NOT NULL,
                category TEXT NOT NULL,
                insight TEXT NOT NULL,
                evidence TEXT,
                action_taken TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
            """)

            # Base table: experiments
            cur.execute("""
            CREATE TABLE IF NOT EXISTS experiments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                channel TEXT NOT NULL,
                hypothesis TEXT NOT NULL,
                test_design TEXT NOT NULL,
                metric_target TEXT NOT NULL,
                status TEXT DEFAULT 'PENDING',
                result_observed TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
            """)

            # Base table: video_history
            cur.execute("""
            CREATE TABLE IF NOT EXISTS video_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                channel TEXT NOT NULL,
                video_id TEXT,
                title TEXT NOT NULL,
                format TEXT DEFAULT 'long',
                views INTEGER DEFAULT 0,
                ctr REAL DEFAULT 0.0,
                avd_pct REAL DEFAULT 0.0,
                retention_30s REAL DEFAULT 0.0,
                notes TEXT,
                published_at TEXT
            )
            """)

            # Base table: covered_themes (Persistent Registry of Topics Covered, Published, and In-Production)
            cur.execute("""
            CREATE TABLE IF NOT EXISTS covered_themes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                channel TEXT NOT NULL,
                theme_slug TEXT NOT NULL,
                core_topic TEXT NOT NULL,
                title_reference TEXT,
                status TEXT NOT NULL DEFAULT 'PUBLISHED', -- 'PUBLISHED', 'IN_PRODUCTION', 'BRIEFING_ISSUED', 'SCRAPPED'
                angle_covered TEXT,
                keywords TEXT, -- JSON array of strings
                format TEXT DEFAULT 'long',
                video_id TEXT,
                views_accumulated INTEGER DEFAULT 0,
                published_at TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(channel, theme_slug)
            )
            """)

            # FTS5 Virtual Table for full-text search across all memories
            cur.execute("""
            CREATE VIRTUAL TABLE IF NOT EXISTS memory_fts USING fts5(
                channel,
                category,
                content,
                evidence,
                tokenize = 'porter unicode61'
            )
            """)

            # FTS5 Virtual Table for semantic theme deduplication
            cur.execute("""
            CREATE VIRTUAL TABLE IF NOT EXISTS covered_themes_fts USING fts5(
                channel,
                core_topic,
                title_reference,
                keywords,
                angle_covered,
                tokenize = 'porter unicode61'
            )
            """)

            # Indexes for ultra-fast lookup
            cur.execute("CREATE INDEX IF NOT EXISTS idx_vh_channel ON video_history(channel)")
            cur.execute("CREATE INDEX IF NOT EXISTS idx_ct_channel_status ON covered_themes(channel, status)")

            con.commit()

    def record_learning(self, channel: str, category: str, insight: str, evidence: str = "", action_taken: str = "") -> int:
        with self._get_connection() as con:
            cur = con.cursor()
            cur.execute("""
                INSERT INTO learnings (channel, category, insight, evidence, action_taken)
                VALUES (?, ?, ?, ?, ?)
            """, (channel, category, insight, evidence, action_taken))
            learning_id = cur.lastrowid

            # Sync to FTS5
            cur.execute("""
                INSERT INTO memory_fts (channel, category, content, evidence)
                VALUES (?, ?, ?, ?)
            """, (channel, category, f"{insight} | Ação: {action_taken}", evidence))
            con.commit()
            return learning_id

    def record_experiment(self, channel: str, hypothesis: str, test_design: str, metric_target: str) -> int:
        with self._get_connection() as con:
            cur = con.cursor()
            cur.execute("""
                INSERT INTO experiments (channel, hypothesis, test_design, metric_target, status)
                VALUES (?, ?, ?, ?, 'RUNNING')
            """, (channel, hypothesis, test_design, metric_target))
            exp_id = cur.lastrowid

            cur.execute("""
                INSERT INTO memory_fts (channel, category, content, evidence)
                VALUES (?, 'experiment', ?, ?)
            """, (channel, f"Hipótese: {hypothesis} | Teste: {test_design}", f"Alvo: {metric_target}"))
            con.commit()
            return exp_id

    def close_experiment(self, exp_id: int, status: str, result_observed: str):
        with self._get_connection() as con:
            cur = con.cursor()
            cur.execute("""
                UPDATE experiments 
                SET status = ?, result_observed = ?, updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
            """, (status, result_observed, exp_id))
            con.commit()

    def auto_ingest_live_patterns(self, channel_slug: str, live_data: Dict[str, Any]) -> int:
        """
        Automatically analyzes real-time crawler results and records key learnings,
        viral patterns, and actionable directives into FTS5 memory.
        """
        recorded = 0
        ch = channel_slug.lower()

        # 1. Ingest Primary Bottleneck Diagnosis
        bot = live_data.get("primary_bottleneck", {})
        if bot:
            self.record_learning(
                channel=ch,
                category="DIAGNOSTIC_LIVE",
                insight=f"Gargalo em tempo real: {bot.get('name')}. {bot.get('symptom')}",
                evidence=f"Inscritos ao vivo: {live_data.get('live_subscribers')} | Total views catálogo: {live_data.get('total_catalog_views')}",
                action_taken=bot.get("action", "")
            )
            recorded += 1

        # 2. Ingest Viral Outliers
        long_outliers = live_data.get("long_videos", {}).get("viral_outliers", [])
        for out in long_outliers[:2]:
            self.record_learning(
                channel=ch,
                category="TOPIC_OUTLIER",
                insight=f"Outlier viral identificado: '{out.get('title')}' gerou {out.get('views')} views (Z-Score = {out.get('z_score')}).",
                evidence=f"Média do canal: {live_data.get('long_videos', {}).get('mean_views')} views. Vídeo superou a média em {out.get('z_score')} desvios-padrão.",
                action_taken="Replicar a premissa temática e a estrutura de promessa nos próximos documentários longos."
            )
            recorded += 1

        # 3. Ingest Keyword Clusters
        clusters = live_data.get("keyword_clusters", [])
        if clusters:
            top_k = clusters[0]
            self.record_learning(
                channel=ch,
                category="KEYWORD_CLUSTER",
                insight=f"Cluster temático com maior tração: '{top_k.get('keyword').upper()}' (média de {top_k.get('mean_views')} views em {top_k.get('frequency')} vídeos).",
                evidence=f"Pico de {top_k.get('max_views')} views registrado neste cluster.",
                action_taken=f"Priorizar palavras-chave derivadas de '{top_k.get('keyword')}' nos títulos de pautas P0."
            )
            recorded += 1

        # 4. Ingest Bridge Opportunities
        bridges = live_data.get("bridge_opportunities", [])
        for b in bridges[:2]:
            if b.get("urgency") == "ALTA":
                self.record_learning(
                    channel=ch,
                    category="SHORTS_BRIDGE",
                    insight=f"Short viral '{b.get('short_title')}' ({b.get('short_views')} views) precisa de ponte para documentário longo.",
                    evidence=f"URL: {b.get('short_url')}",
                    action_taken=f"Vincular ao master: '{b.get('recommended_master_video')}' via botão Vídeo Relacionado no YouTube Studio."
                )
                recorded += 1

        return recorded

    def search(self, query: str, channel: Optional[str] = None, limit: int = 10) -> List[Dict[str, Any]]:
        with self._get_connection() as con:
            cur = con.cursor()
            # Clean and prepare FTS query: e.g. "santos* shorts*"
            words = [w.strip() for w in query.replace('"', '').replace("'", "").split() if len(w.strip()) > 1]
            fts_term = " OR ".join([f"{w}*" for w in words]) if words else query

            rows = []
            if fts_term:
                try:
                    if channel:
                        cur.execute("""
                            SELECT rowid, channel, category, content, evidence, rank
                            FROM memory_fts
                            WHERE memory_fts MATCH ? AND channel = ?
                            ORDER BY rank
                            LIMIT ?
                        """, (fts_term, channel, limit))
                    else:
                        cur.execute("""
                            SELECT rowid, channel, category, content, evidence, rank
                            FROM memory_fts
                            WHERE memory_fts MATCH ?
                            ORDER BY rank
                            LIMIT ?
                        """, (fts_term, limit))
                    rows = cur.fetchall()
                except Exception:
                    rows = []

            # Fallback to standard LIKE if FTS produced 0 results
            if not rows and words:
                like_clauses = " OR ".join(["content LIKE ? OR evidence LIKE ?" for _ in words])
                params = []
                for w in words:
                    params.extend([f"%{w}%", f"%{w}%"])
                
                if channel:
                    query_sql = f"SELECT id as rowid, channel, category, insight as content, evidence, 0 as rank FROM learnings WHERE channel = ? AND ({like_clauses}) LIMIT ?"
                    params = [channel] + params + [limit]
                else:
                    query_sql = f"SELECT id as rowid, channel, category, insight as content, evidence, 0 as rank FROM learnings WHERE {like_clauses} LIMIT ?"
                    params = params + [limit]
                
                cur.execute(query_sql, params)
                rows = cur.fetchall()

            return [dict(r) for r in rows]

    def get_recent_learnings(self, channel: Optional[str] = None, limit: int = 15) -> List[Dict[str, Any]]:
        with self._get_connection() as con:
            cur = con.cursor()
            if channel:
                cur.execute("SELECT * FROM learnings WHERE channel = ? ORDER BY id DESC LIMIT ?", (channel, limit))
            else:
                cur.execute("SELECT * FROM learnings ORDER BY id DESC LIMIT ?", (limit,))
            return [dict(r) for r in cur.fetchall()]

    def get_active_experiments(self, channel: Optional[str] = None) -> List[Dict[str, Any]]:
        with self._get_connection() as con:
            cur = con.cursor()
            if channel:
                cur.execute("SELECT * FROM experiments WHERE channel = ? AND status = 'RUNNING' ORDER BY id DESC", (channel,))
            else:
                cur.execute("SELECT * FROM experiments WHERE status = 'RUNNING' ORDER BY id DESC")
                return [dict(r) for r in cur.fetchall()]

    def register_covered_theme(
        self,
        channel: str,
        core_topic: str,
        title_reference: str = "",
        status: str = "PUBLISHED",
        angle_covered: str = "",
        keywords: Optional[List[str]] = None,
        format: str = "long",
        video_id: str = "",
        views: int = 0,
        published_at: str = ""
    ) -> int:
        """
        Registers or updates a covered theme in persistent memory to prevent duplicate recommendations.
        Status: 'PUBLISHED', 'IN_PRODUCTION', 'BRIEFING_ISSUED', 'SCRAPPED'
        """
        ch = channel.lower()
        theme_slug = generate_topic_slug(f"{core_topic} {title_reference}")
        if not keywords:
            extracted = extract_core_tokens(f"{core_topic} {title_reference} {angle_covered}")
            keywords_list = sorted(list(extracted))
        else:
            keywords_list = keywords

        kw_json = json.dumps(keywords_list, ensure_ascii=False)

        with self._get_connection() as con:
            cur = con.cursor()
            cur.execute("""
                INSERT INTO covered_themes (
                    channel, theme_slug, core_topic, title_reference, status,
                    angle_covered, keywords, format, video_id, views_accumulated, published_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
                ON CONFLICT(channel, theme_slug) DO UPDATE SET
                    title_reference = excluded.title_reference,
                    status = excluded.status,
                    angle_covered = CASE WHEN excluded.angle_covered != '' THEN excluded.angle_covered ELSE covered_themes.angle_covered END,
                    keywords = excluded.keywords,
                    video_id = CASE WHEN excluded.video_id != '' THEN excluded.video_id ELSE covered_themes.video_id END,
                    views_accumulated = CASE WHEN excluded.views_accumulated > 0 THEN excluded.views_accumulated ELSE covered_themes.views_accumulated END,
                    published_at = CASE WHEN excluded.published_at != '' THEN excluded.published_at ELSE covered_themes.published_at END,
                    updated_at = CURRENT_TIMESTAMP
            """, (ch, theme_slug, core_topic, title_reference, status, angle_covered, kw_json, format, video_id, views, published_at))
            theme_id = cur.lastrowid

            # Sync to covered_themes_fts
            cur.execute("DELETE FROM covered_themes_fts WHERE channel = ? AND core_topic = ?", (ch, core_topic))
            cur.execute("""
                INSERT INTO covered_themes_fts (channel, core_topic, title_reference, keywords, angle_covered)
                VALUES (?, ?, ?, ?, ?)
            """, (ch, core_topic, title_reference, " ".join(keywords_list), angle_covered))

            con.commit()
            return theme_id

    def update_theme_status(self, channel: str, theme_slug: str, status: str) -> bool:
        """Updates the lifecycle status of a covered theme ('PUBLISHED', 'IN_PRODUCTION', 'SCRAPPED')."""
        with self._get_connection() as con:
            cur = con.cursor()
            cur.execute("""
                UPDATE covered_themes 
                SET status = ?, updated_at = CURRENT_TIMESTAMP 
                WHERE channel = ? AND theme_slug = ?
            """, (status, channel.lower(), theme_slug))
            con.commit()
            return cur.rowcount > 0

    def list_covered_themes(self, channel: Optional[str] = None, status: Optional[str] = None) -> List[Dict[str, Any]]:
        """Lists all covered themes, optionally filtered by channel and/or lifecycle status."""
        with self._get_connection() as con:
            cur = con.cursor()
            query = "SELECT * FROM covered_themes WHERE 1=1"
            params = []
            if channel:
                query += " AND channel = ?"
                params.append(channel.lower())
            if status:
                query += " AND status = ?"
                params.append(status.upper())
            query += " ORDER BY id DESC"
            cur.execute(query, params)
            rows = cur.fetchall()
            result = []
            for r in rows:
                item = dict(r)
                try:
                    item["keywords"] = json.loads(item["keywords"]) if item.get("keywords") else []
                except Exception:
                    item["keywords"] = []
                result.append(item)
            return result

    def record_video(self, channel: str, title: str, video_id: Optional[str] = None, format: str = "long", notes: str = "", views: int = 0) -> int:
        """Records an episode in production or published into the channel history and registers theme."""
        ch = channel.lower()
        with self._get_connection() as con:
            cur = con.cursor()
            cur.execute("""
                INSERT INTO video_history (channel, video_id, title, format, views, notes)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (ch, video_id or "PENDING", title, format, views, notes))
            vid_id = cur.lastrowid
            con.commit()

        # Automatically register into covered themes
        self.register_covered_theme(
            channel=ch,
            core_topic=title,
            title_reference=title,
            status="PUBLISHED" if video_id and video_id != "PENDING" else "IN_PRODUCTION",
            format=format,
            video_id=video_id or "",
            views=views,
            angle_covered=notes
        )
        return vid_id

    def get_channel_video_titles(self, channel: str) -> List[str]:
        """Returns all video titles previously planned or published for this channel."""
        with self._get_connection() as con:
            cur = con.cursor()
            cur.execute("SELECT title FROM video_history WHERE channel = ?", (channel.lower(),))
            return [r[0] for r in cur.fetchall()]

    def check_theme_coverage(
        self,
        channel: str,
        candidate_topic: str,
        candidate_thesis: str = "",
        threshold: float = 0.35
    ) -> Dict[str, Any]:
        """
        Deep quantitative deduplication check.
        Evaluates whether candidate_topic has already been covered or is currently in production.
        
        Checks 4 layers:
        1. Exact topic / slug match
        2. Substring & title containment
        3. Token Jaccard overlap & core technical keyword intersection
        4. SQLite FTS5 semantic match
        """
        ch = channel.lower()
        cand_norm = normalize_text(candidate_topic)
        cand_tokens = extract_core_tokens(f"{candidate_topic} {candidate_thesis}")
        cand_slug = generate_topic_slug(candidate_topic)

        # 1. Exact slug match in covered_themes
        with self._get_connection() as con:
            cur = con.cursor()
            cur.execute("""
                SELECT * FROM covered_themes 
                WHERE channel = ? AND theme_slug = ? AND status != 'SCRAPPED'
            """, (ch, cand_slug))
            row = cur.fetchone()
            if row:
                t = dict(row)
                return {
                    "is_covered": True,
                    "similarity_score": 1.0,
                    "match_type": "EXACT_SLUG",
                    "matched_topic": t["core_topic"],
                    "title_reference": t["title_reference"] or t["core_topic"],
                    "status": t["status"],
                    "video_id": t.get("video_id"),
                    "reason": f"Tema idêntico já registrado ({t['status']}): '{t['title_reference'] or t['core_topic']}'."
                }

        # 2. Check existing covered themes and video history
        covered_list = self.list_covered_themes(ch)
        video_titles = self.get_channel_video_titles(ch)

        # Merge video history titles into virtual check if not in covered_list
        known_titles = set(video_titles)
        for item in covered_list:
            if item.get("title_reference"):
                known_titles.add(item["title_reference"])

        best_match = None
        highest_score = 0.0
        match_type = ""

        for item in covered_list:
            if item.get("status") == "SCRAPPED":
                continue

            ref_title = item.get("title_reference") or item.get("core_topic") or ""
            ref_norm = normalize_text(ref_title)
            ref_tokens = extract_core_tokens(f"{ref_title} {' '.join(item.get('keywords', []))} {item.get('angle_covered', '')}")

            # Substring containment
            if cand_norm and ref_norm:
                if cand_norm in ref_norm or ref_norm in cand_norm:
                    return {
                        "is_covered": True,
                        "similarity_score": 0.95,
                        "match_type": "SUBSTRING_MATCH",
                        "matched_topic": item["core_topic"],
                        "title_reference": ref_title,
                        "status": item["status"],
                        "video_id": item.get("video_id"),
                        "reason": f"Pauta já contemplada no título existente: '{ref_title}' (Status: {item['status']})."
                    }

            # Keyword Jaccard & Overlap
            if cand_tokens and ref_tokens:
                intersection = cand_tokens.intersection(ref_tokens)
                union = cand_tokens.union(ref_tokens)
                jaccard = len(intersection) / len(union) if union else 0.0
                overlap = len(intersection) / min(len(cand_tokens), len(ref_tokens)) if min(len(cand_tokens), len(ref_tokens)) > 0 else 0.0

                # Strong signal: 2 or more core entities overlap with high relative ratio
                score = max(jaccard, overlap * 0.75)
                if len(intersection) >= 2 and (jaccard >= threshold or overlap >= 0.45):
                    if score > highest_score:
                        highest_score = score
                        best_match = item
                        match_type = "KEYWORD_OVERLAP"

        # Check raw video history titles if covered_list didn't catch it
        if not best_match:
            for vt in video_titles:
                vt_norm = normalize_text(vt)
                vt_tokens = extract_core_tokens(vt)
                if cand_norm in vt_norm or vt_norm in cand_norm:
                    return {
                        "is_covered": True,
                        "similarity_score": 0.90,
                        "match_type": "TITLE_SUBSTRING",
                        "matched_topic": vt,
                        "title_reference": vt,
                        "status": "PUBLISHED",
                        "video_id": "CATALOG_VIDEO",
                        "reason": f"Tema já postado no vídeo: '{vt}'."
                    }
                if cand_tokens and vt_tokens:
                    inter = cand_tokens.intersection(vt_tokens)
                    if len(inter) >= 2 and len(inter) / len(cand_tokens) >= 0.45:
                        score = len(inter) / len(cand_tokens)
                        if score > highest_score:
                            highest_score = score
                            best_match = {
                                "core_topic": vt,
                                "title_reference": vt,
                                "status": "PUBLISHED",
                                "video_id": "CATALOG_VIDEO"
                            }
                            match_type = "TOKEN_OVERLAP"

        # 4. FTS5 Virtual Table Check
        if not best_match and cand_tokens:
            fts_query = " OR ".join([f"{w}*" for w in cand_tokens])
            with self._get_connection() as con:
                cur = con.cursor()
                try:
                    cur.execute("""
                        SELECT core_topic, title_reference, status, rank 
                        FROM covered_themes_fts 
                        WHERE covered_themes_fts MATCH ? AND channel = ?
                        ORDER BY rank
                        LIMIT 1
                    """, (fts_query, ch))
                    fts_row = cur.fetchone()
                    if fts_row and abs(fts_row["rank"]) > 3.0: # High BM25 significance
                        return {
                            "is_covered": True,
                            "similarity_score": round(min(1.0, abs(fts_row["rank"]) / 10.0), 2),
                            "match_type": "FTS5_SEMANTIC",
                            "matched_topic": fts_row["core_topic"],
                            "title_reference": fts_row["title_reference"],
                            "status": fts_row["status"],
                            "video_id": "FTS5_MATCH",
                            "reason": f"Alta correlação semântica ({abs(fts_row['rank']):.1f}) com o tema já coberto: '{fts_row['title_reference'] or fts_row['core_topic']}'."
                        }
                except Exception:
                    pass

        if best_match and highest_score >= threshold:
            ref_t = best_match.get("title_reference") or best_match.get("core_topic")
            return {
                "is_covered": True,
                "similarity_score": round(highest_score, 2),
                "match_type": match_type,
                "matched_topic": best_match["core_topic"],
                "title_reference": ref_t,
                "status": best_match["status"],
                "video_id": best_match.get("video_id"),
                "reason": f"Pauta com sobreposição temática de {int(highest_score*100)}% com o vídeo já produzido: '{ref_t}' ({best_match['status']})."
            }

        return {
            "is_covered": False,
            "similarity_score": round(highest_score, 2),
            "match_type": "NONE",
            "matched_topic": None,
            "title_reference": None,
            "status": "UNCOVERED",
            "video_id": None,
            "reason": "Tema inédito no canal. Sinal verde para análise de potencial (P-Score)."
        }

    def is_topic_covered(self, channel: str, topic: str) -> bool:
        """Checks if a topic or similar title has already been covered to prevent duplicate fatigue."""
        res = self.check_theme_coverage(channel, topic)
        return res["is_covered"]

    def sync_all_baselines_to_covered_themes(self, channels_dir: Optional[Path] = None) -> Dict[str, int]:
        """
        Reads all baseline json files (O Outro Lado, HSL, Brecha) and automatically registers
        every published video into video_history and covered_themes.
        """
        c_dir = channels_dir or (Path(__file__).resolve().parent.parent.parent / "data" / "channels")
        files_map = {
            "o_outro_lado": "outro_lado_baseline.json",
            "hidden_systems_lab": "hsl_baseline.json",
            "brecha": "brecha_baseline.json"
        }

        total_synced = {}
        for ch_slug, fname in files_map.items():
            fpath = c_dir / fname
            if not fpath.exists():
                continue

            try:
                with open(fpath, "r", encoding="utf-8") as f:
                    data = json.load(f)
            except Exception:
                continue

            videos = data.get("videos", [])
            count = 0
            for v in videos:
                title = v.get("title")
                if not title:
                    continue
                vid_id = v.get("youtube_id") or v.get("id") or "UNKNOWN"
                fmt = v.get("format", "long")
                views = int(v.get("views") or 0)
                
                # Register in covered_themes
                self.register_covered_theme(
                    channel=ch_slug,
                    core_topic=title,
                    title_reference=title,
                    status="PUBLISHED",
                    format=fmt,
                    video_id=vid_id,
                    views=views
                )

                # Ensure in video_history
                with self._get_connection() as con:
                    cur = con.cursor()
                    cur.execute("SELECT id FROM video_history WHERE channel = ? AND title = ?", (ch_slug, title))
                    if not cur.fetchone():
                        cur.execute("""
                            INSERT INTO video_history (channel, video_id, title, format, views)
                            VALUES (?, ?, ?, ?, ?)
                        """, (ch_slug, vid_id, title, fmt, views))
                        con.commit()
                count += 1
            total_synced[ch_slug] = count

        # Export human-readable JSON files
        self.export_covered_themes_catalog(c_dir)
        return total_synced

    def export_covered_themes_catalog(self, output_dir: Optional[Path] = None) -> Dict[str, str]:
        """Exports human-readable JSON catalogs of covered themes for editors and squads."""
        out_dir = output_dir or (Path(__file__).resolve().parent.parent.parent / "data" / "channels")
        out_dir.mkdir(parents=True, exist_ok=True)

        channels = ["o_outro_lado", "hidden_systems_lab", "brecha"]
        exported = {}

        for ch in channels:
            themes = self.list_covered_themes(ch)
            published = [t for t in themes if t.get("status") == "PUBLISHED"]
            in_production = [t for t in themes if t.get("status") in ["IN_PRODUCTION", "BRIEFING_ISSUED"]]
            
            catalog = {
                "channel_slug": ch,
                "exported_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "total_covered_count": len(themes),
                "published_count": len(published),
                "in_production_count": len(in_production),
                "in_production_episodes": in_production,
                "published_catalog": published
            }

            fpath = out_dir / f"{ch}_covered_themes.json"
            with open(fpath, "w", encoding="utf-8") as f:
                json.dump(catalog, f, ensure_ascii=False, indent=2)
            exported[ch] = str(fpath)

        return exported

    def seed_baseline_learnings(self):
        """Pre-seeds memory with real baseline lessons from the 3 channels audit."""
        with self._get_connection() as con:
            cur = con.cursor()
            cur.execute("SELECT COUNT(*) FROM learnings")
            if cur.fetchone()[0] > 0:
                return  # already seeded

        # Seed initial high-impact insights
        seeds = [
            ("o_outro_lado", "topic", 
             "Temas de submundo/crime/risco urbano geram até 14x mais visualizações do que física abstrata.", 
             "Short de Santos (1.413 views) vs Isótopo Nuclear (0 views). Longo Pix (108 views) vs 60Hz (13 views).", 
             "Priorizar exclusivamente sistemas com dinheiro, risco físico ou fraude nos próximos 10 vídeos."),
            ("o_outro_lado", "algorithm", 
             "Publicar 1 vídeo longo por dia em canal de 5 inscritos satura a esteira e impede o algoritmo de testar a amostragem de 72h.", 
             "18 vídeos publicados em 3 semanas e 12 deles receberam menos de 20 views.", 
             "Reduzir frequência de longos para 2 por semana; vincular shorts com link de vídeo relacionado."),
            ("hidden_systems_lab", "algorithm", 
             "Uploads de vídeos idênticos são detectados como spam e congelam a distribuição do canal.", 
             "Airport Fuel e Skyscrapers postados 2 vezes cada em intervalo de 10 dias com views despencando.", 
             "Proibir re-upload idêntico. Sempre que ajustar vídeo, mudar título, thumb e primeiro minuto."),
            ("hidden_systems_lab", "shorts", 
             "Shorts com títulos apenas de hashtags (#Shorts #RocketEngine...) têm 0 views no feed.", 
             "3 shorts consecutivos do HSL tiveram 0 visualizações.", 
             "Todo short deve ter gancho semântico de choque nos primeiros 40 caracteres do título."),
            ("hidden_systems_lab", "packaging", 
             "Irreversibilidade física e paradoxos absolutos são a fórmula vencedora no mercado internacional.", 
             "Blast Furnace 'CAN NEVER BE SHUT DOWN' obteve 566 views e Jet Fuel 'WITHOUT STOPPING' obteve 680 views.", 
             "Todos os próximos títulos do HSL devem conter um limite físico ou impossibilidade aparente."),
            ("brecha", "algorithm", 
             "Inscritos inativos (audiência fantasma) sabotam a entrega para novos públicos na aba Browse.", 
             "1.120 inscritos gerando apenas 3 a 11 views nos vídeos longos (CTR < 0.5% na base).", 
             "Não depender de notificações de inscritos; forçar busca com termos específicos de golpes ativos."),
            ("brecha", "shorts", 
             "Shorts divididos em 'Parte 1', 'Parte 2' perdem até 75% da audiência entre partes.", 
             "Série do Pix Errado foi de 19 views (P3) para 5 views (P4).", 
             "Cada Short deve ser autocontido com um micro-estudo de caso completo de 45 segundos."),
            ("brecha", "packaging", 
             "Títulos em ALL CAPS excessivo transmitem sensacionalismo amador e afastam o público qualificado.", 
             "Vídeo do MED com 0 views tinha título 100% em maiúsculas.", 
             "Adotar padrão documental forense sóbrio: 'A Rota dos 180 Segundos' em vez de gritos no título.")
        ]

        for ch, cat, ins, ev, act in seeds:
            self.record_learning(ch, cat, ins, ev, act)
        
        # Seed initial open experiments
        self.record_experiment(
            "o_outro_lado", 
            "Se adicionarmos o link oficial de 'Vídeo Relacionado' nos Shorts de Santos e Apagão, o vídeo longo receberá tráfego contínuo do Shorts feed.",
            "Editar os 2 shorts mais vistos no YouTube Studio e apontar para os masters correspondentes.",
            "> 30 visualizações no vídeo longo vindas de Shorts Feed em 7 dias"
        )
        self.record_experiment(
            "hidden_systems_lab",
            "Se renomearmos os 3 Shorts de hashtags com ganchos de paradoxo em inglês, o YouTube começará a mostrá-los no feed de Shorts (> 500 views).",
            "Mudar títulos para 'The 500ms Disaster That Almost Destroyed the Pad' e medir impressões.",
            "Shown in Feed > 1.000 e Viewed Rate > 60% em 72h"
        )

# Global memory instance
memory = ChiefMemory()
chief_memory = memory
if __name__ == "__main__":
    memory.seed_baseline_learnings()
    print("Memory DB initialized and seeded at:", memory.db_path)
    res = memory.search("shorts santos")
    print(f"Search results for 'shorts santos': {len(res)}")
    for r in res:
        print(" -", r['content'])
