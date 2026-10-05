# -*- coding: utf-8 -*-
"""
Pipeline Unificado: Transcrição via Whisper Local + Construção da Base RAG de Edição Cinematográfica.
Gera:
- JSONs estruturados em data/raw_transcripts/
- Markdowns formatados em data/processed_markdowns/
- Base de busca textual SQLite FTS5 em data/knowledge_base.sqlite
- Base vetorial ChromaDB em data/chroma/
"""

import os
import sys
import json
import sqlite3
import re
import time
from pathlib import Path
from typing import List, Dict, Any

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

from faster_whisper import WhisperModel
import chromadb
from chromadb.config import Settings

RAG_DIR = Path(__file__).resolve().parent
AUDIO_DIR = RAG_DIR / "data" / "audio"
RAW_DIR = RAG_DIR / "data" / "raw_transcripts"
PROCESSED_DIR = RAG_DIR / "data" / "processed_markdowns"
CHROMA_DIR = RAG_DIR / "data" / "chroma"
SQLITE_DB = RAG_DIR / "data" / "knowledge_base.sqlite"

RAW_DIR.mkdir(parents=True, exist_ok=True)
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
CHROMA_DIR.mkdir(parents=True, exist_ok=True)

VIDEO_METADATA = {
    "O41Ixys3BkA": {
        "creator": "Andre Pilli",
        "title": "Faça um filme, não um vídeo",
        "views": "166k",
        "focus": "Storytelling cinematográfico, propósito de cena, ritmo, atmosfera e intenção de câmera."
    },
    "bZdmAIzekN0": {
        "creator": "Gaveta",
        "title": "Meu modo de editar vídeos",
        "views": "450k",
        "focus": "Fluxo de trabalho de edição profissional, timing dramático/cômico, decupagem e ritmo."
    },
    "5xR3w0bbxOs": {
        "creator": "Brendo Rannov",
        "title": "5 Técnicas para Fazer Vídeos CINEMATOGRÁFICOS como um Profissional",
        "views": "145k",
        "focus": "Composição, iluminação dramática, movimentos de câmera, sound design e color grading."
    },
    "LGwuAvuE3A8": {
        "creator": "Brendo Rannov",
        "title": "4 Técnicas simples de EDIÇÃO para deixar qualquer vídeo DINÂMICO",
        "views": "90k",
        "focus": "Cortes na ação, J-Cut, L-Cut, efeitos sonoros diegéticos e dinamismo sem poluição."
    },
    "gWfOdT8TK7E": {
        "creator": "Gabriel Saab",
        "title": "Aprenda a EDITAR como um PROFISSIONAL",
        "views": "512k",
        "focus": "Estrutura de timeline, atalhos, cortes invisíveis, narrativa e acabamento de áudio."
    },
    "hRjzXFScKZc": {
        "creator": "Giulia Paié",
        "title": "Como fazer seus vídeos parecerem filme (mesmo sendo só você e sua câmera)",
        "views": "270k",
        "focus": "Estética de cinema solo, luz difusa, regra dos terços, cores e texturas cinematográficas."
    },
    "T-akUfaSuiA": {
        "creator": "Gus Avancini",
        "title": "Color Grading no CapCut - COR de FILME",
        "views": "199k",
        "focus": "Curvas de tom, saturação seletiva, contraste cinematográfico, Teal & Orange e LUTs."
    },
    "bPhVgGJcsk4": {
        "creator": "Jefe Vilanova",
        "title": "Vídeo CINEMATOGRÁFICO com o CELULAR | Tutorial CapCut",
        "views": "457k",
        "focus": "Taxa de 24fps, regra dos 180 graus (shutter speed), estabilização e pós-produção mobile."
    },
    "pPKiE4OFRlo": {
        "creator": "Brainstorm Tutoriais",
        "title": "Como GRAVAR VÍDEOS cinematográficos - APRENDA EM 5 MINUTOS",
        "views": "64k",
        "focus": "Iluminação de três pontos, profundidade de campo, desfoque de fundo e lentes."
    }
}


