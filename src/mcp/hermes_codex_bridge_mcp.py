# -*- coding: utf-8 -*-
"""
Hermes <-> Codex Bridge — Model Context Protocol (MCP) Server
Allows Hermes to dispatch Themes and Scripts directly to Codex, and allows Codex
to inspect, retrieve, and process pending content from Hermes.

Includes dedicated native pipeline integration for "El Profe de Velas" (D:/agent- el prof del las velas).

Stdio JSON-RPC MCP Server compatible with Hermes, Codex, and Claude/Antigravity.
"""

import sys
import os
import json
import sqlite3
import re
import uuid
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any, List

# Safe UTF-8 output on Windows consoles
try:
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    if hasattr(sys.stderr, 'reconfigure'):
        sys.stderr.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass

# Save pure JSON-RPC stdout channel and redirect sys.stdout to sys.stderr
_rpc_stdout = sys.stdout
sys.stdout = sys.stderr

# Base directories
INBOX_DIR = Path("D:/CHIEF YOUTUBE/codex_inbox")
THEMES_DIR = INBOX_DIR / "themes"
SCRIPTS_DIR = INBOX_DIR / "scripts"
DB_PATH = INBOX_DIR / "inbox.sqlite"
CODEX_CONFIG_PATH = Path(os.path.expanduser("~/.codex/config.toml"))
HERMES_DIR = Path(os.path.expanduser("~/AppData/Local/hermes"))

# Dedicated "El Profe de Velas" directory
PROFE_DIR = Path("D:/agent- el prof del las velas")
PROFE_THEMES_DIR = PROFE_DIR / "themes"

# Ensure inbox directories exist
try:
    INBOX_DIR.mkdir(parents=True, exist_ok=True)
    THEMES_DIR.mkdir(parents=True, exist_ok=True)
    SCRIPTS_DIR.mkdir(parents=True, exist_ok=True)
    if PROFE_DIR.exists():
        PROFE_THEMES_DIR.mkdir(parents=True, exist_ok=True)
except Exception:
    pass

# Known video production / channel mapping
PROJECT_ALIASES: Dict[str, str] = {
    "voicecut": "D:/edition pro/voicecut",
    "edition pro": "D:/edition pro/voicecut",
    "canal brecha": "D:/agents 3.0 brecha - antigravity/canalbrecha",
    "brecha": "D:/agents 3.0 brecha - antigravity/canalbrecha",
    "hsl": "D:/HSL STUDIO AGENTS",
    "hsl studio": "D:/HSL STUDIO AGENTS",
    "o outro lado": "D:/orquestrador - o outro lado",
    "cazador": "D:/EDITOR DO CAZADOR",
    "el cazador de wins": "D:/EDITOR DO CAZADOR",
    "trading labs": "D:/Trading Labs",
    "chief youtube": "D:/CHIEF YOUTUBE",
    "el profe de velas": "D:/agent- el prof del las velas",
    "el prof del las velas": "D:/agent- el prof del las velas",
    "linha de fogo": "D:/LINHA DE FOGO EDITS",
    "linha_de_fogo": "D:/LINHA DE FOGO EDITS",
    "linhadefogo": "D:/LINHA DE FOGO EDITS",
    "profe de velas": "D:/agent- el prof del las velas",
    "profe": "D:/agent- el prof del las velas",
}

def init_db() -> sqlite3.Connection:
    conn = sqlite3.connect(str(DB_PATH))
    conn.execute("PRAGMA journal_mode=WAL;")
    conn.execute("""
        CREATE TABLE IF NOT EXISTS inbox_items (
            id TEXT PRIMARY KEY,
            type TEXT NOT NULL,
            title TEXT NOT NULL,
            channel TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'pending',
            big_idea TEXT,
            hook TEXT,
            target_audience TEXT,
            cta TEXT,
            voice_id TEXT,
            notes TEXT,
            file_path TEXT NOT NULL,
            target_project_path TEXT,
            codex_job_id TEXT,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL,
            raw_payload TEXT
        );
    """)
    conn.commit()
    return conn

def sanitize_filename(name: str) -> str:
    cleaned = re.sub(r'[\\/*?:"<>|]', '', name)
    cleaned = re.sub(r'\s+', '-', cleaned.strip().lower())
    return cleaned[:80] or "item"

def resolve_target_project(channel_or_path: Optional[str]) -> Optional[str]:
    if not channel_or_path:
        return None
    val_clean = channel_or_path.strip().lower()
    for alias, p in PROJECT_ALIASES.items():
        if alias in val_clean:
            return p
    if os.path.exists(channel_or_path):
        return str(Path(channel_or_path).resolve())
    return None

def generate_id(prefix: str) -> str:
    date_str = datetime.now().strftime("%Y%m%d")
    short_hash = uuid.uuid4().hex[:6].upper()
    return f"{prefix}-{date_str}-{short_hash}"

# ==============================================================================
# GENERAL TOOL IMPLEMENTATIONS
# ==============================================================================

