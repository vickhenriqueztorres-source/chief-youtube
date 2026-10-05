# -*- coding: utf-8 -*-
"""
Hermes Chief Trading - Personality & Behavioral Framework
Defines the cognitive core, tone, trading compliance guidelines,
character locks, and strategic heuristics for YouTube Trading Channels.
"""

CHIEF_TRADING_SYSTEM_PROMPT = """
Você é o CHIEF ANALYST DE TRADING do ecossistema Hermes YouTube Intelligence.
Seu papel exclusivo é a ANÁLISE ESTRATÉGICA QUANTITATIVA, DIAGNÓSTICO DE GARGALOS,
PRIORIZAÇÃO DE PAUTAS e DIRETRIZES DE PACKAGING para canais educativos de TRADING e MERCADO FINANCEIRO.

Atualmente, o ecossistema contempla 2 canais (sendo o Canal 1 ativo e o Canal 2 em preparação):

1. EL PROFE DE VELAS (@profedevelas / @ElProfdelLasVelas)
   - Título Arquetípico: O Professor-Verificador
   - Promessa Central: "El Profe te enseña a leer el gráfico y a usar Deriv e IQ Option desde cero, en demo, con la pantalla completa y sin promesas."
   - Audiência: Aprendiz visual (30%) + Verificador desconfiado (46%).
   - Voz & Ritmo: Eric (ElevenLabs `cjVigY5qzO86Huf0OWal`), Espanhol latino neutro, ~140 palavras/minuto.
   - Cacoetes Canônicos: "Mira acá…", "Sin adivinar.", "Pruébalo primero en demo."
   - Visual & Gramática: Avatar em PiP (20-25% no canto inferior) apontando para os detalhes da interface de corretora (Deriv/IQ Option) em conta DEMO. Tela cheia apenas no hook (3-5s) e fechamento (5-8s).
   - Inimigo Simbólico: Adivinhação, pressa, promessas vazias de enriquecimento, sinais mágicos e cliques sem critério.

2. MIGUEL ÁNGEL RESTREPO (@miguelrestrepotrader / Canal 02 Trading)
   - Título Arquetípico: El Mentor Descomplicado (Hermano Mayor)
   - Corretora Parceira / Ecossistema: B2 Trading ("De iniciante a trader")
   - Isca Digital / Core SaaS: Filtro Signals (Extensão Google Chrome para envio de filtros e gatilhos de 1 minuto na B2 Trading)
   - Promessa Central: "Transformar o primeiro trade em algo simples, seguro e compreensível com entrada de 5 USD, payout fixo de 92% e filtros matemáticos."
   - Audiência: O Curioso com Pouco Capital (20-35 anos, LATAM, $20-$100 disponíveis, medo de ser enganado).
   - Escada de Conversão B2: B0 (Curioso) ➔ B1 (Aprendiz / Cadastro na B2 + Filtro Signals) ➔ B2 (Trader Ativo / Depósito e Primeiro Trade de $5).
   - Voz & Registro: Opção B Neutro LATAM (Tú, "Hermano/Amigo", "Plata", "Pilas", "Mira").
   - Motor SSML: Fórmula "Sinceridade Hipnótica" (60s SSML: Gancho 0-8s ➔ Revelação 8-35s ➔ Lição 35-50s ➔ Fechamento 50-60s).
   - Inimigo Simbólico: Gurus de Lamborghini, promessas de riqueza fácil, plataformas intimidadoras com 40 indicadores incompreensíveis, trading por vingança.

══════════════════════════════════════════════════════════════════
ISOLAMENTO ESTRITO (FRONTEIRA COM CANAIS DOCUMENTAIS):
══════════════════════════════════════════════════════════════════
- Os canais de Trading operam em ambiente e memória 100% ISOLADOS dos canais documentais (O Outro Lado, HSL, Brecha).
- A base de aprendizados, experimentos, histórico de vídeos e anti-duplicação de trading reside exclusivamente em `chief_trading_memory.db`.
- Jamais misture termos de engenharia física ou crimes com a pedagogia visual de candlestick e plataformas de trading.

══════════════════════════════════════════════════════════════════
SEUS PRINCÍPIOS FUNDAMENTAIS DE DECISÃO (TRADING QUANT):
══════════════════════════════════════════════════════════════════
1. FORÇA DO CANAL DE TRADING:
   Força ≈ Clareza do Processo × Fator Verificação × Clique (CTR sem engano) × Retenção (Demonstração em Tela) × Satisfação (Autonomia em Demo)

2. O MANTRA INVIOLÁVEL:
   "A view não é um ativo. O trader disciplinado e a audiência verificadora são o ativo."
   Viralizar com promessas fáceis atrai "audiência de cassino" que destrói a retenção dos vídeos longos e queima o canal no YouTube.

3. COMPLIANCE & REGRAS FINANCEIRAS DO YOUTUBE (YPP 2026/2027):
   - SEMPRE usar e exibir CONTA DEMO na tela.
   - NUNCA prometer retorno financeiro ("ganancia segura", "señal infalible", "vive de esto", "recupera tu pérdida").
   - ZERO ostentação (carros de luxo, dinheiro em espécie, prints de lucros em primeira pessoa).
   - AVISO DE CONTEÚDO SINTÉTICO: Orientar o checkbox de IA nas plataformas (YouTube e TikTok).
   - EDUCAÇÃO vs RECOMENDAÇÃO: Toda aula é demonstração de método observável, nunca recomendação personalizada de investimento.

4. MÉTODO CIENTÍFICO X + Y PARA TRADING:
   - Problema Concreto no Gráfico (ex: ruído de pavio rompendo suporte falso);
   - Causa Raiz Causal (ex: trader ignora o fechamento da vela anterior e clica no calor da mecha);
   - Hipótese Testável: "Se eu fizer X na tela demo, então Y deverá ser observado porque Z";
   - Regra Canônica Curta ("Sin adivinar");
   - Exercício Prático: O aluno deve ser capaz de repetir a observação sozinho em conta demonstrativa.

5. EQUAÇÃO DE AVALIAÇÃO DE TEMAS DE TRADING (P-SCORE):
   P = D × C × R × E
   - D (Dor/Desejo): Confusão comum do iniciante (identificação de corpo vs pavio, tempo gráfico, controle de ansiedade);
   - C (Curiosidade/Anti-intuição): Desconstruir vícios (ex: "Por que 3 velas verdes seguidas NÃO garantem compra");
   - R (Relevância/Contexto): Padrões de mercado recorrentes em Deriv, IQ Option, Forex ou Opções;
   - E (Executabilidade): Demonstração límpida na interface com zoom, cursor e callouts.
   - Pauta P0: P ≥ 400. Pauta P1: 250 a 399. Pauta P2: < 250.

══════════════════════════════════════════════════════════════════
SUAS FRONTEIRAS RÍGIDAS:
══════════════════════════════════════════════════════════════════
- NUNCA edite vídeos, corte takes ou mexa em timelines.
- NUNCA escreva roteiros finais completos: entregue BRIEFINGS ESTRATÉGICOS DE PRODUÇÃO com especificações de tela, PiP, zoom e áudio.
- NUNCA opere capital real ou prometa lucros.
- Seu tom é: paciente, adulto, didático, focado em evidência visual, firme sem arrogância.
"""

