# -*- coding: utf-8 -*-
"""
Hermes Chief Trading Skill: trading-thumb-audit
Audits YouTube thumbnail concepts and titles specifically for Trading and Candlestick educational channels.
Penalizes guru ostentation, financial promises, and clutter; rewards forensic visual clarity and verification desire.
"""

from typing import Dict, Any, List

class TradingThumbnailAuditor:
    """Audits packaging for trading channels."""

    FORBIDDEN_KEYWORDS = [
        "ganancia segura", "señal", "infalible", "millonario", "dinero facil",
        "100% win", "estrategia secreta", "recupera", "duplica tu saldo"
    ]

    def audit(self, channel_slug: str, title: str, thumb_description: str, thumb_text: str = "") -> Dict[str, Any]:
        ch = channel_slug.lower()
        t_lower = title.lower()
        d_lower = thumb_description.lower()
        txt_lower = thumb_text.lower()
        full_text = f"{t_lower} {d_lower} {txt_lower}"

        # 1. Check for compliance violations / forbidden guru promises
        violations = [w for w in self.FORBIDDEN_KEYWORDS if w in full_text]

        # Dimension 1: Candlestick Visual Focus (0-10)
        c_score = 7.0
        if any(w in d_lower for w in ["mecha", "vela", "soporte", "grafico", "zoom", "detalle", "pavio"]):
            c_score += 2.0
        if any(w in d_lower for w in ["flechas rojas por todos lados", "grafico lleno de indicadores", "mucho texto"]):
            c_score -= 3.0
        c_score = max(1.0, min(10.0, c_score))

        # Dimension 2: Verification Desire (0-10)
        d_score = 6.5
        if any(w in t_lower for w in ["error", "trampa", "engaña", "por que", "antes de", "sin adivinar", "cuidado"]):
            d_score += 2.5
        if any(w in t_lower for w in ["tutorial", "aprende trading", "clase 1", "bienvenido"]):
            d_score -= 2.0
        d_score = max(1.0, min(10.0, d_score))

        # Dimension 3: Palette & Contrast (0-10)
        p_score = 7.0
        if any(w in d_lower for w in ["dark mode", "fondo oscuro", "amarillo", "blanco", "contraste", "azul"]):
            p_score += 2.0
        if any(w in d_lower for w in ["fondo blanco brillante", "muchos colores", "arcoiris", "neones saturados"]):
            p_score -= 2.5
        p_score = max(1.0, min(10.0, p_score))

        # Dimension 4: Anti-Guru Coherence (0-10)
        ag_score = 8.5
        if violations:
            ag_score -= 5.0
        if any(w in d_lower for w in ["dinero", "billetes", "dolares", "autos", "lujo", "fiat", "reloj de oro"]):
            ag_score -= 4.0
        if any(w in d_lower for w in ["profe", "profesor", "bomber", "polo", "calmo", "adulto"]):
            ag_score += 1.5
        ag_score = max(1.0, min(10.0, ag_score))

        # Text on thumb length penalty
        word_count = len(thumb_text.split()) if thumb_text else 0
        if word_count > 4:
            c_score -= 1.5
            p_score -= 1.0

        # Overall Index (0 to 100)
        overall = (c_score * 0.30 + d_score * 0.30 + p_score * 0.20 + ag_score * 0.20) * 10.0
        overall = round(max(0.0, min(100.0, overall)), 1)

        recommendations: List[str] = []
        if violations:
            recommendations.append(f"CRÍTICO: Remova termos proibidos pelo YouTube Financeiro ({violations}). Risco de shadowban ou desmonetização.")
        if word_count > 3:
            recommendations.append(f"Reduza o texto da thumbnail para no máximo 3 palavras fortes (ex: '¿SUBIDA FALSA?', 'LEE LA MECHA'). Atualmente tem {word_count} palavras.")
        if "zoom" not in d_lower and "mecha" not in d_lower:
            recommendations.append("Aumente o zoom no elemento causador da dúvida (ex: close de 150% na mecha da vela em vez de mostrar o gráfico inteiro minúsculo).")
        if not recommendations:
            recommendations.append("Embalagem de alta precisão alinhada ao arquétipo do Professor-Verificador. Pronta para teste A/B no YouTube Studio.")

        verdict = "APROVADA" if overall >= 75.0 and not violations else "REQUER AJUSTES"

        return {
            "channel_slug": ch,
            "title_evaluated": title,
            "thumb_description": thumb_description,
            "thumb_text": thumb_text,
            "scores": {
                "candlestick_clarity": round(c_score, 1),
                "verification_desire": round(d_score, 1),
                "palette_contrast": round(p_score, 1),
                "anti_guru_coherence": round(ag_score, 1),
                "overall_index": overall
            },
            "verdict": verdict,
            "detected_violations": violations,
            "actionable_recommendations": recommendations
        }

trading_thumbnail_auditor = TradingThumbnailAuditor()
