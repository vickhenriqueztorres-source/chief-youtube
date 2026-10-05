# -*- coding: utf-8 -*-
"""
Hermes Chief Skill: multi-surface-discovery
Implements the Multi-Surface YouTube Discovery Framework:
Total Discovery = Search + Browse/Home + Suggested + Shorts + Playlists + External + Community + Collaboration

Generates integrated ecosystems for video topics, maps traffic sources to the 80/20 rule:
40% Search + 30% Browse/Home + 20% Shorts + 10% External.
"""

from typing import Dict, Any, List, Optional

class DiscoveryEngine:
    """Multi-Surface Discovery Engine for YouTube channels based on Chief & Eugene Schwartz principles."""

    SURFACES = {
        "busca": {
            "name": "Busca (Search)",
            "intent": "Espectador procurando resolver um problema ou tirar uma dúvida concreta.",
            "content_type": "Tutorial, resposta direta, passo a passo forense, dissecação de causa e efeito.",
            "packaging_rule": "Problema Reconhecido + Resultado Desejado + Mecanismo Específico no título, descrição inicial e primeiros 15 segundos.",
            "metric": "Visualizações por Busca & Termos de Pesquisa no YouTube Studio",
            "control_question": "As pessoas encontram exatamente a resposta técnica sem enrolação?"
        },
        "pagina_inicial": {
            "name": "Página Inicial (Browse / Home)",
            "intent": "Espectador navegando sem procurar nada específico. Precisa ser capturado por curiosidade, transformação ou tensão.",
            "content_type": "Experimentos, comparações extremas, transformações, desafios, paradoxos industriais e risco sistêmico.",
            "packaging_rule": "Vender uma IDEIA com contraste causal, não uma busca. Estrutura: 'Eu tentei [ação] para descobrir se [resultado]'.",
            "metric": "Impressões na Home & Taxa de Cliques (CTR)",
            "control_question": "A ideia gera curiosidade imediata mesmo em quem nunca ouviu falar do canal?"
        },
        "videos_sugeridos": {
            "name": "Vídeos Sugeridos (Suggested / Up Next)",
            "intent": "Espectador assistindo a outro vídeo e o YouTube recomenda o seu ao lado.",
            "content_type": "Continuação temática direta, estudo comparativo, aprofundamento ou contra-ponto.",
            "packaging_rule": "Construir vizinhança temática (clusters). Mesmo público, vocabulário idêntico, telas finais e playlists conectadas.",
            "metric": "Visualizações por Vídeos Sugeridos (Suggested Views)",
            "control_question": "O vídeo é a continuação inevitável do conteúdo que o espectador acabou de ver?"
        },
        "shorts": {
            "name": "Shorts (Feed Vertical)",
            "intent": "Consumo rápido em scroll contínuo. Alcance máximo, mas com alto risco de atrair público incompatível.",
            "content_type": "O Momento da Dor / O Paradoxo em 45 segundos. Três funções obrigatórias: Descoberta, Prova e Ponte para o Longo.",
            "packaging_rule": "1º seg: Resultado visual ou conflito imediato; seg 2-5: Promessa; Centro: Demonstração sem corte vazio; Fim: Conclusão + Botão de Vídeo Relacionado.",
            "metric": "Retenção (Viewed vs Swiped Away > 75%) e Inscritos Compatíveis",
            "control_question": "O Short atrai alguém que gostaria de assistir ao documentário longo de 12 minutos?"
        },
        "playlists": {
            "name": "Playlists (Percursos de Transformação)",
            "intent": "Espectador maratonando uma sequência lógica de aprendizagem ou investigação profunda.",
            "content_type": "Série numerada em ordem cronológica ou de complexidade crescente.",
            "packaging_rule": "Nomear pelo benefício/transformação final (ex: 'A Anatomia do Crime Invisível no Brasil'), nunca por pasta genérica.",
            "metric": "Visualizações por Espectador (Views per Viewer) & Retenção da Playlist",
            "control_question": "O término de um episódio força a curiosidade imediata para o próximo?"
        },
        "comunidade": {
            "name": "Aba Comunidade",
            "intent": "Espectador inscrito que já acompanha o canal e participa da rotina editorial.",
            "content_type": "Enquetes de validação de demanda, testes A/B de thumbnails antes do lançamento, bastidores e perguntas sobre dores reais.",
            "packaging_rule": "Descobrir demanda real antes de investir 40 horas na produção de um documentário.",
            "metric": "Votos nas Enquetes & Engajamento com Links de Vídeos Novos",
            "control_question": "A comunidade ajudou a validar se a promessa do tema tem tração antes do roteiro?"
        },
        "externo": {
            "name": "Distribuição Externa",
            "intent": "Pessoas em outras redes (Reddit, LinkedIn, TikTok, Discord, X, WhatsApp) recebendo valor na própria plataforma.",
            "content_type": "Posts forenses nativos que entregam o ouro no texto e oferecem o vídeo longo como aprofundamento definitivo.",
            "packaging_rule": "Nunca postar apenas 'Vídeo novo, clique aqui'. Adaptar a entrada: no LinkedIn o ganho sistêmico, no Reddit o experimento cru e técnico.",
            "metric": "Visualizações Externas com Retenção Qualificada (> 50% AVD)",
            "control_question": "A postagem externa agregou valor real antes de pedir o clique?"
        }
    }

    TARGET_8020_SPLIT = {
        "busca": 0.40,
        "pagina_inicial": 0.30,
        "shorts": 0.20,
        "externo": 0.10
    }

    # Curated archetypes per channel to generate cohesive multi-surface ecosystems
    CHANNEL_DESIRE_MAP = {
        "o_outro_lado": {
            "channel_name": "O Outro Lado",
            "target_audience": "Curiosos por infraestruturas físicas ocultas, tecnologia cotidiana e engenharia do submundo brasileiro.",
            "core_desire": "Entender como os sistemas invisíveis do país funcionam nos bastidores e se proteger de falhas sistêmicas.",
            "tone": "Forense, cinematográfico Denis Villeneuve, rigor técnico."
        },
        "hidden_systems_lab": {
            "channel_name": "Hidden Systems Lab",
            "target_audience": "Systems thinkers, senior backend/infra engineers and physical hardware enthusiasts worldwide.",
            "core_desire": "Master how extreme megastructures and industrial limits survive catastrophic pressure and millisecond tolerances.",
            "tone": "Ultra-precise, industrial, high-tension cold analytics."
        },
        "brecha": {
            "channel_name": "Brecha",
            "target_audience": "Brasileiros de 25 a 55 anos, usuários diários de bancos digitais e Pix que temem ser passados para trás.",
            "core_desire": "Proteger o patrimônio contra engenharia social de alta sofisticação e entender a mecânica exata dos golpes.",
            "tone": "Defesa cotidiana sóbria, sem histeria, autópsia forense do golpe."
        }
    }

    def generate_integrated_ecosystem(self, channel_slug: str, topic: str, thesis: Optional[str] = None) -> Dict[str, Any]:
        """
        Builds the complete 7-surface ecosystem around a single topic/core desire.
        Ensures that Search, Browse, Shorts, Playlists, Community and External work in harmony.
        """
        ch_slug = channel_slug.lower()
        ch_meta = self.CHANNEL_DESIRE_MAP.get(ch_slug, self.CHANNEL_DESIRE_MAP["o_outro_lado"])

        ecosystem = {
            "topic": topic,
            "channel": ch_meta["channel_name"],
            "core_desire": ch_meta["core_desire"],
            "target_audience": ch_meta["target_audience"],
            "ecosystem_pieces": {
                "1_long_for_search": {
                    "surface": "Busca (Intenção Existente)",
                    "title": self._craft_search_title(ch_slug, topic),
                    "objective": "Capturar o espectador que já pesquisa ativamente sobre o problema.",
                    "structure": "Problema Reconhecido + Resultado Desejado + Mecanismo Específico.",
                    "key_search_terms": [f"{topic.lower()}", "como funciona", "engenharia", "bastidores"],
                    "first_15s_rule": "Confirmar em 5 segundos a resposta do termo pesquisado antes de aprofundar na engenharia."
                },
                "2_long_for_browse": {
                    "surface": "Página Inicial / Home (Fórmula Matriz Micro vs Macro)",
                    "title": self._craft_browse_title(ch_slug, topic),
                    "objective": "Gerar clique visceral na amígdala/dopamina via contraste extremo Micro vs Macro (validado por Outlier Z=3.08).",
                    "structure": "Título Matriz = [Escala da Notícia Ruim / Ruína] + [Fração de Tempo Extrema / Unidade Mínima] + [Impacto Nacional / Geográfico].",
                    "thumbnail_concept": "Arquitetura 0,2s: Dark Mode 60-70% + Hero Object Único 4K + Texto Hipnótico de Choque (2-3 palavras em Amarelo Brutalista, zero repetição com título) + Medidor Digital [ 00:01s ] em Destaque Neon.",
                    "ab_testing_6h_protocol": {
                        "option_a": "Curiosidade Pura ('O Segundo Invisível / Exato Que...')",
                        "option_b": "Conflito Direto ('O Erro Que Desligou o Brasil')",
                        "option_c": "Pergunta Ameaçadora ('Por Que o Brasil Quase Parou?')",
                        "rule": "Monitorar CTR a cada 2h. Se CTR < 5.5% após 300 impressões, trocar imediatamente para Opção B."
                    }
                },
                "3_short_discovery": {
                    "surface": "Short 1: Efeito Ponte de Alta Retenção (Momento de Ruptura 45s)",
                    "title": f"O Segundo Exato em Que {topic[:35]} Quase Colapsou",
                    "objective": "Transferir tráfego frio do Shorts Feed diretamente para o tempo de exibição do Master Longo com salto de retenção precoce.",
                    "timing_breakdown": {
                        "0:00 - 0:02": "Colisão Mental: Resultado visual chocante ou falha física em close-up.",
                        "0:02 - 0:15": "Gancho Hipnótico sem saudação: Timestamp exato + Contraste Micro vs Macro.",
                        "0:15 - 0:38": "O Momento de Ruptura em progresso com números concretos e pausas táticas de 0.8s.",
                        "0:38 - 0:45": "Corte no Clímax Absoluto: 'Para entender o que os engenheiros descobriram no minuto seguinte, toque no vídeo relacionado aqui embaixo.'"
                    },
                    "related_video_link": "Apontar obrigatoriamente o botão 'Vídeo Relacionado' no YouTube Studio para o Documentário Master Longo."
                },
                "4_short_problem": {
                    "surface": "Short 2: O Mecanismo Invisível / A Peça de R$ 300",
                    "title": f"A Peça Invisível Que Pode Parar {topic[:30]}",
                    "objective": "Atrair a audiência qualificada explorando o ponto único de falha que a TV aberta nunca mostrou.",
                    "timing_breakdown": {
                        "0:00 - 0:03": "Demonstração da unidade mínima (1 byte, 3 mm, 0.4V) em falha.",
                        "0:03 - 0:15": "Por que a redundância tradicional falha nesse segundo exato.",
                        "0:15 - 0:40": "A evidência física forense da ruptura.",
                        "0:40 - 0:45": "Ponte direta para o documentário mestre via Vídeo Relacionado."
                    }
                },
                "5_playlist_architecture": {
                    "surface": "Loop de Sessão Fechado (Playlist de Retenção Infinita)",
                    "playlist_title": f"Dossiê do Colapso: Os Segundos Que Quase Pararam o Brasil",
                    "sequence_role": "Multiplicar a métrica 'Viewers Who Watched Another Video' (maior peso algorítmico de sugestão em 2026).",
                    "retention_mechanic": "NUNCA enviar para a Home do canal: usar Tela Final (End Screen) nos últimos 15s com 1 ÚNICO vídeo recomendado da mesma temática + parâmetro de playlist automática (&list=PL...) no link fixado dos comentários."
                },
                "6_community_post": {
                    "surface": "Aba Comunidade (Validação Prévia)",
                    "post_type": "Enquete de Decisão Causal",
                    "poll_question": f"Ao investigar os sistemas de {topic[:30]}, o que mais te surpreende?",
                    "poll_options": [
                        "Como uma fração de segundo ou milímetro anula uma infraestrutura bilionária",
                        "A vulnerabilidade silenciosa que abastece milhões de brasileiros",
                        "A física invisível por trás da válvula/cabo/relé",
                        "O protocolo de emergência nos primeiros 600 milissegundos"
                    ],
                    "timing": "Publicar 48 horas antes do vídeo master para aquecer a base ativa."
                },
                "7_external_distribution": {
                    "surface": "Seeding de Metadados Ocultos no SRT & Distribuição Externa",
                    "strategy": "Subir legenda manual (.srt) em texto puro rica em entidades técnicas para indexação semântica Google BERT / Gemini NLP (inserção na barra lateral de canais gigantes de notícias no mesmo dia).",
                    "copy_sample": (
                        f"Dissecamos o relatório forense sobre {topic}. A conclusão é contra-intuitiva: "
                        f"a vulnerabilidade não estava em uma tempestade ou ataque externo, mas em uma fração microscópica que ninguém vigiava. "
                        f"Documentamos a telemetria e o laudo completo."
                    ),
                    "cta": "Subir .srt enriquecido no YouTube Studio e fixar comentário com link da playlist (&list=PL...)."
                }
            },
            "distribution_rule_8020": {
                "busca": "40% do volume inicial de visualizações perenes (evergreen + Seeding SRT).",
                "recomendacao": "30% do pico de amostragem na Home/Sugeridos nas primeiras 72 horas (Fórmula Matriz + Loop de Sessão).",
                "shorts": "20% do volume de descoberta semente (Efeito Ponte 45s via Vídeo Relacionado).",
                "externo": "10% de tráfego semente qualificado de alto AVD."
            }
        }
        return ecosystem

    def _craft_search_title(self, ch_slug: str, topic: str) -> str:
        if ch_slug == "o_outro_lado":
            return f"{topic}: O Mecanismo Invisível Explicado Passo a Passo"
        elif ch_slug == "hidden_systems_lab":
            return f"How {topic} Actually Works: Extreme Engineering Behind the System"
        else:
            return f"Como Identificar o {topic}: O Guia Forense de Defesa Contra a Fraude"

    def _craft_browse_title(self, ch_slug: str, topic: str) -> str:
        if ch_slug == "o_outro_lado":
            if any(w in topic.lower() for w in ["segundo", "segundos", "milímetro", "minuto", "centímetro", "relê", "byte", "volts", "metros"]):
                return topic
            return f"O Segundo Invisível em Que {topic} Quase Parou o Brasil"
        elif ch_slug == "hidden_systems_lab":
            return f"The 400 Millisecond Shockwave That Could Collapse {topic}"
        else:
            return f"A Ligação Que Clonou {topic} em 3 Minutos: A Falha Que Ninguém Avisa"

    def evaluate_channel_discovery_balance(self, long_views: int, short_views: int, search_traffic_pct: float = 0.0) -> Dict[str, Any]:
        """
        Diagnoses if the channel has a healthy 4-surface balance or dangerous reliance on a single surface.
        """
        total_views = (long_views + short_views) or 1
        short_ratio = short_views / total_views
        
        warnings = []
        recommendations = []

        if short_ratio > 0.85:
            warnings.append("Dependência Crítica de Shorts (> 85% do tráfego). Risco severo de Audiência Fantasma.")
            recommendations.append("Ação Emergencial: Vincular obrigatoriamente os Shorts de alta tração aos vídeos longos no YouTube Studio.")
            recommendations.append("Redirecionar pautas para problemas com volume de Busca ativa para equilibrar a base.")

        if search_traffic_pct < 0.10 and long_views < 100:
            warnings.append("Ausência de Tráfego de Busca (< 10%). O canal depende 100% de o algoritmo 'adivinhar' a recomendação.")
            recommendations.append("Formatar os próximos 2 vídeos com foco estrito em Busca (Problema Reconhecido + Mecanismo).")

        return {
            "current_short_share": round(short_ratio * 100, 1),
            "target_8020_model": "40% Busca, 30% Recomendação/Home, 20% Shorts, 10% Externo",
            "is_balanced": len(warnings) == 0,
            "warnings": warnings,
            "strategic_actions": recommendations
        }

discovery_engine = DiscoveryEngine()
