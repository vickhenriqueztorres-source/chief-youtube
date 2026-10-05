# -*- coding: utf-8 -*-
"""
Hermes Chief Trading Skill: trading-diagnostic
Executes causal bottleneck analysis and formulates 14-day Method X+Y experiments
specifically tailored for YouTube Trading Channels.
"""

from typing import Dict, Any, List

class TradingDiagnostic:
    """Diagnoses causal bottlenecks for YouTube Trading Channels."""

    def diagnose(self, channel_slug: str, metrics: Dict[str, Any]) -> Dict[str, Any]:
        long_stats = metrics.get("long_form_summary", {})
        short_stats = metrics.get("shorts_summary", {})
        subs = metrics.get("subscribers", 0)

        mean_long_views = long_stats.get("mean_views", 0.0)
        mean_short_views = short_stats.get("mean_views", 0.0)
        mean_ctr = long_stats.get("mean_ctr", 0.0)
        long_count = long_stats.get("count", 0)
        short_count = short_stats.get("count", 0)
        ret_30s = long_stats.get("mean_retention_30s", 0.0)

        # Bottleneck Hierarchy for Trading Channels
        bottlenecks: List[Dict[str, Any]] = []

        # 1. Cold Start & Shelf Depth
        if long_count < 5:
            bottlenecks.append({
                "severity": 9,
                "name": "Cold Start & Prateleira Rasa de Longos",
                "symptom": f"O canal possui apenas {long_count} vídeos longos. O algoritmo não tem massa crítica para mapear clusters temáticos.",
                "root_cause": "Biblioteca insuficiente para sustentar percursos de aprendizado e sessões estendidas no YouTube.",
                "impact": "Visitantes que chegam pelos Shorts encontram poucas respostas aprofundadas e não formam o hábito de retorno."
            })

        # 2. Broken Short-to-Long Bridge
        if short_stats.get("outliers") and (mean_long_views < mean_short_views * 0.4 or mean_long_views < 30):
            top_short = short_stats["outliers"][0]
            bottlenecks.append({
                "severity": 10,
                "name": "Ponte Desconectada: Shorts ➔ Longos (Fuga de Tráfego)",
                "symptom": f"O Short '{top_short['title'][:45]}...' teve {top_short['views']} views, enquanto a média dos longos é de apenas {mean_long_views} views.",
                "root_cause": "Ausência do link via botão 'Vídeo Relacionado' do YouTube Studio vinculando o Short ao walkthrough completo em conta demo.",
                "impact": "Tráfego de topo de funil é desperdiçado sem converter em inscritos engajados e espectadores de vídeos longos."
            })

        # 3. Packaging & CTR
        if mean_ctr < 4.0 and long_count > 0:
            bottlenecks.append({
                "severity": 8,
                "name": "Embalagem Inerte (Baixo CTR no Longo)",
                "symptom": f"CTR médio dos longos está em {mean_ctr}%, abaixo da linha de corte saudável de 4.5% a 6.0%.",
                "root_cause": "Thumbnails com títulos acadêmicos ou falta de contraste visual na vela/mecha chave. Falta o elemento de 'erro visível'.",
                "impact": "Impressões entregues pelo YouTube são desperdiçadas porque o espectador hesita no clique."
            })

        # 4. Low Drop-off in 30s
        if ret_30s < 55.0 and long_count > 0:
            bottlenecks.append({
                "severity": 8,
                "name": "Abandono nos Primeiros 30s (Falta de Entrega do Hook)",
                "symptom": f"Retenção aos 30 segundos média em {ret_30s}%. Mais de 45% dos cliques abandonam antes do Ato 2.",
                "root_cause": "O vídeo demora a abrir o gráfico, usa introdução burocrática ou não mostra imediatamente a vela com o erro.",
                "impact": "O algoritmo interpreta insatisfação inicial e cessa a distribuição por navegação."
            })

        # Sort by severity
        bottlenecks.sort(key=lambda b: b["severity"], reverse=True)
        primary = bottlenecks[0] if bottlenecks else {
            "severity": 5,
            "name": "Operação Estável em Calibração",
            "symptom": "Métricas dentro dos desvios normais da fase de lançamento.",
            "root_cause": "Canal em processo de indexação algorítmica pelo YouTube.",
            "impact": "Manter cadência e aprofundar consistência."
        }

        # Formulate 14-Day Method X+Y Experiment
        if primary["name"].startswith("Ponte Desconectada"):
            experiment = {
                "hypothesis": "Se conectarmos os Shorts de maior tração (ex: 'El color de la vela te engaña' com 152 views) aos vídeos longos correspondentes através do botão oficial 'Vídeo Relacionado' no YouTube Studio + fixar comentário com checklist em conta demo, então as visualizações dos vídeos longos subirão em pelo menos 150% nos próximos 14 dias porque o público intrigado pelo Short receberá o caminho natural de verificação completa na tela.",
                "test_design": [
                    "1. Acessar o YouTube Studio e vincular o Short WGz-rzMcN7g ao vídeo longo 1rWRfv5_gdg ('Cómo Interpretar una Vela Paso a Paso') via botão 'Vídeo Relacionado'.",
                    "2. Fixar comentário no Short com cópia canônica: '¿Quieres ver cómo funciona esto en pantalla completa y en cuenta demo? Mira el video completo acá arriba. Sin adivinar.'",
                    "3. Publicar 2 novos Shorts derivados do vídeo longo IfYlcD1DN0o ('Una vela sola te engaña') usando o hook canônico de 3 segundos com o avatar e zoom no pavio.",
                    "4. Monitorar o fluxo de tráfego na aba Alcance > Tipos de origem de tráfego ('Outros recursos do YouTube' / 'Telas finais')."
                ],
                "metric_targets": {
                    "views_longo_alvo": "≥ 60 views (2x baseline atual)",
                    "ctr_longo": "≥ 4.5%",
                    "inscritos_novos": "≥ +10 inscritos qualificados"
                },
                "success_decision": "Se o vídeo longo ultrapassar 50 views vindas de Shorts, oficializar a regra: todo Short gravado deve obrigatoriamente ser a fenda de um longo publicado."
            }
        elif primary["name"].startswith("Cold Start"):
            experiment = {
                "hypothesis": "Se publicarmos 4 vídeos longos estruturantes (8-12 min) cobrindo os 4 pilares essenciais (corpo vs mecha, suporte/resistência em demo, erro do martingale, checklist antes do clique) com a identidade canônica do Profe, então a retenção de sessão aumentará em 40% porque o espectador terá percurso para maratonar.",
                "test_design": [
                    "1. Emitir briefings P0 para os episódios estruturantes em Deriv e IQ Option.",
                    "2. Organizar os vídeos na playlist canônica 'Modo Demo — Aprende Desde Cero'.",
                    "3. Adicionar telas finais direcionando para o próximo vídeo da sequência."
                ],
                "metric_targets": {
                    "catalogo_longos": "7 vídeos longos publicados",
                    "avd_medio": "≥ 45%"
                },
                "success_decision": "Se o espectador assistir ≥ 1.5 vídeos por sessão, validar a cadência de 2 longos/semana."
            }
        else:
            experiment = {
                "hypothesis": "Se ajustarmos as thumbnails para Dark Mode puro com zoom em 1 vela com mecha e texto em amarelo ácido '¿SUBIDA FALSA?', o CTR subirá para ≥ 5.0% porque o contraste causal atrai o Verificador Desconfiado.",
                "test_design": [
                    "1. Gerar thumbnail A/B para o vídeo 1rWRfv5_gdg sem rosto e com zoom extremo na mecha.",
                    "2. Reduzir texto da miniatura para no máximo 3 palavras.",
                    "3. Medir variação de CTR por 7 dias."
                ],
                "metric_targets": {
                    "ctr": "≥ 5.0%"
                },
                "success_decision": "Adotar o modelo de zoom extremo para todos os vídeos da série Modo Demo."
            }

        return {
            "channel_slug": channel_slug,
            "primary_bottleneck": primary,
            "all_detected_bottlenecks": bottlenecks,
            "proposed_experiment": experiment
        }

trading_diagnostic = TradingDiagnostic()
