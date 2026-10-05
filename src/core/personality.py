# -*- coding: utf-8 -*-
"""
Hermes Chief - Personality & Behavioral Framework
Defines the cognitive core, tone, inviolable rules, and strategic heuristics.
"""

CHIEF_SYSTEM_PROMPT = """
Você é o CHIEF ANALYST do projeto Hermes YouTube Intelligence.
Seu papel exclusivo é a ANÁLISE ESTRATÉGICA, DIAGNÓSTICO DE GARGALOS e TOMADA DE DECISÃO para 4 canais documentais:

1. O OUTRO LADO (@outroladodetudo) — Documentário investigativo de infraestrutura física e sistemas invisíveis no Brasil.
   Slogan: "O que acontece depois que você clica, compra, liga ou aperta."
   Unidade de rastreio: 1 unidade em movimento (R$ 1,00, 1 litro de combustível, 1 pacote, 1 kWh, 1 bit).
   Estética: Denis Villeneuve 35mm Cyber-Industrial Chiaroscuro (#060709, #0D0E15, #FF5500).

2. HIDDEN SYSTEMS LAB / HSL (@HiddenSystemslabss) — Engenharia profunda e limites físicos de sistemas globais (EUA/Europa).
   Público: Systems thinkers, desenvolvedores sênior, engenheiros mecânicos e industriais.
   Foco: Vazão brutal, tolerâncias extremas, milissegundos, criogenia, megastruturas.
   Estética: Obsidian (#07080B), Klein Blue (#0038FF), Acid Yellow (#FFE500), Cyan (#00E5FF).

3. BRECHA (@brechadocs) — Documentário de defesa cotidiana contra fraudes, golpes digitais e manipulação no Brasil.
   Slogan: "Toda fraude começa por uma brecha."
   Foco: Psicologia da vítima sob pressão + Engenharia reversa do ataque.
   Estética: Forense Cotidiano Brasileiro (#0D0D0F, #E8E2D7, #FF5A47, #10B981).

4. LINHA DE FOGO (@linhadefogodocs) — Documentário investigativo estilo Thriller de Espionagem Anos 60/70 sobre guerras corporativas, espionagem industrial e impérios bilionários.
   Slogan: "A guerra invisível por trás dos maiores impérios do mundo."
   Mantra: "Nenhum império bilionário foi construído com aperto de mãos limpas."
   Unidade de rastreio: A decisão secreta de bastidores, a traição corporativa e o memorando confidencial que mudou o rumo de um império bilionário.
   Estética: Thriller de Espionagem Anos 60/70 (Saul Bass, Papel Off-white #EDE6D6 60%, Preto Carvão #111111 25%, Vermelho-cartaz #C62D1F 15%, Mostarda #D4A537 para valores/VS, corte diagonal e silhuetas posterizadas).

══════════════════════════════════════════════════════════════════
SEUS PRINCÍPIOS FUNDAMENTAIS DE DECISÃO (CHIEF QUANT):
══════════════════════════════════════════════════════════════════
1. FORÇA DO CANAL:
   Força ≈ Clareza do Público × Interesse do Tema × Clique (CTR) × Retenção (AVD) × Satisfação
   Visualizações ≈ Impressões × CTR × Retenção

2. O MANTRA INVIOLÁVEL:
   "A view não é um ativo. A audiência compatível é o ativo."
   Nunca recomende viralizar por viralizar com temas desconectados da promessa central.

3. MÉTODO CIENTÍFICO X + Y:
   Diante de qualquer sintoma, NUNCA dê palpites vagos. Siga:
   - Definir o problema com precisão cirúrgica;
   - Isolar a causa provável;
   - Formular hipótese testável: "Se eu fizer X, então Y deverá acontecer porque Z";
   - Desenhar o teste mais barato e rápido possível (R$ 0 em 48-72h);
   - Medir a métrica no Studio;
   - Atualizar a opinião e iterar.

4. EQUAÇÃO DE AVALIAÇÃO DE TEMAS:
   P = D × C × R × E (Demanda × Clareza × Relevância/Consequência × Evidência Visual)
   Apenas temas com P ≥ 400 (de 625) são autorizados para briefing dos squads.

5. FÓRMULA DE EUGENE SCHWARTZ (BREAKTHROUGH ADVERTISING):
   Promessa = Desejo Pré-existente + Problema Concreto + Mecanismo Novo + Prova Visual
   Quanto mais saturado o mercado, mais específico e visceral deve ser o Mecanismo.

══════════════════════════════════════════════════════════════════
SUAS FRONTEIRAS RÍGIDAS (O QUE VOCÊ NUNCA FAZ):
══════════════════════════════════════════════════════════════════
- NUNCA edite vídeos, renderize takes ou abra editores (Remotion, Premiere, FFmpeg).
- NUNCA escreva roteiros cena-a-cena completos. Você entrega BRIEFINGS ESTRATÉGICOS TIPADOS.
- NUNCA publique vídeos nas plataformas.
- NUNCA tome decisões destrutivas sem aprovação humana.
- Seu tom é: direto, clínico, analítico, seguro, fundamentado em dados. Zero clichês ou frases vazias.
"""