def send_theme_to_codex(
    title: str,
    channel: str,
    big_idea: Optional[str] = None,
    hook: Optional[str] = None,
    target_audience: Optional[str] = None,
    angles_and_research: Optional[str] = None,
    notes: Optional[str] = None,
    target_project_path: Optional[str] = None,
    auto_trigger_codex: bool = False
) -> Dict[str, Any]:
    """Salva um tema/ideia validada no Inbox do Codex e opcionalmente dispara a execução."""
    item_id = generate_id("THM")
    now_iso = datetime.now().isoformat()
    resolved_proj = resolve_target_project(target_project_path) or resolve_target_project(channel)

    filename = f"{item_id}_{sanitize_filename(title)}.md"
    file_path = THEMES_DIR / filename

    content_lines = [
        "---",
        f"id: {item_id}",
        "type: theme",
        f"title: \"{title}\"",
        f"channel: \"{channel}\"",
        "status: pending",
        f"created_at: {now_iso}",
        f"target_project: \"{resolved_proj or ''}\"",
        "---",
        "",
        f"# 🎯 TEMA: {title}",
        "",
        f"**Canal:** {channel}  ",
        f"**Data:** {now_iso}  ",
        f"**ID:** `{item_id}`  ",
        f"**Projeto Destino:** `{resolved_proj or 'Geral / Não especificado'}`  ",
        "",
        "---",
        "",
        "## 💡 Big Idea (A Regra do Um)",
        big_idea or "*Não especificada*",
        "",
        "## 🪝 Hook (Primeiros 3-5 Segundos)",
        hook or "*Não especificado*",
        "",
        "## 👤 Público-Alvo / Avatar (Bob)",
        target_audience or "*Público padrão do canal*",
        "",
        "## 🔍 Ângulos, Narrativa e Pesquisa",
        angles_and_research or "*Sem notas adicionais de pesquisa*",
        "",
        "## ⚙️ Diretrizes para o Codex",
        notes or "Transformar este tema em estrutura de código, pipeline ou roteiro detalhado.",
        ""
    ]

    md_content = "\n".join(content_lines)
    file_path.write_text(md_content, encoding="utf-8")

    # If target project specified, create a mirror copy in that project's inbox/inputs
    mirrored_path = None
    if resolved_proj and os.path.exists(resolved_proj):
        target_dir = Path(resolved_proj) / "inputs" / "themes"
        try:
            target_dir.mkdir(parents=True, exist_ok=True)
            mirror_file = target_dir / filename
            mirror_file.write_text(md_content, encoding="utf-8")
            mirrored_path = str(mirror_file)
        except Exception:
            pass

    codex_job = None
    if auto_trigger_codex:
        prompt = f"Novo tema recebido do Hermes: '{title}' ({item_id}) para o canal '{channel}'. Verifique o arquivo {file_path} e estruture os próximos passos."
        if resolved_proj == PROJECT_ALIASES["linha de fogo"]:
            prompt += " Leia docs/doc-studio/HERMES-MCP-TEMAS.md. Trate o tema como proposta: verifique fontes e alegações, siga os seis atos (0-5) e preserve as revisões humanas."
        trigger_res = trigger_codex_task(prompt=prompt, project_path=resolved_proj)
        codex_job = trigger_res.get("codex_job_id")

    # Save to SQLite
    raw_payload = json.dumps({
        "title": title, "channel": channel, "big_idea": big_idea, "hook": hook,
        "target_audience": target_audience, "angles_and_research": angles_and_research,
        "notes": notes, "target_project_path": resolved_proj, "auto_trigger_codex": auto_trigger_codex
    }, ensure_ascii=False)

    conn = init_db()
    with conn:
        conn.execute("""
            INSERT INTO inbox_items (
                id, type, title, channel, status, big_idea, hook, target_audience,
                notes, file_path, target_project_path, codex_job_id, created_at, updated_at, raw_payload
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            item_id, "theme", title, channel, "pending", big_idea, hook,
            target_audience, notes, str(file_path), resolved_proj, codex_job,
            now_iso, now_iso, raw_payload
        ))

    return {
        "status": "success",
        "message": f"Tema '{title}' enviado com sucesso para o Codex!",
        "item_id": item_id,
        "file_path": str(file_path),
        "mirrored_project_path": mirrored_path,
        "target_project": resolved_proj,
        "codex_triggered": auto_trigger_codex,
        "codex_job_id": codex_job
    }

def send_script_to_codex(
    title: str,
    channel: str,
    script_content: str,
    hook: Optional[str] = None,
    cta: Optional[str] = None,
    voice_id: Optional[str] = None,
    notes: Optional[str] = None,
    target_project_path: Optional[str] = None,
    auto_trigger_codex: bool = False
) -> Dict[str, Any]:
    """Salva um roteiro completo no Inbox do Codex e opcionalmente dispara a execução."""
    item_id = generate_id("SCR")
    now_iso = datetime.now().isoformat()
    resolved_proj = resolve_target_project(target_project_path) or resolve_target_project(channel)

    filename = f"{item_id}_{sanitize_filename(title)}.md"
    file_path = SCRIPTS_DIR / filename

    content_lines = [
        "---",
        f"id: {item_id}",
        "type: script",
        f"title: \"{title}\"",
        f"channel: \"{channel}\"",
        f"voice_id: \"{voice_id or ''}\"",
        "status: pending",
        f"created_at: {now_iso}",
        f"target_project: \"{resolved_proj or ''}\"",
        "---",
        "",
        f"# 📜 ROTEIRO: {title}",
        "",
        f"**Canal:** {channel}  ",
        f"**ID:** `{item_id}`  ",
        f"**Data:** {now_iso}  ",
        f"**Voz Recomendada:** `{voice_id or 'Padrão do canal'}`  ",
        f"**Projeto Destino:** `{resolved_proj or 'Geral / Não especificado'}`  ",
        "",
        "---",
        "",
        "## 🪝 Hook de Abertura",
        hook or "*Ver início do roteiro abaixo*",
        "",
        "## 🎬 Conteúdo Integral do Roteiro",
        "",
        script_content,
        "",
        "---",
        "",
        "## 🎯 Call to Action (CTA)",
        cta or "*Ver final do roteiro*",
        "",
        "## ⚙️ Instruções de Produção para o Codex",
        notes or "Processar narração com VoiceCut / TTS ElevenLabs, organizar cortes de vídeo e gerar assets.",
        ""
    ]

    md_content = "\n".join(content_lines)
    file_path.write_text(md_content, encoding="utf-8")

    # If target project specified, create a mirror copy in that project's inbox/inputs
    mirrored_path = None
    if resolved_proj and os.path.exists(resolved_proj):
        target_dir = Path(resolved_proj) / "inputs" / "scripts"
        try:
            target_dir.mkdir(parents=True, exist_ok=True)
            mirror_file = target_dir / filename
            mirror_file.write_text(md_content, encoding="utf-8")
            mirrored_path = str(mirror_file)
        except Exception:
            pass

    codex_job = None
    if auto_trigger_codex:
        prompt = f"Novo roteiro recebido do Hermes: '{title}' ({item_id}) para o canal '{channel}'. Verifique o arquivo {file_path} e inicie a produção."
        if resolved_proj == PROJECT_ALIASES["linha de fogo"]:
            prompt = f"Roteiro recebido do Hermes: '{title}' ({item_id}) para o canal '{channel}'. Leia {file_path} e docs/doc-studio/HERMES-MCP-TEMAS.md. Valide fontes, voz e contrato de seis atos (0-5); siga os gates humanos antes de qualquer produção."
        trigger_res = trigger_codex_task(prompt=prompt, project_path=resolved_proj)
        codex_job = trigger_res.get("codex_job_id")

    # Save to SQLite
    raw_payload = json.dumps({
        "title": title, "channel": channel, "hook": hook, "cta": cta,
        "voice_id": voice_id, "notes": notes, "target_project_path": resolved_proj,
        "auto_trigger_codex": auto_trigger_codex
    }, ensure_ascii=False)

    conn = init_db()
    with conn:
        conn.execute("""
            INSERT INTO inbox_items (
                id, type, title, channel, status, hook, cta, voice_id,
                notes, file_path, target_project_path, codex_job_id, created_at, updated_at, raw_payload
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            item_id, "script", title, channel, "pending", hook, cta, voice_id,
            notes, str(file_path), resolved_proj, codex_job,
            now_iso, now_iso, raw_payload
        ))

    return {
        "status": "success",
        "message": f"Roteiro '{title}' enviado com sucesso para o Codex!",
        "item_id": item_id,
        "file_path": str(file_path),
        "mirrored_project_path": mirrored_path,
        "target_project": resolved_proj,
        "codex_triggered": auto_trigger_codex,
        "codex_job_id": codex_job
    }

