# -*- coding: utf-8 -*-
"""
Motor de Busca Híbrido da Base de Conhecimento RAG de Edição Cinematográfica.
Combina busca textual FTS5 (BM25) no SQLite com busca vetorial semântica no ChromaDB.
Retorna unidades de conhecimento atômicas e limpas com:
- Técnica / Conceito
- Princípio Causal (por que funciona)
- Instrução Prática de Timeline / Câmera (passo a passo)
- Minuto exato [mm:ss] e link direto do YouTube
"""

import sys
import json
import sqlite3
import argparse
from pathlib import Path
from typing import List, Dict, Any, Optional

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

RAG_DIR = Path(__file__).resolve().parent
SQLITE_DB = RAG_DIR / "data" / "knowledge_base.sqlite"
CHROMA_DIR = RAG_DIR / "data" / "chroma"


def search_fts(query: str, top_k: int = 5) -> List[Dict[str, Any]]:
    """Busca em texto pleno ultra-rápida via SQLite FTS5 (BM25)."""
    if not SQLITE_DB.exists():
        return []

    # Sanitizar query para sintaxe FTS5
    clean_query = " ".join([f'"{w}"' for w in query.replace('"', '').split() if len(w) > 2])
    if not clean_query:
        clean_query = f'"{query.strip()}"'

    conn = sqlite3.connect(str(SQLITE_DB))
    c = conn.cursor()

    try:
        c.execute("""
            SELECT chunk_id, video_id, creator, video_title, concept, url, timestamp_str, timestamp_sec, principle, execution, tags, content, rank
            FROM chunks_fts
            WHERE chunks_fts MATCH ?
            ORDER BY rank
            LIMIT ?
        """, (clean_query, top_k))
        rows = c.fetchall()
    except Exception:
        # Fallback com LIKE
        c.execute("""
            SELECT chunk_id, video_id, creator, video_title, concept, url, timestamp_str, timestamp_sec, principle, execution, tags, content, 0.0
            FROM chunks_fts
            WHERE content LIKE ? OR concept LIKE ? OR tags LIKE ?
            LIMIT ?
        """, (f"%{query}%", f"%{query}%", f"%{query}%", top_k))
        rows = c.fetchall()

    conn.close()

    results = []
    for r in rows:
        results.append({
            "source_type": "fts5_bm25",
            "chunk_id": r[0],
            "video_id": r[1],
            "creator": r[2],
            "title": r[3],
            "concept": r[4],
            "url": r[5],
            "timestamp_str": r[6],
            "timestamp_sec": r[7],
            "principle": r[8],
            "execution": r[9],
            "tags": r[10],
            "content": r[11],
            "score": abs(float(r[12])) if r[12] is not None else 0.0
        })
    return results


def search_vector(query: str, top_k: int = 5) -> List[Dict[str, Any]]:
    """Busca vetorial por similaridade semântica no ChromaDB."""
    if not CHROMA_DIR.exists():
        return []

    try:
        import chromadb
        from chromadb.config import Settings
        client = chromadb.PersistentClient(path=str(CHROMA_DIR), settings=Settings(anonymized_telemetry=False))
        collection = client.get_collection("cinematic_video_editing")
        
        raw = collection.query(
            query_texts=[query],
            n_results=top_k
        )

        results = []
        if raw and raw.get("ids") and len(raw["ids"]) > 0:
            ids = raw["ids"][0]
            docs = raw["documents"][0]
            metas = raw["metadatas"][0]
            distances = raw.get("distances", [[0.0] * len(ids)])[0]

            for i in range(len(ids)):
                m = metas[i]
                results.append({
                    "source_type": "chroma_vector",
                    "chunk_id": ids[i],
                    "video_id": m.get("video_id"),
                    "creator": m.get("creator"),
                    "title": m.get("title"),
                    "concept": m.get("concept"),
                    "url": m.get("url"),
                    "timestamp_str": m.get("timestamp_str"),
                    "timestamp_sec": m.get("timestamp_sec"),
                    "principle": m.get("principle"),
                    "execution": m.get("execution"),
                    "tags": m.get("tags"),
                    "content": docs[i],
                    "distance": distances[i] if distances else 0.0
                })
        return results
    except Exception:
        return []


def search(query: str, top_k: int = 5, mode: str = "hybrid") -> Dict[str, Any]:
    """Orquestra busca híbrida ou direcionada com desduplicação por chunk_id."""
    results = []
    seen_chunks = set()

    if mode in ("vector", "hybrid"):
        v_res = search_vector(query, top_k=top_k)
        for r in v_res:
            if r["chunk_id"] not in seen_chunks:
                seen_chunks.add(r["chunk_id"])
                results.append(r)

    if mode in ("fts", "hybrid") or len(results) < top_k:
        f_res = search_fts(query, top_k=top_k)
        for r in f_res:
            if r["chunk_id"] not in seen_chunks:
                seen_chunks.add(r["chunk_id"])
                results.append(r)

    return {
        "status": "success",
        "query": query,
        "mode": mode,
        "total_results": len(results[:top_k]),
        "results": results[:top_k]
    }


def main():
    parser = argparse.ArgumentParser(description="Busca RAG Curada de Edição de Vídeos Cinematográficos")
    parser.add_argument("query", type=str, help="Pergunta ou termo técnico sobre edição de vídeo")
    parser.add_argument("--k", type=int, default=4, help="Número de resultados a retornar")
    parser.add_argument("--mode", type=str, default="hybrid", choices=["hybrid", "fts", "vector"], help="Modo de busca")
    parser.add_argument("--json", action="store_true", help="Retornar saída em formato JSON bruto")
    args = parser.parse_args()

    res = search(args.query, top_k=args.k, mode=args.mode)

    if args.json:
        print(json.dumps(res, indent=2, ensure_ascii=False))
        return

    print("\n" + "=" * 75)
    print(f"  🔍 RESULTADOS RAG CURADOS: '{args.query}' (Modo: {args.mode.upper()})")
    print("=" * 75)

    if not res["results"]:
        print("Nenhum resultado encontrado para esta consulta.")
        return

    for i, item in enumerate(res["results"], 1):
        concept = item.get("concept") or item.get("title")
        print(f"\n[{i}] 🎬 {concept}")
        print(f"    👤 Criador: {item['creator']} | 📺 Vídeo: {item['title']}")
        print(f"    ⏱ Ponto Exato: {item['timestamp_str']} | 🔗 [Assistir no YouTube]: {item['url']}")
        if item.get("principle"):
            print(f"    🧠 Princípio Causal: {item['principle']}")
        if item.get("execution"):
            print(f"    🛠 Execução Técnica: {item['execution']}")
        if item.get("tags"):
            print(f"    🏷 Palavras-Chave: {item['tags']}")
        print("-" * 75)


if __name__ == "__main__":
    main()
