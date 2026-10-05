# -*- coding: utf-8 -*-
"""
Handler da Skill de Edição Cinematográfica para Hermes Agent.
Conecta à base RAG local (SQLite FTS5 + ChromaDB) e recupera técnicas,
conceitos e transcrições com timestamps exatos dos maiores editores.
"""

import sys
import json
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

RAG_ROOT = Path("D:/CHIEF YOUTUBE/rag_cinematic_editing")
if not RAG_ROOT.exists():
    # Fallback dinâmico pelos parents
    for p in Path(__file__).resolve().parents:
        cand = p / "rag_cinematic_editing"
        if cand.exists():
            RAG_ROOT = cand
            break

if str(RAG_ROOT) not in sys.path:
    sys.path.insert(0, str(RAG_ROOT))

try:
    from search_rag import search
except Exception as e:
    search = None


def handle(query: str, top_k: int = 4, mode: str = "hybrid"):
    """Interface de consulta para o agente Hermes."""
    if not search:
        return {
            "status": "error",
            "message": "Módulo de busca search_rag não encontrado ou banco indisponível."
        }
    return search(query=query, top_k=top_k, mode=mode)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        q = " ".join(sys.argv[1:])
        res = handle(q, top_k=4)
        print(json.dumps(res, indent=2, ensure_ascii=False))
    else:
        print("Uso: python handler.py '<pergunta ou técnica de edição>'")