def list_codex_inbox(
    status: str = "all",
    item_type: str = "all",
    channel: Optional[str] = None,
    limit: int = 20
) -> Dict[str, Any]:
    """Lista itens no Inbox do Codex enviados pelo Hermes."""
    conn = init_db()
    query = "SELECT id, type, title, channel, status, file_path, target_project_path, created_at, updated_at FROM inbox_items WHERE 1=1"
    params: List[Any] = []

    if status != "all":
        query += " AND status = ?"
        params.append(status)
    if item_type != "all":
        query += " AND type = ?"
        params.append(item_type)
    if channel:
        query += " AND lower(channel) LIKE ?"
        params.append(f"%{channel.lower().strip()}%")

    query += " ORDER BY created_at DESC LIMIT ?"
    params.append(limit)

    cursor = conn.cursor()
    cursor.execute(query, params)
    rows = cursor.fetchall()

    items = []
    for r in rows:
        items.append({
            "id": r[0],
            "type": r[1],
            "title": r[2],
            "channel": r[3],
            "status": r[4],
            "file_path": r[5],
            "target_project_path": r[6],
            "created_at": r[7],
            "updated_at": r[8]
        })

    return {
        "total": len(items),
        "filters": {"status": status, "type": item_type, "channel": channel},
        "items": items
    }

def get_codex_inbox_item(item_id: str) -> Dict[str, Any]:
    """Recupera detalhes e conteúdo completo de um tema ou roteiro no Inbox."""
    conn = init_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id, type, title, channel, status, big_idea, hook, target_audience, cta, voice_id, notes, file_path, target_project_path, codex_job_id, created_at, updated_at FROM inbox_items WHERE id = ?", (item_id,))
    row = cursor.fetchone()

    if not row:
        return {"status": "error", "message": f"Item '{item_id}' não encontrado."}

    file_p = Path(row[11])
    content = ""
    if file_p.exists():
        try:
            content = file_p.read_text(encoding="utf-8")
        except Exception as e:
            content = f"Erro ao ler arquivo: {e}"

    return {
        "id": row[0],
        "type": row[1],
        "title": row[2],
        "channel": row[3],
        "status": row[4],
        "big_idea": row[5],
        "hook": row[6],
        "target_audience": row[7],
        "cta": row[8],
        "voice_id": row[9],
        "notes": row[10],
        "file_path": row[11],
        "target_project_path": row[12],
        "codex_job_id": row[13],
        "created_at": row[14],
        "updated_at": row[15],
        "full_markdown_content": content
    }

def update_inbox_item_status(
    item_id: str,
    status: str,
    notes: Optional[str] = None
) -> Dict[str, Any]:
    """Atualiza o status de um item (ex: 'in_progress', 'completed', 'archived')."""
    valid_statuses = ["pending", "in_progress", "completed", "archived"]
    if status not in valid_statuses:
        return {"status": "error", "message": f"Status inválido. Escolha entre: {valid_statuses}"}

    now_iso = datetime.now().isoformat()
    conn = init_db()
    with conn:
        if notes:
            conn.execute(
                "UPDATE inbox_items SET status = ?, notes = notes || ? || ?, updated_at = ? WHERE id = ?",
                (status, "\n[Update] ", notes, now_iso, item_id)
            )
        else:
            conn.execute(
                "UPDATE inbox_items SET status = ?, updated_at = ? WHERE id = ?",
                (status, now_iso, item_id)
            )

    return {
        "status": "success",
        "item_id": item_id,
        "new_status": status,
        "updated_at": now_iso
    }

