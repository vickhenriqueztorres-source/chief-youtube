# -*- coding: utf-8 -*-
"""
Hermes Chief Skill: theme-decider
Evaluates and prioritizes upcoming video ideas using Chief quantitative equations:
P = D x C x R x E (Potential Score, 1 to 625)
S = B - C - R (Strategic Decision Score)
Classifies as P0, P1, P2 and delivers Top 3 validated themes.
"""

import json
from pathlib import Path
from typing import Dict, Any, List, Optional

from src.core.memory import chief_memory

class ThemeDecider:
    """Quantitative decision engine for YouTube documentary themes."""

    # Curated virgin high-potential theme catalog pre-filtered to guarantee zero duplication
    CANDIDATE_POOLS = {
        "o_outro_lado": [
            {
                "episode_id": "OOL_MATRIZ_01",
                "topic": "Os 40 Segundos Que Quase Deixaram São Paulo Sem Água por 3 Meses",
                "unit": "40 segundos vs 20 milhões de sedentos",
                "micro_vs_macro": "40 segundos <-> 20 milhões de sedentos",
                "d": 5, "c": 5, "r": 5, "e": 5, # P = 625
                "benefit": 10, "cost": 3, "risk": 1, # S = 6
                "thesis": "A falha nas válvulas de recalque do Sistema Cantareira (Estação Elevatória Santa Inês) e o golpe de aríete hidráulico que quase colapsou o abastecimento da Grande São Paulo.",
                "hook": "Às 03 horas, 14 minutos e 08 segundos da madrugada, você estava dormindo. O que ninguém em São Paulo sabia é que nos próximos 40 segundos, uma coluna de água de 60 mil toneladas perdeu sustentação dentro da montanha.",
                "thumb_shock_text": "SEM ÁGUA",
                "thumb_digital_meter": "[ 00:40s ]"
            },
            {
                "episode_id": "OOL_MATRIZ_02",
                "topic": "O Erro de 3 Milímetros Que Fechou a Maior Refinaria de Petróleo do Brasil",
                "unit": "3 milímetros vs R$ 2 bilhões parados",
                "micro_vs_macro": "3 milímetros <-> R$ 2 bilhões parados",
                "d": 5, "c": 5, "r": 5, "e": 5, # P = 625
                "benefit": 10, "cost": 3, "risk": 1, # S = 6
                "thesis": "Fissura de fadiga térmica de 3 milímetros em tubulação de alta pressão na REPLAN em Paulínia e o efeito cascata nos estoques de combustível do país.",
                "hook": "Três milímetros. É a espessura de duas moedas empilhadas. Mas dentro da maior refinaria de petróleo do Brasil, em Paulínia, uma rachadura invisível de exatos 3 milímetros paralisou R$ 2 bilhões.",
                "thumb_shock_text": "PAROU TUDO",
                "thumb_digital_meter": "[ 3.0 MM ]"
            },
            {
                "episode_id": "OOL_MATRIZ_03",
                "topic": "O Blecaute Cibernético de 12 Minutos Que Fez os Bancos Perderem R$ 800 Milhões",
                "unit": "12 minutos vs Todo o dinheiro travado",
                "micro_vs_macro": "12 minutos <-> Todo o dinheiro travado",
                "d": 5, "c": 5, "r": 5, "e": 5, # P = 625
                "benefit": 10, "cost": 3, "risk": 1, # S = 6
                "thesis": "Falha de sincronização do relógio atômico (PTP) no SPB/PIX que travou a compensação interbancária nacional por 12 minutos.",
                "hook": "Você tentou pagar a conta, a tela girou e deu erro. Naquele exato minuto, o relógio atômico que sincroniza o Banco Central perdeu o passo por uma fração de segundo — e R$ 800 milhões ficaram presos no limbo.",
                "thumb_shock_text": "DINHEIRO TRAVADO",
                "thumb_digital_meter": "[ 12:00m ]"
            },
            {
                "episode_id": "OOL_MATRIZ_04",
                "topic": "Os 7 Centímetros de Asfalto Que Afundaram o Bairro Inteiro de Maceió",
                "unit": "7 centímetros vs 60 mil desabrigados",
                "micro_vs_macro": "7 centímetros <-> 60 mil desabrigados",
                "d": 5, "c": 5, "r": 5, "e": 5, # P = 625
                "benefit": 10, "cost": 3, "risk": 1, # S = 6
                "thesis": "O colapso estrutural da mina 18 da Braskem em câmera lenta a 1.000 metros de profundidade sob Maceió.",
                "hook": "Começou com uma rachadura na calçada onde cabia a ponta de um dedo. Sete centímetros. Mas a 1.000 metros debaixo daquelas casas em Maceió, o teto de uma caverna gigante de sal estava cedendo no escuro.",
                "thumb_shock_text": "ENGOLIU TUDO",
                "thumb_digital_meter": "[ -7.0 CM ]"
            },
            {
                "episode_id": "OOL_MATRIZ_05",
                "topic": "O Relê de R$ 300 Que Quase Destruiu Itaipu no Meio da Madrugada",
                "unit": "R$ 300 vs Metade da energia do país",
                "micro_vs_macro": "R$ 300 <-> Metade da energia do país",
                "d": 5, "c": 5, "r": 5, "e": 5, # P = 625
                "benefit": 10, "cost": 3, "risk": 1, # S = 6
                "thesis": "Desarme em cascata de linhas de transmissão de 765 kV no setor de Foz do Iguaçu provocado por falha em relé secundário.",
                "hook": "Uma peça eletrônica que custa menos de R$ 300. Mas quando esse único relé tomou a decisão errada no meio da madrugada em Foz do Iguaçu, as linhas de 765 mil volts desarmaram em cascata.",
                "thumb_shock_text": "CUSTA R$ 300",
                "thumb_digital_meter": "[ 765 KV ]"
            },
            {
                "episode_id": "OOL_MATRIZ_06",
                "topic": "O Ponto Cego de 9 Segundos Que Explodiu o Maior Porto de Grãos de Santos",
                "unit": "9 segundos vs 15% do PIB agrícola",
                "micro_vs_macro": "9 segundos <-> 15% do PIB agrícola",
                "d": 5, "c": 5, "r": 5, "e": 4, # P = 500
                "benefit": 9, "cost": 3, "risk": 1, # S = 5
                "thesis": "Incêndio e deflagração por esteira transportadora superaquecida e poeira explosiva de grãos em suspensão nos túneis do Porto de Santos.",
                "hook": "Você olha para um grão de soja e vê comida. Os engenheiros do Porto de Santos olham para a poeira desse grão e veem pólvora pura. Bastaram 9 segundos num sensor cego para incendiar o corredor de exportação.",
                "thumb_shock_text": "VIROU PÓLVORA",
                "thumb_digital_meter": "[ 00:09s ]"
            },
            {
                "episode_id": "OOL_MATRIZ_07",
                "topic": "A Fraude de 1 Byte Que Travou a Receita Federal por 48 Horas",
                "unit": "1 byte vs Fronteiras e portos parados",
                "micro_vs_macro": "1 byte <-> Fronteiras e portos parados",
                "d": 5, "c": 5, "r": 5, "e": 4, # P = 500
                "benefit": 9, "cost": 3, "risk": 1, # S = 5
                "thesis": "Corrupção de tabela master nos servidores aduaneiros da SERPRO/Siscomex que paralisou portos, aeroportos e fronteiras.",
                "hook": "Oito zeros e uns. Um único byte. Mas quando esse byte corrompeu a tabela central de validação aduaneira em Brasília, milhares de caminhões nas fronteiras e navios nos portos congelaram por 48 horas.",
                "thumb_shock_text": "TRAVOU O PAÍS",
                "thumb_digital_meter": "[ 1 BYTE ]"
            },
            {
                "episode_id": "OOL_MATRIZ_08",
                "topic": "Os 15 Metros de Tubulação Que Quase Vazaram Óleo na Bacia de Santos",
                "unit": "15 metros vs Catástrofe ecológica nacional",
                "micro_vs_macro": "15 metros <-> Catástrofe ecológica nacional",
                "d": 5, "c": 5, "r": 5, "e": 4, # P = 500
                "benefit": 9, "cost": 3, "risk": 1, # S = 5
                "thesis": "Válvula submarina de segurança (Blowout Preventer - BOP) atuando no limite sob 2.000 metros de coluna d'água no Pré-Sal.",
                "hook": "A dois mil metros de profundidade no escuro absoluto da Bacia de Santos, apenas uma guilhotina hidráulica de 400 toneladas no fundo do mar separa o litoral brasileiro de um vazamento catastrófico.",
                "thumb_shock_text": "2.000M ABAIXO",
                "thumb_digital_meter": "[ 15.000 PSI ]"
            },
            {
                "episode_id": "OOL_MATRIZ_09",
                "topic": "O Desvio de 0,4 Volts Que Queimou os Trens da Linha 9 em Horário de Pico",
                "unit": "0,4 volts vs 1 milhão de pessoas a pé",
                "micro_vs_macro": "0,4 volts <-> 1 milhão de pessoas a pé",
                "d": 5, "c": 5, "r": 5, "e": 4, # P = 500
                "benefit": 9, "cost": 3, "risk": 1, # S = 5
                "thesis": "Falha de isolamento e proteção diferencial na subestação elétrica de tração ferroviária em São Paulo às 18h.",
                "hook": "Às 18 horas e 04 minutos, um milhão de pessoas tentavam voltar para casa em São Paulo. Dentro de uma subestação blindada, um desvio de 0,4 Volts abriu um arco de fogo que derreteu o sistema.",
                "thumb_shock_text": "CAOS ÀS 18H",
                "thumb_digital_meter": "[ 0.4 VOLTS ]"
            },
            {
                "episode_id": "EP_021",
                "topic": "O Segundo Exato em Que a Internet do Brasil Inteiro Esteve a Ponto de Sumir",
                "unit": "1 segundo vs 220 milhões desconectados",
                "micro_vs_macro": "1 segundo <-> 220 milhões desconectados",
                "d": 5, "c": 5, "r": 5, "e": 5, # P = 625
                "benefit": 10, "cost": 3, "risk": 1, # S = 6
                "thesis": "A âncora de navio cargueiro de 15 toneladas que arrastou os cabos submarinos de fibra óptica na Praia do Futuro em Fortaleza.",
                "hook": "Você acha que a sua internet vem de satélites no espaço. Mas se uma âncora de 15 toneladas arrastar na faixa errada de areia em Fortaleza, 99% da internet do Brasil congela em menos de um segundo.",
                "thumb_shock_text": "APAGOU TUDO",
                "thumb_digital_meter": "[ 00:01s ]"
            }
        ],
        "hidden_systems_lab": [
            {
                "topic": "Nuclear Submarine Atmospheric Regeneration Systems",
                "unit": "1 mole of O2 from seawater electrolysis",
                "d": 5, "c": 5, "r": 5, "e": 4, # P = 500
                "benefit": 10, "cost": 4, "risk": 2, # S = 4
                "thesis": "How submerged military submarines extract breathable oxygen directly from deep seawater via high-pressure electrolysis and catalytic carbon dioxide scrubbers for 180 days.",
                "hook": "150 men are breathing 300 meters beneath the Atlantic Ocean. The air they inhale was liquid seawater 4 minutes ago."
            },
            {
                "topic": "The 1,200 m/s Water Hammer Shockwave in Hydroelectric Penstocks",
                "unit": "1 shockwave of 200 bar",
                "d": 5, "c": 4, "r": 5, "e": 5, # P = 500
                "benefit": 9, "cost": 4, "risk": 1, # S = 4
                "thesis": "The supersonic acoustic pressure wave created when massive hydroelectric valves close too fast, and the subterranean relief caverns that prevent dams from exploding.",
                "hook": "Closing a 4-meter valve 2 seconds too early creates a shockwave traveling at 1,200 meters per second through solid steel."
            },
            {
                "topic": "Data Center Underground Diesel Storage & Continental Black Start",
                "unit": "1,000,000 gallons of military-spec fuel",
                "d": 4, "c": 5, "r": 4, "e": 4, # P = 320
                "benefit": 8, "cost": 3, "risk": 1, # S = 4
                "thesis": "Why artificial intelligence clusters maintain military-grade fuel reserves underground to survive 72 hours of complete civilian grid collapse.",
                "hook": "Behind every clean AI prompt is a subterranean bunker with enough diesel fuel to power a naval destroyer."
            },
            {
                "topic": "Gotthard Base Tunnel Emergency Air Pressure Shunts",
                "unit": "250 km/h aerodynamic piston wave",
                "d": 4, "c": 5, "r": 4, "e": 5, # P = 400
                "benefit": 8, "cost": 3, "risk": 1, # S = 4
                "thesis": "How engineers dissipate the massive 250 km/h piston pressure wave created by bullet trains traversing 57 km beneath the Swiss Alps.",
                "hook": "When a train enters a 57-kilometer tunnel at 250 km/h, the air in front of it acts like a solid piston of concrete."
            }
        ],
        "brecha": [
            {
                "topic": "O Golpe do Boleto Adulterado por Malware no Navegador (Man-in-the-Browser)",
                "unit": "1 linha digitável de 47 dígitos alterada no DOM",
                "d": 5, "c": 5, "r": 5, "e": 5, # P = 625 (Max)
                "benefit": 10, "cost": 4, "risk": 1, # S = 5
                "thesis": "Como extensões maliciosas de navegador interceptam o DOM da página no instante da impressão e alteram apenas o código de barras do boleto para contas laranjas sem disparar antivírus.",
                "hook": "O boleto na sua tela era da fatura real da faculdade. Mas no milissegundo em que você clicou em Imprimir, o código de barras foi trocado por uma extensão fantasma."
            },
            {
                "topic": "O Sequestro do WhatsApp via Notificação na Tela de Bloqueio",
                "unit": "1 SMS com código de 6 dígitos lido na tela apagada",
                "d": 5, "c": 5, "r": 5, "e": 4, # P = 500
                "benefit": 9, "cost": 3, "risk": 1, # S = 5
                "thesis": "A vulnerabilidade física de celulares que exibem o SMS do código de ativação do WhatsApp com o aparelho bloqueado enquanto o usuário se ausenta da mesa por 2 minutos.",
                "hook": "Seu celular estava bloqueado e com senha na mesa. Mas o invasor só precisava de 3 segundos para ler os 6 dígitos na tela apagada."
            },
            {
                "topic": "A Fraude da Venda de Milhas Aéreas e Contas Invadidas no Dark Web",
                "unit": "1 pacote de 100.000 milhas resgatado em 90 segundos",
                "d": 5, "c": 4, "r": 5, "e": 4, # P = 400
                "benefit": 8, "cost": 3, "risk": 1, # S = 4
                "thesis": "Como quadrilhas utilizam credential stuffing em programas de fidelidade de companhias aéreas para emitir passagens internacionais de madrugada antes que o SMS de alerta chegue.",
                "hook": "Você acumulou 150 mil milhas durante 3 anos. Às 04h15 da manhã, um bot emitiu uma passagem para Lisboa em seu nome."
            },
            {
                "topic": "O Golpe da Falsa Portabilidade de Empréstimo Consignado no INSS",
                "unit": "1 contrato de consignado com assinatura eletrônica falsa",
                "d": 4, "c": 5, "r": 5, "e": 4, # P = 400
                "benefit": 8, "cost": 3, "risk": 1, # S = 4
                "thesis": "O esquema criminoso que utiliza dados cadastrais vazados de aposentados para simular quitação de dívidas e transferir saldos para contas digitais abertas com fotos de RG adulterado.",
                "hook": "A ligação prometeu reduzir o juro do seu empréstimo em 40%. Quando você desligou, uma nova dívida de R$ 18.000 apareceu no seu extrato do INSS."
            }
        ]
    }

    def evaluate_themes(self, channel_slug: str, custom_ideas: Optional[List[Dict[str, Any]]] = None) -> Dict[str, Any]:
        """
        Calculates P score and S score for candidate pool and selects Top 3 ranked themes.
        STRICT DEDUPLICATION: Automatically checks persistent ChiefMemory to filter out
        themes, titles, and topics already published or currently in production.
        """
        channel = channel_slug.lower()
        editorial_file = Path(__file__).resolve().parent.parent.parent / "data" / "channels" / f"{channel}_editorial.json"
        editorial_config = {}
        if editorial_file.exists():
            try:
                with open(editorial_file, "r", encoding="utf-8") as ef:
                    editorial_config = json.load(ef)
            except Exception:
                pass

        # Use custom ideas if provided, else check editorial backlog, else fallback to candidate pools
        if custom_ideas:
            candidates = custom_ideas
        elif editorial_config.get("candidate_backlog"):
            candidates = editorial_config["candidate_backlog"]
        else:
            candidates = self.CANDIDATE_POOLS.get(channel, self.CANDIDATE_POOLS["o_outro_lado"])

        evaluated = []
        filtered_duplicates = []

        for c in candidates:
            topic = c["topic"]
            thesis = c.get("thesis", "")

            if c.get("status") in ["PUBLISHED", "IN_PRODUCTION"]:
                filtered_duplicates.append({
                    "episode_id": c.get("episode_id", "N/A"),
                    "topic": topic,
                    "status": "DISQUALIFIED_ALREADY_COVERED",
                    "lifecycle_status": c.get("status"),
                    "matched_reference": topic,
                    "match_type": "EDITORIAL_STATUS",
                    "similarity_score": 1.0,
                    "reason": f"Marcado como {c.get('status')} no backlog editorial."
                })
                continue

            # -------------------------------------------------------------
            # STEP 0: Anti-Duplication Check against Persistent ChiefMemory
            # -------------------------------------------------------------
            coverage = chief_memory.check_theme_coverage(channel, topic, thesis)
            if coverage.get("is_covered"):
                filtered_duplicates.append({
                    "episode_id": c.get("episode_id", "N/A"),
                    "topic": topic,
                    "status": "DISQUALIFIED_ALREADY_COVERED",
                    "lifecycle_status": coverage.get("status"),
                    "matched_reference": coverage.get("title_reference") or coverage.get("matched_topic"),
                    "match_type": coverage.get("match_type"),
                    "similarity_score": coverage.get("similarity_score"),
                    "reason": coverage.get("reason")
                })
                continue # DISQUALIFIED from top recommendations!

            d = c.get("d", 3)
            cl = c.get("c", 3)
            r = c.get("r", 3)
            e = c.get("e", 3)
            
            p_score = d * cl * r * e # Max 625
            
            b = c.get("benefit", 7)
            cost = c.get("cost", 4)
            risk = c.get("risk", 2)
            s_score = b - cost - risk

            # Priority classification
            if p_score >= 450 and s_score >= 2:
                priority = "P0"
                urgency = "PRODUÇÃO IMEDIATA (Próximo ciclo)"
            elif p_score >= 320:
                priority = "P1"
                urgency = "PRÓXIMA ONDA (Ciclo seguinte)"
            else:
                priority = "P2"
                urgency = "BACKLOG / NECESSITA REFATURAÇÃO"

            evaluated.append({
                "episode_id": c.get("episode_id", "N/A"),
                "status": c.get("status", "CANDIDATE"),
                "topic": topic,
                "everyday_object": c.get("everyday_object", c.get("unit", "1 unidade física")),
                "unit": c.get("unit", "1 unidade física"),
                "micro_vs_macro": c.get("micro_vs_macro", ""),
                "thesis": thesis,
                "hook_suggestion": c.get("hook", ""),
                "thumb_shock_text": c.get("thumb_shock_text", ""),
                "thumb_digital_meter": c.get("thumb_digital_meter", ""),
                "p_score": p_score,
                "s_score": s_score,
                "priority": priority,
                "urgency": urgency,
                "factors": {"D": d, "C": cl, "R": r, "E": e}
            })

        # Sort by p_score descending, then s_score
        ranked = sorted(evaluated, key=lambda x: (x["p_score"], x["s_score"]), reverse=True)
        top_3 = ranked[:3]

        strat_rec = (
            f"Iniciar produção com o tema #1 ({top_3[0]['topic']}) que obteve pontuação P={top_3[0]['p_score']} com status 100% inédito no catálogo."
            if top_3 else "Todos os temas candidatos foram desqualificados por já terem sido cobertos no canal. Injetar novas pautas virgens no backlog."
        )

        result = {
            "channel": channel,
            "top_3_selected": top_3,
            "deduplication_audit": {
                "filtered_duplicates_count": len(filtered_duplicates),
                "filtered_duplicates": filtered_duplicates,
                "anti_fatigue_guard": "ATIVO // Deduplicação por FTS5 + Sobreposição de Tokens"
            },
            "full_evaluation_list": ranked,
            "strategic_recommendation": strat_rec
        }

        if editorial_config:
            result["governance"] = {
                "policy_version": editorial_config.get("governance", {}).get("policy_version", "OOL_HYPNOTIC_MATRIX_V5"),
                "inviolable_filters": [f["question"] for f in editorial_config.get("governance", {}).get("inviolable_filters", [])],
                "active_causal_vacuum": editorial_config.get("causal_vacuum_for_next_episode", {}).get("core_dilemma", ""),
                "validated_outlier_benchmark": editorial_config.get("validated_outlier_benchmark", {}),
                "matrix_title_formula": editorial_config.get("matrix_title_formula", {}),
                "thumbnail_02s_architecture": editorial_config.get("thumbnail_02s_architecture", {}),
                "hypnotic_script_laws": editorial_config.get("hypnotic_script_laws", {}),
                "safe_grey_hat_tactics": editorial_config.get("safe_grey_hat_tactics", {})
            }
            result["adaptation_protocol"] = editorial_config.get("adaptation_protocol", {
                "rule_of_autonomy": "O agente NÃO deve copiar mecanicamente 100% da sugestão. Deve adaptar ganchos e nuances mantendo os 5 filtros e evidências."
            })

        return result

theme_decider = ThemeDecider()