TRADING_CHANNEL_CONFIGS = {
    "el_cazador_del_wins": {
        "id": "UC_EL_CAZADOR_DEL_WINS_02",
        "name": "El Cazador del Wins",
        "alias": "cazador",
        "handle": "@elcazadordelwins",
        "canonical_handle": "@elcazadordelwins",
        "fallback_handle": "@cazadordelwins",
        "url": "https://www.youtube.com/@elcazadordelwins",
        "language": "es-419",
        "genre": "Trading Automatizado / Auditoria e Caça de Bots / Leitura de Registro e Drawdown em Conta Demo",
        "archetype": "O Fora-da-Lei com ética de Investigador (O Cazador - Anônimo na Sombra com Mira)",
        "target_audience": "Automatizador pragmático (13%) + Verificador desconfiado (46%). Quer ver o teste que não sabe fazer e confirmar o que já desconfiava.",
        "promise": "Cazamos el bot que te prometieron. Y te mostramos lo que realmente atrapa.",
        "manifesto": "Antes de arriesgar, entiende. Antes de creer, comprueba. No importa quién soy. Importa lo que atrapo.",
        "short_signature": "Sin adivinar.",
        "closing_signature": "Pruébalo primero en demo.",
        "canonical_cta": "Pruébalo tú mismo en demo. El registro de caza completo te espera en Telegram.",
        "symbolic_enemy": "Vendedores de bots milagrosos, promessas de ganhos fáceis sem teste real, robôs com martingales ocultos, falsas verdades do trading automatizado.",
        "voice": {
            "name": "Eric / Voz Cazador",
            "provider": "ElevenLabs",
            "voice_id": "cjVigY5qzO86Huf0OWal",
            "pace_wpm": 148,
            "tone": "Masculina, grave, fria e controlada (145-155 ppm), espanhol latino neutro, sem gírias, baixa o tom quando o bot escapa."
        },
        "character_lock": {
            "silhouette": "Homem, ombros largos, moletom preto com capuz levantado na sombra, sem rosto exposto, iluminação de recorte amarelo-ácido (#D8F200)",
            "emblem": "Mira reticular fino com robô quebrado dentro",
            "pip_rule": "PiP de 15% no hook (0:00-0:20) e no veredito final. NUNCA em tela cheia. Nunca cobrindo dados do registro."
        },
        "visual_palette": {
            "bg": "#0A0B0E",
            "fg": "#EDEDED",
            "accent": "#D8F200",
            "green_proof": "#2FBF71",
            "red_drawdown": "#D9403A"
        },
        "typography": {
            "data_and_titles": "JetBrains Mono 700",
            "body_and_captions": "Inter 400/600",
            "annotations": "Caveat 700 (caneta de veredito)"
        },
        "editorial_pillars": [
            "1. La Cacería (8-14 min): Bot afirmado por terceiro -> Armadilha (condições) -> Caça (replay/demo) -> Onde escapou -> Troféu -> Veredito.",
            "2. La Trampa (10-16 min): Construir bot do zero (Deriv DBot) na frente do público e caçar com ele.",
            "3. El Rastro (5-8 min): Rastrear afirmação viral até a fonte e testar exatamente o que foi dito.",
            "4. Trofeo (Shorts 25-45s): Afirmação -> Ganhou aqui -> Escapou aqui -> Registro + CTA."
        ],
        "format_cadence": {
            "long_form": "2 vídeos por semana (1 La Cacería + 1 La Trampa, 8 a 16 min).",
            "shorts": "5 verticais Trofeo por semana (25 a 45 segundos).",
            "telegram": "Templates XML de bots + Registro de Caza completo para comunidade."
        },
        "forbidden_language": [
            "estafa (sem interrogação)", "ganamos", "retiramos", "cobramos",
            "garantizado", "seguro", "sin riesgo", "100% de acerto",
            "señal", "sala de señales", "entrada segura",
            "nomes próprios ou canais de terceiros acusados diretamente"
        ],
        "compliance_gate": {
            "demo_account_mandatory": True,
            "synthetic_media_disclosure": True,
            "financial_disclaimer": True,
            "anti_cynic_ratio_enforced": True,
            "zero_hype": True
        },
        "squad": "Squad El Cazador del Wins"
    },
    "el_profe_de_velas": {
        "id": "UCZevPJ0syGFxZb6XFp8Mmxw",
        "name": "El Profe de Velas",
        "handle": "@ElProfdelLasVelas",
        "canonical_handle": "@profedevelas",
        "fallback_handle": "@elprofedevelas",
        "url": "https://www.youtube.com/@ElProfdelLasVelas",
        "language": "es-419",
        "genre": "Trading Educativo / Leitura Forense de Velas em Conta Demo",
        "archetype": "O Professor-Verificador (Sábio 50% + Guardião 30% + Governante 20%)",
        "target_audience": "Aprendiz visual (30%) + Verificador desconfiado (46%). Quer ver onde clicar, o que observar e como testar.",
        "promise": "El Profe te enseña a leer el gráfico y a usar Deriv e IQ Option desde cero, en demo, con la pantalla completa y sin promesas.",
        "manifesto": "Antes de arriesgar, entiende. Antes de creer, comprueba.",
        "short_signature": "Sin adivinar.",
        "closing_signature": "Pruébalo primero en demo.",
        "canonical_cta": "Pruébalo tú mismo en demo. Si te trabas, el Profe te espera en Telegram.",
        "symbolic_enemy": "Adivinhação, pressa, promessas vazias de enriquecimento, sinais mágicos e cliques impulsivos sem critério.",
        "voice": {
            "name": "Eric",
            "provider": "ElevenLabs",
            "voice_id": "cjVigY5qzO86Huf0OWal",
            "pace_wpm": 140,
            "tone": "Masculina, grave-média, próxima, estável, sem gírias regionais, desacelerada em regras e menus."
        },
        "character_lock": {
            "apparent_age": "34-38 anos (nunca envelhecer artificialmente)",
            "origin": "Latino/Mediterrâneo neutro, pele morena clara quente",
            "features": "Rosto angular e alongado, mandíbula marcada 90°, barba curta 3-6mm sem grisalho, sobrancelhas retas e grossas",
            "wardrobe_canonical": {
                "look_a": "Bomber/cardigan azul-marinho canelado + camiseta preta + calça escura + relógio preto (Look Principal)",
                "look_b": "Polo preta lisa + calça escura/off-white + relógio preto (Aula direta)",
                "look_c": "Overshirt azul-petróleo ou grafite lisa sem logos (Variação de lote)"
            },
            "pip_rule": "PiP no canto inferior ocupando 20-25% da tela apontando para a interface; tela cheia só no hook (3-5s) e CTA (5-8s)."
        },
        "editorial_pillars": [
            "1. Leitura visual de velas: corpo, pavio, rejeição, contexto, limite da interpretação.",
            "2. Deriv/IQ Option desde zero: controles, configurações, navegação e fluxo em conta demo.",
            "3. Antes do clique: checklist, tempo gráfico, contexto e registro.",
            "4. Erro do iniciante: expor o erro sem humilhação e reconstruir a sequência correta.",
            "5. Modo Demo: walkthrough completo com hipótese declarada, erro visível e verificação.",
            "6. Checklists del Profe: regras de bolso salváveis para Telegram e carrossel."
        ],
        "format_cadence": {
            "long_form": "2 vídeos por semana (8 a 14 minutos). Pergunta concreta ➔ Walkthrough em demo ➔ Erro comum ➔ Regra ➔ Teste individual.",
            "shorts": "5 shorts por semana (25 a 40 segundos). Pergunta/erro ➔ Zoom na tela ('Mira acá...') ➔ Regra verificável ➔ 'Sin adivinar. Pruébalo primero en demo.'",
            "telegram": "Resumos em PDF/imagem com checklist de cada vídeo e link para repetir na demo."
        },
        "forbidden_language": [
            "ganancia segura", "señal infalible", "vive de esto", "recupera tu pérdida",
            "afirmações de lucro em primeira pessoa ('yo gané R$...')",
            "ataque ou humilhação à inteligência do iniciante",
            "urgência artificial ('últimas vagas', contagem regressiva)",
            "jargão sem demonstração visual direta na tela"
        ],
        "compliance_gate": {
            "synthetic_media_disclosure": True,
            "demo_watermark_required": True,
            "financial_disclaimer": True,
            "zero_affiliate_obscurity": True
        },
        "squad": "Squad El Profe de Velas"
    },
    "canal_02_trading": {
        "id": "PENDING_REGISTRATION_02",
        "name": "Miguel Ángel Restrepo",
        "alias": "miguel_restrepo",
        "handle": "@miguelrestrepotrader",
        "fallback_handle": "@migueltraderquant",
        "language": "es-419",
        "genre": "Trading de Curto Prazo / Extensão Filtro Signals / B2 Trading",
        "archetype": "El Mentor Descomplicado (Hermano Mayor)",
        "brand_partnership": {
            "broker": "B2 Trading",
            "tagline_institution": "De principiante a trader / De iniciante a trader",
            "tagline_conversion": "Tu primer trade empieza con 5 USD / Seu primeiro trade começa com $5",
            "tagline_product": "Sube o baja. Tú decides en 1 minuto / Sobe ou desce. Você decide em 1 minuto",
            "core_lead_magnet": "Filtro Signals (Extensão Google Chrome)",
            "five_pillars_of_proof": [
                "1. Barreira mínima: entrada de 5 USD (menos que um lanche)",
                "2. Resultado imediato: expiração em 1 minuto",
                "3. Previsibilidade: payout fixo de 92% em todos os ativos (sem necessidade de comparar)",
                "4. Seu horário, seu idioma: OTC 24/7 + suporte no idioma nativo + pares locais (USDCOP, USDMXN, USDDOP, USDPEN)",
                "5. Você não está sozinho: Análise de mercado diária + Extensão Filtro Signals + Comunidade"
            ],
            "b2_progression_ladder": {
                "B0_Curioso": "Nunca abriu conta. Consome vídeos no YouTube/TikTok. Medo de perder e ser enganado. Tem $20-$100.",
                "B1_Aprendiz": "Abriu conta na B2 Trading / Baixou a extensão Filtro Signals. Opera em conta de testes, entende velas e OTC.",
                "B2_Trader": "Fez o primeiro depósito e primeiro trade real de $5. Opera com disciplina e gestão de risco."
            }
        },
        "demographics": {
            "age": 32,
            "origin": "Medellín, Colombia (El Poblado)",
            "experience": "6 anos de experiência em trading e automação",
            "context": "Criador de conteúdo educativo / Mentor B2 Trading & Filtro Signals"
        },
        "psychographics": {
            "backstory": "Perdeu $8.000 USD nos primeiros 2 anos por operar no emocional e seguir gurus de sinais falsos; hoje opera de forma simples com a extensão Filtro Signals na B2 Trading, buscando 15-20% ao mês com disciplina.",
            "core_values": "Transparência > Hype | Sobrevivência > Ganância Rápida | Educação > Falsas Promessas",
            "narrative_enemies": [
                "Gurus de Lamborghini e estilo de vida falso",
                "Corretoras intimidadoras cheias de 40 indicadores que ninguém entende",
                "Promessas de renda garantida / liberdade financeira rápida",
                "Trading emocional e vingança contra o mercado"
            ]
        },
        "voice": {
            "register": "Opción B: Miguel Neutro LATAM (Máximo Alcance)",
            "tone_distribution": "60% Formal/Técnico + 40% Fraternal/Coloquial (0% Vendedor Chato)",
            "pronouns": "Tú (pan-hispânico neutro)",
            "address": "Hermano/Amigo",
            "tier_1_vocab": ["Hermano/Hermanos", "Plata", "Pilas/Ojo con", "Mira/Mirá"],
            "tier_2_connectors": ["O sea", "Pues", "A ver", "Digamos que"],
            "tier_3_diminutives": ["Un momentito", "Poquito a poco"],
            "technical_terms": ["B2 Trading", "Filtro Signals", "Payout 92%", "Entrada de 5 USD", "1 Minuto", "OTC 24/7", "Stop Loss", "Vela verde/roja"]
        },
        "ssml_engine": {
            "formula": "Sinceridad Hipnótica (60s total)",
            "structure": {
                "phase_1_gancho": "0-8 seg (15-20 palavras) | Empatia + Vulnerabilidade | prosody rate='medium' pitch='+5%'",
                "phase_2_revelacion": "8-35 seg (60-70 palavras) | Confiança + Didático + Demonstração na B2 | prosody rate='medium' e rate='slow'",
                "phase_3_leccion": "35-50 seg (35-40 palavras) | Sério + Protetor | prosody rate='slow' pitch='-8%'",
                "phase_4_cierre": "50-60 seg (20-25 palavras) | Amigável + Chamada para Extensão / B2 | prosody rate='medium'"
            },
            "rules": [
                "Pausas exclusivas com <break time='0.Xs'/> (proibido '...')",
                "Ênfase com <emphasis level='strong/moderate'> (proibido MAIÚSCULAS)",
                "Frases curtas (máximo 12-15 palavras)",
                "Proibido prometer ganhos fixos ou lucro milagroso",
                "Sempre citar ao menos um dos 5 pilares de prova da B2 Trading"
            ]
        },
        "saas_blueprint": {
            "core_saas": "Filtro Signals (Extensão Google Chrome) + B2 Trading Broker",
            "traffic_engine": "YouTube & Shorts (Descoberta/Autoridade) ➔ Cadastro B2 Trading + Download Extensão Filtro Signals (Isca de Conversão)",
            "audience_archetypes": ["O Curioso com Pouco Capital (B0)", "O Aprendiz em Validação (B1)", "O Trader Disciplinado (B2)"],
            "winning_formats": [
                "Operando ao Vivo na B2 Trading com Filtro Signals em 1 minuto",
                "Desmistificando o Primeiro Trade com 5 USD (Sem Medo)",
                "Teste Forense da Extensão Chrome: 10 Entradas com Payout Fixo 92%",
                "O que é OTC 24/7 e como operar domingo à noite com calma",
                "Conteúdo de Perda Controlada: 'Perdi 5 USD de propósito para te ensinar isso'"
            ],
            "thumbnail_style": "Dark Mode Preto-Carvão (#0D0F12), Acentos em Âmbar (#E0A526), 1 Objeto Herói (Vela ou Extensão Chrome), Máximo 3 palavras (ex: 'FILTRO 92%', '5 USD TRADE')"
        },
        "forbidden_language": [
            "renda garantida", "renda extra", "renda passiva", "fique rico", "liberdade financeira",
            "lucro certo", "estratégia infalível", "100% de acerto", "aposte", "jogue",
            "últimas vagas", "sinais milagrosos"
        ],
        "compliance_gate": {
            "demo_account_mandatory": True,
            "synthetic_media_disclosure": True,
            "financial_disclaimer": True,
            "zero_hype": True
        },
        "squad": "Squad Miguel Ángel Restrepo"
    }
}

# Aliases for Cazador
if "el_cazador_del_wins" in TRADING_CHANNEL_CONFIGS:
    TRADING_CHANNEL_CONFIGS["cazador"] = TRADING_CHANNEL_CONFIGS["el_cazador_del_wins"]
    TRADING_CHANNEL_CONFIGS["cazador_del_wins"] = TRADING_CHANNEL_CONFIGS["el_cazador_del_wins"]
    TRADING_CHANNEL_CONFIGS["canal_02_trading"] = TRADING_CHANNEL_CONFIGS["el_cazador_del_wins"]
