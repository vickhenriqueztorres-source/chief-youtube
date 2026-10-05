# -*- coding: utf-8 -*-
"""
Handler de Consulta à Base de Conhecimento RAG - Beto Copy (Copy Camp / Empiricus).
Executa busca híbrida (Vetorial via ChromaDB + Textual/BM25 nos Markdowns das aulas).
"""

import os
import sys
import json
import re
import argparse
from pathlib import Path
from typing import List, Dict, Any, Optional

# Forçar UTF-8 no stdout/stderr no Windows
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

RAG_ROOT = Path(r"C:\Users\brend\Downloads\RAG EMPIRICUS COPY\rag_pipeline")
PROCESSED_DIR = RAG_ROOT / "data" / "processed"
CHROMA_DIR = RAG_ROOT / "data" / "chroma"


def text_search_processed(query: str, top_k: int = 5) -> List[Dict[str, Any]]:
    """Busca textual rápida em todos os arquivos Markdown processados do Copy Camp."""
    if not PROCESSED_DIR.exists():
        return []

    tokens = [t.lower() for t in re.findall(r"\w+", query) if len(t) > 2]
    if not tokens:
        return []

    results = []
    for md_file in PROCESSED_DIR.glob("*.md"):
        try:
            with open(md_file, "r", encoding="utf-8", errors="replace") as f:
                content = f.read()
        except Exception:
            continue

        content_lower = content.lower()
        score = 0
        matches = []
        for t in tokens:
            count = content_lower.count(t)
            if count > 0:
                score += count * 2

        if score > 0:
            # Encontra os melhores trechos que contêm os termos
            paragraphs = [p.strip() for p in content.split("\n\n") if p.strip()]
            best_snippet = ""
            max_p_score = 0
            for p in paragraphs:
                p_lower = p.lower()
                p_score = sum(p_lower.count(t) for t in tokens)
                if p_score > max_p_score:
                    max_p_score = p_score
                    best_snippet = p

            results.append({
                "source": md_file.name,
                "title": md_file.stem,
                "score": score + (max_p_score * 5),
                "type": "text_search",
                "text": best_snippet[:1200] if best_snippet else content[:800]
            })

    results.sort(key=lambda x: x["score"], reverse=True)
    return results[:top_k]


def vector_search_chroma(query: str, top_k: int = 5) -> List[Dict[str, Any]]:
    """Busca vetorial profunda na base ChromaDB utilizando embeddings e reranking MMR."""
    if not CHROMA_DIR.exists():
        return []

    try:
        if str(RAG_ROOT) not in sys.path:
            sys.path.insert(0, str(RAG_ROOT))
        
        from src.vectorstore import ChromaStore
        from src.retrieval import retrieve

        store = ChromaStore(persist_dir=str(CHROMA_DIR))
        raw_results = retrieve(query=query, k=top_k, rerank_method="mmr", store=store)
        
        formatted = []
        for r in raw_results:
            meta = r.get("metadata", {})
            formatted.append({
                "source": meta.get("source", "ChromaDB"),
                "title": meta.get("title", "Lição Copy Camp"),
                "chunk_index": meta.get("chunk_index"),
                "total_chunks": meta.get("total_chunks"),
                "type": "vector_rag",
                "similarity_score": r.get("similarity_score", 0.0),
                "text": r.get("text", "")
            })
        return formatted
    except Exception as e:
        # Se houver erro ou timeout no ChromaDB/embeddings, faz fallback limpo
        return []


def handle(query: str, top_k: int = 5, use_vector: bool = True) -> Dict[str, Any]:
    """
    Função principal que orquestra a busca na base de conhecimento do Beto Copy.
    Tenta busca vetorial se use_vector=True, complementada com busca textual.
    """
    vector_results = []
    if use_vector:
        vector_results = vector_search_chroma(query, top_k=top_k)

    text_results = text_search_processed(query, top_k=top_k)

    # Se vetorial retornou resultados, usa vetorial como primário e adiciona referências textuais
    combined = []
    seen_texts = set()

    for r in vector_results:
        snippet_hash = r.get("text", "")[:100]
        if snippet_hash not in seen_texts:
            seen_texts.add(snippet_hash)
            combined.append(r)

    for r in text_results:
        snippet_hash = r.get("text", "")[:100]
        if snippet_hash not in seen_texts and len(combined) < top_k * 2:
            seen_texts.add(snippet_hash)
            combined.append(r)

    return {
        "status": "success",
        "query": query,
        "total_results": len(combined),
        "results": combined[:top_k]
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Consulta a base de conhecimento de Copywriting do Beto Altenhofen / Empiricus")
    parser.add_argument("query", type=str, help="Pergunta, tema ou termo de copy para buscar")
    parser.add_argument("--k", type=int, default=3, help="Quantidade máxima de resultados a retornar")
    parser.add_argument("--no-vector", action="store_true", help="Desabilitar busca vetorial e usar apenas textual")
    args = parser.parse_args()

    res = handle(args.query, top_k=args.k, use_vector=not args.no_vector)
    print(json.dumps(res, indent=2, ensure_ascii=False))
