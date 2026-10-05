# -*- coding: utf-8 -*-
"""
Hermes Chief - Telegram Bot Interface
Pure Python Telegram Bot client using HTTP long-polling (no heavy third-party framework required).
Allows the Tech Lead / Channel Owner to interact with Hermes Chief anywhere on mobile.

Commands:
  /start, /help   - Welcome banner and command list
  /status         - Multi-channel status summary
  /audit <canal>  - Run quantitative audit on channel (outro_lado, hsl, brecha)
  /themes <canal> - View prioritized theme queue (P = D x C x R x E)
  /briefing <ch>  - Generate squad briefing
  /memory <query> - Search FTS5 persistent memory
  <Free text>     - Talk directly to Chief Analyst brain
"""

import os
import sys
import json
import time
import urllib.request
import urllib.parse
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

TELEGRAM_API_BASE = "https://api.telegram.org/bot"

class HermesTelegramBot:
    def __init__(self, token: str = None):
        self.token = token or os.environ.get("TELEGRAM_BOT_TOKEN", "").strip()
        self.base_url = f"{TELEGRAM_API_BASE}{self.token}"
        self.offset = 0

    def _api_call(self, endpoint: str, data: dict = None) -> dict:
        url = f"{self.base_url}/{endpoint}"
        try:
            if data is not None:
                json_data = json.dumps(data).encode("utf-8")
                req = urllib.request.Request(
                    url,
                    data=json_data,
                    headers={"Content-Type": "application/json"}
                )
            else:
                req = urllib.request.Request(url)
            
            with urllib.request.urlopen(req, timeout=30) as resp:
                res_bytes = resp.read()
                return json.loads(res_bytes.decode("utf-8"))
        except Exception as e:
            return {"ok": False, "description": str(e)}

    def send_message(self, chat_id: int or str, text: str, parse_mode: str = "Markdown") -> bool:
        """Sends message splitting into 4000-char chunks if needed."""
        chunk_size = 3900
        lines = text.split("\n")
        current_chunk = ""
        
        for line in lines:
            if len(current_chunk) + len(line) + 1 > chunk_size:
                data = {"chat_id": chat_id, "text": current_chunk, "parse_mode": parse_mode}
                res = self._api_call("sendMessage", data)
                if not res.get("ok"):
                    # Fallback to plain text if markdown parse fails
                    data.pop("parse_mode", None)
                    self._api_call("sendMessage", data)
                current_chunk = line + "\n"
            else:
                current_chunk += line + "\n"

        if current_chunk.strip():
            data = {"chat_id": chat_id, "text": current_chunk, "parse_mode": parse_mode}
            res = self._api_call("sendMessage", data)
            if not res.get("ok"):
                data.pop("parse_mode", None)
                self._api_call("sendMessage", data)
        return True

    def get_updates(self, timeout: int = 25) -> list:
        data = {"offset": self.offset, "timeout": timeout}
        res = self._api_call("getUpdates", data)
        if res.get("ok"):
            return res.get("result", [])
        return []

    def handle_message(self, message: dict):
        chat_id = message.get("chat", {}).get("id")
        text = (message.get("text") or "").strip()
        from_user = message.get("from", {}).get("first_name", "Creator")

        if not text or not chat_id:
            return

        print(f"[Telegram] Recebido de {from_user} ({chat_id}): {text}")

        # Command routing
        parts = text.split(maxsplit=2)
        cmd = parts[0].lower()

        if cmd in ["/start", "/help"]:
            reply = (
                "🏛️ *HERMES CHIEF // INTELIGÊNCIA ANALÍTICA DE YOUTUBE*\n\n"
                "Tech Lead Quant para os 3 canais documentais:\n"
                "• *O Outro Lado* (`o_outro_lado`)\n"
                "• *Hidden Systems Lab* (`hsl`)\n"
                "• *Brecha* (`brecha`)\n\n"
                "*Comandos Disponíveis:*\n"
                "📊 `/status` - Panorama quantitativo dos 3 canais\n"
                "🔍 `/audit <canal>` - Diagnóstico do gargalo e experimento\n"
                "🎯 `/themes <canal>` - Top temas prioritários (P = D x C x R x E)\n"
                "📦 `/briefing <canal> [ep]` - Emite briefing de produção do squad\n"
                "🧠 `/memory <termo>` - Consulta aprendizados acumulados no FTS5\n"
                "💬 _Ou envie qualquer pergunta estratégica direta para mim._"
            )
            self.send_message(chat_id, reply)

        elif cmd == "/status":
            summary = chief_agent.generate_full_executive_summary()
            lines = ["📊 *PANORAMA MULTI-CANAL // HERMES CHIEF*\n"]
            for slug, d in summary["channels_audited"].items():
                if "error" in d:
                    lines.append(f"*{slug.upper()}*: Erro ao auditar: {d['error']}\n")
                    continue
                m = d["metrics"]
                diag = d["diagnosis"]
                long_s = m["long_form_summary"]
                short_s = m["shorts_summary"]
                top_p0 = d["top_themes"][0]["topic"] if d.get("top_themes") else "N/A"
                lines.append(
                    f"*{d['channel_info'].get('name', slug.upper())}* (`@{d['channel_info'].get('handle', '')}`)\n"
                    f"• Subs: `{m.get('subscribers', 0)}` | Longos: `{long_s.get('count', 0)}` (Média: `{long_s.get('mean_views', 0):.0f}` v)\n"
                    f"• Shorts: `{short_s.get('count', 0)}` (Média: `{short_s.get('mean_views', 0):.0f}` v)\n"
                    f"• Gargalo: *{diag['primary_bottleneck']['name'].split('//')[0].strip()}*\n"
                    f"• Top P0: _{top_p0}_\n"
                )
            lines.append(f"🧪 *Experimentos Ativos:* `{summary['active_experiments_count']}`")
            self.send_message(chat_id, "\n".join(lines))

        elif cmd == "/audit":
            if len(parts) < 2:
                self.send_message(chat_id, "⚠️ *Uso:* `/audit <o_outro_lado | hsl | brecha>`")
                return
            target = parts[1].lower()
            if target == "outro_lado":
                target = "o_outro_lado"
            elif target == "hsl":
                target = "hidden_systems_lab"

            self.send_message(chat_id, f"⏳ _Auditando {target.upper()}... Processando dados quantitativos..._")
            try:
                res = chief_agent.audit_channel(target)
                if res.get("status") != "AUDIT_COMPLETED":
                    self.send_message(chat_id, "❌ *Erro:* Falha ao processar auditoria.")
                    return

                diag = res["diagnosis"]
                exp = diag["proposed_experiment"]
                bot = diag["primary_bottleneck"]
                m = res["metrics"]
                long_s = m["long_form_summary"]
                short_s = m["shorts_summary"]

                reply = (
                    f"🚨 *AUDITORIA QUANT: {target.upper()}*\n"
                    f"━━━━━━━━━━━━━━━━━━━━━\n"
                    f"📈 *Métricas Chave:*\n"
                    f"• Vídeos Longos: `{long_s.get('count', 0)}` (Média: `{long_s.get('mean_views', 0):.0f}` views)\n"
                    f"• CTR Médio: `{long_s.get('mean_ctr', 0):.1f}%` | Retenção 30s: `{long_s.get('mean_retention_30s', 0):.1f}%`\n"
                    f"• Shorts: `{short_s.get('count', 0)}` (Média: `{short_s.get('mean_views', 0):.0f}` views)\n\n"
                    f"🚨 *Gargalo Primário:* *{bot['name']}*\n"
                    f"• *Sintoma:* {bot['symptom']}\n"
                    f"• *Causa Raiz:* {bot['root_cause']}\n\n"
                    f"🧪 *Experimento 14 Dias:*\n"
                    f"• *Hipótese:* {exp['hypothesis']}\n"
                    f"• *Ação 1:* {exp['test_design'][0] if exp.get('test_design') else 'N/A'}\n"
                    f"• *Metas:* `{json.dumps(exp['metric_targets'])}`"
                )
                self.send_message(chat_id, reply)
            except Exception as e:
                self.send_message(chat_id, f"❌ *Erro:* {e}")

        elif cmd == "/themes":
            if len(parts) < 2:
                self.send_message(chat_id, "⚠️ *Uso:* `/themes <o_outro_lado | hsl | brecha>`")
                return
            target = parts[1].lower()
            if target == "outro_lado":
                target = "o_outro_lado"
            elif target == "hsl":
                target = "hidden_systems_lab"

            try:
                res = chief_agent.decide_themes(target)
                themes = res.get("top_3_selected", [])
                lines = [f"🎯 *FILA DE TEMAS: {target.upper()}* (Equação P = D x C x R x E)\n"]
                for i, t in enumerate(themes, 1):
                    lines.append(
                        f"*{i}. [{t['priority']}] {t['topic']}* (P=`{t['p_score']}` | S=`{t.get('s_score', 0)}`)\n"
                        f"• *Unidade:* {t.get('concrete_unit')}\n"
                        f"• *Tese:* {t.get('thesis')}\n"
                    )
                self.send_message(chat_id, "\n".join(lines))
            except Exception as e:
                self.send_message(chat_id, f"❌ *Erro:* {e}")

        elif cmd == "/briefing":
            if len(parts) < 2:
                self.send_message(chat_id, "⚠️ *Uso:* `/briefing <canal> [ep_id]`\nEx: `/briefing brecha EP_007`")
                return
            target = parts[1].lower()
            if target == "outro_lado":
                target = "o_outro_lado"
            elif target == "hsl":
                target = "hidden_systems_lab"
            ep_id = parts[2] if len(parts) > 2 else "EP_NEXT"

            self.send_message(chat_id, f"⏳ _Gerando briefing formal para {target}..._")
            try:
                b = chief_agent.generate_briefing(target, ep_id)
                reply = (
                    f"📦 *BRIEFING OFICIAL EMITIDO // {b['squad'].upper()}*\n"
                    f"━━━━━━━━━━━━━━━━━━━━━\n"
                    f"🎬 *Episódio:* `{b['episode_id']}` | *Prioridade:* `{b['prioridade']}`\n"
                    f"🎯 *Tema:* *{b['tema']}*\n"
                    f"🔬 *Unidade Concreta:* `{b['unidade_investigada']}`\n"
                    f"⚖️ *Métrica Alvo:* {b['metrica_alvo']}\n\n"
                    f"💡 *Abertura (0-15s):*\n_{b['diretrizes_estrategicas']['o_que_priorizar_na_abertura']}_\n\n"
                    f"🚫 *O Que Não Fazer:*\n• " + "\n• ".join(b['diretrizes_estrategicas']['o_que_nao_fazer'][:2]) +
                    f"\n\n📄 _Briefing JSON completo salvo no servidor._"
                )
                self.send_message(chat_id, reply)
            except Exception as e:
                self.send_message(chat_id, f"❌ *Erro:* {e}")

        elif cmd == "/memory":
            query = parts[1] if len(parts) > 1 else ""
            if not query:
                self.send_message(chat_id, "⚠️ *Uso:* `/memory <termo>`\nEx: `/memory santos`")
                return
            results = chief_agent.search_memory(query)
            if not results:
                self.send_message(chat_id, f"🔍 Nenhum registro encontrado para: `{query}`")
                return
            lines = [f"🧠 *MEMÓRIA FTS5 // TERMO:* `{query}`\n"]
            for r in results[:3]:
                lines.append(
                    f"📌 *[{r.get('channel', 'global').upper()} // {r.get('category', 'geral').upper()}]*\n"
                    f"• {r.get('content', '')}\n"
                    f"• _Evidência:_ {r.get('metric_evidence', 'N/A')}\n"
                )
            self.send_message(chat_id, "\n".join(lines))

        else:
            # Free-form consultation with Chief Analyst
            self.send_message(chat_id, "🤔 _Analisando sob os princípios do Hermes Chief..._")
            resp_text = chief_agent.answer_query(text)
            self.send_message(chat_id, resp_text)

    def start_polling(self):
        if not self.token:
            print("❌ ERRO: TELEGRAM_BOT_TOKEN não configurado no ambiente.")
            print("Configure a variável com: $env:TELEGRAM_BOT_TOKEN='seu_token'")
            return

        print(f"🤖 Hermes Chief Telegram Bot iniciado. Polling ativo...")
        while True:
            try:
                updates = self.get_updates()
                for update in updates:
                    self.offset = update["update_id"] + 1
                    if "message" in update:
                        self.handle_message(update["message"])
            except KeyboardInterrupt:
                print("\n🛑 Telegram Bot encerrado pelo usuário.")
                break
            except Exception as e:
                print(f"[Telegram Polling Error] {e}")
                time.sleep(3)


def main():
    token = sys.argv[1] if len(sys.argv) > 1 else None
    bot = HermesTelegramBot(token)
    bot.start_polling()


if __name__ == "__main__":
    main()
