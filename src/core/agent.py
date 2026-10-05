# -*- coding: utf-8 -*-
"""
Hermes Chief - Central Agent Brain
Orchestrates skills, FTS5 memory, personality, and strategic decision loops.
"""

import json
from pathlib import Path
from typing import Dict, Any, List, Optional

from src.core.memory import ChiefMemory, memory
from src.core.personality import CHIEF_SYSTEM_PROMPT, CHANNEL_CONFIGS
from src.skills.metrics_reader import ChannelMetricsReader, metrics_reader
from src.skills.diagnostic import ChannelDiagnostic, channel_diagnostic
from src.skills.thumb_audit import ThumbnailAuditor, thumbnail_auditor
from src.skills.theme_decider import ThemeDecider, theme_decider
from src.skills.squad_briefing import SquadBriefingGenerator, squad_briefing_gen
from src.skills.channel_sync import ChannelDataSynchronizer, channel_synchronizer
from src.skills.live_crawler import LiveChannelCrawler, live_channel_crawler
from src.skills.discovery_engine import DiscoveryEngine, discovery_engine
from src.skills.voice_miner import VoiceOfCustomerMiner, voice_miner
from src.skills.niche_researcher import NicheResearcher, niche_researcher
from src.skills.channel_reverse_engineer import ChannelReverseEngineer, channel_reverse_engineer

