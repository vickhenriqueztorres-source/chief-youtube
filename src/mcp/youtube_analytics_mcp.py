# -*- coding: utf-8 -*-
"""
Hermes Chief - Model Context Protocol (MCP) Server
Exposes YouTube Analytics intelligence, quantitative diagnostics, packaging auditing,
and squad briefing capabilities as MCP tools over stdio JSON-RPC.
"""

import sys
import os
import json
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
# This guarantees that rogue print() calls never corrupt the JSON-RPC stream.
_rpc_stdout = sys.stdout
sys.stdout = sys.stderr

# Ensure root dir is in sys.path
root_dir = Path(__file__).resolve().parent.parent.parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

from src.core.agent import chief_agent
from src.core.memory import chief_memory
from src.core.trading_agent import chief_trading_agent
from src.core.trading_memory import trading_memory

MCP_TOOLS = [
    {
        "name": "mine_spontaneous_language",
        "description": "Minera a linguagem espontânea do público (Passo 2 de Eugene Schwartz / Voice of Customer): extrai citações viscerais, dores, dúvidas não respondidas de concorrentes e mitos populares via YouTube Suggest, comentários reais e fóruns.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "channel_slug": {
                    "type": "string",
                    "enum": ["o_outro_lado", "hidden_systems_lab", "brecha", "linha_de_fogo"],
                    "description": "Canal alvo."
                },
                "topic": {
                    "type": "string",
                    "description": "Opcional: tema ou dor específica para pesquisar nos comentários e buscas."
                }
            },
            "required": ["channel_slug"]
        }
    },
    {
        "name": "plan_discovery_ecosystem",
        "description": "Projeta o ecossistema integrado de 7 peças de descoberta multi-frente (Busca, Home, Shorts de Descoberta, Shorts de Problema, Playlist, Comunidade e Distribuição Externa) segundo a regra 80/20 do YouTube Chief.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "channel_slug": {
                    "type": "string",
                    "enum": ["o_outro_lado", "hidden_systems_lab", "brecha", "linha_de_fogo"],
                    "description": "Canal alvo."
                },
                "topic": {
                    "type": "string",
                    "description": "Opcional: tema ou título do episódio para projetar o ecossistema multi-frente."
                }
            },
            "required": ["channel_slug"]
        }
    },
    {
        "name": "analyze_channel_live",
        "description": "Rastreia o canal do YouTube em tempo real, extrai inscritos reais, estatísticas de vídeos (médias, medianas, desvio padrão, Z-scores), detecta anomalias/outliers virais e vídeos estagnados, identifica clusters de palavras-chave, pontes Shorts->Longos e injeta automaticamente esse aprendizado na memória SQLite FTS5 para tomada de decisão cirúrgica.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "channel_slug": {
                    "type": "string",
                    "enum": ["o_outro_lado", "hidden_systems_lab", "brecha", "all"],
                    "description": "Canal alvo a rastrear em tempo real ou 'all' para todos os 3 canais."
                }
            },
            "required": ["channel_slug"]
        }
    },
    {
        "name": "sync_channel_metrics",
        "description": "Sincroniza vídeos, contagem de visualizações e formatos (Longs vs Shorts) em tempo real direto do YouTube para os canais.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "channel_slug": {
                    "type": "string",
                    "enum": ["o_outro_lado", "hidden_systems_lab", "brecha", "all"],
                    "description": "Canal alvo a sincronizar ou 'all' para todos os 3 canais."
                }
            },
            "required": ["channel_slug"]
        }
    },
    {
        "name": "get_channel_metrics",
        "description": "Ingere e calcula métricas consolidadas de um dos 3 canais documentais (O Outro Lado, HSL, Brecha).",
        "inputSchema": {
            "type": "object",
            "properties": {
                "channel_slug": {
                    "type": "string",
                    "enum": ["o_outro_lado", "hidden_systems_lab", "brecha", "linha_de_fogo"],
                    "description": "Identificador do canal alvo"
                }
            },
            "required": ["channel_slug"]
        }
    },
    {
        "name": "diagnose_channel",
        "description": "Diagnostica o gargalo algorítmico primário do canal (Descoberta, Embalagem, Retenção, Cohorte Fantasma) e gera hipótese de experimento de 14 dias.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "channel_slug": {
                    "type": "string",
                    "enum": ["o_outro_lado", "hidden_systems_lab", "brecha", "linha_de_fogo"]
                }
            },
            "required": ["channel_slug"]
        }
    },
    {
        "name": "evaluate_themes",
        "description": "Prioriza a fila de próximos temas aplicando a equação quantitativa P = D x C x R x E e filtro de segurança editorial.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "channel_slug": {
                    "type": "string",
                    "enum": ["o_outro_lado", "hidden_systems_lab", "brecha", "linha_de_fogo"]
                }
            },
            "required": ["channel_slug"]
        }
    },
    {
        "name": "audit_packaging",
        "description": "Audita a embalagem de thumbnail + título segundo as 4 dimensões (Clareza, Desejo, Diferenciação, Coerência) com escala 0 a 100.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "channel_slug": {"type": "string", "enum": ["o_outro_lado", "hidden_systems_lab", "brecha", "linha_de_fogo"]},
                "title": {"type": "string", "description": "Título do vídeo"},
                "thumbnail_description": {"type": "string", "description": "Descrição dos elementos visuais da thumbnail"},
                "thumbnail_text": {"type": "string", "description": "Texto escrito na thumbnail (máximo 3-4 palavras)"}
            },
            "required": ["channel_slug", "title", "thumbnail_description"]
        }
    },
    {
        "name": "generate_squad_briefing",
        "description": "Emite briefing técnico padronizado em JSON para os squads de edição (O Outro Lado, HSL, Brecha).",
        "inputSchema": {
            "type": "object",
            "properties": {
                "channel_slug": {"type": "string", "enum": ["o_outro_lado", "hidden_systems_lab", "brecha", "linha_de_fogo"]},
                "episode_id": {"type": "string", "description": "Código do episódio (ex: EP_021)"}
            },
            "required": ["channel_slug", "episode_id"]
        }
    },
    {
        "name": "query_chief_memory",
        "description": "Consulta a memória persistente SQLite FTS5 de aprendizados históricos, hipóteses validadas e métricas reais.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "Termo de busca na memória"},
                "channel": {"type": "string", "description": "Opcional: filtrar por canal específico"}
            },
            "required": ["query"]
        }
    },
    {
        "name": "check_topic_coverage",
        "description": "Verifica se uma pauta/tema já foi publicada ou está em produção no canal, evitando duplicatas e fadiga de audiência.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "channel_slug": {"type": "string", "enum": ["o_outro_lado", "hidden_systems_lab", "brecha", "linha_de_fogo"]},
                "topic": {"type": "string", "description": "Tema ou título proposto para teste"},
                "thesis": {"type": "string", "description": "Opcional: tese ou premissa do vídeo para checagem semântica aprofundada"}
            },
            "required": ["channel_slug", "topic"]
        }
    },
    {
        "name": "list_covered_themes",
        "description": "Lista todos os temas cobertos, vídeos publicados e pautas em produção com status de ciclo de vida.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "channel_slug": {"type": "string", "enum": ["o_outro_lado", "hidden_systems_lab", "brecha", "linha_de_fogo"], "description": "Opcional: filtrar por canal"},
                "status": {"type": "string", "enum": ["PUBLISHED", "IN_PRODUCTION", "BRIEFING_ISSUED", "SCRAPPED"], "description": "Opcional: filtrar por status"}
            }
        }
    },
    {
        "name": "sync_covered_themes",
        "description": "Sincroniza todos os vídeos dos baselines e crawlers para o catálogo permanente de temas cobertos.",
        "inputSchema": {
            "type": "object",
            "properties": {}
        }
    },
    {
        "name": "research_niches",
        "description": "Pesquisa nichos monetizáveis para canais faceless no YouTube com Gate de Monetização YPP (bloqueio automático de reused content, inauthentic content, direitos autorais e conformidade com requisitos YPP 2026/2027).",
        "inputSchema": {
            "type": "object",
            "properties": {
                "region": {
                    "type": "string",
                    "default": "BR+US",
                    "description": "Região de análise de tendências (ex: 'BR+US', 'BR', 'US')."
                },
                "territory_filter": {
                    "type": "string",
                    "description": "Opcional: filtrar por território específico ('financas_investimentos', 'golpes_seguranca_digital', 'ia_automacao_saas', 'saude_longevidade_50', 'educacao_ciencia_engenharia', 'historia_misterio_docs')."
                }
            }
        }
    },
    {
        "name": "reverse_engineer_channels",
        "description": "Executa engenharia reversa de canais no YouTube (Brasil e Global / EUA e UK), extraindo padrões estruturais (hook, roteiro, thumbnail, título, cadência) para guiar a criação de 2 novos canais faceless monetizáveis (CPM > $5).",
        "inputSchema": {
            "type": "object",
            "properties": {
                "region_focus": {
                    "type": "string",
                    "default": "BR+GLOBAL",
                    "description": "Foco regional ('BR+GLOBAL', 'BR', 'GLOBAL')."
                }
            }
        }
    }
]

