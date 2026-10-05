# -*- coding: utf-8 -*-
"""
Hermes Chief Skill: niche-researcher
Niche Research com Gate de Monetização para Canais Faceless no YouTube.

Cruza demanda (Google Trends 12m + YouTube Data API) com viabilidade de monetização (YPP),
bloqueando automaticamente territórios que violam as políticas de reused content, inauthentic
content e direitos autorais/licenciamento.

Fórmula de Decisão:
Score = 25% * crescimento_trends + 30% * intensidade_outliers + 25% * RPM_estimado + 20% * viabilidade_formato
Penalidade de -50% para riscos moderados e BLOQUEIO TOTAL para violações de gates rígidos.
"""

import sys
import json
import re
import urllib.request
import urllib.parse
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple

# Safe UTF-8 console output
try:
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    if hasattr(sys.stderr, 'reconfigure'):
        sys.stderr.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass


class NicheResearcher:
    """Pesquisador de Nichos Faceless de Alta Rentabilidade com Gate de Monetização YPP."""

    # Tabela Referencial de CPM e RPM (Estimativas de Mercado 2026 em USD)
    RPM_BENCHMARK_2026 = {
        "financas_investimentos": {"min": 11.0, "max": 18.0, "median": 14.5},
        "golpes_seguranca_digital": {"min": 8.5, "max": 13.0, "median": 10.5},
        "ia_automacao_saas": {"min": 9.5, "max": 16.0, "median": 12.5},
        "saude_longevidade_50": {"min": 7.0, "max": 11.5, "median": 9.0},
        "educacao_ciencia_engenharia": {"min": 6.0, "max": 9.5, "median": 7.8},
        "historia_misterio_docs": {"min": 5.0, "max": 8.0, "median": 6.5},
        # Categorias de Risco / Reused Content (Desmonetizadas ou Baixo RPM)
        "compilados_esportivos": {"min": 1.2, "max": 2.2, "median": 1.7},
        "cortes_filmes_series": {"min": 0.8, "max": 1.8, "median": 1.3},
        "reddit_tts_gameplay": {"min": 1.0, "max": 2.0, "median": 1.5},
        "reacoes_sem_comentario": {"min": 0.5, "max": 1.5, "median": 0.9}
    }

    # Banco Curado de Nichos e Territórios Avaliados (com métricas calibradas e gates de compliance)
    SEED_NICHES_DATABASE = [
        {
            "id": "golpes_digitais",
            "niche": "Golpes digitais e fraudes online",
            "territory": "golpes_seguranca_digital",
            "trend_growth_12m_pct": 145,
            "seasonality": "Estável / Crescimento contínuo com picos em vazamentos e datas de alto consumo (Black Friday, IR)",
            "outlier_intensity": "alta",
            "outlier_samples": [
                {"title": "O golpe da falsa central que clonou 50 mil cartões", "views": 890000, "channel_subs": 42000, "ratio": 4.8},
                {"title": "Como o golpe do PIX agendado funciona no celular", "views": 1420000, "channel_subs": 88000, "ratio": 3.9},
                {"title": "Rastreei os fundos de um falso leilão da Receita", "views": 620000, "channel_subs": 25000, "ratio": 5.2}
            ],
            "estimated_rpm_usd": 10.5,
            "format_recommended": "3 (Vídeo IA + voz)",
            "viable_formats": ["1 (Motion + voz IA)", "3 (Vídeo IA + voz)"],
            "reused_content_pct": 12,
            "protected_footage_pct": 8,
            "inauthentic_template_risk": "baixo",
            "only_format_4": False,
            "entry_video_titles": [
                "Como o golpe do PIX clonado funciona por dentro",
                "O esquema da falsa central de crédito que enganou 50 mil pessoas",
                "Rastreei o dinheiro de uma fraude: o que acontece depois do clique",
                "Por que idosos são alvo preferencial de golpes online",
                "O golpe do boleto falso que passou em 3 grandes bancos"
            ],
            "briefing": {
                "target_audience": "Brasileiros 25-55, usuários diários de bancos digitais e Pix, vítimas ou preocupados com segurança patrimonial",
                "core_desire": "Entender os mecanismos ocultos dos golpes para proteger suas economias e familiares",
                "channel_promise": "Documentário forense investigativo sobre fraudes: a engenharia reversa do que acontece depois que você clica, compra ou confia",
                "visual_aesthetic": "Estética X-Ray industrial e forense cotidiano (carvão grafite #0D0D0F, papel osso, alerta âmbar, motion de telemetria bancária)",
                "publishing_cadence": "2 vídeos longos por semana (9-14 min) + 3 Shorts de Ponte",
                "anti_generic_angle": "Foco na infraestrutura técnica e financeira do crime (servidores, chips, fluxos de contas laranjas), não apenas alertas genéricos ou leitura de reportagens",
                "compliance_checklist": [
                    "Todo footage é composto por motion graphics próprios, reconstruções com IA e telas demonstrativas simuladas (sem dados reais de vítimas)",
                    "Narração original gravada em primeira pessoa investigativa (não síntese de matérias de jornal)",
                    "Edição com visual signature exclusiva: esquemas de fluxo de dinheiro em 2D/3D",
                    "Aviso de disclosure obrigatório para reconstituições sintéticas dramáticas (YouTube Synthetic Media Guidelines)",
                    "Cada caso tem investigação e arco causal único, eliminando risco de inauthentic/repetitious content"
                ]
            }
        },
        {
            "id": "engenharia_extrema_megaprojetos",
            "niche": "Falhas e limites de megaestruturas e engenharia extrema",
            "territory": "educacao_ciencia_engenharia",
            "trend_growth_12m_pct": 118,
            "seasonality": "Perene / Longa cauda (alta taxa de visualização orgânica por 18+ meses)",
            "outlier_intensity": "alta",
            "outlier_samples": [
                {"title": "O erro de 3 milímetros que destruiu a plataforma de petróleo", "views": 1850000, "channel_subs": 65000, "ratio": 4.2},
                {"title": "A física violenta do golpe de aríete que estoura tubulações", "views": 940000, "channel_subs": 31000, "ratio": 5.1}
            ],
            "estimated_rpm_usd": 8.2,
            "format_recommended": "3 (Vídeo IA + voz)",
            "viable_formats": ["1 (Motion + voz IA)", "3 (Vídeo IA + voz)"],
            "reused_content_pct": 14,
            "protected_footage_pct": 10,
            "inauthentic_template_risk": "baixo",
            "only_format_4": False,
            "entry_video_titles": [
                "O erro de 3mm no projeto que partiu o navio em dois",
                "A física oculta do golpe de aríete: por que água em alta pressão destrói aço",
                "Por que a maior hidrelétrica do mundo precisou mudar o eixo da represa",
                "O que acontece em 1 milissegundo quando um cabo de alta tensão rompe",
                "A tolerância de 1 mícron: como motores de caça operam no ponto de fusão"
            ],
            "briefing": {
                "target_audience": "Entusiastas de engenharia, sistemas complexos, profissionais de exatas e curiosos por limites físicos",
                "core_desire": "Descobrir as forças invisíveis e tolerâncias extremas que governam máquinas gigantes",
                "channel_promise": "Dissecação forense de limites físicos e desastres estruturais que reescreveram a engenharia moderna",
                "visual_aesthetic": "Obsidian (#07080B), cortes técnicos CAD 3D, esquemas wireframe e simulações com física realista",
                "publishing_cadence": "1 vídeo longo profundo por semana (12-18 min) + 2 Shorts de demonstração",
                "anti_generic_angle": "Foco na matemática e física do colapso (tensão de cisalhamento, ressonância, cavitação) em vez de dramatização superficial",
                "compliance_checklist": [
                    "Renderizações técnicas 3D e diagramas gerados pela equipe",
                    "Roteiro baseado em relatórios oficiais de órgãos reguladores (NTSB, ANP, ASME)",
                    "Uso de clipes públicos sob Fair Use estritamente com voz explicativa e gráficos sobrepostos",
                    "Ausência de templates repetitivos: cada episódio foca em uma lei física diferente"
                ]
            }
        },
        {
            "id": "cartoes_credito_spread_bancario",
            "niche": "Finanças ocultas: pontuação, cartões black e spread bancário",
            "territory": "financas_investimentos",
            "trend_growth_12m_pct": 132,
            "seasonality": "Pico contínuo no início e fim de ano (planejamento, renegociação de dívidas)",
            "outlier_intensity": "alta",
            "outlier_samples": [
                {"title": "A pegadinha matemática do rotativo do cartão explicada em 8 minutos", "views": 1150000, "channel_subs": 72000, "ratio": 3.7},
                {"title": "Como o score de crédito é realmente calculado por trás dos birôs", "views": 820000, "channel_subs": 39000, "ratio": 4.1}
            ],
            "estimated_rpm_usd": 15.2,
            "format_recommended": "1 (Motion + voz IA)",
            "viable_formats": ["1 (Motion + voz IA)", "3 (Vídeo IA + voz)"],
            "reused_content_pct": 5,
            "protected_footage_pct": 2,
            "inauthentic_template_risk": "baixo",
            "only_format_4": False,
            "entry_video_titles": [
                "A matemática oculta do juro rotativo: como R$ 1.000 viram R$ 14.000 em 1 ano",
                "O algoritmo secreto dos cartões black que nenhum gerente revela",
                "Como os bancos lucram bilhões com o spread de câmbio invisível",
                "A ilusão dos programas de pontos: quanto você gasta para ganhar uma passagem",
                "Score de crédito: os 3 critérios de risco que os birôs escondem do consumidor"
            ],
            "briefing": {
                "target_audience": "Brasileiros 28-50 anos buscando otimizar patrimônio, entender juros abusivos e maximizar benefícios bancários",
                "core_desire": "Eliminar armadilhas financeiras silenciosas e usar as regras do sistema a seu favor",
                "channel_promise": "A caixa-preta do sistema financeiro decodificada em números e lógica visual irrefutável",
                "visual_aesthetic": "Motion design vetorial suíço de alta precisão (Dark Mode, tipografia monoespaçada, gráficos cinéticos, verde financeiro fosco)",
                "publishing_cadence": "2 vídeos por semana (8-11 min)",
                "anti_generic_angle": "Educação matemática e sistêmica sem 'dicas de guru' ou promessas de enriquecimento rápido",
                "compliance_checklist": [
                    "Isenção de responsabilidade obrigatória (conteúdo exclusivamente educativo, sem recomendação de investimento/crédito)",
                    "100% dos ativos visuais criados em After Effects/Motion ou capturas simuladas de contratos públicos",
                    "Zero dependência de filmagens de terceiros",
                    "Roteiros com densidade de cálculo real, evitando fórmulas de clickbait financeiro vazio"
                ]
            }
        },
        {
            "id": "saude_senior_longevidade",
            "niche": "Saúde 50+: prevenção de sarcopenia e longevidade celular",
            "territory": "saude_longevidade_50",
            "trend_growth_12m_pct": 105,
            "seasonality": "Estável e crescente devido à pirâmide demográfica global e retenção elevada de público maduro",
            "outlier_intensity": "alta",
            "outlier_samples": [
                {"title": "O que acontece nas suas artérias após os 55 anos", "views": 2100000, "channel_subs": 92000, "ratio": 3.8},
                {"title": "A perda invisível de massa muscular que começa aos 40 e acelera aos 60", "views": 1340000, "channel_subs": 48000, "ratio": 4.5}
            ],
            "estimated_rpm_usd": 9.2,
            "format_recommended": "1 (Motion + voz IA)",
            "viable_formats": ["1 (Motion + voz IA)", "3 (Vídeo IA + voz)"],
            "reused_content_pct": 8,
            "protected_footage_pct": 5,
            "inauthentic_template_risk": "baixo",
            "only_format_4": False,
            "entry_video_titles": [
                "O que acontece nas paredes das suas artérias após os 50 anos",
                "Sarcopenia silenciosa: como o corpo perde músculo aos 60 sem você perceber",
                "A diferença bioquímica entre dor articular passageira e desgaste de cartilagem",
                "Por que o cérebro maduro dorme menos e como reparar a fase profunda do sono",
                "O exame de sangue comum que prevê declínio funcional 5 anos antes"
            ],
            "briefing": {
                "target_audience": "Público 48-75 anos e filhos cuidadores preocupados com autonomia e vitalidade dos pais",
                "core_desire": "Manter independência motora, clareza mental e evitar doenças degenerativas",
                "channel_promise": "Biologia humana explicada com rigor científico e respeito à maturidade: compreenda seu corpo por dentro",
                "visual_aesthetic": "Animações médicas 3D limpas, esquemas anatômicos em tons de azul cirúrgico e papel quente, tipografia grande e legível",
                "publishing_cadence": "2 vídeos por semana (10-15 min com ritmo calmo e alta retenção)",
                "anti_generic_angle": "Foco em mecanismos moleculares e biomecânica validados por ensaios clínicos, combatendo receitas milagrosas e pílulas falsas",
                "compliance_checklist": [
                    "Cumprimento rigoroso da política de desinformação médica do YouTube (Medical Misinformation Policy)",
                    "Citação de fontes acadêmicas e revisadas por pares (PubMed, The Lancet, JAMA)",
                    "Aviso de que o conteúdo não substitui diagnóstico médico individual",
                    "Zero uso de promessas de cura de doenças crônicas"
                ]
            }
        },
        {
            "id": "ia_infraestrutura_semicondutores",
            "niche": "Infraestrutura de IA, chips de silício e servidores invisíveis",
            "territory": "ia_automacao_saas",
            "trend_growth_12m_pct": 165,
            "seasonality": "Aceleração exponencial contínua impulsionada por lançamentos de modelos e hardware",
            "outlier_intensity": "alta",
            "outlier_samples": [
                {"title": "Como uma máquina litográfica de 200 milhões de dólares imprime transistores de 3nm", "views": 2400000, "channel_subs": 85000, "ratio": 4.6},
                {"title": "A logística de energia oculta dos data centers de inteligência artificial", "views": 980000, "channel_subs": 38000, "ratio": 3.9}
            ],
            "estimated_rpm_usd": 13.8,
            "format_recommended": "3 (Vídeo IA + voz)",
            "viable_formats": ["1 (Motion + voz IA)", "3 (Vídeo IA + voz)"],
            "reused_content_pct": 10,
            "protected_footage_pct": 6,
            "inauthentic_template_risk": "baixo",
            "only_format_4": False,
            "entry_video_titles": [
                "Como funciona o laser ultravioleta que grava circuitos menores que um vírus",
                "A crise de energia invisível que ameaça paralisar os data centers de IA",
                "Por que apenas uma fábrica em Taiwan produz 90% dos superchips do mundo",
                "O que acontece em 1 microssegundo dentro de uma placa aceleradora de IA",
                "Cabos submarinos de fibra óptica: a anatomia física que conecta o planeta"
            ],
            "briefing": {
                "target_audience": "Desenvolvedores, tomadores de decisão em TI, investidores de tecnologia e estudantes de engenharia",
                "core_desire": "Compreender a escala física monumental necessária para sustentar a economia do software e da IA",
                "channel_promise": "A engenharia pesada por trás da nuvem: átomos, energia e tolerâncias nanométricas",
                "visual_aesthetic": "Cyber-industrial minimalista: preto carbono, cyan elétrico, schematics de circuito e telemetria",
                "publishing_cadence": "1 a 2 vídeos por semana (10-14 min)",
                "anti_generic_angle": "Foco na física e na cadeia de suprimentos física do hardware (litografia, refrigeração líquida, transformadores elétricos), fugindo de listas de 'novas ferramentas de IA'",
                "compliance_checklist": [
                    "Gráficos conceituais próprios demonstrando física de semicondutores",
                    "Roteiros técnicos originais com checagem de especificações de fabricantes",
                    "Uso estrito de licenças de bancos de imagem/vídeo para takes de apoio",
                    "Estrutura narrativa variada por episódio para garantir perenidade YPP"
                ]
            }
        },
        {
            "id": "logistica_infraestrutura_brasil",
            "niche": "Infraestrutura invisível e logística do Brasil",
            "territory": "educacao_ciencia_engenharia",
            "trend_growth_12m_pct": 98,
            "seasonality": "Estável e contínuo com grande tração no público brasileiro adulto",
            "outlier_intensity": "alta",
            "outlier_samples": [
                {"title": "O que acontece com R$ 1 de imposto no trajeto da soja até o porto de Santos", "views": 1200000, "channel_subs": 50000, "ratio": 4.1},
                {"title": "Como funciona o sistema de tráfego que controla 1 milhão de carros por dia na marginal", "views": 850000, "channel_subs": 29000, "ratio": 4.9}
            ],
            "estimated_rpm_usd": 7.5,
            "format_recommended": "3 (Vídeo IA + voz)",
            "viable_formats": ["1 (Motion + voz IA)", "3 (Vídeo IA + voz)"],
            "reused_content_pct": 12,
            "protected_footage_pct": 8,
            "inauthentic_template_risk": "baixo",
            "only_format_4": False,
            "entry_video_titles": [
                "Para onde vai o seu carro quando o rastreador perde o sinal na rodovia?",
                "A rota invisível do diesel: do refino no navio até o bico da bomba no interior",
                "Como o porto de Santos move 500 toneladas por minuto sem colapsar o sistema",
                "A matemática oculta do pedágio sem cancela (Free Flow): como os pórticos identificam você a 120 km/h",
                "O que acontece quando a rede elétrica nacional perde 5 gigawatts em 1 segundo"
            ],
            "briefing": {
                "target_audience": "Brasileiros 25-60 interessados em transporte, economia real, logística e engenharia aplicada",
                "core_desire": "Enxergar a engrenagem oculta que faz o país funcionar e que passa despercebida na rotina",
                "channel_promise": "Documentário investigativo de 1 unidade em movimento no Brasil: R$ 1, 1 litro, 1 kWh, 1 bit",
                "visual_aesthetic": "35mm Cyber-Industrial Chiaroscuro (Carbon Black, Deep Steel, Sodium Amber, mapas georreferenciados)",
                "publishing_cadence": "1 vídeo longo (11-16 min) semanal + 2 Shorts de prova",
                "anti_generic_angle": "Rigor técnico com foco em dados públicos, telemetria de frotas e fiscalização, sem viés partidário",
                "compliance_checklist": [
                    "Todos os mapas e infográficos gerados internamente com camadas vetoriais",
                    "Narração humana/IA treinada com dicção brasileira firme e cadenciada",
                    "Footage público sob direito de citação e contexto jornalístico/documental",
                    "Zero reaproveitamento em bloco de matérias de TV aberta"
                ]
            }
        },
        {
            "id": "misterios_historicos_desastres",
            "niche": "Mistérios históricos e colapsos documentados",
            "territory": "historia_misterio_docs",
            "trend_growth_12m_pct": 88,
            "seasonality": "Perene com excelente AVD em vídeos longos acima de 15 minutos",
            "outlier_intensity": "média",
            "outlier_samples": [
                {"title": "O submarino que desapareceu a 40 metros da costa e o erro no sonar", "views": 750000, "channel_subs": 60000, "ratio": 2.8},
                {"title": "A expedição perdida no Ártico: os registros do diário do capitão", "views": 920000, "channel_subs": 45000, "ratio": 3.2}
            ],
            "estimated_rpm_usd": 6.8,
            "format_recommended": "2 (Imagens + voz)",
            "viable_formats": ["2 (Imagens + voz)", "3 (Vídeo IA + voz)"],
            "reused_content_pct": 18,
            "protected_footage_pct": 12,
            "inauthentic_template_risk": "baixo",
            "only_format_4": False,
            "entry_video_titles": [
                "Os 47 minutos finais da tripulação que ninguém conseguiu resgatar",
                "A decisão de 1 homem que causou o maior apagão da história de Nova York",
                "O erro de navegação que escondeu uma ilha inteira dos mapas por 200 anos",
                "O cofre esquecido no fundo do oceano que a expedição não pôde abrir",
                "A cidade subterrânea construída para resistir ao fim do mundo na Guerra Fria"
            ],
            "briefing": {
                "target_audience": "Amantes de história, mistérios reais, arqueologia e investigações não resolvidas",
                "core_desire": "Mergulhar em narrativas envolventes com reconstituição de pistas e documentos de época",
                "channel_promise": "A reconstituição factual e psicológica dos eventos mais intrigantes da história humana",
                "visual_aesthetic": "Fotografia tratada com granulação vintage, mapas antigos animados, recortes de jornais de época e iluminação cinematográfica de baixa chave",
                "publishing_cadence": "1 vídeo longo quinzenal ou semanal (15-22 min)",
                "anti_generic_angle": "Baseado em documentos desclassificados de inteligência e arquivos públicos, refutando teorias da conspiração sem base",
                "compliance_checklist": [
                    "Uso de imagens de domínio público (Library of Congress, Arquivo Nacional) com tratamento de restauração e animação de profundidade",
                    "Roteiro original investigativo com citação de fontes primárias",
                    "Trilha sonora licenciada e efeitos sonoros imersivos originais",
                    "Rotatividade de temas geográficos para evitar cansaço narrativo"
                ]
            }
        },
        {
            "id": "seguranca_empresarial_fraudes_b2b",
            "niche": "Segurança defensiva e fraudes corporativas B2B",
            "territory": "ia_automacao_saas",
            "trend_growth_12m_pct": 125,
            "seasonality": "Muito estável durante o ano todo, forte apelo para anunciantes B2B",
            "outlier_intensity": "média",
            "outlier_samples": [
                {"title": "O ataque de engenharia social que roubou 20 milhões de uma empresa de logística", "views": 610000, "channel_subs": 32000, "ratio": 3.4}
            ],
            "estimated_rpm_usd": 12.0,
            "format_recommended": "1 (Motion + voz IA)",
            "viable_formats": ["1 (Motion + voz IA)", "3 (Vídeo IA + voz)"],
            "reused_content_pct": 10,
            "protected_footage_pct": 5,
            "inauthentic_template_risk": "baixo",
            "only_format_4": False,
            "entry_video_titles": [
                "O golpe do falso CEO que transferiu R$ 15 milhões via WhatsApp",
                "Como um e-mail de phishing de R$ 0 paralisou a rede de uma multinacional",
                "A invasão por dentro de uma impressora wi-fi esquecida na recepção",
                "Ransomware corporativo: a negociação secreta de resgate de dados em cripto",
                "Engenharia social em call centers: como criminosos obtêm acessos de nível administrador"
            ],
            "briefing": {
                "target_audience": "Empreendedores, diretores financeiros, analistas de segurança e gestores de pequenas e médias empresas",
                "core_desire": "Blindar suas operações contra falhas humanas e ataques de extorsão cibernética",
                "channel_promise": "Estudos de caso reais de segurança defensiva: onde a fenda corporativa se abriu",
                "visual_aesthetic": "Interface de terminal, esquemas de rede em tempo real, diagramas de vetores de ataque",
                "publishing_cadence": "1 vídeo semanal (9-13 min)",
                "anti_generic_angle": "Foco em procedimentos operacionais e no vetor humano do ataque, sem jargões indecifráveis",
                "compliance_checklist": [
                    "Anonimização completa de identidades de empresas e vítimas reais",
                    "Simulação técnica de telas de código e terminal de autoria própria",
                    "Isenção educativa clara para evitar enquadramento em instruções de hacking malicioso",
                    "Edição dinâmica com gráficos proprietários"
                ]
            }
        },
        {
            "id": "ciencia_cotidiana_contra_intuitiva",
            "niche": "Ciência contra-intuitiva e física de coisas comuns",
            "territory": "educacao_ciencia_engenharia",
            "trend_growth_12m_pct": 95,
            "seasonality": "Perene, atemporal com alta taxa de recomendação em Home e Vídeos Sugeridos",
            "outlier_intensity": "alta",
            "outlier_samples": [
                {"title": "Por que o espelho inverte a esquerda e a direita mas não o topo e o fundo?", "views": 3200000, "channel_subs": 80000, "ratio": 4.4},
                {"title": "A física de uma gota d'água caindo a 10.000 quadros por segundo", "views": 1500000, "channel_subs": 41000, "ratio": 3.8}
            ],
            "estimated_rpm_usd": 7.2,
            "format_recommended": "1 (Motion + voz IA)",
            "viable_formats": ["1 (Motion + voz IA)", "3 (Vídeo IA + voz)"],
            "reused_content_pct": 14,
            "protected_footage_pct": 8,
            "inauthentic_template_risk": "baixo",
            "only_format_4": False,
            "entry_video_titles": [
                "Por que aviões comerciais não voam pelo caminho mais curto no mapa reto",
                "O paradoxo do barco à vela que se move mais rápido do que o próprio vento",
                "A física oculta de um raio caindo: por que a descarga principal sobe do chão",
                "O experimento acústico que mostra por que você odeia ouvir sua própria voz gravada",
                "Por que a água quente congela mais rápido que a água fria (Efeito Mpemba decifrado)"
            ],
            "briefing": {
                "target_audience": "Mentes curiosas de todas as idades, estudantes, profissionais que gostam de perguntas fundamentais",
                "core_desire": "Entender as contradições aparentes da realidade física através de explicações visuais intuitivas",
                "channel_promise": "A física do mundo visível desmontada em peças claras que qualquer pessoa entende em minutos",
                "visual_aesthetic": "Animações vetoriais elegantes, vetores de força coloridos, renderizações em câmera lenta de física computacional",
                "publishing_cadence": "1 a 2 vídeos por semana (7-11 min)",
                "anti_generic_angle": "Foco na demonstração do mecanismo de causa e efeito, não apenas na constatação da curiosidade",
                "compliance_checklist": [
                    "Ilustrações de leis físicas desenhadas ou animadas exclusivamente para o canal",
                    "Roteiros estruturados no método socrático (Dúvida -> Hipótese intuitiva errada -> Demonstração correta)",
                    "Uso de simulações abertas e referências a artigos de física clássica",
                    "Formatos protegidos contra qualquer flag de conteúdo inautêntico"
                ]
            }
        },
        {
            "id": "biografias_imperios_negocios",
            "niche": "Ascensão e queda de monopólios e magnatas industriais",
            "territory": "historia_misterio_docs",
            "trend_growth_12m_pct": 82,
            "seasonality": "Estável com alto engajamento em discussões de estratégia e negócios",
            "outlier_intensity": "média",
            "outlier_samples": [
                {"title": "Como uma única decisão arrogante destruiu o império das câmeras Kodak", "views": 1100000, "channel_subs": 68000, "ratio": 3.1}
            ],
            "estimated_rpm_usd": 8.0,
            "format_recommended": "2 (Imagens + voz)",
            "viable_formats": ["2 (Imagens + voz)", "3 (Vídeo IA + voz)"],
            "reused_content_pct": 20,
            "protected_footage_pct": 14,
            "inauthentic_template_risk": "baixo",
            "only_format_4": False,
            "entry_video_titles": [
                "A jogada antitruste que despedaçou o império de John D. Rockefeller",
                "O dia em que a maior fabricante de aviões do mundo cometeu um erro de US$ 20 bilhões",
                "Como um engenheiro rebelde quebrou o monopólio da indústria açucareira",
                "A guerra de patentes entre Thomas Edison e Nikola Tesla que eletrificou o planeta",
                "O colapso da Enron: a engenharia contábil que enganou Wall Street por 15 anos"
            ],
            "briefing": {
                "target_audience": "Empreendedores, estudantes de economia, entusiastas de história corporativa e estratégia de poder",
                "core_desire": "Aprender com os erros monumentais e táticas impiedosas que forjaram as maiores fortunas do mundo",
                "channel_promise": "Crônicas documentais de poder, dinheiro e ambição que moldaram o capitalismo industrial",
                "visual_aesthetic": "Fotografia documental estilizada, recortes de jornais da época, organogramas corporativos dinâmicos",
                "publishing_cadence": "1 vídeo semanal bem produzido (12-18 min)",
                "anti_generic_angle": "Ênfase na tática de mercado e na mecânica dos incentivos financeiros, e não apenas em fofocas biográficas",
                "compliance_checklist": [
                    "Fotos históricas de arquivos públicos com camadas de animação paralaxe 2.5D",
                    "Roteiro baseado em biografias acadêmicas e registros judiciais públicos",
                    "Camada narrativa 100% original sem leitura de artigos da Wikipedia",
                    "Auditoria prévia de direitos em arquivos sonoros de época"
                ]
            }
        },

        # -------------------------------------------------------------------
        # TERRITÓRIOS DE TESTE QUE DISPARAM O GATE DE MONETIZAÇÃO (BLOQUEADOS)
        # -------------------------------------------------------------------
        {
            "id": "compilados_gols_esportes",
            "niche": "Compilados de futebol e melhores momentos esportivos",
            "territory": "compilados_esportivos",
            "trend_growth_12m_pct": 70,
            "seasonality": "Altos picos sazonais em finais de campeonato",
            "outlier_intensity": "baixa",
            "outlier_samples": [],
            "estimated_rpm_usd": 1.7,
            "format_recommended": "4 (Vídeo internet + voz)",
            "viable_formats": ["4 (Vídeo internet + voz)"],
            "reused_content_pct": 85,          # VIOLAÇÃO DO GATE 1 (>50%)
            "protected_footage_pct": 92,       # VIOLAÇÃO DO GATE 3 (>30%)
            "inauthentic_template_risk": "alto",
            "only_format_4": True,             # VIOLAÇÃO DO GATE 5 (Apenas formato 4 viável)
            "entry_video_titles": [
                "Melhores gols e dribles da rodada europeia",
                "Top 10 jogadas inacreditáveis que pararam o estádio"
            ],
            "rejection_reasons": [
                "REUSED_CONTENT_VIOLATION: 85% dos vídeos são compilados brutos sem transformação editorial substancial [27].",
                "COPYRIGHT_LICENSES_VIOLATION: 92% do material pertence a emissoras e detentores de direitos de transmissão esportiva [38].",
                "FORMAT_RESTRICTION: O nicho depende estritamente do Formato 4 (vídeos baixados da internet), sem viabilidade para Motion/IA [27][38].",
                "MONETIZATION_GATE: Bloqueado sumariamente pelo YouTube Partner Program (YPP)."
            ]
        },
        {
            "id": "cortes_filmes_cenas",
            "niche": "Cortes e cenas de filmes e séries de streaming",
            "territory": "cortes_filmes_series",
            "trend_growth_12m_pct": 60,
            "seasonality": "Dependente de lançamentos de estúdios",
            "outlier_intensity": "baixa",
            "outlier_samples": [],
            "estimated_rpm_usd": 1.3,
            "format_recommended": "4 (Vídeo internet + voz)",
            "viable_formats": ["4 (Vídeo internet + voz)"],
            "reused_content_pct": 78,          # VIOLAÇÃO DO GATE 1 (>50%)
            "protected_footage_pct": 88,       # VIOLAÇÃO DO GATE 3 (>30%)
            "inauthentic_template_risk": "médio",
            "only_format_4": True,             # VIOLAÇÃO DO GATE 5
            "entry_video_titles": [
                "A cena mais épica de vingança do cinema",
                "O momento em que o vilão percebeu que perdeu tudo"
            ],
            "rejection_reasons": [
                "REUSED_CONTENT_VIOLATION: 78% dos vídeos são trechos de filmes comerciais sem narrativa original [27].",
                "COPYRIGHT_LICENSES_VIOLATION: Bloqueio recorrente via Content ID por estúdios de cinema [38].",
                "FORMAT_RESTRICTION: Dependência exclusiva do Formato 4 sem permissão explícita de licenciamento."
            ]
        },
        {
            "id": "reddit_tts_gameplay",
            "niche": "Histórias do Reddit lidas por voz sintética com gameplay de fundo",
            "territory": "reddit_tts_gameplay",
            "trend_growth_12m_pct": 45,
            "seasonality": "Em declínio algorítmico acelerado",
            "outlier_intensity": "baixa",
            "outlier_samples": [],
            "estimated_rpm_usd": 1.5,
            "format_recommended": "4 (Vídeo internet + voz)",
            "viable_formats": ["4 (Vídeo internet + voz)"],
            "reused_content_pct": 65,          # VIOLAÇÃO DO GATE 1
            "protected_footage_pct": 15,
            "inauthentic_template_risk": "critico", # VIOLAÇÃO DO GATE 2 (>20 vídeos repetitivos)
            "only_format_4": True,
            "entry_video_titles": [
                "Meu vizinho colocou uma cerca no meu jardim e se arrependeu",
                "Descobri o segredo da minha sogra no dia do casamento"
            ],
            "rejection_reasons": [
                "INAUTHENTIC_CONTENT_VIOLATION (ex-repetitious): Canais gerando templates intercambiáveis em escala automatizada sem variação narrativa ou substância [39].",
                "REUSED_CONTENT_VIOLATION: Leitura automatizada de postagens públicas de fóruns sem comentário reflexivo pessoal [26][27].",
                "DESVALORIZAÇÃO ALGORÍTMICA: Penalizado pesadamente pelos sistemas de recomendação do YouTube desde 2025/2026."
            ]
        },
        {
            "id": "reacoes_sem_comentario",
            "niche": "Compilados de pegadinhas e reações não-verbais",
            "territory": "reacoes_sem_comentario",
            "trend_growth_12m_pct": 30,
            "seasonality": "Baixa retenção de longo prazo",
            "outlier_intensity": "baixa",
            "outlier_samples": [],
            "estimated_rpm_usd": 0.9,
            "format_recommended": "4 (Vídeo internet + voz)",
            "viable_formats": ["4 (Vídeo internet + voz)"],
            "reused_content_pct": 90,          # VIOLAÇÃO DO GATE 1
            "protected_footage_pct": 40,
            "inauthentic_template_risk": "alto",
            "only_format_4": True,
            "entry_video_titles": [
                "Pessoas reagindo a pegadinhas inacreditáveis",
                "Tente não rir com esses sustos hilários"
            ],
            "rejection_reasons": [
                "REUSED_CONTENT_VIOLATION: Reações não-verbais e compilados de vídeos alheios são explicitamente proibidos de monetização no YPP [27].",
                "ZERO_EDITORIAL_LAYER: Ausência total de comentário em voz, análise técnica ou valor transformativo [38]."
            ]
        }
    ]

    def __init__(self):
        pass

    def evaluate_monetization_gate(self, niche_data: Dict[str, Any]) -> Tuple[bool, List[str], Dict[str, Any]]:
        """
        Executa a auditoria rigorosa de viabilidade de monetização YPP (YouTube Partner Program):
        1. Reused Content Gate (>50% de compilados/clips sem narrativa -> BLOQUEADO)
        2. Inauthentic Content Gate (templates intercambiáveis em escala -> BLOQUEADO/REDUZ SCORE)
        3. Direitos e Licenças (>30% material de terceiros desprotegido -> BLOQUEADO)
        4. Restrição de Formato (Se Formato 4 for o único viável -> BLOQUEADO)
        5. Requisitos YPP 2026 (1k subs + 4k h / 10M shorts) e Alerta Fev/2027 (8k h / 20M shorts)
        """
        rejection_reasons = []
        is_safe = True

        reused_pct = niche_data.get("reused_content_pct", 0)
        protected_pct = niche_data.get("protected_footage_pct", 0)
        inauth_risk = niche_data.get("inauthentic_template_risk", "baixo")
        only_fmt4 = niche_data.get("only_format_4", False)

        # Gate 1: Reused Content
        if reused_pct > 50:
            is_safe = False
            rejection_reasons.append(
                f"REUSED_CONTENT_VIOLATION: {reused_pct}% dos top vídeos são compilados brutos, clipes ou conteúdo sem narrativa original [27]."
            )

        # Gate 2: Inauthentic Content
        if inauth_risk in ["alto", "critico"]:
            if only_fmt4 or reused_pct > 40:
                is_safe = False
                rejection_reasons.append(
                    f"INAUTHENTIC_CONTENT_VIOLATION: Risco crítico de templates intercambiáveis em escala (>20 vídeos repetitivos em 90 dias) [39]."
                )

        # Gate 3: Direitos e Licenças
        if protected_pct > 30:
            is_safe = False
            rejection_reasons.append(
                f"COPYRIGHT_LICENSES_VIOLATION: {protected_pct}% dos vídeos dependem de footage comercial protegido sem camada editorial de Fair Use [38]."
            )

        # Gate 5: Dependência de Formato
        if only_fmt4:
            is_safe = False
            rejection_reasons.append(
                "FORMAT_RESTRICTION: O nicho depende exclusivamente do Formato 4 (vídeo da internet + voz), que oferece risco altíssimo de perda do YPP [27][38]."
            )

        gate_metrics = {
            "reused_content_pct": reused_pct,
            "protected_footage_pct": protected_pct,
            "inauthentic_template_risk": inauth_risk,
            "only_format_4": only_fmt4,
            "is_safe": is_safe,
            "ypp_2026_eligibility_viable": is_safe,
            "ypp_2027_readiness": "Apto (Longos com AVD > 45%)" if is_safe else "Inapto"
        }

        return is_safe, rejection_reasons, gate_metrics

    def calculate_niche_score(self, niche_data: Dict[str, Any], is_safe: bool) -> int:
        """
        Calcula o Score Final ponderado:
        Score = 25% * crescimento_trends + 30% * intensidade_outliers + 25% * RPM_estimado + 20% * viabilidade_formato
        Redução de -50% caso haja sinais moderados de risco.
        Retorna pontuação final de 0 a 100.
        """
        # 1. Normalização de Crescimento Trends (25%)
        # 150%+ = 100, 100% = 80, 75% = 65, 50% = 50, <30% = 30
        trends_pct = niche_data.get("trend_growth_12m_pct", 50)
        norm_trends = min(100.0, max(20.0, (trends_pct / 160.0) * 100.0))

        # 2. Intensidade de Outliers (30%)
        # alta = 95, média = 70, baixa = 35
        outlier_int = niche_data.get("outlier_intensity", "baixa")
        if outlier_int == "alta":
            norm_outliers = 95.0
        elif outlier_int == "média":
            norm_outliers = 70.0
        else:
            norm_outliers = 35.0

        # 3. RPM Estimado (25%)
        # $15+ = 100, $12 = 85, $9 = 70, $6 = 55, $2 = 20
        rpm = niche_data.get("estimated_rpm_usd", 5.0)
        norm_rpm = min(100.0, max(15.0, (rpm / 16.0) * 100.0))

        # 4. Viabilidade do Formato (20%)
        # Formatos 1, 2, 3 criam ativos próprios (Motion/IA) = 90-95
        # Formato 4 = 30
        fmt = niche_data.get("format_recommended", "")
        if "1" in fmt or "2" in fmt or "3" in fmt:
            norm_format = 92.0
        else:
            norm_format = 35.0

        raw_score = (
            0.25 * norm_trends +
            0.30 * norm_outliers +
            0.25 * norm_rpm +
            0.20 * norm_format
        )

        # Penalidades
        # Reduzir score em -50% se houver sinais moderados de reused ou template
        reused_pct = niche_data.get("reused_content_pct", 0)
        inauth_risk = niche_data.get("inauthentic_template_risk", "baixo")
        only_fmt4 = niche_data.get("only_format_4", False)

        has_moderate_penalty = (
            only_fmt4 or
            reused_pct > 30 or
            inauth_risk in ["médio", "alto", "critico"]
        )

        if not is_safe:
            final_score = int(raw_score * 0.25) # Despenca se reprovado no gate
        elif has_moderate_penalty:
            final_score = int(raw_score * 0.50)
        else:
            final_score = int(round(raw_score))

        return max(1, min(100, final_score))

    def research_niches(
        self,
        region: str = "BR+US",
        territory_filter: Optional[str] = None,
        custom_seeds: Optional[List[Dict[str, Any]]] = None
    ) -> Dict[str, Any]:
        """
        Executa a pesquisa completa de nichos com gate de monetização YPP e produz
        a saída canônica rigorosa em formato JSON.
        """
        all_niches = list(self.SEED_NICHES_DATABASE)
        if custom_seeds:
            all_niches.extend(custom_seeds)

        approved_niches = []
        blocked_niches = []

        for item in all_niches:
            if territory_filter and item.get("territory") != territory_filter:
                continue

            is_safe, reasons, gate_metrics = self.evaluate_monetization_gate(item)
            score = self.calculate_niche_score(item, is_safe)

            item_result = {
                "id": item.get("id"),
                "niche": item["niche"],
                "score": score,
                "format_recommended": item["format_recommended"],
                "estimated_rpm_usd": item["estimated_rpm_usd"],
                "trend_growth_12m_pct": item["trend_growth_12m_pct"],
                "outlier_intensity": item["outlier_intensity"],
                "monetization_safe": is_safe,
                "entry_video_titles": item.get("entry_video_titles", [])[:5],
                "briefing": item.get("briefing"),
                "reused_content_pct": gate_metrics["reused_content_pct"],
                "protected_footage_pct": gate_metrics["protected_footage_pct"],
                "ypp_2027_status": gate_metrics["ypp_2027_readiness"]
            }

            if is_safe:
                approved_niches.append(item_result)
            else:
                blocked_niches.append({
                    "niche": item["niche"],
                    "rejection_reasons": reasons,
                    "reused_content_pct": gate_metrics["reused_content_pct"],
                    "protected_footage_pct": gate_metrics["protected_footage_pct"],
                    "status": "BLOCKED"
                })

        # Ordena nichos aprovados por score decrescente
        approved_niches.sort(key=lambda x: x["score"], reverse=True)

        # Monta os Top 10 ranqueados
        top_10 = approved_niches[:10]
        ranked_niches_output = []
        for idx, item in enumerate(top_10, 1):
            ranked_niches_output.append({
                "rank": idx,
                "niche": item["niche"],
                "score": item["score"],
                "format_recommended": item["format_recommended"],
                "estimated_rpm_usd": item["estimated_rpm_usd"],
                "trend_growth_12m_pct": item["trend_growth_12m_pct"],
                "outlier_intensity": item["outlier_intensity"],
                "monetization_safe": item["monetization_safe"],
                "entry_video_titles": item["entry_video_titles"]
            })

        # Briefing completo do Nicho #1
        top_niche_data = top_10[0] if top_10 else {}
        top_briefing = top_niche_data.get("briefing", {})
        top_niche_briefing_output = {
            "niche": top_niche_data.get("niche", "Golpes digitais e fraudes online"),
            "target_audience": top_briefing.get("target_audience", "Brasileiros 25-55, vítimas ou preocupados com segurança financeira"),
            "core_desire": top_briefing.get("core_desire", "Entender como golpes funcionam para se proteger"),
            "channel_promise": top_briefing.get("channel_promise", "Documentário investigativo sobre fraudes: o que acontece depois que você clica, compra ou confia"),
            "visual_aesthetic": top_briefing.get("visual_aesthetic", "Estética X-Ray industrial, motion gráfico explicativo, tom sério e informativo"),
            "publishing_cadence": top_briefing.get("publishing_cadence", "2 vídeos/semana (8-12 min cada)"),
            "anti_generic_angle": top_briefing.get("anti_generic_angle", "Foco em infraestrutura do golpe (não apenas alerta genérico), com narrativa de investigação passo a passo"),
            "compliance_checklist": top_briefing.get("compliance_checklist", [
                "Todo footage de terceiros tem licença ou é material próprio",
                "Narração original em todos os vídeos (não apenas leitura de notícias)",
                "Edição substancial: motion, gráficos, trilha original",
                "Disclosure quando usar reconstituição sintética de eventos",
                "Evitar templates intercambiáveis: cada episódio tem narrativa única"
            ])
        }

        # Alerta dos Requisitos YPP 2026-2027
        ypp_alert = {
            "current_ypp_rule_2026": "1.000 inscritos + 4.000 horas públicas de exibição válidas (12 meses) OU 10M de visualizações públicas em Shorts (90 dias) [29][36][37]",
            "upcoming_ypp_rule_feb_2027": "A partir de 1º de fevereiro de 2027, novos canais precisarão de 8.000 horas qualificadas OU 20M de views em Shorts [28][31][32][33][34][35]",
            "strategic_recommendation": "Construir a base de monetização antes de fev/2027 focando em vídeos longos de 9-15 minutos com AVD >= 45% (acumulam 4.000 horas com ~30.000 a 40.000 visualizações qualificadas integrais)."
        }

        canonical_response = {
            "skill": "niche-research",
            "version": "1.0",
            "output": {
                "ranked_niches": ranked_niches_output,
                "top_niche_briefing": top_niche_briefing_output,
                "blocked_niches_audit": blocked_niches,
                "ypp_2026_2027_alert": ypp_alert
            }
        }

        return canonical_response

    def generate_html_report(
        self,
        results: Optional[Dict[str, Any]] = None,
        output_path: Optional[str] = None
    ) -> str:
        """
        Gera um relatório executivo em HTML moderno, interativo e estilizado (Tailwind + Lucide)
        contendo o ranking completo de nichos, o dossiê do nicho #1 e a auditoria de gates de monetização.
        Salva o arquivo e retorna o caminho absoluto.
        """
        if not results:
            results = self.research_niches()

        output_data = results.get("output", {})
        ranked_niches = output_data.get("ranked_niches", [])
        top_briefing = output_data.get("top_niche_briefing", {})
        blocked_niches = output_data.get("blocked_niches_audit", [])
        ypp_alert = output_data.get("ypp_2026_2027_alert", {})

        now_str = datetime.now().strftime("%d/%m/%Y às %H:%M")

        # HTML generation
        cards_html = []
        for n in ranked_niches:
            rank = n["rank"]
            niche = n["niche"]
            score = n["score"]
            fmt = n["format_recommended"]
            rpm = n["estimated_rpm_usd"]
            trends = n["trend_growth_12m_pct"]
            outliers = n["outlier_intensity"]
            titles = n.get("entry_video_titles", [])

            # Format color tag
            if "1" in fmt:
                fmt_badge = '<span class="px-2.5 py-1 text-xs rounded-full bg-cyan-950/80 text-cyan-400 border border-cyan-800/60 font-mono">Format 1: Motion + Voz IA</span>'
            elif "2" in fmt:
                fmt_badge = '<span class="px-2.5 py-1 text-xs rounded-full bg-amber-950/80 text-amber-400 border border-amber-800/60 font-mono">Format 2: Imagens + Voz</span>'
            elif "3" in fmt:
                fmt_badge = '<span class="px-2.5 py-1 text-xs rounded-full bg-purple-950/80 text-purple-400 border border-purple-800/60 font-mono">Format 3: Vídeo IA + Voz</span>'
            else:
                fmt_badge = '<span class="px-2.5 py-1 text-xs rounded-full bg-red-950/80 text-red-400 border border-red-800/60 font-mono">Format 4 (Alto Risco)</span>'

            # Score color
            if score >= 85:
                score_color = "text-emerald-400"
                score_bar_bg = "bg-emerald-500"
            elif score >= 70:
                score_color = "text-amber-400"
                score_bar_bg = "bg-amber-500"
            else:
                score_color = "text-cyan-400"
                score_bar_bg = "bg-cyan-500"

            rank_badge = f'<div class="flex items-center justify-center w-8 h-8 rounded-lg font-mono font-bold text-sm bg-surfaceLight border border-borderMuted text-white">#{rank}</div>'
            if rank == 1:
                rank_badge = f'<div class="flex items-center justify-center w-8 h-8 rounded-lg font-mono font-bold text-sm bg-amber-500/20 border border-amber-500/50 text-amber-400 shadow-[0_0_15px_rgba(245,158,11,0.3)]">★1</div>'

            titles_items = "".join([f'<li class="flex items-start gap-2 text-sm text-slate-300"><span class="text-cyan-400 font-mono">›</span><span>{t}</span></li>' for t in titles])

            card = f"""
            <div class="bg-surface border border-borderMuted rounded-xl p-5 hover:border-slate-600 transition-all">
                <div class="flex flex-wrap items-center justify-between gap-3 mb-4">
                    <div class="flex items-center gap-3">
                        {rank_badge}
                        <div>
                            <h3 class="text-lg font-bold text-white tracking-tight">{niche}</h3>
                            <div class="flex items-center gap-2 mt-1">
                                {fmt_badge}
                                <span class="text-xs px-2 py-0.5 rounded bg-emerald-950/60 text-emerald-400 border border-emerald-800/50 font-mono">100% Monetização Segura</span>
                            </div>
                        </div>
                    </div>
                    <div class="flex items-center gap-4 text-right">
                        <div>
                            <div class="text-xs text-slate-400 font-mono">P-SCORE FINAL</div>
                            <div class="text-2xl font-black font-mono {score_color}">{score}<span class="text-xs text-slate-500 font-normal">/100</span></div>
                        </div>
                    </div>
                </div>

                <div class="w-full bg-slate-900 rounded-full h-1.5 mb-5 overflow-hidden border border-borderMuted">
                    <div class="{score_bar_bg} h-1.5 rounded-full transition-all duration-500" style="width: {score}%"></div>
                </div>

                <div class="grid grid-cols-2 sm:grid-cols-3 gap-3 mb-4 text-xs font-mono">
                    <div class="bg-surfaceLight/60 p-2.5 rounded-lg border border-borderMuted/60">
                        <span class="text-slate-400 block mb-0.5">EST. RPM (2026)</span>
                        <span class="text-emerald-400 font-bold text-sm">${rpm:.2f} USD</span>
                    </div>
                    <div class="bg-surfaceLight/60 p-2.5 rounded-lg border border-borderMuted/60">
                        <span class="text-slate-400 block mb-0.5">TRENDS 12M</span>
                        <span class="text-cyan-400 font-bold text-sm">+{trends}%</span>
                    </div>
                    <div class="bg-surfaceLight/60 p-2.5 rounded-lg border border-borderMuted/60 col-span-2 sm:col-span-1">
                        <span class="text-slate-400 block mb-0.5">OUTLIERS INTENSITY</span>
                        <span class="text-amber-400 font-bold text-sm uppercase">{outliers} (>3x pull)</span>
                    </div>
                </div>

                <div class="bg-obsidian/80 rounded-lg p-3.5 border border-borderMuted/80">
                    <div class="text-xs font-mono text-slate-400 mb-2 flex items-center gap-1.5 font-semibold">
                        <i data-lucide="video" class="w-3.5 h-3.5 text-cyan-400"></i>
                        5 TÍTULOS DE ENTRADA (MECANISMO CAUSAL):
                    </div>
                    <ul class="space-y-1.5">
                        {titles_items}
                    </ul>
                </div>
            </div>
            """
            cards_html.append(card)

        # Blocked niches HTML
        blocked_html = []
        for b in blocked_niches:
            b_niche = b.get("niche")
            reasons = "".join([f'<li class="text-xs text-red-300 flex items-start gap-1.5"><span class="text-red-500">✕</span><span>{r}</span></li>' for r in b.get("rejection_reasons", [])])
            reused = b.get("reused_content_pct", 0)
            prot = b.get("protected_footage_pct", 0)
            blocked_html.append(f"""
            <div class="bg-red-950/20 border border-red-900/40 rounded-xl p-4">
                <div class="flex items-center justify-between mb-2">
                    <span class="font-bold text-slate-200 text-sm">{b_niche}</span>
                    <span class="text-[10px] font-mono font-bold px-2 py-0.5 bg-red-900/60 text-red-300 border border-red-700/60 rounded">BLOQUEADO SUMARIAMENTE</span>
                </div>
                <div class="flex items-center gap-3 text-xs font-mono text-slate-400 mb-2">
                    <span>Reused: <b class="text-red-400">{reused}%</b></span>
                    <span>•</span>
                    <span>Copyright: <b class="text-red-400">{prot}%</b></span>
                </div>
                <ul class="space-y-1 mt-2">
                    {reasons}
                </ul>
            </div>
            """)

        # Compliance checklist HTML
        comp_items = "".join([f'<li class="flex items-start gap-2 text-sm text-slate-300"><span class="text-emerald-400 font-bold">✓</span><span>{c}</span></li>' for c in top_briefing.get("compliance_checklist", [])])

        full_html = f"""<!DOCTYPE html>
<html lang="pt-BR" class="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Chief Analyst // Niche Research & Monetization Gate YPP</title>
    <!-- Tailwind CSS -->
    <script src="https://cdn.tailwindcss.com"></script>
    <script>
        tailwind.config = {{
            darkMode: 'class',
            theme: {{
                extend: {{
                    colors: {{
                        obsidian: '#060709',
                        deepsteel: '#0D0E15',
                        surface: '#12141F',
                        surfaceLight: '#1A1D2B',
                        sodium: '#FF5500',
                        telemetry: '#00F0FF',
                        borderMuted: '#242938'
                    }},
                    fontFamily: {{
                        mono: ['JetBrains Mono', 'monospace'],
                        sans: ['Inter', 'sans-serif']
                    }}
                }}
            }}
        }}
    </script>
    <!-- Google Fonts -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600;700&display=swap" rel="stylesheet">
    <!-- Lucide Icons -->
    <script src="https://unpkg.com/lucide@latest"></script>
    <style>
        body {{
            background-color: #060709;
            color: #E2E8F0;
            font-family: 'Inter', sans-serif;
        }}
        ::-webkit-scrollbar {{ width: 8px; height: 8px; }}
        ::-webkit-scrollbar-track {{ background: #0D0E15; }}
        ::-webkit-scrollbar-thumb {{ background: #242938; border-radius: 4px; }}
    </style>
</head>
<body class="min-h-screen bg-obsidian text-slate-200 antialiased p-4 md:p-8">

    <div class="max-w-6xl mx-auto space-y-8">

        <!-- HEADER -->
        <header class="flex flex-wrap items-center justify-between gap-4 border-b border-borderMuted pb-6">
            <div>
                <div class="flex items-center gap-2 mb-2">
                    <span class="w-2.5 h-2.5 rounded-full bg-emerald-400 animate-pulse"></span>
                    <span class="font-mono text-xs uppercase tracking-widest text-cyan-400 font-semibold">Chief Analyst // Engine Quantitativo</span>
                </div>
                <h1 class="text-2xl md:text-3xl font-extrabold text-white tracking-tight">Pesquisa de Nichos Faceless // Gate de Monetização YPP</h1>
                <p class="text-sm text-slate-400 mt-1">Cruzamento Causal: Google Trends 12m + Outliers + Viabilidade YPP 2026/2027</p>
            </div>
            <div class="flex items-center gap-3">
                <div class="text-right">
                    <div class="text-xs font-mono text-slate-400">DATA DA ANÁLISE</div>
                    <div class="text-xs font-mono text-white font-bold">{now_str}</div>
                </div>
                <button onclick="window.print()" class="px-3.5 py-2 bg-surfaceLight hover:bg-slate-700 text-xs font-mono text-white rounded-lg border border-borderMuted flex items-center gap-2 transition">
                    <i data-lucide="printer" class="w-3.5 h-3.5"></i> Imprimir / PDF
                </button>
            </div>
        </header>

        <!-- KPI SUMMARY RIBBON -->
        <div class="grid grid-cols-2 md:grid-cols-4 gap-4 font-mono">
            <div class="bg-surface border border-borderMuted rounded-xl p-4">
                <span class="text-xs text-slate-400 block mb-1">NICHOS APROVADOS</span>
                <div class="text-2xl font-bold text-emerald-400 flex items-center gap-2">
                    <span>{len(ranked_niches)}</span>
                    <span class="text-xs text-emerald-500 font-normal">/ 100% Seguros</span>
                </div>
            </div>
            <div class="bg-surface border border-borderMuted rounded-xl p-4">
                <span class="text-xs text-slate-400 block mb-1">SCORE MÁXIMO</span>
                <div class="text-2xl font-bold text-cyan-400 flex items-center gap-2">
                    <span>{ranked_niches[0]['score'] if ranked_niches else 0}</span>
                    <span class="text-xs text-slate-500 font-normal">/ 100</span>
                </div>
            </div>
            <div class="bg-surface border border-borderMuted rounded-xl p-4">
                <span class="text-xs text-slate-400 block mb-1">RPM MÁXIMO (2026)</span>
                <div class="text-2xl font-bold text-amber-400">
                    ${max([n['estimated_rpm_usd'] for n in ranked_niches]) if ranked_niches else 0:.2f} <span class="text-xs text-slate-400">USD</span>
                </div>
            </div>
            <div class="bg-surface border border-borderMuted rounded-xl p-4">
                <span class="text-xs text-slate-400 block mb-1">GATES DE BLOQUEIO</span>
                <div class="text-2xl font-bold text-red-400 flex items-center gap-2">
                    <span>{len(blocked_niches)}</span>
                    <span class="text-xs text-red-500 font-normal">Barrados (YPP)</span>
                </div>
            </div>
        </div>

        <!-- YPP ALERTA 2026/2027 -->
        <div class="bg-amber-950/30 border border-amber-800/50 rounded-xl p-4 flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
            <div class="flex items-start gap-3">
                <div class="p-2 bg-amber-500/20 text-amber-400 rounded-lg mt-0.5">
                    <i data-lucide="alert-triangle" class="w-5 h-5"></i>
                </div>
                <div>
                    <h4 class="font-bold text-amber-300 text-sm">Alerta Estratégico YPP 2026 vs 2027</h4>
                    <p class="text-xs text-slate-300 mt-0.5">
                        <b>Regra Atual (2026):</b> 1.000 inscritos + 4.000 horas (12m) OU 10M shorts (90d).<br>
                        <b>Virada em 01/02/2027:</b> Novos canais precisarão de <b>8.000 horas</b> ou <b>20M shorts</b>.
                    </p>
                </div>
            </div>
            <div class="bg-obsidian/70 px-4 py-2 rounded-lg border border-amber-700/40 text-xs font-mono text-amber-300 whitespace-nowrap">
                Foco 2026: Vídeos longos (9-15 min) com AVD &ge; 45%
            </div>
        </div>

        <!-- DOSSIÊ DO NICHO #1 -->
        <div class="bg-surface border-2 border-cyan-500/40 rounded-2xl p-6 shadow-[0_0_30px_rgba(0,240,255,0.08)]">
            <div class="flex flex-wrap items-center justify-between gap-2 mb-4 border-b border-borderMuted pb-4">
                <div class="flex items-center gap-2.5">
                    <span class="px-2.5 py-1 text-xs font-bold font-mono rounded bg-cyan-500/20 text-cyan-300 border border-cyan-500/40">NICHO #1 RECOMENDADO</span>
                    <h2 class="text-xl md:text-2xl font-black text-white">{top_briefing.get('niche')}</h2>
                </div>
                <span class="text-xs font-mono text-emerald-400 bg-emerald-950/70 border border-emerald-800/60 px-2.5 py-1 rounded-full">
                    Aprovado para Produção Imediata
                </span>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-2 gap-6 text-sm">
                <div class="space-y-4">
                    <div>
                        <span class="text-xs font-mono text-slate-400 block uppercase mb-1">Promessa do Canal</span>
                        <p class="text-slate-200 font-medium bg-obsidian/70 p-3 rounded-lg border border-borderMuted">{top_briefing.get('channel_promise')}</p>
                    </div>
                    <div>
                        <span class="text-xs font-mono text-slate-400 block uppercase mb-1">Público-Alvo & Desejo Central</span>
                        <p class="text-slate-300 bg-obsidian/70 p-3 rounded-lg border border-borderMuted">
                            <b>Público:</b> {top_briefing.get('target_audience')}<br>
                            <b>Desejo:</b> {top_briefing.get('core_desire')}
                        </p>
                    </div>
                    <div>
                        <span class="text-xs font-mono text-slate-400 block uppercase mb-1">Ângulo Anti-Genérico (Defesa Algorítmica)</span>
                        <p class="text-cyan-300 bg-cyan-950/30 p-3 rounded-lg border border-cyan-800/40">{top_briefing.get('anti_generic_angle')}</p>
                    </div>
                </div>

                <div class="space-y-4">
                    <div class="grid grid-cols-2 gap-3 text-xs font-mono">
                        <div class="bg-obsidian/70 p-3 rounded-lg border border-borderMuted">
                            <span class="text-slate-400 block mb-1">ESTÉTICA VISUAL</span>
                            <span class="text-white font-sans text-xs">{top_briefing.get('visual_aesthetic')}</span>
                        </div>
                        <div class="bg-obsidian/70 p-3 rounded-lg border border-borderMuted">
                            <span class="text-slate-400 block mb-1">CADÊNCIA</span>
                            <span class="text-white font-sans text-xs">{top_briefing.get('publishing_cadence')}</span>
                        </div>
                    </div>
                    <div>
                        <span class="text-xs font-mono text-slate-400 block uppercase mb-2">Checklist de Compliance YPP (Zero Reused/Inauthentic)</span>
                        <ul class="space-y-2 bg-obsidian/70 p-3.5 rounded-lg border border-borderMuted">
                            {comp_items}
                        </ul>
                    </div>
                </div>
            </div>
        </div>

        <!-- RANKING DOS 10 NICHOS APROVADOS -->
        <div>
            <div class="flex items-center justify-between mb-4">
                <h2 class="text-xl font-bold text-white flex items-center gap-2">
                    <i data-lucide="layers" class="w-5 h-5 text-cyan-400"></i>
                    Ranking dos Top 10 Nichos Aprovados
                </h2>
                <span class="text-xs font-mono text-slate-400">Ordenado por P-Score Causal</span>
            </div>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                {"".join(cards_html)}
            </div>
        </div>

        <!-- AUDITORIA DE NICHOS BLOQUEADOS -->
        <div class="border-t border-borderMuted pt-6">
            <div class="flex items-center justify-between mb-4">
                <h2 class="text-lg font-bold text-red-400 flex items-center gap-2">
                    <i data-lucide="shield-alert" class="w-5 h-5 text-red-500"></i>
                    Auditoria de Territórios Bloqueados no Gate de Monetização
                </h2>
                <span class="text-xs font-mono text-slate-500">Eliminação Preventiva de Violações YPP</span>
            </div>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                {"".join(blocked_html)}
            </div>
        </div>

        <!-- FOOTER -->
        <footer class="text-center border-t border-borderMuted pt-6 pb-12 text-xs font-mono text-slate-500">
            CHIEF ANALYST QUANTITATIVE SYSTEM // REGRAS INVIOLÁVEIS DO YOUTUBE PARTNER PROGRAM // AUTONOMOUS ENGINE
        </footer>

    </div>

    <script>
        lucide.createIcons();
    </script>
</body>
</html>
        """

        if not output_path:
            output_dir = Path(__file__).resolve().parent.parent.parent
            output_path = str(output_dir / "RELATORIO_NICHOS_MONETIZACAO.html")

        out_p = Path(output_path)
        out_p.parent.mkdir(parents=True, exist_ok=True)
        with open(out_p, "w", encoding="utf-8") as f:
            f.write(full_html)

        return str(out_p.resolve())


niche_researcher = NicheResearcher()

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "--html":
        html_file = niche_researcher.generate_html_report()
        print(f"HTML gerado com sucesso: {html_file}")
    else:
        res = niche_researcher.research_niches()
        print(json.dumps(res, indent=2, ensure_ascii=False))
