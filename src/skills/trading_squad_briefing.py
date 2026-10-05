# -*- coding: utf-8 -*-
"""
Hermes Chief Trading Skill: trading-squad-briefing
Generates typed, production-ready strategic briefings for YouTube Trading video squads,
ensuring strict adherence to character lock, PiP ratios, voice parameters, and compliance gates.
"""

from typing import Dict, Any, Optional
from datetime import datetime
from src.core.trading_personality import TRADING_CHANNEL_CONFIGS
from src.core.trading_memory import trading_memory

class TradingSquadBriefingGenerator:
    """Emits typed production briefings for trading channel squads."""

    def generate_briefing(self, channel_slug: str, episode_id: str, topic_override: str = "") -> Dict[str, Any]:
        ch = channel_slug.lower()
        is_cazador = any(k in ch for k in ["cazador", "caza", "wins"])
        is_miguel = any(k in ch for k in ["miguel", "restrepo", "b2"])
        
        if is_cazador:
            config = TRADING_CHANNEL_CONFIGS.get("el_cazador_del_wins", TRADING_CHANNEL_CONFIGS.get(ch, {}))
            default_topic = "Cacé el Bot de $997 de Telegram por 14 Días (Aquí Escapó) | La Cacería"
        elif is_miguel:
            config = TRADING_CHANNEL_CONFIGS.get("canal_02_trading", TRADING_CHANNEL_CONFIGS.get(ch, {}))
            default_topic = "Instalé la Extensión Filtro Signals en B2 Trading: 10 Entradas de 1 Minuto"
        else:
            config = TRADING_CHANNEL_CONFIGS.get("el_profe_de_velas", TRADING_CHANNEL_CONFIGS.get(ch, {}))
            default_topic = "La Trampa del Martillo: Por Qué Esta Mecha Te Hace Perder en Soporte"

        topic = topic_override if topic_override else default_topic
        
        # Check topic coverage in memory
        coverage = trading_memory.check_topic_coverage(ch, topic)
        if coverage["is_covered"]:
            status_note = f"ATENÇÃO // TEMA COM SOBREPOSIÇÃO: {coverage['verdict']}"
        else:
            status_note = "SINAL VERDE // TEMA VIRGEM CONFIRMADO PELA MEMÓRIA"
            trading_memory.register_covered_theme(
                channel=ch,
                core_topic=topic,
                title_reference=topic,
                status="IN_PRODUCTION",
                format="long",
                angle_covered=f"Briefing emitido para o squad sob ID {episode_id}"
            )
            
        # Packaging and Character defaults
        if is_cazador:
            titles = [
                topic,
                "Te vendieron este bot como infalible: lo pusimos en la trampa 14 días",
                "¿Funciona o escapa? Cazamos el bot más caro de Telegram en cuenta demo",
                "El error oculto de martingala que quema la cuenta en el día 9"
            ]
            comp_style = "Dark Mode Charcoal (#0A0B0E). Fundo com registro de caça e dados reais em JetBrains Mono."
            focal_el = "Capuz na sombra à direita (#D8F200 no recorte), mira reticular fina com robô quebrado e -34% circulado a vermelho."
            txt_overlay = "14 DÍAS -34%"
            forbid_thumb = "Rosto iluminado, robô brilhante estilo Jarvis, cifrões, saldo verde, setas genéricas, promessas de lucro."
            char_ref = "Ficha Canônica do Cazador (Homem, ombros largos, moletom preto com capuz levantado na sombra)."
            char_look = "Moletom preto com capuz levantado na sombra + iluminação de recorte amarelo-ácido (#D8F200)."
            pip_rules = "PiP de 15% no hook (0:00-0:20) e no veredito final. NUNCA cobrindo os dados do registro."
            full_rules = "Proibido tela cheia do avatar. O Cazador atua na sombra e no PiP controlado."
            v_name = "Eric / Voz Cazador"
            v_id = config.get("voice", {}).get("voice_id", "cjVigY5qzO86Huf0OWal")
            cadence = 148
            structure_acts = [
                {
                    "act": "Ato 1: La Carnada (0:00 - 1:15)",
                    "visual": "Hook com a promessa do bot de $997 e o momento em que ele falha em demo.",
                    "dialogue_direction": "Tom frio, controlado. 'Te dijeron que este bot nunca pierde. Lo pusimos en la trampa. Mira dónde escapó.'"
                },
                {
                    "act": "Ato 2: La Trampa (1:15 - 4:00)",
                    "visual": "Condições de teste no Deriv DBot e replay com registro estrito.",
                    "dialogue_direction": "Walkthrough calmo sem adjetivos vazios. Expor as regras de entrada e gestão de risco do bot."
                },
                {
                    "act": "Ato 3: La Cacería en Demo (4:00 - 8:30)",
                    "visual": "Execução contínua demonstrando onde a volatilidade atropelou a regra.",
                    "dialogue_direction": "Registrar cada vitória e cada perda com a mesma neutralidade. 'El bot no piensa. El mercado tampoco.'"
                },
                {
                    "act": "Ato 4: Por Dentro / El Escape (8:30 - 10:45)",
                    "visual": "Análise forense da quebra e drawdown real de -34% no dia 9.",
                    "dialogue_direction": "Baixar o tom. Destacar o multiplicador de martingala oculto. 'Aquí fue donde la promesa se rompió.'"
                },
                {
                    "act": "Ato 5: El Trofeo (10:45 - 12:30)",
                    "visual": "Registro de caça consolidado com selo ESCAPÓ e aviso educacional.",
                    "dialogue_direction": "Apresentar a tabela final em JetBrains Mono. Transparência matemática total."
                },
                {
                    "act": "Ato 6: Veredito & CTA (12:30 - 13:30)",
                    "visual": "Conclusão na sombra e convite para testar o template em demo no Telegram.",
                    "dialogue_direction": "'Antes de arriesgar, entiende. Antes de creer, comprueba. No importa quién soy. Importa lo que atrapo.'"
                }
            ]
        else:
            titles = [
                topic,
                f"¿Por Qué Falla el Martillo? Mira Esto Antes del Clic | {config.get('name')}",
                "El Error con Esta Vela Que Engaña a los Principiantes (Sin Adivinar)",
                "No Entres en Esta Mecha: Aprende a Leer la Trampa en Demo"
            ]
            comp_style = "Dark Mode (#080A0F). Fundo com gráfico limpo da Deriv/IQ Option em conta demo."
            focal_el = "Zoom macro extremo em 1 vela martelo falsa rompendo suporte, com a mecha destacada em Amarelo Ácido (#FFE500)."
            txt_overlay = "¿REBOTE O TRAMPA?"
            forbid_thumb = "Gurus sorrindo, carrões, pilhas de dinheiro, setas verdes gigantes, promessas de ganho."
            char_ref = "Ficha Forense Canônica v1.0 (Homem 34-38 anos, pele morena clara quente, sem grisalho, barba curta 3-6mm)."
            char_look = "Look A (Bomber canelado azul-marinho + camiseta preta + relógio discreto no pulso esquerdo)."
            pip_rules = "Avatar em PiP no canto inferior ocupando 20% a 25% da tela apontando para o gráfico."
            full_rules = "Avatar em tela cheia EXCLUSIVAMENTE nos primeiros 3-5 segundos e encerramento (5-8s)."
            v_name = config.get("voice", {}).get("name", "Eric")
            v_id = config.get("voice", {}).get("voice_id", "cjVigY5qzO86Huf0OWal")
            cadence = config.get("voice", {}).get("cadence_wpm", 140)
            structure_acts = [
                {
                    "act": "Ato 1: O Gancho do Erro (0:00 - 1:15)",
                    "visual": "Tela cheia inicial (3s) migrando para PiP sobre IQ Option/Deriv em conta demo.",
                    "dialogue_direction": "Tom direto e protetor. 'Mira acá... te dijeron que esta mecha es compra garantizada. Te engañaron.'"
                },
                {
                    "act": "Ato 2: A Anatomia da Vela (1:15 - 3:30)",
                    "visual": "Zoom óptico suave no corpo e na mecha sem adivinhação.",
                    "dialogue_direction": "Didático e calmo. Desacelerar ao explicar rejeição e fechamento."
                },
                {
                    "act": "Ato 3: O Walkthrough Forense (3:30 - 7:00)",
                    "visual": "Execução demonstrativa em conta prática com taxa de payout visível.",
                    "dialogue_direction": "Passo a passo com tela limpa. 'Sin adivinar, comprobamos el contexto.'"
                },
                {
                    "act": "Ato 4: Onde o Principiante Quebra (7:00 - 9:15)",
                    "visual": "Comparativo lado a lado de rompimento falso vs confirmação.",
                    "dialogue_direction": "Expor o erro comum sem humilhação. Reconstruir a regra correta."
                },
                {
                    "act": "Ato 5: A Regra de Bolso del Profe (9:15 - 10:45)",
                    "visual": "Checklist gráfico com selo Sin Adivinar.",
                    "dialogue_direction": "Resumo objetivo salvável em PDF para os alunos no Telegram."
                },
                {
                    "act": "Ato 6: Fechamento & Desafio Demo (10:45 - 11:30)",
                    "visual": "Avatar em tela cheia com disclaimer e CTA para Telegram.",
                    "dialogue_direction": "'Pruébalo primero en demo. Si te trabas, el Profe te espera en Telegram.'"
                }
            ]

        briefing = {
            "metadata": {
                "briefing_id": f"BRIEF-{ch.upper()}-{episode_id}",
                "channel_slug": ch,
                "channel_name": config.get("name", "El Cazador del Wins" if is_cazador else "El Profe de Velas"),
                "handle": config.get("handle", "@elcazadordelwins" if is_cazador else "@ElProfdelLasVelas"),
                "canonical_handle": config.get("canonical_handle", "@elcazadordelwins" if is_cazador else "@profedevelas"),
                "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "target_format": "Vídeo Longo YouTube (8 a 14 minutos) + Shorts de Recorte",
                "coverage_status": status_note
            },
            "packaging_direction": {
                "canonical_title": titles[0],
                "alternative_titles": titles[1:],
                "thumbnail_specification": {
                    "composition": comp_style,
                    "focal_element": focal_el,
                    "text_overlay": txt_overlay,
                    "max_words": 3,
                    "forbidden_elements": forbid_thumb
                }
            },
            "voice_and_audio": {
                "voice_name": v_name,
                "voice_id": v_id,
                "cadence_wpm": cadence,
                "tone": config.get("voice", {}).get("tone", "Masculina, grave, fria e controlada."),
                "background_music": "Sutil, minimalista, estilo vigilância/lo-fi técnico (-24 dB)."
            },
            "character_lock_and_pip": {
                "reference": char_ref,
                "look": char_look,
                "pip_specs": pip_rules,
                "fullscreen_rules": full_rules
            },
            "narrative_structure_6_acts": structure_acts,
            "compliance_and_ypp_gates": {
                "checkbox_synthetic_media": "OBRIGATÓRIO: Marcar 'Sim' para conteúdo alterado/sintético no YouTube Studio.",
                "demo_account_visibility": "OBRIGATÓRIO: Indicador de 'PRACTICE / DEMO' 100% visível na tela e citado na narração.",
                "financial_disclaimers": "INVIOLÁVEL: Simulação estritamente educacional. Proibido prometer ganhos seguros ou infalíveis.",
                "forbidden_terms": config.get("forbidden_language", ["ganancia segura", "estafa", "100%"])
            }
        }

        return briefing

trading_squad_briefing_gen = TradingSquadBriefingGenerator()
