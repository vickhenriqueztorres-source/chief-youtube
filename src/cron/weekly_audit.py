# -*- coding: utf-8 -*-
"""
Hermes Chief - Weekly Automated Audit Job (Cron)
Runs periodically (e.g. every Monday 09:00 AM) to:
1. Re-evaluate metrics and bottlenecks across all 3 channels.
2. Check status of running experiments.
3. Compute progress vs targets.
4. Save an executive weekly snapshot to data/weekly_audits/.
5. Update persistent memory with weekly trajectory.
6. (Optional) Dispatch an executive briefing alert to Telegram.
"""

import sys
import os
import json
from datetime import datetime
from pathlib import Path

# Safe UTF-8 output on Windows consoles
try:
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    if hasattr(sys.stderr, 'reconfigure'):
        sys.stderr.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass

# Ensure root dir is in sys.path
root_dir = Path(__file__).resolve().parent.parent.parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

from src.core.agent import chief_agent
from src.core.memory import chief_memory

def run_weekly_audit() -> dict:
    now = datetime.now()
    year_week = now.strftime("%Y_W%W")
    timestamp_str = now.strftime("%Y-%m-%d %H:%M:%S")

    print(f"\n=======================================================")
    print(f"🛰️ HERMES CHIEF // ROTINA SEMANAL DE AUDITORIA ({year_week})")
    print(f"Executado em: {timestamp_str}")
    print(f"=======================================================\n")

    print("📡 Sincronizando dados dos canais em tempo real antes da auditoria...")
    try:
        chief_agent.sync_all()
        print("✓ Sincronização em tempo real concluída com sucesso.\n")
    except Exception as e:
        print(f"⚠️ Aviso na sincronização (usando dados locais em cache): {e}\n")

    channels = ["o_outro_lado", "hidden_systems_lab", "brecha"]
    audit_results = {}

    for ch in channels:
        print(f"📊 Auditando {ch.upper()}...")
        try:
            res = chief_agent.audit_channel(ch)
            if res.get("status") == "AUDIT_COMPLETED":
                audit_results[ch] = {
                    "bottleneck": res["diagnosis"]["primary_bottleneck"]["name"],
                    "symptom": res["diagnosis"]["primary_bottleneck"]["symptom"],
                    "experiment": res["diagnosis"]["proposed_experiment"],
                    "metrics": res["metrics"],
                    "top_themes": res["top_themes"][:3]
                }
                # Record weekly trajectory in memory
                long_stats = res["metrics"]["long_form_summary"]
                short_stats = res["metrics"]["shorts_summary"]
                insight = (
                    f"Semana {year_week}: Subs={res['metrics'].get('subscribers', 0)}, "
                    f"Longo Views={long_stats.get('mean_views', 0):.0f}, CTR={long_stats.get('mean_ctr', 0):.1f}%, "
                    f"Short Views={short_stats.get('mean_views', 0):.0f}. Gargalo: {res['diagnosis']['primary_bottleneck']['name']}"
                )
                chief_memory.record_learning(
                    ch,
                    "weekly_checkpoint",
                    insight,
                    f"Snapshot semanal {year_week}",
                    "Manter foco na resolução do gargalo primário indicado."
                )
            else:
                audit_results[ch] = {"error": "Falha na auditoria"}
        except Exception as e:
            audit_results[ch] = {"error": str(e)}

    # Get active experiments
    active_exps = chief_memory.get_active_experiments()

    snapshot = {
        "timestamp": timestamp_str,
        "week": year_week,
        "active_experiments_count": len(active_exps),
        "active_experiments": active_exps,
        "channels": audit_results
    }

    # Save to data/weekly_audits/
    output_dir = root_dir / "data" / "weekly_audits"
    output_dir.mkdir(parents=True, exist_ok=True)
    out_file = output_dir / f"weekly_audit_{year_week}.json"

    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(snapshot, f, ensure_ascii=False, indent=2)

    print(f"\n✅ Relatório semanal salvo em: {out_file}")

    # Optional Telegram dispatch
    tg_token = os.environ.get("TELEGRAM_BOT_TOKEN", "").strip()
    tg_chat = os.environ.get("TELEGRAM_CHAT_ID", "").strip()
    if tg_token and tg_chat:
        try:
            from src.interfaces.telegram_bot import HermesTelegramBot
            bot = HermesTelegramBot(tg_token)
            msg = (
                f"📢 *HERMES CHIEF // CHECKPOINT SEMANAL ({year_week})*\n\n"
                f"• *O Outro Lado:* Gargalo: `{audit_results['o_outro_lado']['bottleneck'].split('//')[0].strip()}`\n"
                f"• *Hidden Systems Lab:* Gargalo: `{audit_results['hidden_systems_lab']['bottleneck'].split('//')[0].strip()}`\n"
                f"• *Brecha:* Gargalo: `{audit_results['brecha']['bottleneck'].split('//')[0].strip()}`\n\n"
                f"🧪 *Experimentos Ativos:* `{len(active_exps)}`\n"
                f"📄 _Relatório completo registrado no banco FTS5._"
            )
            bot.send_message(tg_chat, msg)
            print("📲 Notificação enviada via Telegram com sucesso.")
        except Exception as e:
            print(f"⚠️ Não foi possível enviar para o Telegram: {e}")

    return snapshot

if __name__ == "__main__":
    run_weekly_audit()