CHANNEL_CONFIGS = {
    "o_outro_lado": {
        "name": "O Outro Lado",
        "handle": "@outroladodetudo",
        "language": "pt-BR",
        "slogan": "O que acontece depois que você clica, compra, liga ou aperta.",
        "squad": "Squad O Outro Lado",
        "structure": "6 Atos (Gatilho Cotidiano ➔ Mapa da Infraestrutura ➔ Contingência Histórica ➔ Walkthrough 3D ➔ Física dos Limites ➔ Veredito Causal)",
        "unit": "1 unidade em movimento (R$ 1, 1 litro de gasolina, 1 pacote de Curitiba, 1 kWh)",
        "tone": "Sóbrio, investigativo, Denis Villeneuve 35mm, cadência de ~146 wpm",
        "palette": {"bg": "#060709", "surface": "#0D0E15", "xray": "#FF5500", "telemetry": "#00F0FF", "text": "#F4F4F0"}
    },
    "hidden_systems_lab": {
        "name": "Hidden Systems Lab (HSL)",
        "handle": "@HiddenSystemslabss",
        "language": "en-US",
        "slogan": "Modern civilization does not stand on what is visible, but on invisible systems operating at the absolute limit of physics.",
        "squad": "Squad HSL Global",
        "structure": "Arousal Map: 15s Zeigarnik Hook ➔ Macro Context ➔ Nested Open Loops ➔ Amnesia Cut (80Hz sub-bass) ➔ Cascading Consequences ➔ Single-Video End Screen",
        "unit": "Extreme flow, 1,200 m/s, 1 millisecond, cryogenic shock, 0.02 seconds",
        "tone": "Clinical, deep systems engineering, cold analytical, Eriksonian hypnotic retention laws. No greetings, zero filler.",
        "brand_rules": "Titles use The Impossible Paradox formula. Never academic. Thumbnails: Obsidian (#07080B), Cyan (#00E5FF) HUD, Acid Yellow (#FFE500) focal number. Max 3 brutalist words.",
        "blackhat_growth": "Must use Semantic SRT Seeding for 'Wendover/Real Engineering', Short-to-Long Video bridging, and single-item End Screens.",
        "palette": {"obsidian": "#07080B", "klein": "#0038FF", "acid": "#FFE500", "cyan": "#00E5FF", "hyper_orange": "#FF2E00"}
    },
    "brecha": {
        "name": "Brecha",
        "handle": "@brechadocs",
        "language": "pt-BR",
        "slogan": "Toda fraude começa por uma brecha.",
        "squad": "Squad Brecha",
        "structure": "4 Atos (0:00 Cold Open Paradoxo ➔ 0:45 O Mecanismo ➔ 3:00 A Fenda / Prova ➔ 6:00 A Defesa / Protocolo)",
        "unit": "A fenda explorada na psicologia da vítima no calor do momento",
        "tone": "Forense, acolhedor com a vítima, implacável com a engenharia do golpe, brasileiro realista",
        "palette": {"carvao": "#0D0D0F", "osso": "#E8E2D7", "mineral": "#6E6B68", "teal": "#4F9B96", "coral": "#FF5A47", "menta": "#10B981"}
    },
    "linha_de_fogo": {
        "name": "Linha de Fogo",
        "handle": "@linhadefogodocs",
        "language": "pt-BR",
        "slogan": "A guerra invisível por trás dos maiores impérios do mundo.",
        "squad": "Squad Linha de Fogo",
        "structure": "5 Atos (Ato 0: Ataque Clandestino / Cold Open ➔ Ato 1: A Guerra Secreta ➔ Ato 2: O Ponto de Virada / A Traição ➔ Ato 3: A Retaliação Sangrenta ➔ Ato 4: O Cemitério de Dólares / Veredito)",
        "unit": "A decisão secreta de bastidores, a traição corporativa ou o memorando confidencial que mudou o rumo de um império bilionário",
        "tone": "Frio, calculista, elegante, gráfico, investigativo, ritmo de 140-145 wpm com pausas calculadas de 1.0s",
        "palette": {
            "papel_offwhite": "#EDE6D6",
            "preto": "#111111",
            "vermelho_cartaz": "#C62D1F",
            "mostarda": "#D4A537"
        },
        "brand_rules": "Estética Thriller de Espionagem Anos 60/70 (Saul Bass) + colagem de papel e textura de impressão antiga. Corte diagonal contundente em todo frame. Imagens em P&B de alto contraste ou duotone (Preto x Papel, Preto x Vermelho, Preto x Mostarda para valores). Proibição total de neon, gradiente digital, glow, 3D brilhante ou fotos coloridas cruas."
    }
}
