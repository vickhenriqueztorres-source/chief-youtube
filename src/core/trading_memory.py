# -*- coding: utf-8 -*-
"""
Hermes Chief Trading - SQLite FTS5 Isolated Persistent Memory Engine
Manages tactical memory, learned lessons, verified experiments, video track records,
and the 4-layer anti-duplication guardian for YouTube Trading Channels.
Completely decoupled from documentary channels memory (chief_memory.db).
"""

import sqlite3
import os
import json
import re
import unicodedata
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any, Optional, Set, Tuple

TRADING_STOPWORDS = {
    # Spanish
    "de", "la", "el", "en", "para", "con", "una", "un", "los", "las", "por", "que", "como", "mas",
    "este", "esta", "pero", "del", "al", "sus", "su", "o", "ser", "cuando", "muy", "nos", "yo",
    "tambien", "solo", "hasta", "esto", "entre", "era", "despues", "sin", "mismo", "tener", "quien",
    "te", "ese", "ellos", "estan", "tu", "tenia", "fueron", "esa", "ni", "mi", "donde", "cual",
    "mira", "aca", "este", "esta", "estos", "estas", "hacer", "puede", "dos", "veces", "segundos",
    "minutos", "horas", "dias", "primeros", "canal", "video", "aprende", "paso",
    # Portuguese
    "de", "a", "o", "que", "e", "do", "da", "em", "um", "para", "com", "nao", "uma", "os", "no", "se",
    # English
    "the", "of", "and", "to", "in", "is", "that", "for", "it", "as", "was", "with", "on", "at", "by",
    "this", "from", "they", "we", "say", "or", "an", "will", "my", "one", "all", "what", "so", "up"
}

def normalize_trading_text(text: str) -> str:
    """Removes accents, lowercase, removes special characters."""
    if not text:
        return ""
    nfkd = unicodedata.normalize('NFKD', text)
    no_accents = ''.join([c for c in nfkd if not unicodedata.combining(c)])
    cleaned = re.sub(r'[^a-zA-Z0-9\s]', ' ', no_accents.lower())
    return ' '.join(cleaned.split())

def stem_trading_token(word: str) -> str:
    """Suffix stemmer for Spanish and Portuguese trading terminology."""
    w = word.lower()
    if len(w) <= 3:
        return w
    # Spanish/Portuguese plurals and verb forms
    if w.endswith('ores') and len(w) > 5:
        return w[:-4] + 'or'
    if w.endswith('iones') and len(w) > 5:
        return w[:-5] + 'ion'
    if w.endswith('ados') or w.endswith('adas'):
        return w[:-2]
    if w.endswith('ado') or w.endswith('ada'):
        return w[:-1]
    if w.endswith('idos') or w.endswith('idas'):
        return w[:-2]
    if w.endswith('ido') or w.endswith('ida'):
        return w[:-1]
    if w.endswith('es') and len(w) > 4:
        return w[:-2]
    if w.endswith('s') and not w.endswith('ss') and len(w) > 3:
        return w[:-1]
    return w

TRADING_SYNONYM_EXPANSIONS = {
    "vela": ["candlestick", "patron", "cuerpo", "mecha", "barra"],
    "mecha": ["pavio", "sombra", "rechazo", "absorcion", "cola"],
    "cuerpo": ["volumen", "tamano", "fuerza", "impulso"],
    "soporte": ["suelo", "piso", "demanda", "rebote", "zona_baja"],
    "resistencia": ["techo", "oferta", "bloqueo", "rechazo", "zona_alta"],
    "deriv": ["broker", "dtrader", "sinteticos", "volatilidad"],
    "iq": ["iq_option", "broker", "binarias", "opciones"],
    "demo": ["practica", "prueba", "sin_riesgo", "virtual", "verificacion"],
    "martillo": ["hammer", "pinbar", "rechazo", "inversion"],
    "envolvente": ["engulfing", "cobertura", "fuerza", "quiebre"],
    "falso": ["trampa", "fakeout", "rompimiento_falso", "engano"],
    "tendencia": ["canal", "impulso", "retroceso", "continuacion"]
}

def extract_trading_core_tokens(text: str) -> Set[str]:
    """Extracts significant stemmed keywords and synonyms for trading deduplication."""
    norm = normalize_trading_text(text)
    words = norm.split()
    tokens = set()
    for w in words:
        if len(w) >= 3 and w not in TRADING_STOPWORDS:
            st = stem_trading_token(w)
            tokens.add(st)
            if st in TRADING_SYNONYM_EXPANSIONS:
                for syn in TRADING_SYNONYM_EXPANSIONS[st]:
                    tokens.add(stem_trading_token(syn))
    return tokens