def list_codex_projects() -> Dict[str, Any]:
    """Descobre e lista os projetos ativos do Codex e pipelines de produção disponíveis."""
    projects: List[Dict[str, Any]] = []

    # 1. Known pipeline aliases
    for alias, p in PROJECT_ALIASES.items():
        exists = os.path.exists(p)
        projects.append({
            "name": alias.title(),
            "path": p,
            "exists": exists,
            "type": "known_pipeline"
        })

    # 2. Extract trusted projects from ~/.codex/config.toml
    if CODEX_CONFIG_PATH.exists():
        try:
            txt = CODEX_CONFIG_PATH.read_text(encoding="utf-8")
            matches = re.findall(r'\[projects\.["\'](.*?)["\']\]', txt)
            for m in matches:
                normalized = m.replace("\\\\?\\", "").replace("\\\\", "/")
                if not any(p["path"].lower() == normalized.lower() for p in projects):
                    projects.append({
                        "name": Path(normalized).name or normalized,
                        "path": normalized,
                        "exists": os.path.exists(normalized),
                        "type": "codex_trusted_project"
                    })
        except Exception as e:
            sys.stderr.write(f"Error parsing codex config.toml: {e}\n")

    return {
        "total": len(projects),
        "projects": projects
    }

def trigger_codex_task(
    prompt: str,
    project_path: Optional[str] = None,
    model: Optional[str] = None
) -> Dict[str, Any]:
    """Dispara uma tarefa no Codex CLI usando codex exec de forma não-bloqueante."""
    # Resolve nomes de canal e caminhos legados antes de escolher o checkout.
    project_path = resolve_target_project(project_path) or project_path
    codex_cmd = Path("C:/Users/brend/AppData/Roaming/npm/codex.cmd")
    if not codex_cmd.exists():
        codex_cmd = Path("codex")

    cmd = [str(codex_cmd), "exec"]
    if model:
        cmd.extend(["-m", model])
    if project_path and os.path.exists(project_path):
        cmd.extend(["-C", str(Path(project_path).resolve())])

    # Run in background via subprocess
    job_id = f"job-{uuid.uuid4().hex[:8]}"
    log_file = INBOX_DIR / f"{job_id}.log"

    cmd.append(prompt)

    try:
        with open(log_file, "w", encoding="utf-8") as out:
            proc = subprocess.Popen(
                cmd,
                stdout=out,
                stderr=subprocess.STDOUT,
                cwd=project_path if (project_path and os.path.exists(project_path)) else None,
                creationflags=subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0
            )

        return {
            "status": "triggered",
            "codex_job_id": job_id,
            "pid": proc.pid,
            "log_file": str(log_file),
            "command": " ".join(cmd[:4]) + " ..."
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Falha ao disparar o Codex: {str(e)}"
        }

