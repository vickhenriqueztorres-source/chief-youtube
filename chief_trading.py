#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Hermes Chief Trading - Command Line Interface (CLI) Entrypoint
Dedicated quant strategic engine for YouTube Trading Channels (Canal 1: El Profe de Velas, Canal 2: Em preparação).
Completely decoupled from documentary channels.
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
root_dir = Path(__file__).resolve().parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

from src.core.trading_agent import chief_trading_agent
from src.core.trading_memory import trading_memory

TRADING_BANNER = r"""
╔══════════════════════════════════════════════════════════════════════════════╗
║   Ψ  HERMES CHIEF TRADING // ESTRATÉGIA QUANT & PEDAGOGIA FORENSE  Ψ        ║
║   CANAL 01: EL PROFE DE VELAS (@profedevelas)  │  CANAL 02: EL CAZADOR DEL WINS (@elcazadordelwins)
║   "A view não é um ativo. O trader disciplinado e a verificação são o ativo."║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

def print_separator(char="─", length=76):
    print(char * length)

def cmd_audit(channel_slug: str):
    print(f"\n🚀 EXECUTANDO AUDITORIA QUANT DE TRADING // CANAL: {channel_slug.upper()}")
    print_separator()
    res = chief_trading_agent.audit_channel(channel_slug)

    metrics = res["metrics"]
    diag = res["diagnosis"]
    long_stats = metrics["long_form_summary"]
    short_stats = metrics["shorts_summary"]

    print(f"📊 MÉTRICAS CONSOLIDADAS:")
    print(f"  • Canal: {metrics.get('channel_name')} ({metrics.get('handle')}) | Inscritos: {metrics.get('subscribers')}")
    print(f"  • Total de Vídeos: {metrics.get('total_videos_analyzed')} uploads | Razão Shorts/Longos: {metrics.get('shorts_to_long_ratio')}")
    print(f"  • Vídeos Longos: {long_stats.get('count')} uploads | Média Views: {long_stats.get('mean_views')} | CTR Médio: {long_stats.get('mean_ctr')}%")
    print(f"  • Retenção aos 30s: {long_stats.get('mean_retention_30s')}% | Duração Média (AVD): {long_stats.get('mean_avd_pct')}%")
    print(f"  • Shorts: {short_stats.get('count')} uploads | Média Views: {short_stats.get('mean_views')}")
    
    if short_stats.get("outliers"):
        print(f"  • Outlier Viral Detectado:")
        for out in short_stats["outliers"]:
            print(f"     🔥 '{out['title'][:55]}...' ({out['views']} views, Z={out['z_score']}, {out['multiplier_vs_subs']}x inscritos)")

    print_separator()
    bot = diag["primary_bottleneck"]
    print(f"🚨 DIAGNÓSTICO DO GARGALO PRIMÁRIO:")
    print(f"  • Gargalo: {bot['name']}")
    print(f"  • Sintoma: {bot['symptom']}")
    print(f"  • Causa Raiz: {bot['root_cause']}")
    print(f"  • Impacto: {bot['impact']}")

    exp = diag["proposed_experiment"]
    print_separator()
    print(f"🧪 EXPERIMENTO DE 14 DIAS (MÉTODO X + Y):")
    print(f"  • Hipótese: {exp['hypothesis']}")
    print(f"  • Plano de Ação:")
    for a in exp["test_design"]:
        print(f"     {a}")
    print(f"  • Metas Quantitativas:")
    for k, v in exp["metric_targets"].items():
        print(f"     - {k}: {v}")
    print(f"  • Veredito de Sucesso: {exp['success_decision']}")

    print_separator()
    print(f"🎯 TOP 3 TEMAS PRIORIZADOS (EQUAÇÃO P = D x C x R x E):")
    for i, t in enumerate(res["top_themes"], 1):
        print(f"  [{i}] [{t['priority']}] {t['topic']} (P={t['p_score']}/625 | S={t['s_score']}/5)")
        print(f"      Pilar: {t['pillar']}")
        print(f"      Tese: {t['thesis']}")
        print(f"      Frase Canônica: '{t['canonical_phrase']}'")

def cmd_themes(channel_slug: str):
    print(f"\n🧠 AVALIAÇÃO DE TEMAS DE TRADING (QUANT P-SCORE & ANTI-DUPLICAÇÃO) // {channel_slug.upper()}")
    print_separator()
    res = chief_trading_agent.evaluate_themes(channel_slug)

    print(f"Total de Candidatos: {res['total_candidates_analyzed']} | Aprovados (Virgens): {res['approved_virgin_themes']} | Rejeitados: {res['rejected_duplicate_themes']}")
    print_separator()

    if res["duplicates_blocked"]:
        print("🛡️ TEMAS BLOQUEADOS PELO GUARDIÃO DE MEMÓRIA (ANTI-FADIGA):")
        for blk in res["duplicates_blocked"]:
            print(f"  ⛔ {blk['topic']}")
            print(f"     Razão: {blk['reason']} | {blk['verdict']}")
        print_separator()

    print("✅ TEMAS APROVADOS PARA PRODUÇÃO:")
    for i, t in enumerate(res["top_themes"], 1):
        sc = t["scores"]
        print(f"  [{i}] [{t['priority']}] {t['topic']}")
        print(f"      Score P: {t['p_score']}/625 (D={sc['D']} C={sc['C']} R={sc['R']} E={sc['E']} | Segurança S={sc['S']}/5)")
        print(f"      Pilar: {t['pillar']}")
        print(f"      Tese: {t['thesis']}")
        print(f"      Gancho 0-15s: \"{t['hook_suggestion']}\"")
        print()

def cmd_briefing(channel_slug: str, episode_id: str, topic_override: str = ""):
    print(f"\n📑 EMISSÃO DE BRIEFING ESTRATÉGICO DE PRODUÇÃO // {channel_slug.upper()}")
    print_separator()
    b = chief_trading_agent.generate_briefing(channel_slug, episode_id, topic_override)

    meta = b["metadata"]
    pkg = b["packaging_direction"]
    char = b["character_lock_and_pip"]
    voice = b["voice_and_audio"]
    comp = b["compliance_and_ypp_gates"]

    print(f"ID DO BRIEFING: {meta['briefing_id']}")
    print(f"Canal: {meta['channel_name']} ({meta['handle']}) | Data: {meta['generated_at']}")
    print(f"Status de Memória: {meta['coverage_status']}")
    print_separator()
    print(f"EMBALAGEM:")
    print(f"  • Título Principal: {pkg['canonical_title']}")
    print(f"  • Thumb Focal: {pkg['thumbnail_specification']['focal_element']}")
    print(f"  • Texto na Thumb: '{pkg['thumbnail_specification']['text_overlay']}' (Max: {pkg['thumbnail_specification']['max_words']} palavras)")
    print(f"  • Proibido na Thumb: {pkg['thumbnail_specification']['forbidden_elements']}")
    print_separator()
    print(f"DIRETRIZES DO AVATAR & ÁUDIO:")
    print(f"  • Voz: {voice['voice_name']} (ElevenLabs ID: {voice['voice_id']}) | Ritmo: {voice['cadence_wpm']} wpm")
    print(f"  • Look Canônico: {char['look']}")
    print(f"  • Regra de PiP: {char['pip_specs']}")
    print(f"  • Regra de Tela Cheia: {char['fullscreen_rules']}")
    print_separator()
    print("ESTRUTURA NARRATIVA (6 ATOS):")
    for act in b["narrative_structure_6_acts"]:
        print(f"\n  🎬 {act['act']}")
        print(f"     Visual: {act['visual']}")
        print(f"     Instrução: {act['dialogue_direction']}")
    print_separator()
    print("GATES DE COMPLIANCE & YOUTUBE PARTNER PROGRAM:")
    print(f"  • Mídia Sintética: {comp['checkbox_synthetic_media']}")
    print(f"  • Marcação Demo: {comp['demo_account_visibility']}")
    print(f"  • Disclaimer: {comp['financial_disclaimers']}")

def cmd_thumb(channel_slug: str, title: str, thumb_desc: str, thumb_text: str = ""):
    print(f"\n👁️ AUDITORIA DE EMBALAGEM DE TRADING // {channel_slug.upper()}")
    print_separator()
    res = chief_trading_agent.audit_thumbnail(channel_slug, title, thumb_desc, thumb_text)

    scores = res["scores"]
    print(f"Título Avaliado: {title}")
    print(f"Descrição da Thumb: {thumb_desc}")
    if thumb_text:
        print(f"Texto na Thumb: '{thumb_text}'")
    print_separator()
    print(f"PONTUAÇÕES (0 a 10):")
    print(f"  • Foco Visual em Vela: {scores['candlestick_clarity']}/10")
    print(f"  • Desejo de Verificação: {scores['verification_desire']}/10")
    print(f"  • Contraste e Paleta: {scores['palette_contrast']}/10")
    print(f"  • Coerência Anti-Guru: {scores['anti_guru_coherence']}/10")
    print(f"  • ÍNDICE GERAL DE EMBALAGEM: {scores['overall_index']}/100")
    print_separator()
    print(f"VEREDITO: {res['verdict']}")
    if res["detected_violations"]:
        print(f"🚨 VIOLAÇÕES CRÍTICAS DETECTADAS: {res['detected_violations']}")
    print("RECOMENDAÇÕES ACIONÁVEIS:")
    for r in res["actionable_recommendations"]:
        print(f"  👉 {r}")

def cmd_ecosystem(channel_slug: str, topic: str):
    print(f"\n🌐 ECOSSISTEMA INTEGRADO DE DESCOBERTA (7 PEÇAS) // {channel_slug.upper()}")
    print_separator()
    t = topic if topic else "La Trampa del Martillo en Cuenta Demo"
    res = chief_trading_agent.plan_discovery_ecosystem(channel_slug, t)

    print(f"Tema Central: {res['core_topic']}")
    print(f"Framework: {res['architecture_framework']}")
    print_separator()
    for key, piece in res["integrated_ecosystem_7_pieces"].items():
        print(f"\n🧩 {key.upper()} ➔ {piece['surface']}")
        if "suggested_title" in piece:
            print(f"   Título: \"{piece['suggested_title']}\"")
        if "duration" in piece:
            print(f"   Duração: {piece['duration']}")
        if "structure" in piece:
            print(f"   Estrutura: {piece['structure']}")
        if "copy" in piece:
            print(f"   Copy:\n{piece['copy']}")

def cmd_memory(query: str, channel: Optional[str] = None):
    print(f"\n🧠 CONSULTA À MEMÓRIA PERSISTENTE SQLITE FTS5 (TRADING) // TERMO: '{query}'")
    print_separator()
    results = trading_memory.search_memory(query, channel=channel)
    if not results:
        print("Nenhum aprendizado ou experimento encontrado para essa busca.")
        return

    for i, r in enumerate(results, 1):
        print(f"  [{i}] Canal: {r['channel'].upper()} | Categoria: {r['category']}")
        print(f"      Insight: {r['content']}")
        if r.get('evidence'):
            print(f"      Evidência: {r['evidence']}")
        print()

def cmd_live(channel_slug: str):
    print(f"\n📡 RASTREANDO CANAL DO YOUTUBE EM TEMPO REAL // {channel_slug.upper()}")
    print_separator()
    res = chief_trading_agent.live_sync(channel_slug)
    if res.get("status") == "LIVE_SYNC_SUCCESS":
        print(f"✅ Sincronização em tempo real concluída com sucesso!")
        print(f"   • Inscritos: {res['subscribers']}")
        print(f"   • Total de vídeos encontrados: {res['total_videos_found']}")
        print(f"   • Vídeos longos: {res['long_videos_count']} | Shorts: {res['shorts_count']}")
        print(f"   • Memória e baseline local atualizados.")
    else:
        print(f"❌ Falha no rastreio: {res.get('error')}")

def interactive_loop():
    print(TRADING_BANNER)
    print("Modo Interativo do Chief Trading Analyst ativado. Digite 'ajuda' para comandos ou 'sair'.\n")
    while True:
        try:
            line = input("ChiefTrading> ").strip()
            if not line:
                continue
            if line.lower() in ["sair", "exit", "quit"]:
                print("Encerrando sessão estratégica. Até a próxima.")
                break
            if line.lower() in ["ajuda", "help"]:
                print("Comandos disponíveis:")
                print("  audit [canal]                     - Executa auditoria quantitativa completa")
                print("  themes [canal]                    - Avalia e prioriza temas P0/P1 com anti-duplicação")
                print("  briefing [canal] [id] [tema]      - Emite briefing executivo de 6 atos para o squad")
                print("  thumb [canal] [título] [desc]     - Audita embalagem (thumbnail + título)")
                print("  ecosystem [canal] [tema]          - Projeta as 7 peças de descoberta multi-frente")
                print("  live [canal]                      - Rastreia métricas ao vivo no YouTube via yt-dlp")
                print("  memory [termo]                    - Busca aprendizados na memória SQLite FTS5")
                continue

            parts = line.split()
            sub = parts[0].lower()
            ch = parts[1] if len(parts) > 1 else "el_profe_de_velas"

            if sub == "audit":
                cmd_audit(ch)
            elif sub == "themes":
                cmd_themes(ch)
            elif sub == "briefing":
                ep_id = parts[2] if len(parts) > 2 else "EP_001"
                t_over = " ".join(parts[3:]) if len(parts) > 3 else ""
                cmd_briefing(ch, ep_id, t_over)
            elif sub == "thumb":
                t_title = parts[2] if len(parts) > 2 else "La Trampa de la Mecha"
                t_desc = " ".join(parts[3:]) if len(parts) > 3 else "Zoom na mecha"
                cmd_thumb(ch, t_title, t_desc)
            elif sub == "ecosystem":
                t_over = " ".join(parts[2:]) if len(parts) > 2 else ""
                cmd_ecosystem(ch, t_over)
            elif sub == "live":
                cmd_live(ch)
            elif sub == "memory":
                q = " ".join(parts[1:])
                cmd_memory(q)
            else:
                print(f"Comando não reconhecido: {sub}. Digite 'ajuda'.")
        except (KeyboardInterrupt, EOFError):
            print("\nEncerrando sessão.")
            break

def main():
    parser = argparse.ArgumentParser(description="Hermes Chief Trading // Strategic Intelligence CLI")
    subparsers = parser.add_subparsers(dest="subcommand", help="Subcomandos do Chief Trading")

    p_audit = subparsers.add_parser("audit", help="Auditoria quantitativa completa do canal de trading")
    p_audit.add_argument("channel", default="el_profe_de_velas", nargs="?", help="Slug do canal (padrão: el_profe_de_velas)")

    p_themes = subparsers.add_parser("themes", help="Avaliação e priorização quantitativa de temas de trading")
    p_themes.add_argument("channel", default="el_profe_de_velas", nargs="?", help="Slug do canal")

    p_brief = subparsers.add_parser("briefing", help="Emissão de briefing de produção para o squad de trading")
    p_brief.add_argument("channel", default="el_profe_de_velas", nargs="?", help="Slug do canal")
    p_brief.add_argument("episode_id", default="EP_001", nargs="?", help="Identificador do episódio (ex: EP_004)")
    p_brief.add_argument("--tema", default="", help="Tema customizado para o briefing")

    p_thumb = subparsers.add_parser("thumb", help="Auditoria de thumbnail e título para trading")
    p_thumb.add_argument("channel", default="el_profe_de_velas", nargs="?", help="Slug do canal")
    p_thumb.add_argument("title", help="Título do vídeo")
    p_thumb.add_argument("desc", help="Descrição visual da thumbnail")
    p_thumb.add_argument("--text", default="", help="Texto inserido na imagem")

    p_eco = subparsers.add_parser("ecosystem", help="Projeta ecossistema integrado de 7 peças de descoberta multi-frente")
    p_eco.add_argument("channel", default="el_profe_de_velas", nargs="?", help="Slug do canal")
    p_eco.add_argument("--tema", default="", help="Tema do ecossistema")

    p_mem = subparsers.add_parser("memory", help="Consulta à memória SQLite FTS5 de trading")
    p_mem.add_argument("query", help="Termo de busca")

    p_live = subparsers.add_parser("live", help="Rastreia canal ao vivo no YouTube via yt-dlp")
    p_live.add_argument("channel", default="el_profe_de_velas", nargs="?", help="Slug do canal")

    subparsers.add_parser("interactive", help="Inicia console interativo com o Chief Trading")

    args = parser.parse_args()

    if not args.subcommand or args.subcommand == "interactive":
        interactive_loop()
        return

    ch = getattr(args, "channel", "el_profe_de_velas")
    if args.subcommand == "audit":
        cmd_audit(ch)
    elif args.subcommand == "themes":
        cmd_themes(ch)
    elif args.subcommand == "briefing":
        cmd_briefing(ch, args.episode_id, getattr(args, "tema", ""))
    elif args.subcommand == "thumb":
        cmd_thumb(ch, args.title, args.desc, getattr(args, "text", ""))
    elif args.subcommand == "ecosystem":
        cmd_ecosystem(ch, getattr(args, "tema", ""))
    elif args.subcommand == "memory":
        cmd_memory(args.query)
    elif args.subcommand == "live":
        cmd_live(ch)

if __name__ == "__main__":
    main()