def is_trading_channel(ch: Optional[str]) -> bool:
    if not ch:
        return False
    c = str(ch).lower()
    return "profe" in c or "vela" in c or "trading" in c

def handle_call_tool(name: str, args: dict) -> dict:
    if name == "mine_spontaneous_language":
        ch = args.get("channel_slug", "brecha")
        top = args.get("topic")
        res = chief_agent.research_spontaneous_language(ch, top)
        return {"content": [{"type": "text", "text": json.dumps(res, ensure_ascii=False, indent=2)}]}

    elif name == "plan_discovery_ecosystem":
        ch = args.get("channel_slug", "o_outro_lado")
        top = args.get("topic")
        if is_trading_channel(ch):
            res = chief_trading_agent.plan_discovery_ecosystem(ch, top or "Leitura de Velas em Demo")
        else:
            res = chief_agent.plan_discovery_ecosystem(ch, top)
        return {"content": [{"type": "text", "text": json.dumps(res, ensure_ascii=False, indent=2)}]}

    elif name == "analyze_channel_live":
        ch = args.get("channel_slug", "all")
        if is_trading_channel(ch):
            res = chief_trading_agent.live_sync(ch)
        elif ch == "all":
            res = chief_agent.run_live_intelligence_all()
        else:
            res = chief_agent.run_live_intelligence(ch)
        return {"content": [{"type": "text", "text": json.dumps(res, ensure_ascii=False, indent=2)}]}

    elif name == "sync_channel_metrics":
        ch = args.get("channel_slug", "all")
        if is_trading_channel(ch):
            res = chief_trading_agent.live_sync(ch)
        elif ch == "all":
            res = chief_agent.sync_all()
        else:
            res = chief_agent.sync_channel(ch)
        return {"content": [{"type": "text", "text": json.dumps(res, ensure_ascii=False, indent=2)}]}

    elif name == "get_channel_metrics":
        ch = args.get("channel_slug")
        if is_trading_channel(ch):
            raw = chief_trading_agent.get_channel_data(ch)
            summary = chief_trading_agent.metrics_reader.analyze_channel(raw)
        else:
            raw = chief_agent.get_channel_data(ch)
            summary = chief_agent.metrics_reader.analyze_channel(raw)
        return {"content": [{"type": "text", "text": json.dumps(summary, ensure_ascii=False, indent=2)}]}

    elif name == "diagnose_channel":
        ch = args.get("channel_slug")
        if is_trading_channel(ch):
            audit = chief_trading_agent.audit_channel(ch)
            diag = audit["diagnosis"]
        else:
            raw = chief_agent.get_channel_data(ch)
            metrics = chief_agent.metrics_reader.analyze_channel(raw)
            diag = chief_agent.diagnostic.diagnose(ch, metrics)
        return {"content": [{"type": "text", "text": json.dumps(diag, ensure_ascii=False, indent=2)}]}

    elif name == "evaluate_themes":
        ch = args.get("channel_slug")
        if is_trading_channel(ch):
            themes = chief_trading_agent.evaluate_themes(ch)
        else:
            themes = chief_agent.decide_themes(ch)
        return {"content": [{"type": "text", "text": json.dumps(themes, ensure_ascii=False, indent=2)}]}

    elif name == "audit_packaging":
        ch = args.get("channel_slug")
        if is_trading_channel(ch):
            res = chief_trading_agent.audit_thumbnail(
                channel_slug=ch,
                title=args.get("title"),
                thumb_desc=args.get("thumbnail_description"),
                thumb_text=args.get("thumbnail_text", "")
            )
        else:
            res = chief_agent.audit_thumbnail(
                channel_slug=ch,
                title=args.get("title"),
                thumb_description=args.get("thumbnail_description"),
                thumb_text=args.get("thumbnail_text", "")
            )
        return {"content": [{"type": "text", "text": json.dumps(res, ensure_ascii=False, indent=2)}]}

    elif name == "generate_squad_briefing":
        ch = args.get("channel_slug")
        if is_trading_channel(ch):
            custom_p = args.get("custom_params")
            top_over = custom_p.get("topic", "") if isinstance(custom_p, dict) else ""
            res = chief_trading_agent.generate_briefing(
                channel_slug=ch,
                episode_id=args.get("episode_id", "EP_001"),
                topic_override=top_over
            )
        else:
            res = chief_agent.generate_briefing(
                channel_slug=ch,
                episode_id=args.get("episode_id"),
                custom_params=args.get("custom_params")
            )
        return {"content": [{"type": "text", "text": json.dumps(res, ensure_ascii=False, indent=2)}]}

    elif name == "query_chief_memory":
        ch = args.get("channel")
        if is_trading_channel(ch):
            res = trading_memory.search_memory(query=args.get("query"), channel=ch)
        else:
            res = chief_agent.search_memory(query=args.get("query"), channel=ch)
        return {"content": [{"type": "text", "text": json.dumps(res, ensure_ascii=False, indent=2)}]}

    elif name == "check_topic_coverage":
        ch = args.get("channel_slug")
        top = args.get("topic")
        the = args.get("thesis", "")
        if is_trading_channel(ch):
            res = trading_memory.check_topic_coverage(ch, top)
        else:
            res = chief_agent.check_topic_coverage(ch, top, the)
        return {"content": [{"type": "text", "text": json.dumps(res, ensure_ascii=False, indent=2)}]}

    elif name == "list_covered_themes":
        ch = args.get("channel_slug")
        st = args.get("status")
        if is_trading_channel(ch):
            res = trading_memory.list_covered_themes(ch, st)
        else:
            res = chief_agent.list_covered_themes(ch, st)
        return {"content": [{"type": "text", "text": json.dumps(res, ensure_ascii=False, indent=2)}]}

    elif name == "sync_covered_themes":
        res = chief_agent.sync_covered_themes()
        return {"content": [{"type": "text", "text": json.dumps(res, ensure_ascii=False, indent=2)}]}

    elif name == "research_niches":
        reg = args.get("region", "BR+US")
        terr = args.get("territory_filter")
        res = chief_agent.research_niches(region=reg, territory_filter=terr)
        return {"content": [{"type": "text", "text": json.dumps(res, ensure_ascii=False, indent=2)}]}

    elif name == "reverse_engineer_channels":
        reg = args.get("region_focus", "BR+GLOBAL")
        res = chief_agent.reverse_engineer_channels(region_focus=reg)
        return {"content": [{"type": "text", "text": json.dumps(res, ensure_ascii=False, indent=2)}]}

    else:
        raise ValueError(f"Ferramenta desconhecida: {name}")

def main():
    """Simple JSON-RPC 2.0 stdio server loop for MCP."""
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            req = json.loads(line)
            req_id = req.get("id")
            method = req.get("method")

            # Ignore notifications (calls without id) per JSON-RPC 2.0 spec
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
                        "serverInfo": {"name": "hermes-chief-quant", "version": "1.0.0"},
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
