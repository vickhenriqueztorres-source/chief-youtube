# -*- coding: utf-8 -*-
"""
Hermes Chief Skill: squad-briefing
Generates structured, typed JSON briefings for the editing squads of the 3 channels.
Strictly separates strategic decision from production execution.
"""

import json
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, Any, Optional

class SquadBriefingGenerator:
    """Produces canonical JSON briefs for editing squads without touching timelines."""

    def __init__(self, output_dir: Optional[Path] = None):
        self.output_dir = output_dir or (Path(__file__).resolve().parent.parent.parent / "data" / "briefings_output")
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def generate_briefing(self, channel_slug: str, episode_id: str, custom_params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Creates an executive JSON briefing for the designated channel squad.
        """
        channel = channel_slug.lower()
        now = datetime.now()
        deadline = (now + timedelta(days=7)).strftime("%Y-%m-%d")

        # Map channel slugs to editorial config filenames
        slug_to_file = {
            "hidden_systems_lab": "hsl_editorial.json",
            "hsl": "hsl_editorial.json",
            "o_outro_lado": "o_outro_lado_editorial.json",
            "outro_lado": "o_outro_lado_editorial.json",
            "brecha": "brecha_editorial.json",
            "linha_de_fogo": "linha_de_fogo_editorial.json",
            "linhadefogo": "linha_de_fogo_editorial.json"
        }
        editorial_filename = slug_to_file.get(channel, f"{channel}_editorial.json")
        editorial_file = Path(__file__).resolve().parent.parent.parent / "data" / "channels" / editorial_filename
        editorial_config = {}
        if editorial_file.exists():
            try:
                with open(editorial_file, "r", encoding="utf-8") as ef:
                    editorial_config = json.load(ef)
            except Exception:
                pass

        ep_norm = episode_id.upper().replace("_", "").replace("-", "")
        approved_ep = editorial_config.get("current_approved_episode", {})
        backlog_eps = editorial_config.get("candidate_backlog", [])
        approved_norm = approved_ep.get("episode_id", "").upper().replace("_", "").replace("-", "")

        if channel in ["o_outro_lado", "outro_lado"]:
            squad = "Squad O Outro Lado"
            tema = custom_params.get("tema", "Os 40 Segundos Que Quase Deixaram São Paulo Sem Água por 3 Meses") if custom_params else "Os 40 Segundos Que Quase Deixaram São Paulo Sem Água por 3 Meses"
            unidade = custom_params.get("unidade", "40 segundos nas válvulas de recalque vs 20 milhões de sedentos") if custom_params else "40 segundos nas válvulas de recalque vs 20 milhões de sedentos"
            tese = "A falha crítica nas válvulas de recalque e bombas de alta pressão do Sistema Cantareira (Estação Elevatória Santa Inês), onde um golpe de aríete hidráulico de 40 segundos quase destruiu a adutora principal de São Paulo."
            publico = "Brasileiros de 18 a 44 anos impactados pelo contraste extremo Micro vs Macro e vulnerabilidade sistêmica de infraestruturas críticas."
            desejo = "Descobrir o mecanismo oculto que quase causou uma catástrofe nacional em uma fração cirúrgica de tempo."
            angulo = "Fórmula Matriz: [Catástrofe / Notícia Ruim] + [Tempo Cirúrgico / Mecanismo Invisível] (Contraste Micro vs Macro validado pelo outlier Z=3.08)."
            promessa = "Revelar em tensão forense como uma falha invisível de segundos ou milímetros ameaça milhões de brasileiros sem que a TV aberta explique."
            referencias = [
                "SABESP / ANA - Relatório Técnico de Segurança Hídrica do Sistema Cantareira e Estação Elevatória Santa Inês",
                "ONS / ANEEL - Relatórios de Análise de Perturbação (RAP) de Infraestruturas Críticas Nacionais",
                "ABNT NBR 12215 - Projeto de Linha Adutora de Água e Transientes Hidráulicos (Golpe de Aríete)"
            ]
            prioridade = "P0"
            risco = "Manter rigor 100% forense e documental (35mm Denis Villeneuve chiaroscuro). Zero clickbait vazio; a promessa da capa deve ser provada nos primeiros 15 segundos."
            metrica_alvo = "CTR > 7.5% na Home (A/B test nas primeiras 6h; corte em 5.5% após 300 impressões) e Retenção > 65%"
            entregaveis = [
                "Master do Documentário Longo (1080p 30fps) com As 5 Leis Hipnóticas (Open Loops, Pattern Interrupt a cada 35-50s com sub-grave braam/heartbeat, números concretos e pausas táticas de 0.8s)",
                "Short Ponte Vertical 9:16 (Momento de Ruptura de 45s cortado no clímax absoluto + botão 'Vídeo Relacionado' apontando para o Master)",
                "3 Thumbnails 4K (Arquitetura 0,2s: Dark Mode 60-70% + Hero Object Único + Texto de Choque 2-3 palavras em Amarelo Brutalista SEM repetir título + Medidor Digital Neon [ 00:01s ])",
                "Arquivo de Legenda Manual (.srt) em texto puro com Seeding de Metadados Semânticos (BERT/Gemini NLP) + Loop de Sessão Fechado (End Screen de 1 único vídeo nos últimos 15s + &list=PL... no comentário fixado)"
            ]
            o_que_nao_fazer = [
                "NÃO repetir nenhuma palavra do título dentro do texto da thumbnail (máximo 2 a 3 palavras de choque na capa).",
                "NÃO fazer saudações ou introduções genéricas; abrir nos primeiros 15s com timestamp cirúrgico + colapso macro + causa microscópica.",
                "NÃO fechar blocos narrativos sem abrir a próxima pergunta invisível (Open Loop constante)."
            ]
            o_que_priorizar_na_abertura = (
                "0:00 - 0:15 (Gancho Hipnótico): Timestamp exato ('Às 03h14m08s, você estava dormindo...') + "
                "Contraste Micro vs Macro (fração de segundos/milímetros vs milhões de pessoas atingidas) + "
                "Comandos embutidos com pausas táticas de 0.8s nas palavras-gatilho: Observe, Silêncio, Falhou, Invisível, Ruptura."
            )
            o_que_evitar = [
                "Evitar números vagos ('muito dinheiro', 'grande distância') — ancorar sempre em números concretos ('R$ 4.238 por minuto', '1.840 km de cabo pressurizado').",
                "Evitar enviar o espectador para a home no final — usar exclusivamente 1 vídeo recomendado na End Screen (últimos 15s) e link com &list=PL... no comentário fixado."
            ]

        elif channel in ["hidden_systems_lab", "hsl"]:
            if approved_ep and (ep_norm == approved_norm or ep_norm in ["HSL028", "HSL_028", "028", "HSLP1002"]):
                squad = "Squad HSL Global"
                tema = custom_params.get("tema", approved_ep.get("title_master", approved_ep.get("topic", "Data Center Underground Diesel Storage & Continental Black Start"))) if custom_params else approved_ep.get("title_master", approved_ep.get("topic", "Data Center Underground Diesel Storage & Continental Black Start"))
                unidade = custom_params.get("unidade", approved_ep.get("unit", "1,000,000 gallons of military-spec fuel")) if custom_params else approved_ep.get("unit", "1,000,000 gallons of military-spec fuel")
                tese = approved_ep.get("thesis", "Why artificial intelligence clusters maintain military-grade fuel reserves underground to survive 72 hours of complete civilian grid collapse.")
                publico = approved_ep.get("target_audience", "Senior systems engineers, AI infrastructure architects, electrical engineers, industrial enthusiasts (USA, UK, EU).")
                desejo = approved_ep.get("dominant_desire", "Discovering the extreme physical and mechanical reality supporting invisible digital cloud and AI infrastructure.")
                angulo = approved_ep.get("editorial_angle", "The physical paradox that 21st-century neural networks are physically tethered to 20th-century heavy mechanical diesel compression engines.")
                promessa = approved_ep.get("main_promise", "Reveal the hidden subterranean architecture of high-density data centers: the 10-second UPS flywheel cascade, the underground fuel delivery grid, and the protocol for surviving a total continental blackout.")
                referencias = approved_ep.get("references", [
                    "Uptime Institute - Tier IV Data Center Backup Power & Fuel Storage Standards",
                    "IEEE Standard 446 - Recommended Practice for Emergency and Standby Power Systems",
                    "NFPA 110 - Standard for Emergency and Standby Power Systems (Fuel Maintenance & Polishing Protocols)"
                ])
                prioridade = approved_ep.get("priority", "P0")
                risco = approved_ep.get("risk", "Balance mathematical equations with dramatic industrial visuals (underground fuel halls, massive Cat/Cummins V16 generators, switchgear arc flash zones).")
                metrica_alvo = approved_ep.get("target_metric", "Average View Duration > 50% and > 1.000 views in first 72h.")
                entregaveis = [
                    "Master Episode 1080p 30fps (9 to 13 minutes) normalized to -16 LUFS",
                    "3 Standalone Shorts 9:16 (Each containing a 45s self-contained paradox)",
                    "3 A/B/C 4K Thumbnail Packages (Hero Object + Vector HUD telemetry)",
                    "Clean .packaging.json with search-optimized title variants"
                ]
                o_que_nao_fazer = [
                    "DO NOT publish Shorts titled with just hashtags (#Shorts #Engineering). Every Short MUST have a 40-character paradox hook.",
                    "DO NOT use fictional cyberpunk interfaces. Use only engineering telemetry and CAD/X-Ray orthographic diagrams.",
                    "DO NOT re-upload duplicate video files under any circumstance."
                ]
                o_que_priorizar_na_abertura = approved_ep.get("opening_priority", "0:00 - 0:15: Behind every clean AI prompt is a subterranean bunker with enough military-spec diesel fuel to power a naval destroyer for 72 hours.")
                o_que_evitar = [
                    "Avoid cartoonish 3D figures or generic stock video of people turning lights on in houses.",
                    "Avoid speeding up narration; maintain Chris's cold, surgical, 146 wpm delivery."
                ]
            else:
                squad = "Squad HSL Global"
                tema = custom_params.get("tema", "How Engineers Restart a Dead Power Grid from Absolute Zero (Black Start)") if custom_params else "How Engineers Restart a Dead Power Grid from Absolute Zero (Black Start)"
                unidade = custom_params.get("unidade", "0.0 Megawatts (Zero Electrical Reference)") if custom_params else "0.0 Megawatts (Zero Electrical Reference)"
                tese = "Modern civilization depends on electrical inertia; restarting a continental system without grid voltage requires bootstrapping physics from diesel crankshafts to gigawatt dams."
                publico = "Senior systems engineers, backend architects, electrical engineers, industrial enthusiasts (USA & Europe)."
                desejo = "Understanding how complex distributed systems recover from catastrophic total failure states (disaster recovery at continental scale)."
                angulo = "The physics of synchronous frequency: why energizing a dead transmission line requires absorbing massive capacitive reactive power without tripping generators."
                promessa = "Reveal the exact sequence of 12 mechanical operations that bring a dark continent back to 50/60.00 Hz."
                referencias = [
                    "NERC Reliability Standard EOP-005-3 - System Restoration from Blackstart Resources",
                    "IEEE Power & Energy Magazine - The Black Start Dilemma in Inverter-Dominated Grids",
                    "ENTSO-E Blackout & Restoration Guidelines"
                ]
                prioridade = "P0"
                risco = "Becoming too dry/academic. Balance mathematical equations with dramatic industrial visuals (giant turbine halls, high voltage switchyards)."
                metrica_alvo = "Average View Duration > 50% and > 1.000 views in first 72h."
                entregaveis = [
                    "Master Episode 1080p 30fps (9 to 13 minutes) normalized to -16 LUFS",
                    "3 Standalone Shorts 9:16 (Each containing a 45s self-contained paradox)",
                    "3 A/B/C 4K Thumbnail Packages (Hero Object + Vector HUD telemetry)",
                    "Clean .packaging.json with search-optimized title variants"
                ]
                o_que_nao_fazer = [
                    "DO NOT publish Shorts titled with just hashtags (#Shorts #Engineering). Every Short MUST have a 40-character paradox hook.",
                    "DO NOT use fictional cyberpunk interfaces. Use only engineering telemetry and CAD/X-Ray orthographic diagrams.",
                    "DO NOT re-upload duplicate video files under any circumstance."
                ]
                o_que_priorizar_na_abertura = (
                    "0:00 - 0:15: Total continental silence. A substation with zero volts. "
                    "Paradoxo: To start a turbine, you need electricity. To generate electricity, you need a turbine. How do you break the loop?"
                )
                o_que_evitar = [
                    "Avoid cartoonish 3D figures or generic stock video of people turning lights on in houses.",
                    "Avoid speeding up narration; maintain Chris's cold, surgical, 146 wpm delivery."
                ]

        elif channel == "brecha":
            if approved_ep and ep_norm == approved_norm:
                squad = "Squad Brecha V2 (Cinematic Investigative Noir)"
                tema = custom_params.get("tema", approved_ep.get("title_master", "O Adesivo de 5 cm Que Pode Mandar Seu Pix Para Outra Conta")) if custom_params else approved_ep.get("title_master", "O Adesivo de 5 cm Que Pode Mandar Seu Pix Para Outra Conta")
                unidade = custom_params.get("unidade", approved_ep.get("anatomy", {}).get("everyday_object", "Placa de acrílico de QR Code no balcão com adesivo de 5 cm sobreposto")) if custom_params else approved_ep.get("anatomy", {}).get("everyday_object", "Placa de acrílico de QR Code no balcão com adesivo de 5 cm sobreposto")
                tese = "Dissecação forense e engenharia sombria do cotidiano: como uma pequena fissura física em um objeto de confiança desvia recursos em segundos sem disparar alertas."
                publico = "Brasileiros de 18 a 44 anos, espectadores de documentários investigativos, tecnologia, finanças e engenharia reversa."
                desejo = "Fechar o loop cognitivo do Paradoxo de Zeigarnik e enxergar a engrenagem invisível por trás de objetos cotidianos."
                angulo = approved_ep.get("anatomy", {}).get("breach_point", "A fissura física entre o objeto legítimo e o elemento adulterado no ponto cego da rotina.")
                promessa = "Dissecar a anatomia da falha nos 3 Mundos (Mundo Real, Evidência em Papel #E9E4DA, Sistema A->B->C) e blindar o espectador com 3 protocolos práticos."
                referencias = [
                    "Banco Central do Brasil - Arquitetura e Regras do SPI / Payload EMVCo",
                    "ANATEL / DEIC - Relatórios Periciais de Engenharia Social e Adulteração Física",
                    "FEBRABAN - Dossiê de Prevenção e Anatomia de Fraudes Financeiras"
                ]
                prioridade = "P0"
                risco = "Evitar termos bloqueados ('golpe, roubo, quadrilha') no título para não acionar o filtro Harmful & Dangerous Policies (Yellow Icon)."
                metrica_alvo = "CTR de Browse/Home > 8.5%, Retenção 0:30 > 70% e Retenção nos Shorts em Loop > 125%"
                entregaveis = [
                    "Master Documentário (8 a 11 min) em Cinematic Investigative Noir (#0A0A0A Obsidian, #171717 Charcoal, #E9E4DA Paper Bone White, #EF2B1D Brecha Red Fissura) alternando entre os 3 Mundos (01 Mundo Real, 02 Evidência Física, 03 Sistema A->B->C) + Picos Límbicos a cada 7-10s (+10% exposição por 3 frames + som CRACK)",
                    "4 Shorts 9:16 com Topologia em Laço Perfeito (Infinite Loop: a última meia-frase completa sintaticamente o segundo 0.0s da abertura + drone contínuo)",
                    "Thumbnail V2 (Lei de Weber 0.2s): Composição 55/45 ou 60/40 — Hero Object Cotidiano (45-65%) + Fissura Vermelha (#EF2B1D) + Consequência em 2 a 4 palavras em Sans Condensada Pesada (ex: 'PIX DESVIADO') sobre mesa escura",
                    "Arquivo .SRT com Envenenamento Semântico (Vetor 1: locução exata + clusters de alto CPM nos segundos finais silenciosos para indexação Gemini/BERT) + Guilhotina de Sequestro de Sessão nos últimos 15s + 1 Armadilha Técnica de Comentários"
                ]
                o_que_nao_fazer = [
                    "NÃO usar as palavras 'golpe', 'roubo', 'quadrilha' ou ALL CAPS gritado no título.",
                    "NÃO usar ciano (#00E5FF), amarelo ácido, HUD sci-fi, estética Matrix ou fonte monoespaçada como protagonista.",
                    "NÃO fazer CTA genérico ('inscreva-se e deixe o like'); aplicar a Guilhotina de Atenção nos últimos 15s abrindo o loop para o próximo dossiê com apenas 1 vídeo na Tela Final #0A0A0A."
                ]
                o_que_priorizar_na_abertura = (
                    "0:00 - 0:15 (Abertura Eriksoniana): Dado/Situação Improvável -> Consequência Visceral -> [Corte Seco + Som CRACK] -> Revelação do Mecanismo. "
                    "Zero saudações. A Fissura Vermelha (#EF2B1D) rasga a tela no segundo exato da ruptura."
                )
                o_que_evitar = [
                    "Evitar repetir palavras do título no texto da thumbnail (Thumbnail = Consequência | Título = Mecanismo).",
                    "Evitar mais de 10 segundos sem um Pico Límbico óptico/acústico."
                ]
            else: # brecha V2 fallback
                squad = "Squad Brecha V2 (Cinematic Investigative Noir)"
                tema = custom_params.get("tema", "Os 180 Segundos Antes de R$ 5.000 Sumirem") if custom_params else "Os 180 Segundos Antes de R$ 5.000 Sumirem"
                unidade = custom_params.get("unidade", "180 segundos entre a confirmação e a pulverização em 4 destinos") if custom_params else "180 segundos entre a confirmação e a pulverização em 4 destinos"
                tese = "Dissecação forense da assimetria temporal: enquanto a reação humana leva 45 minutos, a automação pulveriza o saldo em 180 segundos."
                publico = "Brasileiros de 18 a 44 anos que assistem documentários investigativos, finanças e engenharia reversa."
                desejo = "Compreender a arquitetura oculta do sistema financeiro e proteger seu patrimônio."
                angulo = "Guilhotina Temporal (Efeito Zeigarnik): os três minutos invisíveis entre o clique na tela e o esvaziamento das camadas."
                promessa = "Mostrar na mesa de evidências (#E9E4DA) e no diagrama A->B->C exatamente o que ocorre nesses 180 segundos e como ativar a contenção."
                referencias = [
                    "Banco Central do Brasil - Resolução BCB nº 103 (Regulamento MED)",
                    "FEBRABAN - Relatório de Prevenção e Combate a Fraudes Eletrônicas",
                    "DEIC/SP - Inquéritos sobre Contas de Passagem em Cascata"
                ]
                prioridade = "P0"
                risco = "Evitar tom policial sensacionalista ou termos bloqueados no título. Manter estética Cinematic Investigative Noir."
                metrica_alvo = "CTR de Browse/Home > 8.5%, Retenção 0:30 > 70% e Retenção nos Shorts em Loop > 125%"
                entregaveis = [
                    "Master Documentário (8 a 11 min) em Cinematic Investigative Noir (#0A0A0A, #171717, #E9E4DA, #EF2B1D) com os 3 Mundos + Picos Límbicos a cada 7-10s",
                    "4 Shorts 9:16 em Topologia de Laço Perfeito (Infinite Loop)",
                    "Thumbnail V2 (Lei de Weber 0.2s): Hero Object + Fissura Vermelha (#EF2B1D) + Consequência em 2-4 palavras ('TARDE DEMAIS')",
                    "Arquivo .SRT com Envenenamento Semântico de alto CPM + Sequestro de Sessão nos últimos 15s"
                ]
                o_que_nao_fazer = [
                    "NÃO usar 'golpe/roubo/quadrilha' ou ALL CAPS no título.",
                    "NÃO usar estética sci-fi, ciano ou neon.",
                    "NÃO encerrar o vídeo sem abrir o loop imediato para o próximo episódio (Sequestro de Sessão)."
                ]
                o_que_priorizar_na_abertura = (
                    "0:00 - 0:15 (Abertura Eriksoniana): 'Às 14h12, R$ 5.000 entraram nesta conta. Às 14h15, o dinheiro já estava dividido entre quatro destinos. "
                    "Quando o sistema tentou bloquear a primeira transferência, praticamente não havia mais nada para bloquear. [Corte + CRACK] Esses três minutos são o verdadeiro centro desta história.'"
                )
                o_que_evitar = [
                    "Evitar repetir palavras do título na thumbnail.",
                    "Evitar fontes monoespaçadas fora de timestamps, números e IDs de documentos."
                ]

        elif channel in ["linha_de_fogo", "linhadefogo"]:
            squad = "Squad Linha de Fogo (Espionage Thriller 60s/70s)"
            found_ep = None
            if approved_ep:
                found_ep = approved_ep
            else:
                for b_ep in backlog_eps:
                    if b_ep.get("episode_id", "").upper() == ep_norm:
                        found_ep = b_ep
                        break

            if found_ep:
                tema = custom_params.get("tema", found_ep.get("topic", "A Guerra Secreta de Espiões entre Coca-Cola e Pepsi na União Soviética")) if custom_params else found_ep.get("topic", "A Guerra Secreta de Espiões entre Coca-Cola e Pepsi na União Soviética")
                unidade = custom_params.get("unidade", found_ep.get("unit", "1 frota militar de submarinos soviéticos trocada por refrigerante")) if custom_params else found_ep.get("unit", "1 frota militar de submarinos soviéticos trocada por refrigerante")
                tese = found_ep.get("thesis", "Como a diplomacia corporativa da Guerra Fria transformou a Pepsi na 6ª maior marinha militar do mundo para sufocar a Coca.")
                publico = "22 a 55 anos (foco 25-45): empreendedores, investidores, executivos e entusiastas de história corporativa e estratégia de bastidores."
                desejo = "Ver o que aconteceu a portas fechadas nas salas de reunião onde magnatas decidiram destruir seus concorrentes."
                angulo = "Ataque Clandestino ➔ Retaliação do Rival ➔ Consequência Bilionária (Lado A | CORTE DIAGONAL | Lado B)."
                promessa = "Revelar os documentos secretos, a sabotagem interna e as decisões impiedosas que construíram e derrubaram impérios bilionários."
                referencias = [
                    "Wall Street Journal / Financial Times / Forbes - Arquivos e Reportagens de Época",
                    "Processos Judiciais Públicos, Quebras de Contrato e Registros Antitruste (FTC/DOJ)",
                    "Biografias Autorizadas e Dossiês Documentais de Guerras Corporativas"
                ]
                prioridade = "P0"
                risco = "Evitar tom escolar ou biografia Wikipedia. Manter estética Thriller de Espionagem Anos 60/70 (Saul Bass) e tensão de guerra fria corporativa."
                metrica_alvo = "CTR de Browse/Home > 8.0%, Retenção 0:30 > 65% e AVD > 52%"
                entregaveis = [
                    "Master do Documentário (11:00 a 14:30 min, 1080p/4K 24fps) com 5 Atos Canônicos, silhuetas posterizadas, colagem de papel e jazz de espionagem (sax, contrabaixo, teletipo)",
                    "2 Shorts de Gancho Verticais 9:16 (30-50s) com corte diagonal dividindo Lado A e Lado B + botão oficial apontando para o Longo",
                    "3 Thumbnails 4K (Blueprint Saul Bass): Rosto de Magnata em meia-luz ou 2 Logos em colisão + Corte Diagonal Vermelho (#C62D1F) + Texto de Choque de 2-3 palavras (ex: 'FROTA SECRETA')",
                    "Arquivo de Legenda (.srt) em texto puro + End Screen de vídeo único apontando para o próximo dossiê do canal"
                ]
                o_que_nao_fazer = [
                    "NÃO usar estética neon, gradientes digitais, glow sci-fi ou visual dark cinematográfico genérico.",
                    "NÃO usar fotografia colorida crua sem tratamento em duotone (Preto x Papel, Preto x Vermelho ou Preto x Mostarda).",
                    "NÃO fazer títulos escolares/descritivos ('A história da rivalidade...'); usar títulos de conflito causal extremo."
                ]
                o_que_priorizar_na_abertura = (
                    "0:00 - 0:15 (Gancho Hipnótico Zeigarnik): Fato mais absurdo e inacreditável revelado de imediato + "
                    "Corte diagonal na tela dividindo os dois rivais + som de teletipo/clique mecânico. Zero saudações."
                )
                o_que_evitar = [
                    "Evitar clichês motivacionais ou celebração corporativa higienizada.",
                    "Evitar mostarda (#D4A537) em excesso (máximo 10% do frame, reservada exclusivamente para dinheiro ou selos de valor)."
                ]
            else:
                tema = custom_params.get("tema", "A Guerra Secreta de Espiões entre Coca-Cola e Pepsi na União Soviética") if custom_params else "A Guerra Secreta de Espiões entre Coca-Cola e Pepsi na União Soviética"
                unidade = custom_params.get("unidade", "1 frota militar de submarinos soviéticos trocada por refrigerante") if custom_params else "1 frota militar de submarinos soviéticos trocada por refrigerante"
                tese = "Como a diplomacia corporativa da Guerra Fria transformou a Pepsi na 6ª maior marinha militar do mundo para sufocar a Coca."
                publico = "22 a 55 anos (foco 25-45): empreendedores, investidores, executivos e entusiastas de história corporativa e estratégia de bastidores."
                desejo = "Ver o que aconteceu a portas fechadas nas salas de reunião onde magnatas decidiram destruir seus concorrentes."
                angulo = "Ataque Clandestino ➔ Retaliação do Rival ➔ Consequência Bilionária (Lado A | CORTE DIAGONAL | Lado B)."
                promessa = "Revelar os documentos secretos, a sabotagem interna e as decisões impiedosas que construíram e derrubaram impérios bilionários."
                referencias = [
                    "Wall Street Journal / Financial Times / Forbes - Arquivos e Reportagens de Época",
                    "Processos Judiciais Públicos, Quebras de Contrato e Registros Antitruste (FTC/DOJ)",
                    "Biografias Autorizadas e Dossiês Documentais de Guerras Corporativas"
                ]
                prioridade = "P0"
                risco = "Evitar tom escolar ou biografia Wikipedia. Manter estética Thriller de Espionagem Anos 60/70 (Saul Bass) e tensão de guerra fria corporativa."
                metrica_alvo = "CTR de Browse/Home > 8.0%, Retenção 0:30 > 65% e AVD > 52%"
                entregaveis = [
                    "Master do Documentário (11:00 a 14:30 min, 1080p/4K 24fps) com 5 Atos Canônicos, silhuetas posterizadas, colagem de papel e jazz de espionagem (sax, contrabaixo, teletipo)",
                    "2 Shorts de Gancho Verticais 9:16 (30-50s) com corte diagonal dividindo Lado A e Lado B + botão oficial apontando para o Longo",
                    "3 Thumbnails 4K (Blueprint Saul Bass): Rosto de Magnata em meia-luz ou 2 Logos em colisão + Corte Diagonal Vermelho (#C62D1F) + Texto de Choque de 2-3 palavras (ex: 'FROTA SECRETA')",
                    "Arquivo de Legenda (.srt) em texto puro + End Screen de vídeo único apontando para o próximo dossiê do canal"
                ]
                o_que_nao_fazer = [
                    "NÃO usar estética neon, gradientes digitais, glow sci-fi ou visual dark cinematográfico genérico.",
                    "NÃO usar fotografia colorida crua sem tratamento em duotone (Preto x Papel, Preto x Vermelho ou Preto x Mostarda).",
                    "NÃO fazer títulos escolares/descritivos ('A história da rivalidade...'); usar títulos de conflito causal extremo."
                ]
                o_que_priorizar_na_abertura = (
                    "0:00 - 0:15 (Gancho Hipnótico Zeigarnik): Fato mais absurdo e inacreditável revelado de imediato + "
                    "Corte diagonal na tela dividindo os dois rivais + som de teletipo/clique mecânico. Zero saudações."
                )
                o_que_evitar = [
                    "Evitar clichês motivacionais ou celebração corporativa higienizada.",
                    "Evitar mostarda (#D4A537) em excesso (máximo 10% do frame, reservada exclusivamente para dinheiro ou selos de valor)."
                ]

        # Mine or attach spontaneous customer language (Eugene Schwartz Step 2)
        spontaneous_lang = {}
        try:
            from src.skills.voice_miner import voice_miner
            voc_data = voice_miner.synthesize_customer_language(channel, tema)
            spontaneous_lang = {
                "visceral_quotes_for_hook": voc_data["voice_of_customer"]["visceral_quotes_for_hook"],
                "unresolved_competitor_doubts": voc_data["voice_of_customer"]["unresolved_competitor_doubts"],
                "popular_myths_to_debunk": voc_data["voice_of_customer"]["popular_myths_to_debunk"],
                "search_queries_in_autocomplete": voc_data["searches_in_youtube_autocomplete"]
            }
        except Exception:
            pass

        # Discovery Ecosystem (The 7 coordinated surfaces)
        ecosystem_summary = {}
        try:
            from src.skills.discovery_engine import discovery_engine
            eco = discovery_engine.generate_integrated_ecosystem(channel, tema)
            ecosystem_summary = {
                "longo_para_busca": eco["ecosystem_pieces"]["1_long_for_search"]["title"],
                "longo_para_home": eco["ecosystem_pieces"]["2_long_for_browse"]["title"],
                "short_1_descoberta": {
                    "titulo": eco["ecosystem_pieces"]["3_short_discovery"]["title"],
                    "gancho_0_2s": eco["ecosystem_pieces"]["3_short_discovery"]["timing_breakdown"]["0:00 - 0:02"],
                    "ponte_video_relacionado": "Vincular no Studio ao Documentário Longo"
                },
                "short_2_problema": eco["ecosystem_pieces"]["4_short_problem"]["title"],
                "playlist_percurso": eco["ecosystem_pieces"]["5_playlist_architecture"]["playlist_title"],
                "enquete_comunidade_48h": eco["ecosystem_pieces"]["6_community_post"]["poll_question"],
                "copy_redes_externas": eco["ecosystem_pieces"]["7_external_distribution"]["copy_sample"]
            }
        except Exception:
            pass

        # 4 Acts narrative structure
        acts_structure = [
            {"ato": 1, "nome": "O Choque / A Fenda", "tempo": "0:00 - 2:00", "objetivo": "Entregar a promessa nos primeiros 15s com a citação visceral e mostrar a vulnerabilidade real."},
            {"ato": 2, "nome": "O Mecanismo Invisível", "tempo": "2:00 - 5:00", "objetivo": "Desmascarar o mito popular e demonstrar a física/engenharia da falha."},
            {"ato": 3, "nome": "A Dissecação Forense", "tempo": "5:00 - 8:00", "objetivo": "Responder à dúvida que nenhum concorrente explicou com provas concretas."},
            {"ato": 4, "nome": "A Consequência & Defesa", "tempo": "8:00 - 10:30", "objetivo": "Apresentar a solução definitiva e acionar o CTA para o próximo vídeo da playlist."}
        ]

        briefing_dict = {
            "squad": squad,
            "episode_id": episode_id,
            "canal": channel,
            "data_emissao": now.strftime("%Y-%m-%d %H:%M"),
            "prazo_entrega": deadline,
            "prioridade": prioridade,
            "metrica_alvo": metrica_alvo,
            "tema": tema,
            "unidade_investigada": unidade,
            "tese_central": tese,
            "publico_alvo": publico,
            "desejo_dominante": desejo,
            "angulo_editorial": angulo,
            "promessa_principal": promessa,
            "linguagem_espontanea_do_publico": spontaneous_lang,
            "estrutura_narrativa_4_atos": acts_structure,
            "ecossistema_descoberta": ecosystem_summary,
            "referencias_documentais": referencias,
            "riscos_e_mitigacao": risco,
            "entregaveis_obrigatorios": entregaveis,
            "diretrizes_estrategicas": {
                "o_que_priorizar_na_abertura": o_que_priorizar_na_abertura,
                "o_que_nao_fazer": o_que_nao_fazer,
                "o_que_evitar": o_que_evitar
            }
        }

        if editorial_config:
            pol_ver = editorial_config.get("policy_version") or editorial_config.get("governance", {}).get("policy_version", "BRECHA_TOPIC_GREENLIGHT_V1")
            briefing_dict["governanca_editorial"] = {
                "politica": pol_ver,
                "status_decisao": approved_ep.get("decision", "GREENLIT") if ep_norm == approved_norm else "AD_HOC",
                "filtros_validados": approved_ep.get("filter_validation", {}) if ep_norm == approved_norm else {},
                "anatomia_objeto_cotidiano": approved_ep.get("anatomy", {}) if ep_norm == approved_norm else {}
            }

        if custom_params:
            for k, v in custom_params.items():
                if k in briefing_dict:
                    if isinstance(briefing_dict[k], dict) and isinstance(v, dict):
                        briefing_dict[k].update(v)
                    else:
                        briefing_dict[k] = v
                else:
                    briefing_dict[k] = v

        # Save to disk
        out_file = self.output_dir / f"briefing_{channel}_{episode_id}.json"
        with open(out_file, "w", encoding="utf-8") as f:
            json.dump(briefing_dict, f, indent=2, ensure_ascii=False)

        # Register into persistent ChiefMemory as IN_PRODUCTION to prevent duplicate planning
        try:
            from src.core.memory import chief_memory
            chief_memory.register_covered_theme(
                channel=channel,
                core_topic=tema,
                title_reference=tema,
                status="IN_PRODUCTION",
                angle_covered=tese,
                format="long",
                video_id=episode_id
            )
        except Exception:
            pass

        briefing_dict["saved_path"] = str(out_file)
        return briefing_dict

squad_briefing_gen = SquadBriefingGenerator()
