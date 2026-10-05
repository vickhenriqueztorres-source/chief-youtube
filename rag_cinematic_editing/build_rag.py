# -*- coding: utf-8 -*-
"""
Pipeline de Ingestão e Construção da Base de Conhecimento RAG de Edição Cinematográfica.
Coleta transcrições dos maiores profissionais e canais sobre:
'como editar videos e deixar cinematograficos'
Gera:
1. JSONs brutos com timestamps em data/raw_transcripts/
2. Markdowns enriquecidos em data/processed_markdowns/
3. Banco SQLite FTS5 para busca textual ultra-rápida (BM25)
4. Banco Vetorial ChromaDB com embeddings para busca semântica
"""

import os
import sys
import json
import sqlite3
import re
from pathlib import Path
from typing import List, Dict, Any

# Suporte a UTF-8 no Windows
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

from youtube_transcript_api import YouTubeTranscriptApi

RAG_DIR = Path(__file__).resolve().parent
RAW_DIR = RAG_DIR / "data" / "raw_transcripts"
PROCESSED_DIR = RAG_DIR / "data" / "processed_markdowns"
CHROMA_DIR = RAG_DIR / "data" / "chroma"
SQLITE_DB = RAG_DIR / "data" / "knowledge_base.sqlite"

RAW_DIR.mkdir(parents=True, exist_ok=True)
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
CHROMA_DIR.mkdir(parents=True, exist_ok=True)

# Curadoria dos principais vídeos e mestres do nicho
CURATED_VIDEOS = [
    {
        "id": "O41Ixys3BkA",
        "creator": "Andre Pilli",
        "title": "Faça um filme, não um vídeo",
        "views": "166k",
        "focus": "Storytelling cinematográfico, propósito de cena, ritmo, atmosfera e intenção de câmera."
    },
    {
        "id": "bZdmAIzekN0",
        "creator": "Gaveta",
        "title": "Meu modo de editar vídeos",
        "views": "450k",
        "focus": "Fluxo de trabalho de edição profissional, timing cômico e dramático, seleção de takes e ritmo."
    },
    {
        "id": "5xR3w0bbxOs",
        "creator": "Brendo Rannov",
        "title": "5 Técnicas para Fazer Vídeos CINEMATOGRÁFICOS como um Profissional",
        "views": "145k",
        "focus": "Composição, iluminação dramática, movimentos de câmera, sound design e color grading."
    },
    {
        "id": "LGwuAvuE3A8",
        "creator": "Brendo Rannov",
        "title": "4 Técnicas simples de EDIÇÃO para deixar qualquer vídeo DINÂMICO",
        "views": "90k",
        "focus": "Cortes na ação, J-Cut, L-Cut, efeitos sonoros diegéticos e dinamismo sem poluição."
    },
    {
        "id": "gWfOdT8TK7E",
        "creator": "Gabriel Saab",
        "title": "Aprenda a EDITAR como um PROFISSIONAL",
        "views": "512k",
        "focus": "Estrutura de timeline, atalhos, cortes invisíveis, narrativa e acabamento de áudio."
    },
    {
        "id": "hRjzXFScKZc",
        "creator": "Giulia Paié",
        "title": "Como fazer seus vídeos parecerem filme (mesmo sendo só você e sua câmera)",
        "views": "270k",
        "focus": "Estética de cinema solo, luz difusa, regra dos terços, cores e texturas cinematográficas."
    },
    {
        "id": "T-akUfaSuiA",
        "creator": "Gus Avancini",
        "title": "Color Grading no CapCut - COR de FILME",
        "views": "199k",
        "focus": "Curvas de tom, saturação seletiva, contraste cinematográfico, Teal & Orange e LUTs."
    },
    {
        "id": "RL2GYkYryjk",
        "creator": "Gus Avancini",
        "title": "Edição CINEMATOGRÁFICA no CapCut pra PC",
        "views": "60k",
        "focus": "Keyframes, máscaras dinâmicas, letterbox 2.35:1, sound design imersivo e transições suaves."
    },
    {
        "id": "bPhVgGJcsk4",
        "creator": "Jefe Vilanova",
        "title": "Vídeo CINEMATOGRÁFICO com o CELULAR | Tutorial CapCut",
        "views": "457k",
        "focus": "Taxa de 24fps, regra dos 180 graus (shutter speed), estabilização e pós-produção mobile."
    },
    {
        "id": "pPKiE4OFRlo",
        "creator": "Brainstorm Tutoriais",
        "title": "Como GRAVAR VÍDEOS cinematográficos - APRENDA EM 5 MINUTOS",
        "views": "64k",
        "focus": "Iluminação de três pontos, profundidade de campo, desfoque de fundo e lentes."
    },
    {
        "id": "PCTiKGgDW3U",
        "creator": "Brainstorm Tutoriais",
        "title": "Aprenda DAVINCI RESOLVE em 5 MINUTOS",
        "views": "672k",
        "focus": "DaVinci Resolve: Cut page, Edit page, Color grading profissional em nós (Nodes) e Fairlight."
    },
    {
        "id": "REtL9SJ0AA4",
        "creator": "Bem fácil, na real",
        "title": "EDITAR VÍDEOS é bem fácil, na real",
        "views": "694k",
        "focus": "Fundamentos da montagem, decupagem, eliminação de gordura e cadência narrativa."
    },
    {
        "id": "an30TKGMA-c",
        "creator": "Augusto Editor",
        "title": "Como fazer Edição de VÍDEO CINEMATOGRÁFICO no CAPCUT | FÁCIL",
        "views": "78k",
        "focus": "Letterbox, curvas de velocidade (Speed Ramping), sound effects de impacto e ambiência."
    },
    {
        "id": "Wv3Hmf2Dxlo",
        "creator": "Shutterstock Tutorials",
        "title": "9 Cuts Every Video Editor Should Know | Filmmaking Tips",
        "views": "4.6M",
        "focus": "Standard Cut, Jump Cut, J-Cut, L-Cut, Match Cut, Cutaway, Cross Cut, Smash Cut, Invisible Cut."
    },
    {
        "id": "zXF0kfePL60",
        "creator": "Collin Michael",
        "title": "How To Edit CINEMATIC VIDEOS in CapCut (Ultimate Guide)",
        "views": "1.1M",
        "focus": "Proporções cinematográficas, motion blur em 24fps, color grading, curvas de aceleração e Foley."
    },
    {
        "id": "GYud_W7Ou9E",
        "creator": "Peter McKinnon",
        "title": "Make your footage look Cinematic FAST! Premiere Pro Tutorial",
        "views": "1.2M",
        "focus": "Lumetri Color, contraste natural, tons de pele (skin tones), vinhetas sutis e atmosfera."
    }
]


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


