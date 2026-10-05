# -*- coding: utf-8 -*-
"""
Hermes Chief Trading Skill: trading-discovery-engine
Projects the 7-piece multi-front discovery ecosystem (Search, Home, Shorts de Descoberta,
Shorts de Erro, Playlist, Comunidade, Telegram) according to the 80/20 rule for YouTube Trading Channels.
"""

from typing import Dict, Any, Optional

class TradingDiscoveryEngine:
    """Plans multi-surface discovery ecosystems for trading content."""

    def plan_ecosystem(self, channel_slug: str, topic: str) -> Dict[str, Any]:
        ch = channel_slug.lower()

        return {
            "channel_slug": ch,
            "core_topic": topic,
            "architecture_framework": "80/20 Trading Discovery (40% Busca + 30% Recomendação/Home + 20% Shorts + 10% Telegram)",
            "integrated_ecosystem_7_pieces": {
                "1_long_search": {
                    "surface": "Busca do YouTube (Alta Intenção)",
                    "title_formula": "Problema Reconhecido + Plataforma em Demo + Mecanismo Concreto",
                    "suggested_title": f"Cómo Identificar {topic} en Deriv / IQ Option Paso a Paso (Cuenta Demo)",
                    "objective": "Capturar tráfego perene de pessoas com dúvidas ativas sobre a plataforma e leitura de velas.",
                    "seo_tags": ["lectura de velas", "deriv cuenta demo", "iq option principiantes", "patrones de velas explicados"]
                },
                "2_long_browse_home": {
                    "surface": "Página Inicial / Navegação (Browse)",
                    "title_formula": "Paradoxo Causal + Desconstrução de Mito",
                    "suggested_title": f"El Error con {topic} Que Hace Perder al 90% (Sin Adivinar)",
                    "objective": "Gerar clique orgânico pela curiosidade técnica e pelo contraste anti-guru.",
                    "hook_element": "Avatar em tela cheia com expressão atenta: 'Mira acá: no entres todavía.'"
                },
                "3_short_discovery_proof": {
                    "surface": "Feed dos Shorts (Topo do Funil)",
                    "duration": "28 a 35 segundos",
                    "structure": "0-2s Choque visual na vela ➔ 3-15s Zoom no detalhe da mecha ➔ 16-25s Regra do Profe ➔ 26-30s CTA para o longo.",
                    "suggested_title": f"¿Por qué falla {topic}? Mira la mecha. #trading #velasjaponesas",
                    "related_video_link_target": "Longo de Busca ou Browse"
                },
                "4_short_hidden_error": {
                    "surface": "Feed dos Shorts (Retenção e Desejo)",
                    "duration": "30 a 40 segundos",
                    "structure": "0-3s 'Estás cometiendo este error con las velas' ➔ Demonstração de clique precipitado ➔ Veredito: 'Sin adivinar. Pruébalo primero en demo.'",
                    "suggested_title": f"El color te engaña en {topic} #tradingtips #deriv"
                },
                "5_playlist_track": {
                    "surface": "Playlists de Transformação (Sessão Prolongada)",
                    "playlist_name": "Modo Demo: Aprende a Leer el Gráfico Desde Cero",
                    "position_in_track": "Módulo 2: Anatomía de la Vela y Rechasos Falsos",
                    "next_video_recommendation": "Checklist de 3 Pasos Antes de Tocar el Botón"
                },
                "6_community_post": {
                    "surface": "Aba Comunidade do YouTube",
                    "timing": "48 horas antes da publicação do longo",
                    "type": "Enquete com imagem comparativa",
                    "copy": "Pregunta rápida para la comunidad:\n\nCuando ves esta vela en un soporte, ¿qué haces?\n\n🅰️ Compro de inmediato\n🅱️ Espero la siguiente vela para confirmar\n🅲️ Miro el cuerpo y no la mecha\n\nEl jueves abrimos la pantalla y lo comprobamos en cuenta demo. Sin adivinar.",
                    "metric_goal": "≥ 100 votos para sinalizar demanda ao algoritmo"
                },
                "7_telegram_checklist": {
                    "surface": "Canal Oficial do Telegram",
                    "timing": "No momento exato da publicação do longo",
                    "format": "Card visual escuro (checklist resumido) + áudio curto do Profe",
                    "copy": f"📋 CHECKLIST DEL PROFE // {topic.upper()}\n\n1. Mira el cuerpo: ¿tiene fuerza o es exaustión?\n2. Revisa la mecha: ¿hubo rechazo real o absorción?\n3. Antes del clic: confirma en cuenta demo.\n\n▶️ Mira la explicación completa en el video de hoy: [LINK]\n\nSin adivinar. Pruébalo primero en demo."
                }
            }
        }

trading_discovery_engine = TradingDiscoveryEngine()