def read_hermes_latest_sessions(limit: int = 5) -> Dict[str, Any]:
    """Lê as sessões e histórico recente do Hermes para contexto cruzado."""
    state_db = HERMES_DIR / "state.db"
    sessions = []

    if state_db.exists():
        try:
            conn = sqlite3.connect(f"file:{state_db}?mode=ro", uri=True)
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, title, created_at, updated_at 
                FROM sessions 
                ORDER BY updated_at DESC LIMIT ?
            """, (limit,))
            for r in cursor.fetchall():
                sessions.append({
                    "session_id": r[0],
                    "title": r[1],
                    "created_at": r[2],
                    "updated_at": r[3]
                })
            conn.close()
        except Exception as e:
            sys.stderr.write(f"Error reading hermes state.db: {e}\n")

    return {
        "total": len(sessions),
        "sessions": sessions
    }

# ==============================================================================
# SPECIALIZED: EL PROFE DE VELAS TOOL IMPLEMENTATIONS
# ==============================================================================

def _get_next_profe_episode_number() -> int:
    """Detecta o próximo número de episódio disponível em D:/agent- el prof del las velas."""
    max_num = 0
    if PROFE_DIR.exists():
        for d in PROFE_DIR.iterdir():
            if d.is_dir() and d.name.startswith("episode-"):
                match = re.search(r'episode-(\d+)', d.name)
                if match:
                    num = int(match.group(1))
                    if num > max_num:
                        max_num = num
    return max_num + 1

def list_profe_de_velas_episodes() -> Dict[str, Any]:
    """Lista todos os episódios existentes de 'El Profe de Velas' com seus status de roteiro, áudio e vídeo."""
    if not PROFE_DIR.exists():
        return {"status": "error", "message": f"Diretório {PROFE_DIR} não encontrado."}

    episodes = []
    for d in sorted(PROFE_DIR.iterdir()):
        if d.is_dir() and d.name.startswith("episode-"):
            has_script_json = (d / "script.json").exists()
            has_script_md = (d / "script.production.md").exists()
            has_voice = (d / "voice.wav").exists()
            has_video = any(d.glob("*.mp4"))
            has_qa = (d / "qa_report.md").exists()

            title = ""
            slot_id = ""
            if has_script_json:
                try:
                    s_data = json.loads((d / "script.json").read_text(encoding="utf-8"))
                    title = s_data.get("title", "")
                    slot_id = s_data.get("slot_id", "")
                except Exception:
                    pass

            episodes.append({
                "folder_name": d.name,
                "path": str(d),
                "title": title,
                "slot_id": slot_id,
                "has_script_json": has_script_json,
                "has_script_md": has_script_md,
                "has_voice_wav": has_voice,
                "has_video_render": has_video,
                "has_qa_report": has_qa
            })

    return {
        "channel": "El Profe de Velas",
        "channel_dir": str(PROFE_DIR),
        "total_episodes": len(episodes),
        "next_suggested_episode_number": _get_next_profe_episode_number(),
        "episodes": episodes
    }

def get_profe_de_velas_episode(episode_name: str) -> Dict[str, Any]:
    """Recupera os detalhes, roteiro e status de um episódio específico de El Profe de Velas."""
    target_folder = PROFE_DIR / episode_name
    if not target_folder.exists() or not target_folder.is_dir():
        # Tenta buscar por número (ex: '03' ou '3')
        found = None
        for d in PROFE_DIR.iterdir():
            if d.is_dir() and f"episode-{int(episode_name):02d}" in d.name:
                found = d
                break
        if found:
            target_folder = found
        else:
            return {"status": "error", "message": f"Episódio '{episode_name}' não encontrado em {PROFE_DIR}."}

    script_json_data = {}
    if (target_folder / "script.json").exists():
        try:
            script_json_data = json.loads((target_folder / "script.json").read_text(encoding="utf-8"))
        except Exception as e:
            script_json_data = {"error": str(e)}

    script_md = ""
    if (target_folder / "script.production.md").exists():
        try:
            script_md = (target_folder / "script.production.md").read_text(encoding="utf-8")
        except Exception:
            pass

    qa_report = ""
    if (target_folder / "qa_report.md").exists():
        try:
            qa_report = (target_folder / "qa_report.md").read_text(encoding="utf-8")
        except Exception:
            pass

    videos = [f.name for f in target_folder.glob("*.mp4")]

    return {
        "episode_folder": target_folder.name,
        "path": str(target_folder),
        "script_json": script_json_data,
        "script_production_md": script_md,
        "qa_report": qa_report,
        "rendered_videos": videos,
        "has_voice": (target_folder / "voice.wav").exists()
    }

def send_profe_de_velas_theme(
    title: str,
    problem: str,
    visual_evidence: str,
    didactic_rule: str,
    demo_exercise: str,
    slot_id: Optional[str] = None,
    thumbnail_hook: Optional[str] = None,
    notes: Optional[str] = None,
    auto_trigger_codex: bool = False
) -> Dict[str, Any]:
    """
    Envia um tema estruturado especificamente para 'El Profe de Velas' (es-419).
    Segue o framework pedagógico: Problema -> Evidência Visual -> Regra Didática -> Exercício Demo.
    """
    item_id = generate_id("PROFE-THM")
    now_iso = datetime.now().isoformat()
    clean_slug = sanitize_filename(title)
    slot = slot_id or f"velas.{clean_slug[:30]}"

    filename = f"{item_id}_{clean_slug}.md"
    inbox_file = THEMES_DIR / filename
    profe_mirror_file = PROFE_THEMES_DIR / filename

    content_lines = [
        "---",
        f"id: {item_id}",
        "channel: \"El Profe de Velas\"",
        "language: es-419",
        f"slot_id: \"{slot}\"",
        f"title: \"{title}\"",
        f"thumbnail_text: \"{thumbnail_hook or 'SIN ADIVINAR'}\"",
        "status: pending",
        f"created_at: {now_iso}",
        "voice: \"Gil - Warm, Natural & Mexican\"",
        "signature: \"Sin adivinar. · Pruébalo primero en demo.\"",
        "compliance: \"CONTENIDO EDUCATIVO · SIN SEÑALES\"",
        "---",
        "",
        f"# 🕯️ EL PROFE DE VELAS // TEMA: {title}",
        "",
        f"**Slot ID:** `{slot}`  ",
        f"**Capa / Thumbnail:** `{thumbnail_hook or 'SIN ADIVINAR'}`  ",
        f"**Data:** {now_iso}  ",
        "",
        "---",
        "",
        "## ❌ 1. O Problema / O Erro Comum do Aluno",
        problem,
        "",
        "## 👁️ 2. A Evidência Visível no Gráfico (O que olhar primeiro)",
        visual_evidence,
        "",
        "## 📐 3. A Regra Didática / Mecanismo Claro (Sin Adivinar)",
        didactic_rule,
        "",
        "## 🧪 4. Exercício Prático Obrigatório (Pruébalo primero en demo)",
        demo_exercise,
        "",
        "## ⚙️ Diretrizes para o Codex / Pipeline",
        notes or "Estruturar o próximo episódio em D:/agent- el prof del las velas, preparar script.json e script.production.md.",
        "",
        "> *Aprende a leer lo que las velas muestran, sin memorizar patrones y sin adivinar la siguiente.*"
    ]

    md_text = "\n".join(content_lines)
    inbox_file.write_text(md_text, encoding="utf-8")
    try:
        profe_mirror_file.write_text(md_text, encoding="utf-8")
    except Exception:
        pass

    codex_job = None
    if auto_trigger_codex:
        prompt = f"Novo tema para El Profe de Velas: '{title}' ({item_id}). Arquivo: {profe_mirror_file}. Prepare a pasta do episódio e o rascunho de script.production.md."
        trigger_res = trigger_codex_task(prompt=prompt, project_path=str(PROFE_DIR))
        codex_job = trigger_res.get("codex_job_id")

    # Save to SQLite
    raw_payload = json.dumps({
        "channel": "El Profe de Velas", "title": title, "slot_id": slot, "problem": problem,
        "visual_evidence": visual_evidence, "didactic_rule": didactic_rule, "demo_exercise": demo_exercise,
        "thumbnail_hook": thumbnail_hook, "notes": notes
    }, ensure_ascii=False)

    conn = init_db()
    with conn:
        conn.execute("""
            INSERT INTO inbox_items (
                id, type, title, channel, status, big_idea, hook, target_audience,
                notes, file_path, target_project_path, codex_job_id, created_at, updated_at, raw_payload
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            item_id, "theme", title, "El Profe de Velas", "pending", didactic_rule, thumbnail_hook,
            "Iniciante em opções/velas (es-419)", notes, str(profe_mirror_file), str(PROFE_DIR), codex_job,
            now_iso, now_iso, raw_payload
        ))

    return {
        "status": "success",
        "message": f"Tema para El Profe de Velas '{title}' salvo e espelhado com sucesso!",
        "item_id": item_id,
        "slot_id": slot,
        "profe_project_file": str(profe_mirror_file),
        "inbox_file": str(inbox_file),
        "codex_triggered": auto_trigger_codex,
        "codex_job_id": codex_job
    }