def process_video_transcript(video_info: Dict[str, Any], api: YouTubeTranscriptApi, conn: sqlite3.Connection) -> List[Dict[str, Any]]:
    vid = video_info["id"]
    creator = video_info["creator"]
    title = video_info["title"]
    views = video_info["views"]
    focus = video_info["focus"]
    url = f"https://www.youtube.com/watch?v={vid}"

    print(f"\n▶ Processando [{creator}]: {title} ({vid})...")
    
    # 1. Fetch transcript
    try:
        tl = api.list(vid)
        target = None
        for pref in ["pt", "pt-BR", "pt-PT", "en"]:
            for t in tl:
                if t.language_code == pref or t.language_code.startswith(pref):
                    target = t
                    break
            if target:
                break
        if not target:
            target = list(tl)[0]

        snippets = target.fetch()
        print(f"  ✓ {len(snippets)} snippets coletados ({target.language_code})")
    except Exception as e:
        print(f"  ✗ Falha ao obter transcrição: {e}")
        return []

    # 2. Salvar RAW JSON
    raw_path = RAW_DIR / f"{vid}.json"
    with open(raw_path, "w", encoding="utf-8") as f:
        json.dump({
            "video_info": video_info,
            "language": target.language_code,
            "is_generated": target.is_generated,
            "snippets": [{"text": s.text, "start": s.start, "duration": s.duration} for s in snippets]
        }, f, ensure_ascii=False, indent=2)

    # 3. Agrupar em blocos/parágrafos de ~30 a 60 segundos
    chunks = []
    current_block_texts = []
    current_start = 0.0
    current_duration = 0.0

    full_markdown_lines = [
        "---",
        f'title: "{title}"',
        f'creator: "{creator}"',
        f'video_id: "{vid}"',
        f'url: "{url}"',
        f'views: "{views}"',
        f'focus: "{focus}"',
        f'language: "{target.language_code}"',
        f'total_snippets: {len(snippets)}',
        "---\n",
        f"# {title}",
        f"**Criador / Especialista:** {creator} | **Visualizações:** {views} | [Assistir no YouTube]({url})\n",
        f"**Foco Principal:** {focus}\n",
        "## Transcrição Completa Estruturada\n"
    ]

    chunk_index = 0
    for s in snippets:
        clean_text = s.text.replace("\n", " ").strip()
        if not clean_text:
            continue
        
        if not current_block_texts:
            current_start = s.start

        current_block_texts.append(clean_text)
        current_duration = (s.start + s.duration) - current_start

        # Quebra de bloco se passar de ~45 segundos ou ~90 palavras
        words_count = sum(len(txt.split()) for txt in current_block_texts)
        if current_duration >= 40.0 or words_count >= 80:
            block_content = " ".join(current_block_texts)
            ts_str = seconds_to_timestamp(current_start)
            ts_url = f"{url}&t={int(current_start)}s"
            
            full_markdown_lines.append(f"### `[{ts_str}]` [{creator} - {title}]({ts_url})")
            full_markdown_lines.append(f"{block_content}\n")

            chunks.append({
                "chunk_id": f"{vid}_{chunk_index:03d}",
                "video_id": vid,
                "title": title,
                "creator": creator,
                "url": ts_url,
                "timestamp_str": ts_str,
                "timestamp_sec": current_start,
                "content": block_content
            })
            chunk_index += 1
            current_block_texts = []

    # Bloco remanescente
    if current_block_texts:
        block_content = " ".join(current_block_texts)
        ts_str = seconds_to_timestamp(current_start)
        ts_url = f"{url}&t={int(current_start)}s"
        full_markdown_lines.append(f"### `[{ts_str}]` [{creator} - {title}]({ts_url})")
        full_markdown_lines.append(f"{block_content}\n")
        chunks.append({
            "chunk_id": f"{vid}_{chunk_index:03d}",
            "video_id": vid,
            "title": title,
            "creator": creator,
            "url": ts_url,
            "timestamp_str": ts_str,
            "timestamp_sec": current_start,
            "content": block_content
        })

    # 4. Salvar Markdown Processado
    safe_slug = re.sub(r"[^\w\-]", "_", f"{creator}_{title}")[:60]
    md_path = PROCESSED_DIR / f"{safe_slug}.md"
    with open(md_path, "w", encoding="utf-8") as f:
        f.write("\n".join(full_markdown_lines))

    print(f"  ✓ Markdown gerado em: {md_path.name} ({len(chunks)} blocos)")

    # 5. Inserir no SQLite FTS5
    c = conn.cursor()
    for ch in chunks:
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
    conn.commit()

    return chunks