def generate_trading_topic_slug(text: str) -> str:
    """Generates an alphanumeric slug from the most significant tokens."""
    tokens = sorted(list(extract_trading_core_tokens(text)))
    if tokens:
        return '_'.join(tokens[:5])
    norm = normalize_trading_text(text)
    return re.sub(r'[^a-z0-9]+', '_', norm).strip('_')[:50]

def get_trading_db_path() -> Path:
    """Returns local project trading memory path or fallback to user home directory."""
    local_dir = Path(__file__).resolve().parent.parent.parent / ".hermes" / "memory"
    if local_dir.exists():
        return local_dir / "chief_trading_memory.db"
    
    home_dir = Path.home() / ".hermes" / "memory"
    home_dir.mkdir(parents=True, exist_ok=True)
    return home_dir / "chief_trading_memory.db"

class ChiefTradingMemory:
    """Isolated SQLite FTS5 Memory Engine for YouTube Trading Channels."""

    def __init__(self, db_path: Optional[Path] = None):
        self.db_path = db_path or get_trading_db_path()
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
                published_at TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
            """)

            # Base table: covered_themes
            cur.execute("""
            CREATE TABLE IF NOT EXISTS covered_themes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                channel TEXT NOT NULL,
                theme_slug TEXT NOT NULL,
                core_topic TEXT NOT NULL,
                title_reference TEXT,
                status TEXT DEFAULT 'PUBLISHED',
                angle_covered TEXT,
                keywords TEXT,
                format TEXT DEFAULT 'long',
                video_id TEXT,
                views_accumulated INTEGER DEFAULT 0,
                published_at TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(channel, theme_slug)
            )
            """)

            # Virtual Table: FTS5 for memory search
            cur.execute("""
            CREATE VIRTUAL TABLE IF NOT EXISTS memory_fts USING fts5(
                channel,
                category,
                content,
                evidence,
                tokenize='porter unicode61'
            )
            """)

            # Virtual Table: FTS5 for covered_themes anti-duplication
            cur.execute("""
            CREATE VIRTUAL TABLE IF NOT EXISTS covered_themes_fts USING fts5(
                channel,
                core_topic,
                title_reference,
                keywords,
                angle_covered,
                tokenize='porter unicode61'
            )
            """)

            con.commit()

    def record_learning(self, channel: str, category: str, insight: str, evidence: str = "", action_taken: str = "") -> int:
        ch = channel.lower()
        with self._get_connection() as con:
            cur = con.cursor()
            cur.execute("""
                INSERT INTO learnings (channel, category, insight, evidence, action_taken)
                VALUES (?, ?, ?, ?, ?)
            """, (ch, category, insight, evidence, action_taken))
            learning_id = cur.lastrowid
            
            cur.execute("""
                INSERT INTO memory_fts (channel, category, content, evidence)
                VALUES (?, ?, ?, ?)
            """, (ch, category, insight, f"{evidence} {action_taken}".strip()))
            con.commit()
            return learning_id

    def record_experiment(self, channel: str, hypothesis: str, test_design: str, metric_target: str) -> int:
        ch = channel.lower()
        with self._get_connection() as con:
            cur = con.cursor()
            cur.execute("""
                INSERT INTO experiments (channel, hypothesis, test_design, metric_target, status)
                VALUES (?, ?, ?, ?, 'RUNNING')
            """, (ch, hypothesis, test_design, metric_target))
            exp_id = cur.lastrowid
            con.commit()
            return exp_id

    def search_memory(self, query: str, channel: Optional[str] = None, limit: int = 10) -> List[Dict[str, Any]]:
        clean_q = normalize_trading_text(query)
        words = clean_q.split()
        if not words:
            return []

        fts_term = " OR ".join(words)
        with self._get_connection() as con:
            cur = con.cursor()
            rows = []
            try:
                if channel:
                    cur.execute("""
                        SELECT rowid, channel, category, content, evidence, rank
                        FROM memory_fts
                        WHERE memory_fts MATCH ? AND channel = ?
                        ORDER BY rank LIMIT ?
                    """, (fts_term, channel.lower(), limit))
                else:
                    cur.execute("""
                        SELECT rowid, channel, category, content, evidence, rank
                        FROM memory_fts
                        WHERE memory_fts MATCH ?
                        ORDER BY rank LIMIT ?
                    """, (fts_term, limit))
                rows = cur.fetchall()
            except Exception:
                rows = []

            return [dict(r) for r in rows]

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
        ch = channel.lower()
        theme_slug = generate_trading_topic_slug(f"{core_topic} {title_reference}")
        if not keywords:
            extracted = extract_trading_core_tokens(f"{core_topic} {title_reference} {angle_covered}")
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

            cur.execute("DELETE FROM covered_themes_fts WHERE channel = ? AND core_topic = ?", (ch, core_topic))
            cur.execute("""
                INSERT INTO covered_themes_fts (channel, core_topic, title_reference, keywords, angle_covered)
                VALUES (?, ?, ?, ?, ?)
            """, (ch, core_topic, title_reference, " ".join(keywords_list), angle_covered))

            con.commit()
            return theme_id

    def check_topic_coverage(self, channel: str, proposed_topic: str) -> Dict[str, Any]:
        """
        4-Layer Anti-Duplication Protocol for Trading Channels:
        1. Exact Slug Match
        2. Substring & Exact Title Containment
        3. Keyword Jaccard Overlap (Threshold: >= 40%)
        4. FTS5 Semantic Search
        """
        ch = channel.lower()
        topic_norm = normalize_trading_text(proposed_topic)
        topic_slug = generate_trading_topic_slug(proposed_topic)
        topic_tokens = extract_trading_core_tokens(proposed_topic)

        # Layer 1: Exact Slug
        with self._get_connection() as con:
            cur = con.cursor()
            cur.execute("SELECT * FROM covered_themes WHERE channel = ? AND theme_slug = ?", (ch, topic_slug))
            row = cur.fetchone()
            if row:
                r = dict(row)
                return {
                    "is_covered": True,
                    "reason": "EXACT_SLUG_MATCH",
                    "similarity_score": 1.0,
                    "status": r["status"],
                    "matched_theme": r["core_topic"],
                    "title_reference": r["title_reference"],
                    "video_id": r["video_id"],
                    "verdict": "REJEITADO - Tema já abordado no canal de trading."
                }

            # Layer 2: Title Substring Containment
            cur.execute("SELECT * FROM covered_themes WHERE channel = ?", (ch,))
            all_themes = cur.fetchall()
            for t in all_themes:
                t_dict = dict(t)
                existing_title = normalize_trading_text(t_dict["title_reference"] or t_dict["core_topic"])
                if (len(topic_norm) > 10 and topic_norm in existing_title) or (len(existing_title) > 10 and existing_title in topic_norm):
                    return {
                        "is_covered": True,
                        "reason": "TITLE_SUBSTRING_CONTAINMENT",
                        "similarity_score": 0.95,
                        "status": t_dict["status"],
                        "matched_theme": t_dict["core_topic"],
                        "title_reference": t_dict["title_reference"],
                        "video_id": t_dict["video_id"],
                        "verdict": f"REJEITADO - Substring idêntica ao vídeo já existente: '{t_dict['title_reference']}'."
                    }

            # Layer 3: Keyword Jaccard Overlap
            if topic_tokens:
                for t in all_themes:
                    t_dict = dict(t)
                    try:
                        kws = set(json.loads(t_dict["keywords"])) if t_dict.get("keywords") else set()
                    except Exception:
                        kws = set()
                    
                    if not kws:
                        kws = extract_trading_core_tokens(f"{t_dict['core_topic']} {t_dict.get('title_reference', '')}")
                    
                    if kws:
                        intersection = topic_tokens.intersection(kws)
                        union = topic_tokens.union(kws)
                        jaccard = len(intersection) / len(union) if union else 0.0
                        if jaccard >= 0.40:
                            return {
                                "is_covered": True,
                                "reason": "HIGH_KEYWORD_OVERLAP",
                                "similarity_score": round(jaccard, 3),
                                "status": t_dict["status"],
                                "matched_theme": t_dict["core_topic"],
                                "title_reference": t_dict["title_reference"],
                                "overlapping_entities": list(intersection),
                                "verdict": f"REJEITADO - Sobreposição técnica de {round(jaccard*100, 1)}% com '{t_dict['core_topic']}' ({list(intersection)})."
                            }

            # Layer 4: FTS5 Semantic Search
            if topic_tokens:
                fts_query = " OR ".join(list(topic_tokens)[:5])
                try:
                    cur.execute("""
                        SELECT core_topic, title_reference, rank
                        FROM covered_themes_fts
                        WHERE covered_themes_fts MATCH ? AND channel = ?
                        ORDER BY rank LIMIT 1
                    """, (fts_query, ch))
                    fts_match = cur.fetchone()
                    if fts_match and fts_match["rank"] < -5.0:
                        return {
                            "is_covered": True,
                            "reason": "SEMANTIC_FTS5_BM25",
                            "similarity_score": round(abs(fts_match["rank"]) / 10.0, 2),
                            "status": "POSSIBLE_OVERLAP",
                            "matched_theme": fts_match["core_topic"],
                            "title_reference": fts_match["title_reference"],
                            "verdict": f"ALERTA DE SOBREPOSIÇÃO - BM25 score relevante com '{fts_match['core_topic']}'. Exige novo ângulo."
                        }
                except Exception:
                    pass

        return {
            "is_covered": False,
            "reason": "UNCOVERED",
            "similarity_score": 0.0,
            "verdict": "SINAL VERDE - Tema 100% virgem no canal de trading."
        }

    def list_covered_themes(self, channel: Optional[str] = None, status: Optional[str] = None) -> List[Dict[str, Any]]:
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
        ch = channel.lower()
        with self._get_connection() as con:
            cur = con.cursor()
            cur.execute("""
                INSERT INTO video_history (channel, video_id, title, format, views, notes)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (ch, video_id or "PENDING", title, format, views, notes))
            vid_id = cur.lastrowid
            con.commit()

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

    def bootstrap_trading_memory(self):
        """Pre-populates baseline memory for El Profe de Velas."""
        ch = "el_profe_de_velas"
        
        # Initial learnings based on real channel data and archetype bible
        initial_learnings = [
            ("retention", "Short outlier WGz-rzMcN7g ('El color de la vela te engaña: mira esto primero') atingiu 152 views (38x inscritos). Hipótese validada: O público iniciante é atraído por quebra de regra visual simples (cor da vela não determina direção).", "Views: 152 | AVD: 78.4% | CTR: 8.5%", "Priorizar pautas de desconstrução de mitos de velas no Ato 1."),
            ("packaging", "Hashtags genéricas (#pocketoption, #opcionesbinarias) em títulos de Shorts deprimem CTR qualificado e atraem tráfego bot/descartável. O título textual claro supera hashtags vazias.", "Short com hashtags vazias teve apenas 11 views vs 152 views no short com título de impacto.", "Eliminar hashtags de corretoras do título visível; usar frases curtas com 'Mira acá' ou 'Sin adivinar'."),
            ("pedagogy", "O arquétipo do Professor-Verificador funciona porque a dor dominante do mercado latino de trading é a desconfiança em gurus jovens com ostentação. A autoridade vem de tela aberta em conta demo e erro visível.", "Canal cresce com base em verificação e clareza, não com pose de riqueza.", "Preservar 100% a identidade em conta demo, nunca mostrar saldo ou prometer ganhos."),
            ("character_lock", "Avatar Eric (ElevenLabs cjVigY5qzO86Huf0OWal) deve operar estritamente em PiP 20-25% no canto inferior apontando para o gráfico. Tela cheia só no hook e CTA.", "Ficha forense canônica v1.0.", "Manter rigorosamente o look bomber azul / polo preta e ritmo de 140 wpm.")
        ]
        
        for cat, ins, ev, act in initial_learnings:
            self.record_learning(ch, cat, ins, ev, act)

        # Existing published videos from YouTube
        existing_longs = [
            ("1rWRfv5_gdg", "Cómo Interpretar una Vela Paso a Paso", 32, "Leitura visual básica de corpo e mecha"),
            ("IfYlcD1DN0o", "Una vela sola te engaña: aprende a leer la secuencia", 11, "Sequência de contexto vs vela isolada"),
            ("uiGMJ8i2J1s", "Una vela grande no prueba nada: este error engaña a los principiantes", 9, "Armadilha de tamanho de vela e exaustão")
        ]
        for vid, title, views, notes in existing_longs:
            self.record_video(ch, title, video_id=vid, format="long", notes=notes, views=views)

        existing_shorts = [
            ("WGz-rzMcN7g", "El color de la vela te engaña: mira esto primero", 152, "Outlier viral do canal sobre cor vs contexto"),
            ("I0f_Tl4qvbM", "Estás leyendo MAL las velas: usa estas 3 zonas", 68, "3 zonas de leitura de pavio e corpo"),
            ("qBV1TFbuk5M", "Una vela verde grande NO demuestra que seguirá subiendo", 52, "Falso rompimento em vela grande"),
            ("HL_iKe6KMfE", "La mecha NO cuenta toda la historia", 32, "Leitura forense de mecha e rejeição"),
            ("lK_yKfot65Q", "Tres velas verdes NO garantizan la cuarta", 19, "Quebra do vício de martingale"),
            ("mEz4Lzqw1G4", "Aprende a esperar confirmación antes del clic", 11, "Checklist antes da entrada")
        ]
        for vid, title, views, notes in existing_shorts:
            self.record_video(ch, title, video_id=vid, format="short", notes=notes, views=views)

# Singleton instances
trading_memory = ChiefTradingMemory()
# Auto-bootstrap initial memory if fresh
if not trading_memory.list_covered_themes("el_profe_de_velas"):
    trading_memory.bootstrap_trading_memory()