def send_profe_de_velas_script(
    title: str,
    blocks: List[Dict[str, Any]],
    slot_id: Optional[str] = None,
    thumbnail_text: Optional[str] = None,
    episode_number: Optional[int] = None,
    slug: Optional[str] = None,
    notes: Optional[str] = None,
    auto_trigger_codex: bool = False
) -> Dict[str, Any]:
    """
    Cria a pasta do episódio em D:/agent- el prof del las velas, gera script.production.md
    e script.json prontos para narração ElevenLabs (Gil) e renderização no Codex.
    """
    item_id = generate_id("PROFE-SCR")
    now_iso = datetime.now().isoformat()
    ep_num = episode_number or _get_next_profe_episode_number()
    clean_slug = slug or sanitize_filename(title)[:35]
    slot = slot_id or f"velas.ep{ep_num:02d}-{clean_slug}"

    ep_folder_name = f"episode-{ep_num:02d}-{clean_slug}"
    ep_dir = PROFE_DIR / ep_folder_name
    ep_dir.mkdir(parents=True, exist_ok=True)
    (ep_dir / "audio").mkdir(exist_ok=True)

    # Voice ID approved for Gil
    VOICE_ID = "SzatlCk7ZMTGly6rtgt4"
    VOICE_NAME = "Gil - Warm, Natural & Mexican"

    # Normalize blocks
    formatted_blocks = []
    for idx, b in enumerate(blocks, start=1):
        block_id = b.get("id") or f"B{idx:02d}"
        b_type = b.get("type", "evidencia")
        narration = b.get("narration", "").strip()
        visual_intent = b.get("visual_intent", "")
        marks = b.get("marks", [])
        delivery = b.get("delivery", {
            "emocion": "calma",
            "tono": "conversación cercana",
            "intencion": "explicar con claridad sin prisa",
            "ritmo": "sereno y didáctico"
        })

        formatted_blocks.append({
            "id": block_id,
            "type": b_type,
            "narration": narration,
            "visual_intent": visual_intent,
            "marks": marks,
            "card": b.get("card", None),
            "avatar": "none",
            "delivery": delivery
        })

    # Ensure mandatory closures in final block if not present
    last_block = formatted_blocks[-1]
    if "pruébalo primero en demo" not in last_block["narration"].lower() and "sin adivinar" not in last_block["narration"].lower():
        last_block["narration"] += " Sin adivinar. Pruébalo primero en demo."

    # 1. script.json
    script_json_payload = {
        "version": "1.0",
        "slot_id": slot,
        "title": title,
        "thumbnail": thumbnail_text or "SIN ADIVINAR",
        "language": "es-419",
        "format": "F6",
        "status": "ready",
        "voice_name": VOICE_NAME,
        "voice_id": VOICE_ID,
        "music": False,
        "captions": False,
        "humanization": {
            "source": "itsjwill/humanizer-x",
            "commit": "51539bc409a8f65f1bfd98e6b32a5f83e1a68550",
            "mode": "voice-adapted-es-419",
            "policy": "Controlled classroom cadence; no English slang, fake hesitation, detector-evasion claims or excessive fillers."
        },
        "blocks": formatted_blocks
    }

    script_json_path = ep_dir / "script.json"
    script_json_path.write_text(json.dumps(script_json_payload, ensure_ascii=False, indent=2), encoding="utf-8")

    # 2. script.production.md
    md_lines = [
        "---",
        "status: ready",
        f"slot_id: {slot}",
        f"titulo: \"{title}\"",
        f"thumbnail: \"{thumbnail_text or 'SIN ADIVINAR'}\"",
        "idioma: es-419",
        "formato: F6",
        "duracion_objetivo: 04:00-04:30",
        f"voz: {VOICE_NAME}",
        "subtitulos: false",
        f"created_at: {now_iso}",
        "---",
        "",
        f"# EPISODIO {ep_num:02d} // {title}",
        "",
    ]

    for b in formatted_blocks:
        md_lines.append(f"# {b['id']} — tipo: {b['type']}")
        md_lines.append(f"- visual: {b['visual_intent']}")
        md_lines.append(f"- entrega: {json.dumps(b['delivery'], ensure_ascii=False)}")
        md_lines.append(f"- narracion: |\n    {b['narration']}")
        md_lines.append("")

    script_md_path = ep_dir / "script.production.md"
    script_md_path.write_text("\n".join(md_lines), encoding="utf-8")

    # 3. Mirror in general codex_inbox
    inbox_script_file = SCRIPTS_DIR / f"{item_id}_{ep_folder_name}.md"
    inbox_script_file.write_text("\n".join(md_lines), encoding="utf-8")

    # 4. Trigger Codex if requested
    codex_job = None
    if auto_trigger_codex:
        prompt = f"Novo episódio criado para El Profe de Velas: '{title}' na pasta {ep_dir}. O script.json e script.production.md já estão gerados. Inicie a produção e geração de voz com a voz Gil."
        trigger_res = trigger_codex_task(prompt=prompt, project_path=str(ep_dir))
        codex_job = trigger_res.get("codex_job_id")

    # 5. Save to SQLite
    raw_payload = json.dumps({
        "channel": "El Profe de Velas", "episode_number": ep_num, "title": title,
        "slot_id": slot, "blocks_count": len(formatted_blocks), "notes": notes
    }, ensure_ascii=False)

    conn = init_db()
    with conn:
        conn.execute("""
            INSERT INTO inbox_items (
                id, type, title, channel, status, voice_id, notes, file_path,
                target_project_path, codex_job_id, created_at, updated_at, raw_payload
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            item_id, "script", f"Episodio {ep_num:02d}: {title}", "El Profe de Velas",
            "pending", VOICE_ID, notes, str(script_json_path), str(ep_dir), codex_job,
            now_iso, now_iso, raw_payload
        ))

    return {
        "status": "success",
        "message": f"Episódio {ep_num:02d} '{title}' criado com sucesso na pasta de produção do Profe de Velas!",
        "item_id": item_id,
        "episode_number": ep_num,
        "episode_dir": str(ep_dir),
        "script_json": str(script_json_path),
        "script_production_md": str(script_md_path),
        "voice_selected": VOICE_NAME,
        "blocks_count": len(formatted_blocks),
        "codex_triggered": auto_trigger_codex,
        "codex_job_id": codex_job
    }

# ==============================================================================
# MCP PROTOCOL DEFINITIONS
# ==============================================================================

MCP_TOOLS = [
    {
        "name": "send_profe_de_velas_theme",
        "description": "Envia um tema validado especificamente para o canal 'El Profe de Velas' (es-419). Salva no Inbox do Codex e espelha em D:/agent- el prof del las velas/themes com a estrutura pedagógica do canal.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "title": {"type": "string", "description": "Título didático da aula (ex: 'Antes de mirar la próxima vela, aprende a leer estas tres juntas')"},
                "problem": {"type": "string", "description": "O erro comum do aluno iniciante (ex: confiar só na cor ou decorar padrão isolado)"},
                "visual_evidence": {"type": "string", "description": "O que o gráfico realmente mostra (cuerpo, mecha, cierre, solapamiento, contexto)"},
                "didactic_rule": {"type": "string", "description": "A regra ou princípio didático ('Sin adivinar')"},
                "demo_exercise": {"type": "string", "description": "O exercício prático que o aluno deve testar ('Pruébalo primero en demo')"},
                "slot_id": {"type": "string", "description": "ID do slot/aula (ex: 'velas.fuerza-y-rechazo')"},
                "thumbnail_hook": {"type": "string", "description": "Texto visual curto da capa (ex: 'NO MIRES UNA SOLA')"},
                "notes": {"type": "string", "description": "Instruções técnicas para o Codex"},
                "auto_trigger_codex": {"type": "boolean", "description": "Se true, chama o Codex CLI para iniciar o trabalho imediatamente", "default": False}
            },
            "required": ["title", "problem", "visual_evidence", "didactic_rule", "demo_exercise"]
        }
    },
    {
        "name": "send_profe_de_velas_script",
        "description": "Cria e despacha um roteiro completo de 'El Profe de Velas' direto para o pipeline de produção (D:/agent- el prof del las velas/episode-XX/). Gera script.json com voz Gil (ElevenLabs), script.production.md e prepara para renderização.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "title": {"type": "string", "description": "Título oficial do episódio"},
                "blocks": {
                    "type": "array",
                    "description": "Lista de blocos da aula (Hook, Contrato, Evidencia, Mecanismo, Cierre)",
                    "items": {
                        "type": "object",
                        "properties": {
                            "id": {"type": "string", "description": "ID do bloco (ex: 'B01', 'B02')"},
                            "type": {"type": "string", "enum": ["hook", "gancho", "contrato", "evidencia", "mecanismo", "ejemplo", "contraejemplo", "checklist", "cierre"]},
                            "narration": {"type": "string", "description": "Fala exata do professor em espanhol neutro (es-419)"},
                            "visual_intent": {"type": "string", "description": "Diretiva do que a tela/gráfico deve mostrar nesse trecho"},
                            "marks": {"type": "array", "description": "Marcações visuais de zoom, círculo ou labels"}
                        },
                        "required": ["narration", "visual_intent"]
                    }
                },
                "slot_id": {"type": "string", "description": "ID do slot do episódio (ex: 'velas.cierre-manda')"},
                "thumbnail_text": {"type": "string", "description": "Texto impactante para a capa do YouTube"},
                "episode_number": {"type": "integer", "description": "Número do episódio (deixe vazio para autodetectar o próximo, ex: 4)"},
                "slug": {"type": "string", "description": "Slug da pasta do episódio (ex: 'mecha-vs-cuerpo')"},
                "notes": {"type": "string", "description": "Instruções extras para o Codex"},
                "auto_trigger_codex": {"type": "boolean", "description": "Se true, dispara o Codex CLI para iniciar a geração de voz e vídeo imediatamente", "default": False}
            },
            "required": ["title", "blocks"]
        }
    },
    {
        "name": "list_profe_de_velas_episodes",
        "description": "Lista todos os episódios produzidos e em andamento de 'El Profe de Velas', verificando existência de roteiro, narração em áudio (voice.wav) e vídeo renderizado.",
        "inputSchema": {
            "type": "object",
            "properties": {}
        }
    },
    {
        "name": "get_profe_de_velas_episode",
        "description": "Consulta os arquivos e dados de um episódio específico de 'El Profe de Velas' (script.json, script.production.md, qa_report e vídeos renderizados).",
        "inputSchema": {
            "type": "object",
            "properties": {
                "episode_name": {"type": "string", "description": "Nome da pasta do episódio (ex: 'episode-03-tres-velas') ou número (ex: '3')"}
            },
            "required": ["episode_name"]
        }
    },
    {
        "name": "send_theme_to_codex",
        "description": "Envia um tema/ideia validada do Hermes diretamente para o Codex. Cria um arquivo markdown estruturado no Inbox compartilhado, registra no SQLite e opcionalmente espelha no projeto de destino e dispara o Codex.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "title": {"type": "string", "description": "Título ou tema central do vídeo"},
                "channel": {"type": "string", "description": "Canal destino (ex: 'Canal Brecha', 'El Cazador de Wins', 'Trading Labs', 'O Outro Lado', 'VoiceCut', 'El Profe de Velas')"},
                "big_idea": {"type": "string", "description": "A Big Idea / Premissa central única do tema (A Regra do Um)"},
                "hook": {"type": "string", "description": "Ideia ou texto do hook inicial (colisão mental dos primeiros 3-5s)"},
                "target_audience": {"type": "string", "description": "Público-alvo / Avatar / Nível de consciência (Bob)"},
                "angles_and_research": {"type": "string", "description": "Ângulos narrativos, dados, fontes e referências"},
                "notes": {"type": "string", "description": "Instruções específicas para o Codex"},
                "target_project_path": {"type": "string", "description": "Caminho ou nome do projeto de destino"},
                "auto_trigger_codex": {"type": "boolean", "description": "Se true, invoca o Codex CLI automaticamente para iniciar a tarefa imediatamente", "default": False}
            },
            "required": ["title", "channel"]
        }
    },
    {
        "name": "send_script_to_codex",
        "description": "Envia um roteiro completo gerado no Hermes para o Codex. Salva o roteiro com marcações de cena, hook, CTA e diretrizes para produção/VoiceCut.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "title": {"type": "string", "description": "Título do roteiro / vídeo"},
                "channel": {"type": "string", "description": "Canal destino"},
                "script_content": {"type": "string", "description": "Texto completo do roteiro com blocos de narração, marcações visuais e sonoras"},
                "hook": {"type": "string", "description": "O hook de abertura (3 primeiros segundos)"},
                "cta": {"type": "string", "description": "A chamada para ação (Call to Action)"},
                "voice_id": {"type": "string", "description": "Voz ElevenLabs ou tom de narração sugerido"},
                "notes": {"type": "string", "description": "Instruções para o Codex"},
                "target_project_path": {"type": "string", "description": "Caminho do projeto destino"},
                "auto_trigger_codex": {"type": "boolean", "description": "Se true, invoca o Codex CLI automaticamente", "default": False}
            },
            "required": ["title", "channel", "script_content"]
        }
    },
    {
        "name": "list_codex_inbox",
        "description": "Lista temas e roteiros no Inbox do Codex enviados pelo Hermes. Permite filtrar por status, tipo ou canal.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "status": {"type": "string", "enum": ["all", "pending", "in_progress", "completed", "archived"], "default": "all"},
                "item_type": {"type": "string", "enum": ["all", "theme", "script"], "default": "all"},
                "channel": {"type": "string", "description": "Filtrar por nome de canal"},
                "limit": {"type": "integer", "default": 20}
            }
        }
    },
    {
        "name": "get_codex_inbox_item",
        "description": "Obtém detalhes completos e o conteúdo na íntegra de um tema ou roteiro pelo ID.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "item_id": {"type": "string", "description": "ID do item (ex: 'THM-20261001-XXXX' ou 'SCR-20261001-XXXX')"}
            },
            "required": ["item_id"]
        }
    },
    {
        "name": "update_inbox_item_status",
        "description": "Atualiza o status de um tema ou roteiro no Codex (ex: marcar como 'in_progress', 'completed' ou 'archived') com notas opcionais.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "item_id": {"type": "string", "description": "ID do item"},
                "status": {"type": "string", "enum": ["pending", "in_progress", "completed", "archived"]},
                "notes": {"type": "string", "description": "Notas sobre o progresso ou link dos artefatos produzidos"}
            },
            "required": ["item_id", "status"]
        }
    },
    {
        "name": "list_codex_projects",
        "description": "Lista os projetos conhecidos do Codex e canais de vídeo configurados no sistema para fácil direcionamento.",
        "inputSchema": {
            "type": "object",
            "properties": {}
        }
    },
    {
        "name": "trigger_codex_task",
        "description": "Dispara uma tarefa diretamente no Codex CLI (codex exec) para processar um tema, roteiro ou comando.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "prompt": {"type": "string", "description": "Instruções para o Codex"},
                "project_path": {"type": "string", "description": "Diretório do projeto onde o Codex deve operar"},
                "model": {"type": "string", "description": "Modelo a ser usado pelo Codex (opcional)"}
            },
            "required": ["prompt"]
        }
    },
    {
        "name": "read_hermes_latest_sessions",
        "description": "Consulta as últimas sessões e histórico do Hermes para facilitar a sincronização de contexto com o Codex.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "limit": {"type": "integer", "default": 5}
            }
        }
    }
]

def handle_call_tool(name: str, args: Dict[str, Any]) -> Dict[str, Any]:
    if name == "send_profe_de_velas_theme":
        res = send_profe_de_velas_theme(**args)
    elif name == "send_profe_de_velas_script":
        res = send_profe_de_velas_script(**args)
    elif name == "list_profe_de_velas_episodes":
        res = list_profe_de_velas_episodes()
    elif name == "get_profe_de_velas_episode":
        res = get_profe_de_velas_episode(**args)
    elif name == "send_theme_to_codex":
        res = send_theme_to_codex(**args)
    elif name == "send_script_to_codex":
        res = send_script_to_codex(**args)
    elif name == "list_codex_inbox":
        res = list_codex_inbox(**args)
    elif name == "get_codex_inbox_item":
        res = get_codex_inbox_item(**args)
    elif name == "update_inbox_item_status":
        res = update_inbox_item_status(**args)
    elif name == "list_codex_projects":
        res = list_codex_projects()
    elif name == "trigger_codex_task":
        res = trigger_codex_task(**args)
    elif name == "read_hermes_latest_sessions":
        res = read_hermes_latest_sessions(**args)
    else:
        raise ValueError(f"Ferramenta desconhecida: {name}")

    return {"content": [{"type": "text", "text": json.dumps(res, ensure_ascii=False, indent=2)}]}

def main():
    """Stdio JSON-RPC loop."""
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            req = json.loads(line)
            req_id = req.get("id")
            method = req.get("method")

            if req_id is None:
                continue

            if method == "tools/list":
                resp = {"jsonrpc": "2.0", "id": req_id, "result": {"tools": MCP_TOOLS}}
            elif method == "tools/call":
                params = req.get("params", {})
                name = params.get("name")
                args = params.get("arguments", {})
                tool_res = handle_call_tool(name, args)
                resp = {"jsonrpc": "2.0", "id": req_id, "result": tool_res}
            elif method == "initialize":
                resp = {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "result": {
                        "protocolVersion": "2024-11-05",
                        "serverInfo": {"name": "hermes-codex-bridge", "version": "1.1.0"},
                        "capabilities": {"tools": {}}
                    }
                }
            else:
                resp = {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32601, "message": "Method not found"}}

            _rpc_stdout.write(json.dumps(resp, ensure_ascii=False) + "\n")
            _rpc_stdout.flush()

        except Exception as e:
            if 'req_id' in locals() and req_id is not None:
                err_resp = {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32000, "message": str(e)}}
                _rpc_stdout.write(json.dumps(err_resp, ensure_ascii=False) + "\n")
                _rpc_stdout.flush()

if __name__ == "__main__":
    main()