def build_chroma_store(all_chunks: List[Dict[str, Any]]):
    print(f"\n📦 Indexando {len(all_chunks)} chunks no ChromaDB ({CHROMA_DIR})...")
    import chromadb
    from chromadb.config import Settings

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
        print(f"  ✓ {min(i + batch_size, len(all_chunks))}/{len(all_chunks)} indexados no ChromaDB...")

    print("✓ ChromaDB construído com sucesso!")


def main():
    print("=================================================================")
    print("  CONSTRUINDO RAG DE EDIÇÃO DE VÍDEOS CINEMATOGRÁFICOS")
    print("=================================================================")
    
    init_sqlite_db()
    conn = sqlite3.connect(str(SQLITE_DB))
    api = YouTubeTranscriptApi()

    all_chunks = []
    for video_info in CURATED_VIDEOS:
        chunks = process_video_transcript(video_info, api, conn)
        all_chunks.extend(chunks)

    conn.close()

    print(f"\n✨ Total de vídeos processados: {len(CURATED_VIDEOS)}")
    print(f"✨ Total de blocos/chunks estruturados: {len(all_chunks)}")
    print(f"✨ SQLite FTS5 pronto em: {SQLITE_DB}")

    # Indexar no ChromaDB
    build_chroma_store(all_chunks)

    print("\n🎉 BASE RAG FINALIZADA COM SUCESSO!")


if __name__ == "__main__":
    main()
