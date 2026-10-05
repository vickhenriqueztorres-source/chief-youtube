# -*- coding: utf-8 -*-
"""
Hermes Chief Trading Skill: trading-theme-decider
Evaluates, scores, and prioritizes trading educational themes using the Quant P-Score equation
(P = D * C * R * E) + Safety Filter (S), integrated with the 4-layer Anti-Duplication Memory Guardian.
"""

from typing import Dict, Any, List, Optional
from src.core.trading_memory import trading_memory

class TradingThemeDecider:
    """Evaluates trading topics using quantitative rigor and anti-duplication memory."""

    THEME_CANDIDATE_BANK = {
        "el_cazador_del_wins": [
            {
                "topic": "Cacé el Bot de $997 de Telegram por 14 Días (Aquí Escapó) | La Cacería",
                "d_score": 5, "c_score": 5, "r_score": 5, "e_score": 5, "s_score": 5,
                "pillar": "La Cacería",
                "thesis": "Mostra o teste de 14 dias em conta demo do bot vendido como infalível no Telegram, revelando o drawdown de -34% no dia 9 por quebra de volatilidade.",
                "hook_suggestion": "Te vendieron este bot por 997 dólares diciendo que nunca pierde. Lo pusimos en la trampa 14 días seguidos. Mira exactamente dónde escapó el día 9.",
                "canonical_phrase": "Cazamos el bot que te prometieron. Y te mostramos lo que realmente atrapa."
            },
            {
                "topic": "Construí la Trampa desde Cero en Deriv DBot: El Error de Martingala | La Trampa",
                "d_score": 5, "c_score": 5, "r_score": 5, "e_score": 5, "s_score": 5,
                "pillar": "La Trampa",
                "thesis": "Montagem transparente de um bot no Deriv DBot demonstrando matematicamente por que multiplicadores de martingala 2.1x quebram qualquer banca em sequências de 7 derrotas.",
                "hook_suggestion": "Vamos a armar la trampa en vivo desde cero. Te voy a mostrar el bloque exacto de código que los vendedores de bots ocultan para que no veas cómo queman tu dinero.",
                "canonical_phrase": "Antes de arriesgar, entiende. Antes de creer, comprueba."
            },
            {
                "topic": "Rastreé el Bot Viral de $500 al Día: Lo que Realmente Atrapa | El Rastro",
                "d_score": 5, "c_score": 4, "r_score": 5, "e_score": 5, "s_score": 5,
                "pillar": "El Rastro",
                "thesis": "Desmonte minucioso da promessa viral de $500/dia, submetendo a estratégia a 200 repetições com slippage e spreads simulados.",
                "hook_suggestion": "Este video tiene 2 millones de vistas y dice que este bot genera $500 al día. Fuimos a buscar la fuente original y lo metimos en la jaula de pruebas.",
                "canonical_phrase": "No importa quién soy. Importa lo que atrapo."
            },
            {
                "topic": "Probé el Bot de RSI 14 en Demo: El Momento Exacto donde Quemó la Cuenta",
                "d_score": 5, "c_score": 5, "r_score": 4, "e_score": 5, "s_score": 5,
                "pillar": "La Cacería",
                "thesis": "Evidência visual de como indicadores convencionais como RSI geram sinais falsos catastróficos em tendências fortes sem filtro de ruído.",
                "hook_suggestion": "Te dijeron que cuando el RSI toca 70 tienes que vender sí o sí. Pusimos un bot a ejecutar esa regla automática. Mira lo que le pasó a la cuenta en 3 horas.",
                "canonical_phrase": "El gráfico no perdona la pereza. Pruébalo primero en demo."
            }
        ],
        "el_profe_de_velas": [
            {
                "topic": "La Trampa del Martillo: Por Qué Esta Mecha Te Hace Perder en Soporte",
                "d_score": 5, "c_score": 5, "r_score": 4, "e_score": 5, "s_score": 5,
                "pillar": "Leitura visual de velas",
                "thesis": "O iniciante decora que martelo é compra garantida. O Profe abre a tela da Deriv e mostra como uma mecha inferior em zona sem confirmação é apenas absorção momentânea que engole o trader.",
                "hook_suggestion": "Ves un martillo en un soporte y crees que el precio va a rebotar. Clic inmediato. Y tres segundos después, la vela siguiente rompe hacia abajo. Mira acá: no fue mala suerte; fue una trampa que no supiste leer.",
                "canonical_phrase": "El martillo te muestra una hipótesis, no un cheque firmado. Sin adivinar."
            },
            {
                "topic": "El Checklist de 3 Pasos Antes de Tocar el Botón (Sin Adivinar)",
                "d_score": 5, "c_score": 4, "r_score": 5, "e_score": 5, "s_score": 5,
                "pillar": "Antes do clique",
                "thesis": "A pressa do clique destrói o iniciante. O Profe entrega um protocolo de tela: 1. Contexto das últimas 3 velas; 2. Tempo de expiração alinhado; 3. Limite do pavio verificado.",
                "hook_suggestion": "Antes de poner el dedo en el botón verde o rojo, tu ojo tiene que revisar exactamente estos tres puntos en la pantalla. Si falta uno solo, la operación no existe. Pruébalo primero en demo.",
                "canonical_phrase": "Si no puedes explicar la entrada en voz alta antes del clic, todavía estás adivinando."
            },
            {
                "topic": "Deriv Desde Cero: Configura Tu Cuenta Demo y Evita el Clic Accidental",
                "d_score": 5, "c_score": 4, "r_score": 4, "e_score": 5, "s_score": 5,
                "pillar": "Deriv/IQ Option desde zero",
                "thesis": "A interface da corretora assusta e induz ao erro. O Profe faz um walkthrough guiado de 10 minutos ensinando a limpar gráficos, configurar tempo e blindar a conta de testes.",
                "hook_suggestion": "El 80% de los errores de un principiante no ocurren por el gráfico; ocurren porque configuraron mal el tiempo o tocaron el botón equivocado en la plataforma. Hoy abrimos Deriv desde cero.",
                "canonical_phrase": "Primero dominas los controles de la pantalla. La velocidad viene después."
            },
            {
                "topic": "El Error del Martingale: Por Qué Doblar la Entrada Destruye Tu Proceso",
                "d_score": 5, "c_score": 5, "r_score": 5, "e_score": 4, "s_score": 5,
                "pillar": "Erro do iniciante",
                "thesis": "Desmonta a falácia matemática mais perigosa do trading latino. Mostra na demo como 4 derrotas seguidas em martingale aniquilam semanas de disciplina.",
                "hook_suggestion": "Perdiste una operación y tu primer impulso es meter el doble en la siguiente para 'recuperar'. Te voy a mostrar en cuenta demo exactamente cómo esa trampa mental te deja sin margen.",
                "canonical_phrase": "El mercado no te debe nada. Duplicar la entrada no es estrategia; es desesperación."
            },
            {
                "topic": "Ruptura Falsa vs Ruptura Real: El Secreto Está en el Cierre de la Vela",
                "d_score": 5, "c_score": 5, "r_score": 4, "e_score": 5, "s_score": 5,
                "pillar": "Leitura visual de velas",
                "thesis": "A diferença causal entre uma mecha que apenas perfura o nível e um corpo que fecha do outro lado com rejeição observável.",
                "hook_suggestion": "¿Cuántas veces viste el precio superar la línea, entraste convencido y la vela cerró adentro dejando una mecha gigante? Mira acá: la mecha perfora; el cuerpo confirma.",
                "canonical_phrase": "Nunca operes una ruptura mientras la vela esté viva. Espera el cierre. Sin adivinar."
            },
            {
                "topic": "Vela Doji en Zona Clave: Lo Que la Mayoría Ignora Sobre la Indecisión",
                "d_score": 4, "c_score": 4, "r_score": 4, "e_score": 5, "s_score": 5,
                "pillar": "Leitura visual de velas",
                "thesis": "O Doji não é um sinal de reversão imediata; é um equilíbrio momentâneo de forças. O Profe ensina a esperar a vela de confirmação seguinte.",
                "hook_suggestion": "Ves una vela con cuerpo casi invisible y mechas a los dos lados. Te dijeron que es cambio de tendencia inmediato. Falso. Una vela Doji es una pausa, no una orden de disparo.",
                "canonical_phrase": "El Doji te pide paciencia, no velocidad. Obsérvalo primero en demo."
            }
        ],
        "miguel_trader": [
            {
                "topic": "Instalé la Extensión Filtro Signals en B2 Trading: 10 Entradas de 1 Minuto",
                "d_score": 5, "c_score": 5, "r_score": 5, "e_score": 5, "s_score": 5,
                "pillar": "Extensão Filtro Signals & B2 Trading",
                "thesis": "Mostra na prática a extensão do Chrome enviando gatilhos filtrados em tempo real na B2 Trading com 92% de payout fixo e entradas de $5.",
                "hook_suggestion": "El 90% de los principiantes pierden porque hacen clic por ansiedad en cualquier vela. Instalé la extensión Filtro Signals en B2 Trading para que veas cómo filtra las entradas falsas en tiempo real.",
                "canonical_phrase": "La extensión no adivina el futuro: filtra las entradas basura para que operes con calma."
            },
            {
                "topic": "Tu Primer Trade de 5 USD en B2 Trading: Guía Paso a Paso para Principiantes",
                "d_score": 5, "c_score": 5, "r_score": 5, "e_score": 5, "s_score": 5,
                "pillar": "Onboarding B0 -> B1 -> B2",
                "thesis": "Desmistifica o primeiro trade na B2 Trading, provando que não é preciso ser expert nem ter milhares de dólares. 1 minuto, 92% payout e $5 de entrada.",
                "hook_suggestion": "Si nunca hiciste un trade en tu vida, esta pantalla te va a parecer un juego de niños comparada con las plataformas viejas. Solo 5 dólares, 1 minuto, y 92% fijo.",
                "canonical_phrase": "No necesitas entender 40 indicadores. Solo necesitas entender tu primer trade de 5 dólares."
            },
            {
                "topic": "Probé el Payout Fijo del 92% en B2 Trading Durante el Fin de Semana (OTC 24/7)",
                "d_score": 5, "c_score": 4, "r_score": 5, "e_score": 5, "s_score": 5,
                "pillar": "Mercado OTC 24/7 & Previsibilidade",
                "thesis": "Explica o que é OTC de forma simples e opera no domingo à noite com a extensão Filtro Signals ativa, mostrando que o payout não oscila para baixo.",
                "hook_suggestion": "¿Sabías que no tienes que esperar al lunes para operar? En B2 Trading el mercado OTC funciona sábado y domingo con exactamente el mismo 92% de payout.",
                "canonical_phrase": "Opera en tu horario y en tu idioma. Sin sorpresas de payout que baja al 60%."
            },
            {
                "topic": "Perdí 5 USD a Propósito en B2 Trading para Enseñarte Esta Regla de Oro",
                "d_score": 5, "c_score": 5, "r_score": 4, "e_score": 5, "s_score": 5,
                "pillar": "Gestão de Risco & Honestidade",
                "thesis": "Gera autoridade e confiança extrema mostrando uma operação perdedora ao vivo por ignorar o filtro da extensão, ensinando que a disciplina supera a pressa.",
                "hook_suggestion": "Voy a perder 5 dólares en vivo para que tú no los pierdas. Mira lo que pasa cuando tocas el botón sin esperar la confirmación de la extensión Filtro Signals.",
                "canonical_phrase": "Perder 5 dólares para aprender una lección es la universidad de trading más barata del mundo."
            },
            {
                "topic": "B2 Trading vs Otras Plataformas: Por Qué Dejé los Gráficos Llenos de Ruido",
                "d_score": 5, "c_score": 4, "r_score": 4, "e_score": 5, "s_score": 5,
                "pillar": "Diferenciação de Marca & Posicionamento",
                "thesis": "Compara a simplicidade do gráfico limpo da B2 Trading com plataformas antigas que intimidam o iniciante com 40 indicadores inúteis.",
                "hook_suggestion": "Las plataformas tradicionales fueron hechas para confundirte con 40 indicadores. B2 Trading se hizo para que entiendas en 1 minuto: sube o baja.",
                "canonical_phrase": "Sube o baja. Tú decides en 1 minuto. Sin complicaciones innecesarias."
            }
        ]
    }

    def evaluate_themes(self, channel_slug: str) -> Dict[str, Any]:
        ch = channel_slug.lower()
        if any(k in ch for k in ["cazador", "caza", "wins"]):
            candidates = self.THEME_CANDIDATE_BANK.get("el_cazador_del_wins", [])
        elif any(k in ch for k in ["miguel", "restrepo", "canal_02", "quant", "b2"]):
            candidates = self.THEME_CANDIDATE_BANK.get("miguel_trader", [])
        elif any(k in ch for k in ["profe", "vela"]):
            candidates = self.THEME_CANDIDATE_BANK.get("el_profe_de_velas", [])
        else:
            candidates = self.THEME_CANDIDATE_BANK.get(ch, [])

        evaluated_themes = []
        rejected_themes = []

        for item in candidates:
            topic = item["topic"]
            # 4-Layer Anti-Duplication Check via ChiefTradingMemory
            coverage = trading_memory.check_topic_coverage(ch, topic)
            
            if coverage["is_covered"]:
                rejected_themes.append({
                    "topic": topic,
                    "reason": coverage["reason"],
                    "verdict": coverage["verdict"],
                    "matched_theme": coverage.get("matched_theme")
                })
                continue

            d = item.get("d_score", 4)
            c = item.get("c_score", 4)
            r = item.get("r_score", 4)
            e = item.get("e_score", 4)
            s = item.get("s_score", 5)

            p_score = d * c * r * e  # Max: 625

            if p_score >= 400:
                priority = "P0 - PRODUÇÃO IMEDIATA"
            elif p_score >= 250:
                priority = "P1 - EM FILA"
            else:
                priority = "P2 - REAVALIAR"

            evaluated_themes.append({
                "topic": topic,
                "priority": priority,
                "p_score": p_score,
                "s_score": s,
                "scores": {"D": d, "C": c, "R": r, "E": e, "S": s},
                "pillar": item.get("pillar", "Geral"),
                "thesis": item.get("thesis", ""),
                "hook_suggestion": item.get("hook_suggestion", ""),
                "canonical_phrase": item.get("canonical_phrase", "Sin adivinar.")
            })

        # Sort evaluated by P-Score descending
        evaluated_themes.sort(key=lambda x: x["p_score"], reverse=True)

        return {
            "channel_slug": ch,
            "total_candidates_analyzed": len(candidates),
            "approved_virgin_themes": len(evaluated_themes),
            "rejected_duplicate_themes": len(rejected_themes),
            "top_themes": evaluated_themes,
            "duplicates_blocked": rejected_themes
        }

trading_theme_decider = TradingThemeDecider()
