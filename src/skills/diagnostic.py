# -*- coding: utf-8 -*-
"""
Hermes Chief Skill: channel-diagnostic
Transforms quantitative metric readings into causal bottleneck diagnosis
and formulates rigorous 14-day test hypotheses following the Chief X + Y method.
"""

from typing import Dict, Any, List

class ChannelDiagnostic:
    """Diagnoses YouTube growth bottlenecks using the Chief quantitative framework."""

    BOTTLENECKS = {
        "DESCOBERTA_COLD_START": {
            "name": "Gargalo de Descoberta // Cold Start Algorítmico",
            "symptom": "Pouquíssimas impressões totais (< 500) e visualizações médias < 25.",
            "cause": "Canal recente sem histórico, postagens em ritmo excessivo sem cohortes sementes ativas."
        },
        "EMBALAGEM_CTR": {
            "name": "Gargalo de Embalagem // Baixa Taxa de Clique",
            "symptom": "Impressões existem (> 1.000), mas CTR na Home/Browse está abaixo de 4.0%.",
            "cause": "Títulos descritivos/acadêmicos e thumbnails sem Contraste Causal ou Promessa Visceral."
        },
        "HOOK_ABERTURA": {
            "name": "Gargalo de Gancho // Abandono nos Primeiros 30 Segundos",
            "symptom": "Retenção na marca de 0:30 cai abaixo de 55%.",
            "cause": "Abertura expositiva, saudações burocráticas, repetição do título ou ausência de paradoxo inicial."
        },
        "AUDIENCIA_FANTASMA": {
            "name": "Gargalo de Audiência Fantasma // Inscritos Inativos",
            "symptom": "Base de inscritos relevante (> 500), mas visualizações em novos uploads < 2% dos inscritos.",
            "cause": "Inscritos herdados de virais desconexos ou métodos externos que ignoram uploads longos."
        },
        "DESCONEXAO_SHORTS": {
            "name": "Gargalo de Desconexão // Shorts Desalinhados do Longo",
            "symptom": "Shorts têm tração (> 1.000 views), mas vídeos longos permanecem estagnados (< 50 views).",
            "cause": "Shorts sem gancho forense, títulos de hashtags ou falta de botão 'Vídeo Relacionado' ativo."
        },
        "CANIBALIZACAO_CONTEUDO": {
            "name": "Gargalo de Autocanibalização // Uploads Repetidos",
            "symptom": "Queda abrupta de impressões após re-uploads de vídeos com mesmo tema.",
            "cause": "Upload de arquivos idênticos gerando sinal de spam no ContentID do algoritmo."
        }
    }

    def diagnose(self, channel_slug: str, metrics_summary: Dict[str, Any]) -> Dict[str, Any]:
        """
        Evaluates metrics against channel configuration and returns diagnosis + experiment.
        """
        subscribers = metrics_summary.get("subscribers", 0)
        long_stats = metrics_summary.get("long_form_summary", {})
        short_stats = metrics_summary.get("shorts_summary", {})
        
        avg_views = long_stats.get("mean_views", 0)
        avg_ctr = long_stats.get("mean_ctr", 0.0)
        short_views = short_stats.get("mean_views", 0)
        total_longs = long_stats.get("count", 0)

        diagnosed_bottlenecks = []

        # Check Audiência Fantasma
        if subscribers > 500 and avg_views < (subscribers * 0.03):
            diagnosed_bottlenecks.append("AUDIENCIA_FANTASMA")

        # Check Descoberta / Cold Start
        if avg_views < 30 and total_longs >= 5:
            diagnosed_bottlenecks.append("DESCOBERTA_COLD_START")

        # Check Desconexão Shorts
        if short_views > 500 and avg_views < 100:
            diagnosed_bottlenecks.append("DESCONEXAO_SHORTS")

        # Fallback if no specific trigger fired
        if not diagnosed_bottlenecks:
            if avg_ctr < 4.0:
                diagnosed_bottlenecks.append("EMBALAGEM_CTR")
            else:
                diagnosed_bottlenecks.append("HOOK_ABERTURA")

        primary_id = diagnosed_bottlenecks[0]
        primary_info = self.BOTTLENECKS[primary_id]

        # Generate Channel-Specific Experiment
        experiment = self._generate_experiment(channel_slug, primary_id, metrics_summary)

        return {
            "channel": channel_slug,
            "primary_bottleneck": {
                "id": primary_id,
                "name": primary_info["name"],
                "symptom": primary_info["symptom"],
                "root_cause": primary_info["cause"]
            },
            "secondary_bottlenecks": [self.BOTTLENECKS[b]["name"] for b in diagnosed_bottlenecks[1:]],
            "evidence_snapshot": {
                "subscribers": subscribers,
                "mean_views_long": avg_views,
                "mean_views_short": short_views,
                "total_videos_analyzed": total_longs + short_stats.get("count", 0),
                "trend": long_stats.get("trend", "UNKNOWN")
            },
            "proposed_experiment": experiment
        }

    def _generate_experiment(self, channel_slug: str, bottleneck_id: str, metrics: Dict[str, Any]) -> Dict[str, Any]:
        if channel_slug == "o_outro_lado":
            return {
                "duration_days": 14,
                "hypothesis": "Se alinharmos os próximos 3 episódios em uma única série temática ('A Máquina do Dinheiro Oculto') e vincularmos os Shorts virais via botão de Vídeo Relacionado, o número de Espectadores Recorrentes crescerá em > 40% porque o público semente terá relevância contínua.",
                "test_design": [
                    "Ação 1: Vincular no YouTube Studio os 2 Shorts virais (Santos 1.4k e Apagão 1.1k) aos seus documentários longos correspondentes.",
                    "Ação 2: Produzir 2 novos episódios com P ≥ 450 (Jammer de Carro Roubado e O Chip da Bomba de Combustível).",
                    "Ação 3: Limitar cadência a 2 vídeos longos por semana para permitir amostragem algorítmica de 72h."
                ],
                "metric_targets": {
                    "returning_viewers": "+40% na aba Audience",
                    "browse_ctr": "> 6.0%",
                    "retention_30s": "> 65%"
                },
                "success_decision": "Consolidar editorial exclusivamente em Infraestrutura de Crime/Dinheiro e pausar temas de física pura.",
                "failure_decision": "Se a CTR não subir com a nova embalagem, rever a paleta de cores e o enquadramento do objeto hero na thumbnail."
            }

        elif channel_slug == "hidden_systems_lab":
            return {
                "duration_days": 14,
                "hypothesis": "Se substituirmos os títulos de apenas hashtags nos Shorts por paradoxos em inglês ('The 500ms Disaster That Almost Destroyed the Pad') e removermos os re-uploads duplicados, o canal recuperará a confiança do algoritmo e os Shorts atingirão > 500 views.",
                "test_design": [
                    "Ação 1: Deletar ou colocar como privado os uploads duplicados (Airport Fuel e Skyscrapers Water).",
                    "Ação 2: Renomear os 3 Shorts zerados com gancho de paradoxo nos primeiros 40 caracteres.",
                    "Ação 3: Publicar o próximo master ('The 1,200 m/s Water Hammer Shockwave') com thumb de Hero Object em alto contraste."
                ],
                "metric_targets": {
                    "shorts_shown_in_feed": "> 1.500 impressões",
                    "viewed_vs_swiped": "> 60% Viewed",
                    "long_views": "> 300 views nas primeiras 72h"
                },
                "success_decision": "Adotar títulos de paradoxo absoluto em 100% dos próximos 15 vídeos do HSL.",
                "failure_decision": "Se o alcance em inglês continuar travado, auditar a pronúncia e ritmo da narração ElevenLabs (Chris)."
            }

        else: # brecha
            return {
                "duration_days": 14,
                "hypothesis": "Se eliminarmos o ALL CAPS nos títulos, substituirmos por copy forense de cronômetro ('A Rota dos 180 Segundos') e pararmos de dividir Shorts em partes sequenciais, a retenção e o clique externo crescerão sem depender dos inscritos inativos.",
                "test_design": [
                    "Ação 1: Renomear os 6 vídeos longos existentes no canal adotando a fórmula forense Eugene Schwartz.",
                    "Ação 2: Publicar 2 episódios novos sobre fraudes com alta busca ativa (Spoofing da URA Bancária e Golpe do Falso Comprovante).",
                    "Ação 3: Postar Shorts autocontidos de 45s com o 'Momento da Brecha' explícito aos 15 segundos."
                ],
                "metric_targets": {
                    "external_search_traffic": "> 35% das visualizações",
                    "ctr_impressions": "> 7.5%",
                    "avd_pct": "> 50%"
                },
                "success_decision": "Manter tom documental premium de Defesa Cotidiana e iniciar produção da série 'Anatomia do Golpe'.",
                "failure_decision": "Se inscritos continuarem sabotando a CTR da Home, criar campanhas direcionadas para reciclar a base."
            }

channel_diagnostic = ChannelDiagnostic()
