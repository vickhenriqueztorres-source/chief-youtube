# -*- coding: utf-8 -*-
"""
Hermes Chief Skill: thumbnail-audit
Performs quantitative and psychological evaluation of YouTube Thumbnails + Titles.
Applies Eugene Schwartz Breakthrough Advertising and Chief P²PT visual criteria.
"""

from typing import Dict, Any, List

class ThumbnailAuditor:
    """Audits YouTube thumbnails and titles against visual cognitive psychology."""

    CHANNEL_PALETTES = {
        "o_outro_lado": {
            "primary": "#FF5500 (Sodium Amber) / #FFD600 (Brutalist Shock Yellow) / #00F0FF (Laser Cyan Digital Meter)",
            "bg": "#060709 (Carbon Black - 60-70% Dark Mode)",
            "rules": "Arquitetura de Leitura em 0,2s: (1) Dark Mode 60-70% + ponto focal saturado; (2) Hero Object Único (isolamento causal); (3) Texto de Choque máx 2-3 palavras (ex: 'APAGOU TUDO', '40 SEGUNDOS', 'SEM ÁGUA') SEM repetir palavras do título; (4) Medidor Digital em Destaque Neon (ex: '[ 00:01s ]'). Zero rostos forçados."
        },
        "hidden_systems_lab": {
            "primary": "#00E5FF (Cyan) / #FFE500 (Acid)",
            "bg": "#07080B (Obsidian)",
            "rules": "Exige retícula HUD ortogonal vetorial, macro industrial do gargalo, tolerâncias mecânicas visíveis."
        },
        "brecha": {
            "primary": "#EF2B1D (Brecha Red — Fissura) / #E9E4DA (Paper Bone White)",
            "bg": "#0A0A0A (Obsidian Black) / #171717 (Charcoal) + Textura Física (Madeira Escura / Papel / Metal)",
            "rules": "Cinematic Investigative Noir (V2): OBJETO COTIDIANO (Hero Object 45-65%) + FISSURA VERMELHA (#EF2B1D) + CONSEQUÊNCIA (2 a 4 palavras em Sans Condensada Pesada). Composição 55/45 ou 60/40. Thumbnail = Consequência | Título = Mecanismo. Proibido ciano (#00E5FF), HUD sci-fi, ALL CAPS e termos 'golpe/roubo/quadrilha' no título."
        }
    }

    def audit(self, channel_slug: str, title: str, thumb_description: str, thumb_text: str = "") -> Dict[str, Any]:
        """
        Scores and analyzes a thumbnail + title pair.
        """
        channel = channel_slug.lower()
        palette_info = self.CHANNEL_PALETTES.get(channel, self.CHANNEL_PALETTES["o_outro_lado"])

        # Evaluation criteria 0-10
        # 1. Clareza: can the viewer decode it in 0.2 seconds on mobile (160x90px)?
        # 2. Desejo: does it trigger loss aversion, systemic vulnerability fear (amygdala), or micro-vs-macro contrast?
        # 3. Diferenciação: does it stand out from sea of generic YouTube junk?
        # 4. Coerência: does thumb match title without repeating title words (1+1=3)?

        title_lower = title.lower()
        thumb_lower = thumb_description.lower()

        clareza = 9
        desejo = 8
        diferenciacao = 9
        coerencia = 9
        reasons = []
        actionable_tweaks = []

        # Penalize title if too abstract
        if any(w in title_lower for w in ["química", "física da", "máquina de", "diário oficial", "drones"]):
            desejo -= 2
            reasons.append("Tema com conotação acadêmica/burocrática; baixa ativação de desejo humano direto.")
            actionable_tweaks.append("Usar Fórmula Matriz: [Catástrofe / Notícia Ruim] + [Tempo Cirúrgico / Mecanismo Invisível].")

        # Brecha V2 specific checks: Harmful & Dangerous filter words, ALL CAPS, and Fissura signature
        if channel == "brecha":
            banned_words = [w for w in ["golpe", "roubo", "quadrilha", "fraude", "criminosos"] if w in title_lower]
            if banned_words:
                diferenciacao -= 3
                desejo -= 1
                reasons.append(
                    f"Termos bloqueados detectados no título ({', '.join(banned_words)}). Aciona o filtro Harmful & Dangerous Policies do YouTube e atrai audiência fantasma de boletim policial."
                )
                actionable_tweaks.append(
                    "Substituir termos policiais pelo Paradoxo de Zeigarnik focado no mecanismo e objeto físico (ex: 'O Adesivo de 5 cm Que Pode Mandar Seu Pix Para Outra Conta')."
                )

            if sum(1 for c in title if c.isupper()) / (len(title) + 1) > 0.35:
                diferenciacao -= 2
                reasons.append("ALL CAPS excessivo aproxima o canal de sensacionalismo policial barato e reduz retenção de sessão longa.")
                actionable_tweaks.append("Usar Title Case documental sóbrio. O drama deve vir do paradoxo técnico e da mesa de evidências.")

            has_fissure = any(w in thumb_lower for w in ["fissura", "rachadura", "rasgo", "rasgado", "#ef2b1d", "corte vermelho", "fenda", "quebrad"])
            if not has_fissure:
                diferenciacao -= 2
                reasons.append("Ausência da Assinatura Visual V2 ('A Fissura' em #EF2B1D) na descrição da thumbnail.")
                actionable_tweaks.append("Incluir a Fissura Vermelha (#EF2B1D) ou rasgo físico separando o Hero Object cotidiano da consequência.")

            if any(w in thumb_lower for w in ["ciano", "cyan", "#00e5ff", "hud", "sci-fi", "neon", "matrix"]):
                coerencia -= 3
                reasons.append("Violação da Identidade V2: uso de ciano/HUD sci-fi/neon estritamente proibido no Cinematic Investigative Noir.")
                actionable_tweaks.append("Substituir por mesa de evidências em madeira escura, Obsidian (#0A0A0A), Paper Bone White (#E9E4DA) e Brecha Red (#EF2B1D).")

        # Check for Triad: Result, Mechanism, Tension / Micro vs Macro
        has_mechanism = any(w in thumb_lower or w in title_lower for w in [
            "chip", "cabo", "solda", "radar", "sensor", "ura", "bomba", "turbina", "pressão",
            "segundo", "segundos", "milímetro", "milímetros", "minuto", "minutos", "centímetro", "centímetros",
            "relê", "relé", "byte", "volts", "metros", "âncora", "válvula", "adesivo", "cm", "qr code", "número", "áudio", "voz", "senha", "biometria"
        ])
        has_tension = any(w in thumb_lower or w in title_lower for w in [
            "apaga", "apagou", "morre", "roubo", "colapso", "multa", "bloqueado", "fuga", "sem rastro",
            "perder", "sem água", "fechou", "explodiu", "travou", "afundaram", "destruiu", "sumir", "sumirem", "parou", "queimou",
            "outra conta", "outro dono", "falsa", "desviado", "burlada", "não impedem"
        ])

        if not has_mechanism:
            desejo -= 1
            reasons.append("Falta unidade mínima / fração de tempo extrema ou objeto tangível (Micro vs Macro).")
            actionable_tweaks.append("Inserir fração cirúrgica ou objeto físico no título (ex: 'Os 180 Segundos...', 'O Adesivo de 5 cm...', 'O Áudio de 4 Segundos...').")

        if not has_tension:
            desejo -= 2
            reasons.append("Baixa tensão dramática; não ativa o Efeito Zeigarnik nem medo de vulnerabilidade sistêmica.")
            actionable_tweaks.append("Adicionar consequência direta na thumb (ex: 'PIX DESVIADO', 'SEU NÚMERO VOLTOU', 'A VOZ ERA FALSA').")

        # Text on thumb length check (0.2s Read Architecture: max 2-3 words for O Outro Lado, max 2-4 words for Brecha V2)
        thumb_words = [w.strip(".,!?:;[]()") for w in thumb_text.split() if w.strip(".,!?:;[]()")]
        word_count_thumb = len(thumb_words)
        max_words = 4 if channel == "brecha" else 3
        if word_count_thumb > max_words:
            clareza -= 2
            reasons.append(f"Texto na thumb com {word_count_thumb} palavras. A Arquitetura de 0,2s (Lei de Weber) exige no máximo 2 a {max_words} palavras de Consequência.")
            actionable_tweaks.append(f"Reduzir texto na thumb para 2-{max_words} palavras em Sans Condensada Pesada (ex: 'PIX DESVIADO', 'SEU NÚMERO VOLTOU', 'A VOZ ERA FALSA').")

        # Check for title word repetition in thumbnail text (forbidden in 1+1=3 and 0.2s Architecture)
        title_significant_words = {w.strip(".,!?:;").lower() for w in title.split() if len(w.strip(".,!?:;")) > 3}
        repeated_words = [w for w in thumb_words if w.lower() in title_significant_words]
        if repeated_words:
            coerencia -= 2
            reasons.append(f"Repetição proibida de palavras entre Título (Mecanismo) e Thumbnail (Consequência): {', '.join(repeated_words)}.")
            actionable_tweaks.append("Manter separação cognitiva estrita: Thumbnail = Consequência | Título = Mecanismo, sem repetir palavras.")

        # Calculate final index (0-100)
        overall_score = round(((clareza * 0.3) + (desejo * 0.3) + (diferenciacao * 0.2) + (coerencia * 0.2)) * 10, 1)

        if overall_score >= 80:
            recommendation = "MANTER"
            action_summary = "Aprovado com louvor. Embalagem com alto potencial de conversão no Browse."
        elif overall_score >= 60:
            recommendation = "AJUSTAR"
            action_summary = "Potencial bom, mas requer 1 ou 2 ajustes visuais cirúrgicos antes de publicar."
        else:
            recommendation = "REFAZER"
            action_summary = "Embalagem fraca. Risco elevado de travar em CTR < 2.5% e matar a distribuição do vídeo."

        return {
            "channel": channel,
            "title_evaluated": title,
            "thumb_description": thumb_description,
            "thumb_text": thumb_text,
            "scores": {
                "clareza": clareza,
                "desejo": desejo,
                "diferenciacao": diferenciacao,
                "coerencia": coerencia,
                "overall_index": overall_score
            },
            "recommendation": recommendation,
            "diagnostic_reasons": reasons if reasons else ["Composição atende aos padrões de contraste e especificidade do Chief."],
            "actionable_tweaks": actionable_tweaks if actionable_tweaks else ["Manter renderização em 4K sem alterações."],
            "brand_compliance": palette_info
        }

thumbnail_auditor = ThumbnailAuditor()