class ChiefAnalystAgent:
    """The Autonomous Chief Analyst Agent for YouTube Documentary Channels."""

    def __init__(self, memory_instance: Optional[ChiefMemory] = None):
        self.memory = memory_instance or memory
        self.metrics_reader = metrics_reader
        self.diagnostic = channel_diagnostic
        self.auditor = thumbnail_auditor
        self.theme_decider = theme_decider
        self.briefing_gen = squad_briefing_gen
        self.synchronizer = channel_synchronizer
        self.live_crawler = live_channel_crawler
        self.discovery = discovery_engine
        self.voice_miner = voice_miner
        self.niche_researcher = niche_researcher
        self.channel_reverse_engineer = channel_reverse_engineer
        self.configs = CHANNEL_CONFIGS
        self.base_data_dir = Path(__file__).resolve().parent.parent.parent / "data" / "channels"

    def get_channel_data(self, channel_slug: str) -> Dict[str, Any]:
        slug = channel_slug.lower()
        if "outro" in slug:
            p = self.base_data_dir / "outro_lado_baseline.json"
        elif "hsl" in slug or "hidden" in slug:
            p = self.base_data_dir / "hsl_baseline.json"
        elif "brecha" in slug:
            p = self.base_data_dir / "brecha_baseline.json"
        else:
            p = self.base_data_dir / f"{slug}_baseline.json"

        if p.exists():
            return self.metrics_reader.load_from_json(p)
        raise FileNotFoundError(f"Dados do canal '{channel_slug}' não encontrados em {p}")

    def sync_channel(self, channel_slug: str, csv_path: Optional[str] = None) -> Dict[str, Any]:
        """Sincroniza dados em tempo real do YouTube para o canal especificado."""
        return self.synchronizer.sync_channel(channel_slug, csv_path=csv_path)

    def sync_all(self, csv_dir: Optional[str] = None) -> Dict[str, Any]:
        """Sincroniza dados em tempo real de todos os 3 canais gerenciados."""
        return self.synchronizer.sync_all(csv_dir=csv_dir)

    def run_live_intelligence(self, channel_slug: str) -> Dict[str, Any]:
        """
        Executa a análise quantitativa ao vivo no YouTube:
        1. Varre metadados, inscritos e todos os vídeos (longos e shorts).
        2. Computa velocidade, outliers Z-score, clusters e gargalos.
        3. Grava automaticamente os aprendizados na memória SQLite FTS5.
        4. Avalia as pautas P0 calibradas com base nos dados reais de hoje.
        """
        live_res = self.live_crawler.analyze_live_channel(channel_slug)
        memory_records = self.memory.auto_ingest_live_patterns(channel_slug, live_res)
        themes_res = self.theme_decider.evaluate_themes(channel_slug)

        return {
            "status": "LIVE_INTELLIGENCE_READY",
            "channel_slug": live_res["channel_slug"],
            "channel_name": live_res["channel_name"],
            "handle": live_res["handle"],
            "live_subscribers": live_res["live_subscribers"],
            "total_videos_analyzed": live_res["total_videos_analyzed"],
            "total_catalog_views": live_res["total_catalog_views"],
            "long_videos_stats": live_res["long_videos"],
            "shorts_stats": live_res["shorts_videos"],
            "shorts_to_long_ratio": live_res["shorts_to_long_ratio"],
            "keyword_clusters": live_res["keyword_clusters"],
            "bridge_opportunities": live_res["bridge_opportunities"],
            "primary_bottleneck": live_res["primary_bottleneck"],
            "top_p0_themes": themes_res.get("top_3_selected", themes_res.get("top_themes", []))[:3],
            "memory_patterns_ingested": memory_records,
            "timestamp": live_res["analyzed_at"]
        }

    def run_live_intelligence_all(self) -> Dict[str, Any]:
        """Executa a análise quantitativa ao vivo para todos os 3 canais gerenciados."""
        results = {}
        for slug in ["o_outro_lado", "hidden_systems_lab", "brecha"]:
            results[slug] = self.run_live_intelligence(slug)
        return results

    def audit_channel(self, channel_slug: str) -> Dict[str, Any]:
        """Runs end-to-end audit for a channel: metrics -> diagnosis -> top themes -> memory update."""
        raw_data = self.get_channel_data(channel_slug)
        metrics_summary = self.metrics_reader.analyze_channel(raw_data)
        diag_result = self.diagnostic.diagnose(channel_slug, metrics_summary)
        themes_result = self.theme_decider.evaluate_themes(channel_slug)

        # Record insight in FTS5 memory automatically
        bottleneck_name = diag_result["primary_bottleneck"]["name"]
        self.memory.record_learning(
            channel=channel_slug,
            category="diagnostic",
            insight=f"Gargalo primário detectado: {bottleneck_name}",
            evidence=f"Views médias: {metrics_summary.get('long_form_summary', {}).get('mean_views')} | Trend: {metrics_summary.get('long_form_summary', {}).get('trend')}",
            action_taken=diag_result["proposed_experiment"]["hypothesis"][:120] + "..."
        )

        return {
            "channel_slug": channel_slug,
            "channel_info": self.configs.get(channel_slug, {}),
            "metrics": metrics_summary,
            "diagnosis": diag_result,
            "top_themes": themes_result["top_3_selected"],
            "status": "AUDIT_COMPLETED"
        }

    def audit_thumbnail(self, channel_slug: str, title: str, thumb_description: str, thumb_text: str = "") -> Dict[str, Any]:
        res = self.auditor.audit(channel_slug, title, thumb_description, thumb_text)
        
        # Log in memory
        self.memory.record_learning(
            channel=channel_slug,
            category="thumbnail_audit",
            insight=f"Título: {title} | Veredito: {res['recommendation']} (Score {res['scores']['overall_index']})",
            evidence=thumb_description,
            action_taken="; ".join(res["actionable_tweaks"])
        )
        return res

    def decide_themes(self, channel_slug: str, custom_ideas: Optional[List[Dict[str, Any]]] = None) -> Dict[str, Any]:
        return self.theme_decider.evaluate_themes(channel_slug, custom_ideas)

    def check_topic_coverage(self, channel_slug: str, topic: str, thesis: str = "") -> Dict[str, Any]:
        """Verifica se um tema já foi coberto, publicado ou se está em produção no canal."""
        return self.memory.check_theme_coverage(channel_slug, topic, thesis)

    def list_covered_themes(self, channel_slug: Optional[str] = None, status: Optional[str] = None) -> List[Dict[str, Any]]:
        """Lista todos os temas cobertos e o status atual de cada um no catálogo."""
        return self.memory.list_covered_themes(channel_slug, status)

    def sync_covered_themes(self) -> Dict[str, int]:
        """Sincroniza todos os vídeos dos baselines e crawler para o registro de temas cobertos."""
        return self.memory.sync_all_baselines_to_covered_themes()

    def generate_briefing(self, channel_slug: str, episode_id: str, custom_params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        briefing = self.briefing_gen.generate_briefing(channel_slug, episode_id, custom_params)
        
        # Record in memory
        self.memory.record_learning(
            channel=channel_slug,
            category="squad_briefing",
            insight=f"Briefing emitido para {episode_id}: {briefing['tema']}",
            evidence=f"Meta: {briefing['metrica_alvo']} | Prazo: {briefing['prazo_entrega']}",
            action_taken=f"Salvo em {briefing['saved_path']}"
        )
        return briefing

    def plan_discovery_ecosystem(self, channel_slug: str, topic: Optional[str] = None) -> Dict[str, Any]:
        """Projeta o ecossistema integrado de 7 peças de descoberta multi-frente para um tema."""
        ch = channel_slug.lower()
        if not topic:
            top_themes = self.decide_themes(ch).get("top_3_selected", [])
            topic = top_themes[0]["topic"] if top_themes else "Engenharia de Sistemas Críticos"

        ecosystem = self.discovery.generate_integrated_ecosystem(ch, topic)

        # Record in FTS5 memory
        self.memory.record_learning(
            channel=ch,
            category="DISCOVERY_ECOSYSTEM",
            insight=f"Ecossistema multi-frente projetado para '{topic}'. 7 peças coordenadas no modelo 80/20.",
            evidence=f"Busca: '{ecosystem['ecosystem_pieces']['1_long_for_search']['title']}' | Home: '{ecosystem['ecosystem_pieces']['2_long_for_browse']['title']}'",
            action_taken=f"Executar divisão 40% busca, 30% recomendação, 20% shorts, 10% externo."
        )
        return ecosystem

    def research_spontaneous_language(self, channel_slug: str, topic: Optional[str] = None) -> Dict[str, Any]:
        """
        Executa a mineração de linguagem espontânea (Eugene Schwartz Passo 2):
        1. Captura buscas reais no auto-complete do YouTube.
        2. Analisa comentários de vídeos concorrentes extraindo frases literais, dúvidas e mitos.
        3. Registra os achados na memória SQLite FTS5 (categoria: VOICE_OF_CUSTOMER).
        """
        ch = channel_slug.lower()
        if not topic:
            top_themes = self.decide_themes(ch).get("top_3_selected", [])
            topic = top_themes[0]["topic"] if top_themes else "Golpe do Pix"

        res = self.voice_miner.synthesize_customer_language(ch, topic)
        voc = res["voice_of_customer"]

        # Record in FTS5 memory
        evidence_str = f"Vídeos analisados: {len(res['competitor_videos_analyzed'])} | Comentários minerados: {res['total_real_comments_parsed']}"
        action_str = f"Ancorar o gancho de 0-15s na citação: {voc['visceral_quotes_for_hook'][0][:80]}"
        self.memory.record_learning(
            channel=ch,
            category="VOICE_OF_CUSTOMER",
            insight=f"Linguagem espontânea minerada para '{topic}'. Citação mestre: '{voc['visceral_quotes_for_hook'][0]}'",
            evidence=evidence_str,
            action_taken=action_str
        )
        return res

    def research_niches(
        self,
        region: str = "BR+US",
        territory_filter: Optional[str] = None,
        custom_seeds: Optional[List[Dict[str, Any]]] = None
    ) -> Dict[str, Any]:
        """
        Executa pesquisa de nichos para canais faceless no YouTube:
        1. Cruza demanda (Google Trends 12m + YouTube Data API) com viabilidade de monetização.
        2. Bloqueia territórios que violam políticas de reused content, inauthentic content e direitos autorais.
        3. Avalia requisitos YPP 2026 e alerta de fev/2027.
        4. Registra os aprendizados na memória SQLite FTS5 (categoria: NICHE_RESEARCH).
        """
        res = self.niche_researcher.research_niches(
            region=region,
            territory_filter=territory_filter,
            custom_seeds=custom_seeds
        )
        ranked = res.get("output", {}).get("ranked_niches", [])
        top_niche = ranked[0] if ranked else {}
        top_name = top_niche.get("niche", "N/A")
        top_score = top_niche.get("score", 0)
        top_rpm = top_niche.get("estimated_rpm_usd", 0.0)

        # Record in FTS5 memory
        self.memory.record_learning(
            channel="global",
            category="NICHE_RESEARCH",
            insight=f"Nicho #1 Recomendado: '{top_name}' (Score {top_score}/100 | RPM ~${top_rpm:.2f} USD). Formato: {top_niche.get('format_recommended')}.",
            evidence=f"Trends 12m: +{top_niche.get('trend_growth_12m_pct')}% | Outliers: {top_niche.get('outlier_intensity')}. Aprovado no Gate YPP 2026/2027.",
            action_taken=f"Pautas de entrada sugeridas: '{'; '.join(top_niche.get('entry_video_titles', [])[:2])}'"
        )
        return res

    def reverse_engineer_channels(
        self,
        region_focus: str = "BR+GLOBAL",
        discovery_method: str = "all",
        custom_channels: Optional[List[Dict[str, Any]]] = None
    ) -> Dict[str, Any]:
        """
        Executa engenharia reversa de canais YouTube no Brasil e no mundo via múltiplos métodos:
        (Velocity Breakout, Supply Vacuum, Suggested Hijack, Cross-Language Arbitrage, Mechanism-Specific).
        1. Analisa canais faceless em hiper-crescimento (+50k/100k subs em 90d, CPM > $5).
        2. Elimina ativamente o 'Generic Trap' (nichos saturados com atrito algorítmico).
        3. Formula as recomendações dos 2 novos canais (BR + Global) em oceanos azuis.
        4. Registra os padrões na memória SQLite FTS5 (categoria: REVERSE_ENGINEER).
        """
        res = self.channel_reverse_engineer.reverse_engineer(
            region_focus=region_focus,
            discovery_method=discovery_method,
            custom_channels=custom_channels
        )
        recs = res.get("output", {}).get("recommendations", {})
        br_rec = recs.get("brazil_channel", {})
        glob_rec = recs.get("global_channel", {})

        # Record in FTS5 memory
        self.memory.record_learning(
            channel="global",
            category="REVERSE_ENGINEER",
            insight=f"Modelagem Multi-Método ({discovery_method}): [BR] '{br_rec.get('niche')}' (CPM ~${br_rec.get('estimated_cpm_usd')}) | [GLOBAL] '{glob_rec.get('niche')}' (CPM ~${glob_rec.get('estimated_cpm_usd')}).",
            evidence=f"Oceanos azuis validados contra Generic Trap. Ganchos imediatos < 12s. 100% YPP safe.",
            action_taken=f"Produzir vídeos iniciais focados no mecanismo específico causal."
        )
        return res

    def generate_reverse_engineer_html(self, discovery_method: str = "all", output_path: Optional[str] = None) -> str:
        """Gera o dashboard visual em HTML com a engenharia reversa multi-método de canais BR e globais."""
        res = self.reverse_engineer_channels(discovery_method=discovery_method)
        return self.channel_reverse_engineer.generate_html_report(res, output_path)

    def search_memory(self, query: str, channel: Optional[str] = None, limit: int = 10) -> List[Dict[str, Any]]:
        return self.memory.search(query, channel, limit)

    def generate_full_executive_summary(self) -> Dict[str, Any]:
        """Generates cross-channel comparative status report."""
        channels = ["o_outro_lado", "hidden_systems_lab", "brecha"]
        audits = {}
        for c in channels:
            try:
                audits[c] = self.audit_channel(c)
            except Exception as e:
                audits[c] = {"error": str(e)}

        active_experiments = self.memory.get_active_experiments()
        recent_learnings = self.memory.get_recent_learnings(limit=10)

        return {
            "title": "DOSSIÊ EXECUTIVO DE INTELIGÊNCIA // 3 CANAIS DOCUMENTAIS",
            "channels_audited": audits,
            "active_experiments_count": len(active_experiments),
            "active_experiments": active_experiments,
            "recent_memory_learnings": recent_learnings
        }

    def answer_query(self, user_msg: str) -> str:
        """Lightweight analytical conversational response in Chief personality."""
        msg_lower = user_msg.lower()

        # Route to specific functions if matching keywords
        if "outro lado" in msg_lower and ("auditoria" in msg_lower or "diagnostico" in msg_lower or "analise" in msg_lower):
            audit = self.audit_channel("o_outro_lado")
            p_bot = audit["diagnosis"]["primary_bottleneck"]
            return (
                f"🛰️ [CHIEF DIAGNÓSTICO // O OUTRO LADO]\n"
                f"• Gargalo Primário: {p_bot['name']}\n"
                f"• Causa: {p_bot['root_cause']}\n"
                f"• Média Views Longo: {audit['metrics']['long_form_summary']['mean_views']} | Média Shorts: {audit['metrics']['shorts_summary']['mean_views']}\n"
                f"• Hipótese de Resgate: {audit['diagnosis']['proposed_experiment']['hypothesis']}\n"
                f"• Próximo Tema P0: {audit['top_themes'][0]['topic']} (P={audit['top_themes'][0]['p_score']})\n"
                f"• Decisão: Pare de postar 1 longo por dia. Reduza para 2/sem e conecte o Short de Santos (1.4k) ao master correspondente."
            )

        elif ("hsl" in msg_lower or "hidden" in msg_lower) and ("auditoria" in msg_lower or "diagnostico" in msg_lower or "analise" in msg_lower):
            audit = self.audit_channel("hidden_systems_lab")
            p_bot = audit["diagnosis"]["primary_bottleneck"]
            return (
                f"⚡ [CHIEF DIAGNÓSTICO // HIDDEN SYSTEMS LAB]\n"
                f"• Gargalo Primário: {p_bot['name']}\n"
                f"• Anomalia Crítica: Uploads duplicados (Airport Fuel e Skyscrapers) causaram canibalização algorítmica.\n"
                f"• Shorts com 0 Views: Falha de embalagem. Títulos com apenas hashtags foram rejeitados no feed.\n"
                f"• Fórmula Validada: Títulos de paradoxo absoluto (Blast Furnace - 566 views / Jet Fuel - 680 views).\n"
                f"• Próximo Tema P0: {audit['top_themes'][0]['topic']} (P={audit['top_themes'][0]['p_score']})\n"
                f"• Decisão: Deletar duplicatas e renomear os Shorts de hashtags com ganchos de paradoxo em inglês."
            )

        elif "brecha" in msg_lower and ("auditoria" in msg_lower or "diagnostico" in msg_lower or "analise" in msg_lower):
            audit = self.audit_channel("brecha")
            p_bot = audit["diagnosis"]["primary_bottleneck"]
            return (
                f"🛡️ [CHIEF DIAGNÓSTICO // CANAL BRECHA]\n"
                f"• Gargalo Primário: {p_bot['name']}\n"
                f"• Diagnóstico do Paradoxo: 1.120 inscritos inativos ignoram o vídeo longo (CTR < 0.5% nos inscritos).\n"
                f"• Potencial: Canal com maior dor visceral no Brasil (R$ 2.5B em golpes Pix). Short de IA bateu 590 views.\n"
                f"• Erro de Embalagem: Títulos em ALL CAPS excessivo afastam o tom documental sóbrio.\n"
                f"• Próximo Tema P0: {audit['top_themes'][0]['topic']} (P={audit['top_themes'][0]['p_score']})\n"
                f"• Decisão: Higienizar títulos (retirar ALL CAPS) e focar em termos de busca de golpes ativos."
            )

        elif "descoberta" in msg_lower or "ecossistema" in msg_lower or "80/20" in msg_lower:
            ch = "o_outro_lado"
            if "hsl" in msg_lower or "hidden" in msg_lower: ch = "hidden_systems_lab"
            elif "brecha" in msg_lower: ch = "brecha"
            eco = self.plan_discovery_ecosystem(ch)
            p = eco["ecosystem_pieces"]
            return (
                f"🌐 [CHIEF // SISTEMA DE DESCOBERTA MULTI-FRENTE - {eco['channel'].upper()}]\n"
                f"Tema Alvo: {eco['topic']}\n"
                f"Desejo Central: {eco['core_desire']}\n"
                f"--------------------------------------------------\n"
                f"1. Busca: '{p['1_long_for_search']['title']}'\n"
                f"2. Home/Recomendação: '{p['2_long_for_browse']['title']}'\n"
                f"3. Short 1 (Descoberta): '{p['3_short_discovery']['title']}' (Vídeo Relacionado ➔ Longo)\n"
                f"4. Short 2 (Problema/Falha): '{p['4_short_problem']['title']}'\n"
                f"5. Playlist: '{p['5_playlist_architecture']['playlist_title']}'\n"
                f"6. Comunidade: Enquete de validação 48h antes ('{p['6_community_post']['poll_question']}')\n"
                f"7. Externo: Reddit/LinkedIn com copy técnica forense.\n"
                f"--------------------------------------------------\n"
                f"📊 Regra 80/20: 40% Busca | 30% Recomendação | 20% Shorts | 10% Externo."
            )

        elif "voz" in msg_lower or "linguagem" in msg_lower or "comentario" in msg_lower or "reclamac" in msg_lower:
            ch = "o_outro_lado"
            if "hsl" in msg_lower or "hidden" in msg_lower: ch = "hidden_systems_lab"
            elif "brecha" in msg_lower: ch = "brecha"
            voc_res = self.research_spontaneous_language(ch)
            voc = voc_res["voice_of_customer"]
            quotes = "\n".join([f"  • {q}" for q in voc["visceral_quotes_for_hook"][:3]])
            doubts = "\n".join([f"  • {d}" for d in voc["unresolved_competitor_doubts"][:2]])
            return (
                f"🗣️ [CHIEF // VOZ DO CLIENTE & LINGUAGEM ESPONTÂNEA - {ch.upper()}]\n"
                f"Tema: {voc_res['topic']}\n"
                f"Vídeos de Concorrentes Escaneados: {len(voc_res['competitor_videos_analyzed'])}\n"
                f"--------------------------------------------------\n"
                f"🔥 CITAÇÕES VISCERAIS (Para Gancho 0-15s):\n{quotes}\n"
                f"❓ DÚVIDAS NÃO RESPONDIDAS NOS CONCORRENTES:\n{doubts}\n"
                f"--------------------------------------------------\n"
                f"💡 Recomendação de Roteiro: {voc_res['script_anchors']['hook_0_15s_recommendation']}"
            )

        elif any(k in msg_lower for k in [
            "pesquisa de nicho", "pesquisa de nichos", "quais canais criar",
            "nichos monetizaveis", "encontrar nichos", "analise de demanda", "niche research"
        ]):
            niche_res = self.research_niches()
            output = niche_res.get("output", {})
            ranked = output.get("ranked_niches", [])
            top_briefing = output.get("top_niche_briefing", {})
            blocked = output.get("blocked_niches_audit", [])

            wants_html = "html" in msg_lower or "pagina" in msg_lower or "painel" in msg_lower or "dashboard" in msg_lower
            html_path_str = ""
            if wants_html:
                html_file = self.niche_researcher.generate_html_report(niche_res)
                html_url = html_file.replace('\\', '/')
                html_path_str = f"🌐 RELATÓRIO HTML INTERATIVO GERADO:\n📄 Arquivo: {html_file}\n🔗 Link: file:///{html_url}\n\n"

            lines = [
                f"{html_path_str}📊 [PESQUISA DE NICHOS // GATE DE MONETIZAÇÃO YPP]:",
                "Fórmula: Score = 25% Trends + 30% Outliers + 25% RPM + 20% Formato\n",
                "🏆 TOP 5 NICHOS APROVADOS (100% Monetização Segura):"
            ]
            for n in ranked[:5]:
                lines.append(f"#{n['rank']} {n['niche']} (Score: {n['score']}) | RPM: ~${n['estimated_rpm_usd']:.2f} USD | Formato: {n['format_recommended']}")

            lines.extend([
                f"\n🎯 DOSSIÊ DO NICHO #1: {top_briefing.get('niche')}",
                f"• Promessa: {top_briefing.get('channel_promise')}",
                f"• Público-Alvo: {top_briefing.get('target_audience')}",
                f"• Estética: {top_briefing.get('visual_aesthetic')}",
                f"• Ângulo Anti-Genérico: {top_briefing.get('anti_generic_angle')}",
                f"• Títulos de Entrada: '{'; '.join(ranked[0].get('entry_video_titles', [])[:3])}'",
                f"\n🚫 GATE DE MONETIZAÇÃO: {len(blocked)} nichos descartados (Reused/Inauthentic/Copyright/Apenas Formato 4).",
                f"⚠️ ATENÇÃO YPP: Em fev/2027 a exigência sobe para 8.000 horas qualificadas."
            ])
            return "\n".join(lines)

        elif any(k in msg_lower for k in [
            "engenharia reversa", "buscar canais para modelar", "canais para modelar",
            "encontrar canais faceless", "reverse engineer", "quais canais criar no br e em ingles", "modelar canais",
            "potenciais canais virais", "metodos de busca", "canais virais"
        ]):
            # Detect discovery method
            method = "all"
            if any(k in msg_lower for k in ["velocidade", "vph", "breakout"]):
                method = "velocity_breakout"
            elif any(k in msg_lower for k in ["vacuo", "oferta", "content gap"]):
                method = "supply_vacuum"
            elif any(k in msg_lower for k in ["sugerido", "sugeridos", "hijack", "barra lateral"]):
                method = "suggested_hijack"
            elif any(k in msg_lower for k in ["arbitragem", "cross", "traduzir", "gringo"]):
                method = "cross_language_arbitrage"
            elif any(k in msg_lower for k in ["mecanismo", "especifico", "anti-generico", "anti generico"]):
                method = "mechanism_specific"

            re_res = self.reverse_engineer_channels(discovery_method=method)
            output = re_res.get("output", {})
            br_ch = output.get("brazil_channels", [])
            glob_ch = output.get("global_channels", [])
            recs = output.get("recommendations", {})
            br_rec = recs.get("brazil_channel", {})
            glob_rec = recs.get("global_channel", {})
            methods_applied = output.get("discovery_methods_applied", [])

            wants_html = "html" in msg_lower or "pagina" in msg_lower or "painel" in msg_lower or "dashboard" in msg_lower
            html_path_str = ""
            if wants_html:
                html_file = self.channel_reverse_engineer.generate_html_report(re_res)
                html_url = html_file.replace('\\', '/')
                html_path_str = f"🌐 RELATÓRIO HTML INTERATIVO GERADO:\n📄 Arquivo: {html_file}\n🔗 Link: file:///{html_url}\n\n"

            lines = [
                f"{html_path_str}🔍 [ENGENHARIA REVERSA MULTI-MÉTODO // 2 NOVOS CANAIS OCEANOS AZUIS]:",
                f"Método de Descoberta: {method.upper()} (Filtro de 5 Métodos: VPH Breakout, Vácuo de Oferta, Sugeridos, Arbitragem e Mecanismo Específico)",
                f"🛡️ FILTRO ANTI-GENÉRICO: Desqualificados tópicos saturados (Pix, FTX, pontes) para evitar atrito algorítmico.\n",
                f"🇧🇷 NOVO CANAL 1 (BRASIL // PORTUGUÊS):",
                f"• Nicho: {br_rec.get('niche')}",
                f"• Por que sobe rápido: {br_rec.get('why_this_beats_generic')}",
                f"• Formato: {br_rec.get('format')} | CPM Estimado: ~${br_rec.get('estimated_cpm_usd')} USD",
                f"• Gancho Causal (0-15s): {br_rec.get('hook_structure')[:110]}...",
                f"• Roteiro: {br_rec.get('script_structure')[:110]}...",
                f"• Cadência: {br_rec.get('ideal_duration')} • {br_rec.get('ideal_frequency')}",
                f"• 3 Ideias Iniciais: '{'; '.join(br_rec.get('entry_video_ideas', [])[:3])}'\n",
                f"🌐 NOVO CANAL 2 (GLOBAL // INGLÊS - US/UK):",
                f"• Nicho: {glob_rec.get('niche')}",
                f"• Why it scales fast: {glob_rec.get('why_this_beats_generic')}",
                f"• Formato: {glob_rec.get('format')} | CPM Estimado: ~${glob_rec.get('estimated_cpm_usd')} USD",
                f"• Hook (0-15s): {glob_rec.get('hook_structure')[:110]}...",
                f"• Script: {glob_rec.get('script_structure')[:110]}...",
                f"• Cadence: {glob_rec.get('ideal_duration')} • {glob_rec.get('ideal_frequency')}",
                f"• 3 Entry Ideas: '{'; '.join(glob_rec.get('entry_video_ideas', [])[:3])}'\n",
                f"📊 CANAIS RECENTES DESCOBERTOS: {len(br_ch)} no Brasil e {len(glob_ch)} globais (VPH > 500 / Canais < 90 dias).",
                f"🛡️ CHECKLIST YPP: 100% autoral, zero compilações, viável no pipeline atual de IA/Motion."
            ]
            return "\n".join(lines)

        elif "memoria" in msg_lower or "historico" in msg_lower:
            mems = self.search_memory(user_msg, limit=5)
            if not mems:
                return "Nenhum aprendizado específico encontrado no FTS5 para esses termos."
            lines = ["🧠 [MEMÓRIA PERSISTENTE FTS5 // CHIEF]:"]
            for m in mems:
                lines.append(f"• [{m.get('channel', 'global').upper()}] {m.get('content', '')}")
            return "\n".join(lines)

        else:
            return (
                "🎯 CHIEF ANALYST ONLINE // Modo de Comando:\n"
                "• Digite 'analisar outro lado', 'analisar hsl' ou 'analisar brecha' para auditoria completa.\n"
                "• Digite 'temas <canal>' para avaliar a fila de produção P0/P1/P2.\n"
                "• Digite 'briefing <canal>' para emitir ordem JSON para o squad.\n"
                "• Digite 'pesquisa de nichos' para buscar nichos faceless com gate de monetização YPP.\n"
                "• Digite 'engenharia reversa de canais' para dissecar canais e extrair padrões para novos canais BR e Global.\n"
                "• Digite 'memoria <termo>' para consultar a base FTS5 de aprendizados históricos."
            )

    # Convenience aliases for interfaces
    get_multi_channel_summary = generate_full_executive_summary
    get_next_themes = decide_themes
    query_knowledge = search_memory
    find_monetizable_niches = research_niches
    reverse_engineer = reverse_engineer_channels
    ask = answer_query

chief_agent = ChiefAnalystAgent()
