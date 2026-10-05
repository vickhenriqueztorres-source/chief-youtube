# -*- coding: utf-8 -*-
"""
Hermes Chief - Command Line Interface (CLI)
Provides rich interactive console and scriptable commands for the Chief Analyst.
"""

import sys
import os
import io
import json
import argparse
from pathlib import Path
from typing import Optional, List, Dict, Any

# Safe UTF-8 output on Windows consoles
try:
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    if hasattr(sys.stderr, 'reconfigure'):
        sys.stderr.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass

# Ensure root in sys.path
root_dir = Path(__file__).resolve().parent.parent.parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

from src.core.agent import chief_agent

ASCII_BANNER = r"""
╔══════════════════════════════════════════════════════════════════════════════╗
║   Ψ  HERMES CHIEF // STRATEGIC YOUTUBE INTELLIGENCE (QUANT ENGINE)  Ψ       ║
║   O OUTRO LADO  •  HIDDEN SYSTEMS LAB (HSL)  •  BRECHA DEFESA DIGITAL       ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

def print_separator(char="─", length=76):
    print(char * length)

def cmd_audit(channel_slug: str):
    print(f"\n🚀 EXECUTANDO AUDITORIA QUANT // CANAL: {channel_slug.upper()}")
    print_separator()
    res = chief_agent.audit_channel(channel_slug)
    
    metrics = res["metrics"]
    diag = res["diagnosis"]
    long_stats = metrics["long_form_summary"]
    short_stats = metrics["shorts_summary"]

    print(f"📊 MÉTRICAS CONSOLIDADAS:")
    print(f"  • Inscritos Atuais: {metrics.get('subscribers')} | Total Vídeos Analisados: {metrics.get('total_videos_analyzed')}")
    print(f"  • Vídeos Longos: {long_stats.get('count')} uploads | Média Views: {long_stats.get('mean_views')} | CTR Médio: {long_stats.get('mean_ctr')}%")
    print(f"  • Retenção aos 30s: {long_stats.get('mean_retention_30s')}% | Duração Média (AVD): {long_stats.get('mean_avd_pct')}%")
    print(f"  • Tendência Macro: {long_stats.get('trend')} | Média Móvel (Últimos 3): {long_stats.get('rolling_avg_3_latest')}")
    print(f"  • Shorts: {short_stats.get('count')} uploads | Média Views: {short_stats.get('mean_views')} | Razão Longo/Short: {metrics.get('shorts_to_long_ratio')}")
    
    print_separator()
    bot = diag["primary_bottleneck"]
    print(f"🚨 DIAGNÓSTICO DO GARGALO PRIMÁRIO:")
    print(f"  • Gargalo: {bot['name']}")
    print(f"  • Sintoma: {bot['symptom']}")
    print(f"  • Causa Raiz: {bot['root_cause']}")

    exp = diag["proposed_experiment"]
    print_separator()
    print(f"🧪 EXPERIMENTO DE 14 DIAS (MÉTODO X + Y):")
    print(f"  • Hipótese: {exp['hypothesis']}")
    print(f"  • Plano de Ação:")
    for a in exp["test_design"]:
        print(f"     {a}")
    print(f"  • Metas:")
    for k, v in exp["metric_targets"].items():
        print(f"     - {k}: {v}")
    print(f"  • Veredito de Sucesso: {exp['success_decision']}")

    print_separator()
    print(f"🎯 TOP 3 TEMAS PRIORIZADOS (EQUAÇÃO P = D x C x R x E):")
    for i, t in enumerate(res["top_themes"], 1):
        print(f"  [{i}] [{t['priority']}] {t['topic']} (P={t['p_score']}/625 | S={t['s_score']})")
        print(f"      Tese: {t['thesis']}")
        print(f"      Gancho 0-15s: {t['hook_suggestion']}")

def cmd_thumb(channel_slug: str, title: str, thumb_desc: str, thumb_text: str = ""):
    print(f"\n👁️ AUDITORIA DE EMBALAGEM // {channel_slug.upper()}")
    print_separator()
    res = chief_agent.audit_thumbnail(channel_slug, title, thumb_desc, thumb_text)
    
    scores = res["scores"]
    print(f"Título Avaliado: {title}")
    print(f"Descrição da Thumb: {thumb_desc}")
    if thumb_text:
        print(f"Texto na Thumb: '{thumb_text}'")
    print_separator()
    print(f"PONTUAÇÕES (0 a 10):")
    print(f"  • Clareza: {scores['clareza']}/10 | Desejo: {scores['desejo']}/10")
    print(f"  • Diferenciação: {scores['diferenciacao']}/10 | Coerência: {scores['coerencia']}/10")
    print(f"  • ÍNDICE GERAL DE EMBALAGEM: {scores['overall_index']}/100")
    print_separator()
    print(f"VEREDITO: {res['recommendation']}")
    print(f"Diagnóstico: {'; '.join(res['diagnostic_reasons'])}")
    print(f"Ajustes Recomendados: {'; '.join(res['actionable_tweaks'])}")

def cmd_themes(channel_slug: str):
    print(f"\n📋 FILA DE TEMAS QUANT // {channel_slug.upper()}")
    print_separator()
    res = chief_agent.decide_themes(channel_slug)
    print(f"Diretriz Estratégica: {res['strategic_recommendation']}\n")
    for i, t in enumerate(res["full_evaluation_list"], 1):
        print(f"#{i:02d} [{t['priority']}] P={t['p_score']:3d} | S={t['s_score']:2d} -> {t['topic']}")
        print(f"    Unidade: {t['unit']}")
        print(f"    Fatores: D={t['factors']['D']} C={t['factors']['C']} R={t['factors']['R']} E={t['factors']['E']}")
        print(f"    Tese: {t['thesis']}")

def cmd_briefing(channel_slug: str, episode_id: str, custom_tema: str = ""):
    print(f"\n📦 GERANDO BRIEFING OFICIAL DO SQUAD // {channel_slug.upper()} [{episode_id}]")
    print_separator()
    params = {"tema": custom_tema} if custom_tema else None
    res = chief_agent.generate_briefing(channel_slug, episode_id, params)
    print(f"Briefing gerado com sucesso!")
    print(f"Arquivo salvo em: {res['saved_path']}")
    print_separator()
    print(json.dumps(res, indent=2, ensure_ascii=False))

def cmd_memory(query: str, channel_slug: str = None):
    print(f"\n🧠 CONSULTA À MEMÓRIA PERSISTENTE FTS5 // TERMO: '{query}'")
    print_separator()
    res = chief_agent.search_memory(query, channel_slug, limit=10)
    if not res:
        print("Nenhum registro encontrado no FTS5.")
        return
    for i, r in enumerate(res, 1):
        ch = r.get("channel", "global").upper()
        cat = r.get("category", "geral").upper()
        print(f"[{i}] [{ch} // {cat}]")
        print(f"    {r.get('content', '')}")
        if r.get("evidence"):
            print(f"    Evidência: {r.get('evidence')}")
        print()

def cmd_report():
    print(f"\n📑 GERANDO RELATÓRIO EXECUTIVO MULTI-CANAL...")
    print_separator()
    rep = chief_agent.generate_full_executive_summary()
    print(f"Total Experimentos Ativos: {rep['active_experiments_count']}")
    for ch, data in rep["channels_audited"].items():
        if "error" in data:
            print(f"\n❌ Canal: {ch.upper()} - Erro: {data['error']}")
            continue
        long_s = data["metrics"]["long_form_summary"]
        p_bot = data["diagnosis"]["primary_bottleneck"]
        print(f"\n🛰️ Canal: {ch.upper()} ({data['channel_info'].get('handle')})")
        print(f"   • Subs: {data['metrics']['subscribers']} | Vídeos: {data['metrics']['total_videos_analyzed']}")
        print(f"   • Gargalo: {p_bot['name']}")
        print(f"   • Top P0: {data['top_themes'][0]['topic']} (P={data['top_themes'][0]['p_score']})")

def cmd_sync(channel_slug: str = "all", csv_path: Optional[str] = None):
    print(f"\n📡 SINCRONIZAÇÃO EM TEMPO REAL // YOUTUBE")
    print_separator()
    slug = (channel_slug or "all").lower()
    if slug in ["all", "todos"]:
        print("Sincronizando todos os 3 canais gerenciados via YouTube...")
        results = chief_agent.sync_all()
        for s, res in results.items():
            print(f"  • {res['channel_name']}: {res['total_videos_catalog']} vídeos catalogados ({res['updated_views_count']} atualizados, {res['new_videos_inserted']} novos inseridos)")
    else:
        res = chief_agent.sync_channel(slug, csv_path=csv_path)
        print(f"Canal: {res['channel_name']}")
        print(f"Total de Vídeos no Catálogo: {res['total_videos_catalog']}")
        print(f"Visualizações Atualizadas: {res['updated_views_count']}")
        print(f"Novos Vídeos Inseridos: {res['new_videos_inserted']}")
        if res.get('csv_records_merged'):
            print(f"Registros de CSV (CTR/Retenção) Mesclados: {res['csv_records_merged']}")
        print(f"Arquivo Atualizado: {res['baseline_path']}")
    print_separator()
    print("✅ Sincronização concluída com sucesso! Os dados mais recentes estão prontos para análise.\n")

def cmd_live(channel_slug: str = "all"):
    slug = (channel_slug or "all").lower()
    if slug in ["all", "todos"]:
        print(f"\n🛰️ DOSSIÊ DE INTELIGÊNCIA EM TEMPO REAL // TODOS OS CANAIS")
        print_separator()
        results = chief_agent.run_live_intelligence_all()
        for s, res in results.items():
            _print_single_live_dossier(res)
    else:
        print(f"\n🛰️ DOSSIÊ DE INTELIGÊNCIA EM TEMPO REAL // {slug.upper()}")
        print_separator()
        res = chief_agent.run_live_intelligence(slug)
        _print_single_live_dossier(res)

def _print_single_live_dossier(res: dict):
    print(f"📡 CANAL: {res['channel_name']} ({res['handle']})")
    print(f"  • Inscritos ao Vivo: {res['live_subscribers']}")
    print(f"  • Catálogo Analisado: {res['total_videos_analyzed']} vídeos | Total de Views: {res['total_catalog_views']:,}")
    
    long_s = res["long_videos_stats"]
    short_s = res["shorts_stats"]
    print(f"  • Longos: {long_s['count']} vídeos | Média: {long_s['mean_views']} views | Mediana: {long_s['median_views']} | Desvio (σ): {long_s['std_dev_views']}")
    print(f"  • Shorts: {short_s['count']} vídeos | Média: {short_s['mean_views']} views | Razão Shorts/Longos: {res['shorts_to_long_ratio']}x")
    
    print_separator("-", 60)
    print("🔥 ANOMALIAS & OUTLIERS DETECTADOS:")
    if long_s["viral_outliers"]:
        for out in long_s["viral_outliers"]:
            print(f"  [VIRAL Z≥1.5] '{out['title'][:45]}...' ➔ {out['views']} views (Z={out['z_score']})")
    else:
        print("  • Nenhum outlier viral detectado em longos.")
    print(f"  • Vídeos Estagnados (≤5 views): {len(long_s['stalled_videos'])} títulos")

    if res.get("keyword_clusters"):
        print_separator("-", 60)
        print("🏷️ TOP CLUSTERS DE PALAVRAS-CHAVE:")
        for k in res["keyword_clusters"][:4]:
            print(f"  • '{k['keyword'].upper()}': média de {k['mean_views']} views ({k['frequency']} vídeos | pico: {k['max_views']})")

    if res.get("bridge_opportunities"):
        print_separator("-", 60)
        print("🌉 PONTES SHORTS ➔ LONGOS (Ação YouTube Studio):")
        for b in res["bridge_opportunities"][:3]:
            print(f"  • Short: '{b['short_title'][:40]}...' ({b['short_views']} views)")
            print(f"    ➔ Vincular como Vídeo Relacionado de: '{b['recommended_master_video']}'")

    bot = res["primary_bottleneck"]
    print_separator("-", 60)
    print("🚨 DIAGNÓSTICO EM TEMPO REAL:")
    print(f"  • Gargalo: {bot['name']}")
    print(f"  • Sintoma: {bot['symptom']}")
    print(f"  • Diretriz Cirúrgica: {bot['action']}")

    print_separator("-", 60)
    print("🎯 TOP PAUTAS P0 RECOMENDADAS PARA PRODUÇÃO:")
    for i, t in enumerate(res.get("top_p0_themes", []), 1):
        print(f"  [{i}] [P0] {t.get('topic')} (P={t.get('p_score')}/625)")
        print(f"      Tese: {t.get('thesis')}")

    print_separator("-", 60)
    print(f"🧠 Memória Atualizada: {res['memory_patterns_ingested']} padrões injetados no SQLite FTS5.")
    print_separator()

def cmd_ecosystem(channel_slug: str = "o_outro_lado", topic: str = ""):
    ch = (channel_slug or "o_outro_lado").lower()
    if ch == "outro_lado": ch = "o_outro_lado"
    elif ch == "hsl": ch = "hidden_systems_lab"

    eco = chief_agent.plan_discovery_ecosystem(ch, topic if topic else None)
    p = eco["ecosystem_pieces"]

    print(f"\n🌐 ECOSSISTEMA INTEGRADO DE DESCOBERTA // {eco['channel'].upper()}")
    print_separator()
    print(f"🎯 Tema Central: {eco['topic']}")
    print(f"👤 Público-Alvo: {eco['target_audience']}")
    print(f"🔥 Desejo Dominante: {eco['core_desire']}")
    print_separator("-", 60)
    print("AS 7 PEÇAS COORDENADAS DE DISTRIBUIÇÃO:")
    print(f"\n[1] BUSCA (Intenção Existente):")
    print(f"    • Título: \"{p['1_long_for_search']['title']}\"")
    print(f"    • Estrutura: {p['1_long_for_search']['structure']}")
    print(f"    • Regra 15s: {p['1_long_for_search']['first_15s_rule']}")
    print(f"\n[2] PÁGINA INICIAL / HOME (Recomendação & Paradoxo):")
    print(f"    • Título: \"{p['2_long_for_browse']['title']}\"")
    print(f"    • Conceito Visual: {p['2_long_for_browse']['thumbnail_concept']}")
    print(f"\n[3] SHORT 1 (Descoberta & Prova Forense):")
    print(f"    • Título: \"{p['3_short_discovery']['title']}\"")
    print(f"    • Gancho (0-2s): {p['3_short_discovery']['timing_breakdown']['0:00 - 0:02']}")
    print(f"    • Conexão: {p['3_short_discovery']['related_video_link']}")
    print(f"\n[4] SHORT 2 (Problema & Erro Oculto):")
    print(f"    • Título: \"{p['4_short_problem']['title']}\"")
    print(f"\n[5] PLAYLIST (Percurso de Transformação):")
    print(f"    • Título da Série: \"{p['5_playlist_architecture']['playlist_title']}\"")
    print(f"    • Mecanismo de Sessão: {p['5_playlist_architecture']['retention_mechanic']}")
    print(f"\n[6] COMUNIDADE (Validação Prévia 48h antes):")
    print(f"    • Enquete: \"{p['6_community_post']['poll_question']}\"")
    print(f"\n[7] DISTRIBUIÇÃO EXTERNA (Reddit, LinkedIn, Discord):")
    print(f"    • Copy Técnica: {p['7_external_distribution']['copy_sample']}")
    print_separator("-", 60)
    print("📊 REGRA 80/20 DE DESCOBERTA:")
    print("    • 40% Busca (Perenidade) | 30% Recomendação/Home (Pico) | 20% Shorts (Ponte) | 10% Externo (Qualificado)")
    print_separator()

def cmd_voice(channel_slug: str = "brecha", topic: str = ""):
    ch = (channel_slug or "brecha").lower()
    if ch == "outro_lado": ch = "o_outro_lado"
    elif ch == "hsl": ch = "hidden_systems_lab"

    print(f"\n🗣️ MINERAÇÃO DE LINGUAGEM ESPONTÂNEA (VOZ DO CLIENTE) // {ch.upper()}")
    print_separator()
    print("🛰️ Coletando buscas em tempo real e comentários de vídeos concorrentes...")

    res = chief_agent.research_spontaneous_language(ch, topic if topic else None)
    voc = res["voice_of_customer"]
    anchors = res["script_anchors"]

    print(f"🎯 Tema / Dor Investigada: {res['topic']}")
    print(f"📹 Vídeos de Concorrentes Escaneados: {len(res['competitor_videos_analyzed'])}")
    print(f"💬 Comentários Reais Minerados: {res['total_real_comments_parsed']}")

    if res["searches_in_youtube_autocomplete"]:
        print_separator("-", 60)
        print("🔎 O QUE O PÚBLICO DIGITA NO YOUTUBE (Auto-Complete em Tempo Real):")
        for s in res["searches_in_youtube_autocomplete"][:6]:
            print(f"  • \"{s}\"")

    print_separator("-", 60)
    print("🔥 CITAÇÕES VISCERAIS DO PÚBLICO (Para o Gancho de 0-15s):")
    for q in voc["visceral_quotes_for_hook"][:3]:
        print(f"  • {q}")

    print_separator("-", 60)
    print("❓ DÚVIDAS NÃO RESPONDIDAS NOS CONCORRENTES (A Brecha do Seu Vídeo):")
    for d in voc["unresolved_competitor_doubts"][:3]:
        print(f"  • {d}")

    print_separator("-", 60)
    print("🛡️ MITOS E FALSAS SEGURANÇAS A DESMASCARAR (Ato 2):")
    for m in voc["popular_myths_to_debunk"][:3]:
        print(f"  • {m}")

    print_separator("-", 60)
    print("💡 DIRETRIZES CIRÚRGICAS PARA O ROTEIRISTA:")
    print(f"  • Abertura: {anchors['hook_0_15s_recommendation']}")
    print(f"  • Miolo: {anchors['act_2_counterpoint']}")
    print(f"  • Conclusão: {anchors['act_3_unanswered_gap']}")
    print_separator()

def interactive_loop():
    print(ASCII_BANNER)
    print("Modo Interativo do Chief Analyst ativado.")
    print("Comandos disponíveis: 'live <canal>', 'audit <canal>', 'thumb <canal>', 'themes <canal>', 'briefing <canal>', 'memory <termo>', 'report', 'ajuda', 'sair'.\n")
    
    while True:
        try:
            cmd_line = input("CHIEF [quant] ➔ ").strip()
            if not cmd_line:
                continue
            if cmd_line.lower() in ["sair", "exit", "quit", "q"]:
                print("Encerrando sessão do Chief Analyst. Integridade mantida.")
                break

            parts = cmd_line.split()
            action = parts[0].lower()

            if action in ["live", "realtime", "aovivo"]:
                ch = parts[1] if len(parts) > 1 else "all"
                cmd_live(ch)

            elif action in ["audit", "auditar", "analise"]:
                ch = parts[1] if len(parts) > 1 else "o_outro_lado"
                cmd_audit(ch)

            elif action in ["themes", "temas"]:
                ch = parts[1] if len(parts) > 1 else "o_outro_lado"
                cmd_themes(ch)

            elif action in ["briefing", "brief"]:
                ch = parts[1] if len(parts) > 1 else "o_outro_lado"
                ep = parts[2] if len(parts) > 2 else "EP01"
                cmd_briefing(ch, ep)

            elif action in ["memory", "memoria", "busca"]:
                q = " ".join(parts[1:]) if len(parts) > 1 else "shorts"
                cmd_memory(q)

            elif action in ["ecosystem", "ecossistema", "descoberta"]:
                ch = parts[1] if len(parts) > 1 else "o_outro_lado"
                tema = " ".join(parts[2:]) if len(parts) > 2 else ""
                cmd_ecosystem(ch, tema)

            elif action in ["voice", "voz", "reclamacoes", "duvidas"]:
                ch = parts[1] if len(parts) > 1 else "brecha"
                tema = " ".join(parts[2:]) if len(parts) > 2 else ""
                cmd_voice(ch, tema)

            elif action in ["report", "relatorio"]:
                cmd_report()

            elif action in ["thumb", "thumbnail"]:
                ch = parts[1] if len(parts) > 1 else "o_outro_lado"
                title = input("Título do vídeo: ")
                desc = input("Descrição visual da thumb: ")
                txt = input("Texto escrito na thumb (opcional): ")
                cmd_thumb(ch, title, desc, txt)

            elif action == "sync":
                ch = parts[1] if len(parts) > 1 else "all"
                cmd_sync(ch)

            elif action in ["ajuda", "help"]:
                print("\nComandos:")
                print("  live [canal|all]                  -> Inteligência quantitativa em tempo real com dados ao vivo")
                print("  sync [canal|all]                  -> Sincronização automática de dados via YouTube")
                print("  audit <o_outro_lado|hsl|brecha>   -> Auditoria quantitativa completa")
                print("  themes <o_outro_lado|hsl|brecha>  -> Decisão de temas P0/P1/P2")
                print("  briefing <canal> <ep_id>          -> Emissão de briefing JSON para squad")
                print("  thumb <canal>                     -> Auditoria de thumbnail e título")
                print("  memory <busca>                    -> Consulta à memória FTS5")
                print("  report                            -> Relatório multi-canal consolidado")
                print("  sair                              -> Sair da CLI\n")

            else:
                # Conversational response
                response = chief_agent.answer_query(cmd_line)
                print(f"\n{response}\n")

        except (KeyboardInterrupt, EOFError):
            print("\nEncerrando sessão.")
            break
        except Exception as e:
            print(f"\n❌ Erro: {e}\n")

def main():
    parser = argparse.ArgumentParser(description="Hermes Chief - CLI de Inteligência Analítica para YouTube")
    subparsers = parser.add_subparsers(dest="subcommand")

    # Subcommand: live
    p_live = subparsers.add_parser("live", help="Executa inteligência quantitativa em tempo real direto do YouTube")
    p_live.add_argument("channel", nargs="?", default="all", choices=["o_outro_lado", "hidden_systems_lab", "brecha", "outro_lado", "hsl", "all"], help="Canal alvo ou 'all'")

    # Subcommand: sync
    p_sync = subparsers.add_parser("sync", help="Sincroniza vídeos e métricas em tempo real direto do YouTube")
    p_sync.add_argument("channel", nargs="?", default="all", choices=["o_outro_lado", "hidden_systems_lab", "brecha", "outro_lado", "hsl", "all"], help="Canal alvo ou 'all'")
    p_sync.add_argument("--csv", default=None, help="Caminho opcional para arquivo de exportação CSV do YouTube Studio")

    # Subcommand: audit
    p_audit = subparsers.add_parser("audit", help="Executa auditoria completa de um canal")
    p_audit.add_argument("channel", choices=["o_outro_lado", "hidden_systems_lab", "brecha", "outro_lado", "hsl"], help="Canal alvo")

    # Subcommand: themes
    p_themes = subparsers.add_parser("themes", help="Avalia e prioriza próximos temas")
    p_themes.add_argument("channel", choices=["o_outro_lado", "hidden_systems_lab", "brecha", "outro_lado", "hsl"], help="Canal alvo")

    # Subcommand: briefing
    p_brief = subparsers.add_parser("briefing", help="Gera briefing JSON para squad de edição")
    p_brief.add_argument("channel", choices=["o_outro_lado", "hidden_systems_lab", "brecha", "outro_lado", "hsl"], help="Canal alvo")
    p_brief.add_argument("episode_id", help="Identificador do episódio (ex: EP_020)")
    p_brief.add_argument("--tema", default="", help="Título ou tema customizado")

    # Subcommand: thumb
    p_thumb = subparsers.add_parser("thumb", help="Audita embalagem de thumbnail + título")
    p_thumb.add_argument("channel", help="Canal alvo")
    p_thumb.add_argument("title", help="Título do vídeo")
    p_thumb.add_argument("desc", help="Descrição visual da thumbnail")
    p_thumb.add_argument("--text", default="", help="Texto grafado na thumbnail")

    # Subcommand: memory
    p_mem = subparsers.add_parser("memory", help="Consulta memória FTS5")
    p_mem.add_argument("query", help="Termo de busca")
    p_mem.add_argument("--channel", default=None, help="Filtrar por canal")

    # Subcommand: ecosystem
    p_eco = subparsers.add_parser("ecosystem", help="Projeta o ecossistema integrado de 7 peças de descoberta multi-frente")
    p_eco.add_argument("channel", choices=["o_outro_lado", "hidden_systems_lab", "brecha", "outro_lado", "hsl"], help="Canal alvo")
    p_eco.add_argument("--tema", default="", help="Tema customizado para o ecossistema")

    # Subcommand: voice
    p_voice = subparsers.add_parser("voice", help="Minera linguagem espontânea, dores, dúvidas e mitos reais do público")
    p_voice.add_argument("channel", choices=["o_outro_lado", "hidden_systems_lab", "brecha", "outro_lado", "hsl"], help="Canal alvo")
    p_voice.add_argument("--tema", default="", help="Tema ou dor para minerar")

    # Subcommand: report
    subparsers.add_parser("report", help="Gera relatório consolidado dos 3 canais")

    # Subcommand: interactive
    subparsers.add_parser("interactive", help="Inicia console interativo com o Chief")

    args = parser.parse_args()

    if not args.subcommand or args.subcommand == "interactive":
        interactive_loop()
        return

    # Slug normalization
    ch_raw = getattr(args, "channel", None) or ""
    ch_slug = ch_raw.lower()
    if ch_slug == "outro_lado":
        ch_slug = "o_outro_lado"
    elif ch_slug == "hsl":
        ch_slug = "hidden_systems_lab"

    if args.subcommand == "live":
        cmd_live(ch_slug if ch_slug else "all")
    elif args.subcommand == "sync":
        cmd_sync(ch_slug if ch_slug else "all", getattr(args, "csv", None))
    elif args.subcommand == "audit":
        cmd_audit(ch_slug)
    elif args.subcommand == "themes":
        cmd_themes(ch_slug)
    elif args.subcommand == "briefing":
        cmd_briefing(ch_slug, args.episode_id, args.tema)
    elif args.subcommand == "thumb":
        cmd_thumb(ch_slug, args.title, args.desc, args.text)
    elif args.subcommand == "memory":
        cmd_memory(args.query, args.channel)
    elif args.subcommand == "ecosystem":
        cmd_ecosystem(ch_slug, getattr(args, "tema", ""))
    elif args.subcommand == "voice":
        cmd_voice(ch_slug, getattr(args, "tema", ""))
    elif args.subcommand == "report":
        cmd_report()

if __name__ == "__main__":
    main()