def seconds_to_timestamp(seconds: float) -> str:
    m = int(seconds // 60)
    s = int(seconds % 60)
    return f"{m:02d}:{s:02d}"


def init_sqlite_db():
    conn = sqlite3.connect(str(SQLITE_DB))
    c = conn.cursor()
    c.execute("DROP TABLE IF EXISTS chunks_fts")
    c.execute("""
        CREATE VIRTUAL TABLE chunks_fts USING fts5(
            chunk_id UNINDEXED,
            video_id UNINDEXED,
            title,
            creator,
            url UNINDEXED,
            timestamp_str UNINDEXED,
            timestamp_sec UNINDEXED,
            content,
            tokenize='unicode61 remove_diacritics 2'
        )
    """)
    conn.commit()
    conn.close()


def main():
    print("=" * 65)
    print("  TRANSCRIÇÃO E CONSTRUÇÃO DO RAG DE EDIÇÃO CINEMATOGRÁFICA")
    print("=" * 65)

    init_sqlite_db()
    conn = sqlite3.connect(str(SQLITE_DB))
    c = conn.cursor()

    print("\n⚡ Carregando WhisperModel (tiny int8 CPU)...")
    model = WhisperModel("tiny", device="cpu", compute_type="int8")
    print("✓ Whisper pronto.")

    all_chunks = []

    for vid, meta in VIDEO_METADATA.items():
        audio_file = AUDIO_DIR / f"{vid}.mp3"
        if not audio_file.exists():
            print(f"⚠ Áudio não encontrado para {vid} ({meta['creator']}), pulando...")
            continue

        print(f"\n▶ Transcrevendo [{meta['creator']}]: {meta['title']} ({vid})...")
        t0 = time.time()
        
        # 1. Transcrever com Whisper
        segments_gen, info = model.transcribe(str(audio_file), language="pt")
        raw_segments = []
        for s in segments_gen:
            clean = s.text.replace("\n", " ").strip()
            if clean:
                raw_segments.append({
                    "start": s.start,
                    "end": s.end,
                    "duration": s.end - s.start,
                    "text": clean
                })
        
        elapsed = time.time() - t0
        print(f"  ✓ {len(raw_segments)} falas transcritas em {elapsed:.1f}s (Duração áudio: {info.duration:.1f}s)")

        # 2. Salvar JSON Bruto
        raw_json_path = RAW_DIR / f"{vid}.json"
        with open(raw_json_path, "w", encoding="utf-8") as f:
            json.dump({
                "video_id": vid,
                "metadata": meta,
                "duration": info.duration,
                "language": info.language,
                "segments": raw_segments
            }, f, ensure_ascii=False, indent=2)

        # 3. Agrupar em blocos semânticos de ~40-60 segundos para RAG
        video_chunks = []
        current_texts = []
        current_start = 0.0
        current_duration = 0.0
        url = f"https://www.youtube.com/watch?v={vid}"

        markdown_lines = [
            "---",
            f'title: "{meta["title"]}"',
            f'creator: "{meta["creator"]}"',
            f'video_id: "{vid}"',
            f'url: "{url}"',
            f'views: "{meta["views"]}"',
            f'focus: "{meta["focus"]}"',
            f'duration_sec: {int(info.duration)}',
            f'total_segments: {len(raw_segments)}',
            "---\n",
            f"# {meta['title']}",
            f"**Criador:** {meta['creator']} | **Views:** {meta['views']} | [Assistir no YouTube]({url})\n",
            f"**Foco:** {meta['focus']}\n",
            "## Transcrição Integral Estruturada\n"
        ]

        chunk_idx = 0
        for seg in raw_segments:
            if not current_texts:
                current_start = seg["start"]
            current_texts.append(seg["text"])
            current_duration = seg["end"] - current_start

            words_count = sum(len(t.split()) for t in current_texts)
            if current_duration >= 40.0 or words_count >= 75:
                content = " ".join(current_texts)
                ts_str = seconds_to_timestamp(current_start)
                ts_url = f"{url}&t={int(current_start)}s"

                markdown_lines.append(f"### `[{ts_str}]` [{meta['creator']} - {meta['title']}]({ts_url})")
                markdown_lines.append(f"{content}\n")

                chunk_obj = {
                    "chunk_id": f"{vid}_{chunk_idx:03d}",
                    "video_id": vid,
                    "title": meta["title"],
                    "creator": meta["creator"],
                    "url": ts_url,
                    "timestamp_str": ts_str,
                    "timestamp_sec": current_start,
                    "content": content
                }
                video_chunks.append(chunk_obj)
                chunk_idx += 1
                current_texts = []

        if current_texts:
            content = " ".join(current_texts)
            ts_str = seconds_to_timestamp(current_start)
            ts_url = f"{url}&t={int(current_start)}s"
            markdown_lines.append(f"### `[{ts_str}]` [{meta['creator']} - {meta['title']}]({ts_url})")
            markdown_lines.append(f"{content}\n")
            chunk_obj = {
                "chunk_id": f"{vid}_{chunk_idx:03d}",
                "video_id": vid,
                "title": meta["title"],
                "creator": meta["creator"],
                "url": ts_url,
                "timestamp_str": ts_str,
                "timestamp_sec": current_start,
                "content": content
            }
            video_chunks.append(chunk_obj)

        # 4. Salvar Markdown Processado
        safe_name = re.sub(r"[^\w\-]", "_", f"{meta['creator']}_{meta['title']}")[:60]
        md_file = PROCESSED_DIR / f"{safe_name}.md"
        with open(md_file, "w", encoding="utf-8") as f:
            f.write("\n".join(markdown_lines))

        print(f"  ✓ Markdown gerado: {md_file.name} ({len(video_chunks)} blocos)")

        # 5. Indexar no SQLite FTS5
        for ch in video_chunks:
            c.execute("""
                INSERT INTO chunks_fts (chunk_id, video_id, title, creator, url, timestamp_str, timestamp_sec, content)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                ch["chunk_id"],
                ch["video_id"],
                ch["title"],
                ch["creator"],
                ch["url"],
                ch["timestamp_str"],
                ch["timestamp_sec"],
                ch["content"]
            ))

        all_chunks.extend(video_chunks)

    conn.commit()
    conn.close()

    print(f"\n=================================================================")
    print(f"✨ Total de vídeos indexados: {len(VIDEO_METADATA)}")
    print(f"✨ Total de chunks na base de conhecimento: {len(all_chunks)}")
    print(f"✨ SQLite FTS5 atualizado em: {SQLITE_DB}")

    # 6. Indexar no ChromaDB
    print(f"\n📦 Indexando {len(all_chunks)} chunks no ChromaDB ({CHROMA_DIR})...")
    client = chromadb.PersistentClient(path=str(CHROMA_DIR), settings=Settings(anonymized_telemetry=False))
    try:
        client.delete_collection("cinematic_video_editing")
    except Exception:
        pass

    collection = client.create_collection(
        name="cinematic_video_editing",
        metadata={"hnsw:space": "cosine"}
    )

    batch_size = 50
    for i in range(0, len(all_chunks), batch_size):
        batch = all_chunks[i:i + batch_size]
        ids = [c["chunk_id"] for c in batch]
        documents = [c["content"] for c in batch]
        metadatas = [{
            "video_id": c["video_id"],
            "title": c["title"],
            "creator": c["creator"],
            "url": c["url"],
            "timestamp_str": c["timestamp_str"],
            "timestamp_sec": c["timestamp_sec"]
        } for c in batch]

        collection.add(
            ids=ids,
            documents=documents,
            metadatas=metadatas
        )

    print("✓ ChromaDB construído com sucesso!")
    print("\n🎉 BASE RAG DE EDIÇÃO CINEMATOGRÁFICA 100% OPERACIONAL!")


if __name__ == "__main__":
    main()
