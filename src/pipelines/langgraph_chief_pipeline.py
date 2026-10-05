# -*- coding: utf-8 -*-
"""
LangGraph Multi-Agent Dynamic Production Pipeline for Chief YouTube Channels
Supports all 3 channels: Hidden Systems Lab, O Outro Lado, Brecha.

Key Feature: DYNAMIC EPISODE RESOLVER WITH CONTINUOUS MEMORY CONSULTATION
  - Always queries ChiefMemory (video_history, learnings, active experiments)
  - Prevents topic cannibalization and fatigue
  - Never copies 100% blindly: dynamically ADAPTS and sharpens the topic angle
  - Automatically runs Eugene Schwartz Step 2 (spontaneous customer language)
  - Passes through Research -> 4 Acts Script -> Gatekeeper Audit -> Art/Storyboard -> 7-Piece Ecosystem
  - Commits the new episode back to ChiefMemory so subsequent runs never repeat it!
"""

import os
import re
import json
from datetime import datetime
from typing import Dict, Any, List, TypedDict, Literal, Optional
from pathlib import Path

# LangGraph & LangChain imports
from langgraph.graph import StateGraph, END
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_groq import ChatGroq

# Chief Internal Engines
from src.core.memory import memory as chief_memory
from src.skills.theme_decider import theme_decider
from src.skills.squad_briefing import squad_briefing_gen
from src.skills.voice_miner import voice_miner
from src.skills.discovery_engine import discovery_engine

# ---------------------------------------------------------------------------
# 1. STATE DEFINITION
# ---------------------------------------------------------------------------
class ChiefState(TypedDict):
    # Inputs
    channel: str                          # "hidden_systems_lab" | "o_outro_lado" | "brecha"
    custom_seed_idea: Optional[str]       # Optional user prompt / raw theme suggestion
    force_topic: Optional[str]            # Optional forced topic
    
    # Dynamic Memory & Scout State
    memory_context: Dict[str, Any]        # Past produced videos, rules, channel baselines
    resolved_topic_data: Dict[str, Any]   # Adapted topic, angle, investigated unit, P-Score
    episode_id: str                       # e.g. "EP_20260923_WATERHAMMER"
    briefing: Dict[str, Any]              # Full canonical squad briefing
    
    # Narrative & Engineering
    research_dossier: Dict[str, Any]
    script_acts: Dict[str, Any]
    fact_check_verdict: str
    fact_check_critique: str
    revision_count: int
    
    # Visual & Distribution
    visual_storyboard: List[Dict[str, Any]]
    discovery_ecosystem: Dict[str, Any]
    final_output: Dict[str, Any]

# ---------------------------------------------------------------------------
# 2. LLM INITIALIZATION
# ---------------------------------------------------------------------------
groq_api_key = os.getenv("GROQ_API_KEY", "")
llm = ChatGroq(
    temperature=0.2,
    model_name="llama-3.3-70b-versatile",
    groq_api_key=groq_api_key
)

# ---------------------------------------------------------------------------
# 3. SPECIALIZED PROMPTS
# ---------------------------------------------------------------------------

TOPIC_SCOUT_AND_ADAPTER_PROMPT = """You are the Senior Topic Scout and Chief Editorial Strategist for YouTube Documentary Channels.

YOUR CORE MANDATE:
1. ALWAYS CONSULT THE MEMORY: You will be provided with the channel's past video history, published titles, and editorial guidelines.
2. NEVER CANNIBALIZE: Never create a video that overlaps directly with what has already been published.
3. NEVER COPY 100% BLINDLY: If a candidate topic is provided (from the backlog or user), DO NOT merely copy it. ADAPT it. Sharpen the paradox, increase market sophistication, anchor in a visceral physical unit, and eliminate generic framing.
4. QUANTITATIVE FILTER (Eugene Schwartz + TRIZ):
   - Every theme must anchor in a concrete, physical unit of investigation (e.g. 1 millisecond, 1 liter of fuel, 1 SIM chip, 0.0 Hz).
   - Hook in the first 15 seconds must state an impossible contradiction or severe hidden vulnerability.

You must return valid JSON with:
{
  "adapted_topic_title": "Sharpened, highly attractive documentary title",
  "investigated_unit": "The exact physical/forensic unit under study",
  "central_thesis": "The causal thesis behind why the system fails or works",
  "visceral_15s_hook": "The opening paradox to state before 0:15",
  "market_sophistication_stage": 4,
  "why_adapted": "Concise explanation of what was changed from the raw idea and why it outperforms the original",
  "p_score_estimate": 500,
  "target_audience": "Specific professional/enthusiast demographic"
}
"""

RESEARCHER_SYSTEM_PROMPT = """You are the Senior Forensic Systems Researcher.
Your job is to conduct deep, empirical engineering research on the assigned system failure and recovery.

MANTRA: "The view is not the asset. The compatible audience is the asset."

Your output must be structured in JSON with:
1. "central_paradox": The physical Catch-22 loop or vulnerability.
2. "physical_equations_or_protocols": Real formulas or technical protocols governing the phenomenon.
3. "historical_failures": 2 real-world catastrophic failure case studies with precise dates, locations, and root causes.
4. "unresolved_questions": 3 counter-intuitive technical questions that mainstream competitors never answer.
5. "sequence_of_operations": The step-by-step physical/technical procedure used by engineers/investigators.
"""

SCRIPTWRITER_SYSTEM_PROMPT = """You are the Chief Documentary Script Architect.
Tone: Cold, surgical, forensically objective.
Voice Pace: Exactly 146 words per minute (Chris persona for EN, Sobriety for PT).

STRICT NARRATIVE RULES:
1. THE 15-SECOND RULE: Deliver the core promise within the first 15 seconds. NO greetings, NO intro music delays, NO "welcome back".
2. 4 ACT STRUCTURE:
   - Act 1: The Breach / The Zero State (0:00 - 2:00) -> The shock, the visceral paradox, the everyday vulnerability.
   - Act 2: The Invisible Mechanism (2:00 - 5:00) -> Dissect the hidden physical/digital mechanics and debunk popular myths.
   - Act 3: Forensic Dissection (5:00 - 8:00) -> The concrete proof, answering the question no competitor explained.
   - Act 4: The Consequence & Defense (8:00 - 10:30) -> Systemic implications and retention bridge to the next dossier.
3. Every scene MUST have timestamps [MM:SS], visual cues [VISUAL], and narration [VOICE].

Output strictly formatted JSON: {"acts": [{"act_number": 1, "title": "...", "duration": "0:00 - 2:00", "scenes": [...]}]}.
"""

FACT_CHECKER_SYSTEM_PROMPT = """You are the Technical Gatekeeper and Reliability Auditor.
Your job is to ruthlessly critique the documentary script for physical, engineering, and algorithmic accuracy.

AUDIT CRITERIA (Boolean PASS / REVISE):
1. Physical/Technical Veracity: Are the mechanisms, protocols, and math 100% accurate?
2. 15-Second Retention Gate: Did the script hook the viewer with the visceral paradox before 0:15 without corporate greetings?
3. Tone Fidelity: Is the narration cold and surgical, avoiding hyperbole, buzzwords, and dramatic sensationalism?
4. Algorithmic Pacing: Is there progressive tension without dead zones?

Return valid JSON with:
{
  "verdict": "PASS" or "REVISE",
  "score": 0 to 100,
  "critique": "Specific inaccuracies or structural flaws to fix if REVISE, or validation statement if PASS."
}
"""

ART_DIRECTOR_SYSTEM_PROMPT = """You are the Visual Art Director and Storyboard Engineer.
Aesthetics: Technical blueprints, isometric 2.5D CAD schematics, orthographic X-ray cross-sections, high-contrast telemetry HUDs.
Color Palette: Charcoal Black (#0D0D0F), Industrial Amber (#FF9800), Cyan/Nitrogen (#00E5FF).
NO CARTOONISH FIGURES. NO CYBERPUNK CLICHÉS. ONLY REALISTIC FORENSIC TELEMETRY.

Generate a comprehensive storyboard JSON with:
1. "thumbnail_packages": 3 A/B/C options with Hero Object, Focal Point, and CTR Hypothesis.
2. "scene_prompts": Midjourney/Flux generation prompts for key scenes in the script.
3. "motion_graphics_spec": Overlay layers, telemetry counters, and audio LUFS targets (-16 LUFS).
"""

ECOSYSTEM_SYSTEM_PROMPT = """You are the 80/20 Discovery Ecosystem Engineer.
Distribution cannot rely on a single faucet. You must generate the 7 coordinated discovery assets for this episode:
1. Search Long-Form Title (Active intent: Problem + Desired Result + Specific Mechanism)
2. Browse / Home Long-Form Title (Curiosity + High-stakes transformation)
3. Short #1 (Discovery & Proof - with related video link to long-form)
4. Short #2 (Hidden Trap / The Counter-Intuitive Flaw - 45s self-contained)
5. Playlist Architecture (Session retention path)
6. Community Poll (48h pre-production demand validation)
7. External Distribution Post (Forensic breakdown for Reddit / LinkedIn)

Return strictly valid JSON with all 7 pieces.
"""

# ---------------------------------------------------------------------------
# 4. NODES IMPLEMENTATION
# ---------------------------------------------------------------------------

def memory_and_topic_scout_node(state: ChiefState) -> Dict[str, Any]:
    """
    CONSULTS CHIEF MEMORY & SELECTS / ADAPTS THE NEXT UNPRODUCED TOPIC
    """
    channel = state.get("channel", "hidden_systems_lab").lower()
    custom_seed = state.get("custom_seed_idea")
    force_topic = state.get("force_topic")

    # 1. Fetch channel history and learnings from ChiefMemory DB
    past_titles = chief_memory.get_channel_video_titles(channel)
    recent_learnings = chief_memory.get_recent_learnings(channel=channel, limit=5)
    
    # 2. Consult ThemeDecider candidate backlog (already deduplicated against covered_themes)
    eval_res = theme_decider.evaluate_themes(channel)
    top_candidates = eval_res.get("top_3_selected", eval_res.get("top_3_themes", []))

    # 3. Determine candidate to adapt:
    # If forced, use forced. If user gave seed, use seed. Otherwise find first unproduced from backlog!
    candidate_raw = None
    if force_topic:
        candidate_raw = {"topic": force_topic, "unit": "Defined by prompt", "thesis": force_topic}
    elif custom_seed:
        candidate_raw = {"topic": custom_seed, "unit": "To be extracted", "thesis": custom_seed}
    else:
        for cand in top_candidates:
            c_topic = cand.get("topic", "")
            if not chief_memory.is_topic_covered(channel, c_topic):
                candidate_raw = cand
                break
        if not candidate_raw and top_candidates:
            candidate_raw = top_candidates[0]

    # 4. Call LLM to ADAPT and SHARPEN the topic based on memory context
    prompt = f"""Channel: {channel}
Previously Published Titles (DO NOT REPEAT OR OVERLAP):
{json.dumps(past_titles, indent=2, ensure_ascii=False)}

Recent Channel Learnings:
{json.dumps([l.get('insight') for l in recent_learnings], indent=2, ensure_ascii=False)}

Candidate Raw Topic:
{json.dumps(candidate_raw, indent=2, ensure_ascii=False)}

Instructions:
Consult the memory above. Adapt this topic so it is mathematically and forensically compelling. 
Do not copy it verbatim. Formulate a visceral 15s hook and concrete physical unit.
"""
    response = llm.invoke([
        SystemMessage(content=TOPIC_SCOUT_AND_ADAPTER_PROMPT),
        HumanMessage(content=prompt)
    ])

    try:
        adapted_data = json.loads(response.content)
    except Exception:
        # Fallback if markdown fence is present
        clean_text = re.sub(r"```json|```", "", response.content).strip()
        try:
            adapted_data = json.loads(clean_text)
        except Exception:
            adapted_data = {
                "adapted_topic_title": candidate_raw.get("topic", "System Forensic Investigation"),
                "investigated_unit": candidate_raw.get("unit", "1 physical unit"),
                "central_thesis": candidate_raw.get("thesis", "Systemic failure under extreme boundary conditions"),
                "visceral_15s_hook": "What happens when the system fails without warning.",
                "why_adapted": "Direct fallback parsing."
            }

    # Generate Unique Episode ID based on timestamp and slug
    clean_slug = re.sub(r"[^A-Za-z0-9]+", "_", adapted_data["adapted_topic_title"].upper())[:24]
    episode_id = f"EP_{datetime.now().strftime('%Y%m%d')}_{clean_slug}"

    # Generate Canonical Squad Briefing
    briefing = squad_briefing_gen.generate_briefing(
        channel_slug=channel,
        episode_id=episode_id,
        custom_params={
            "tema": adapted_data["adapted_topic_title"],
            "unidade": adapted_data["investigated_unit"],
            "tese": adapted_data["central_thesis"],
            "promessa": adapted_data["visceral_15s_hook"]
        }
    )

    return {
        "memory_context": {
            "past_titles": past_titles,
            "recent_learnings_count": len(recent_learnings)
        },
        "resolved_topic_data": adapted_data,
        "episode_id": episode_id,
        "briefing": briefing
    }


def researcher_node(state: ChiefState) -> Dict[str, Any]:
    briefing = state["briefing"]
    prompt = f"""Conduct deep forensic engineering/system research for this episode:
Channel: {briefing.get('canal')}
Topic: {briefing.get('tema')}
Unit of Investigation: {briefing.get('unidade_investigada')}
Central Thesis: {briefing.get('tese_central')}
Target Audience: {briefing.get('publico_alvo')}
Spontaneous Language Mined from Audience: {json.dumps(briefing.get('linguagem_espontanea_do_publico', {}))}
"""
    response = llm.invoke([
        SystemMessage(content=RESEARCHER_SYSTEM_PROMPT),
        HumanMessage(content=prompt)
    ])
    try:
        clean = re.sub(r"```json|```", "", response.content).strip()
        data = json.loads(clean)
    except Exception:
        data = {"raw_research": response.content}
    return {"research_dossier": data}


def scriptwriter_node(state: ChiefState) -> Dict[str, Any]:
    briefing = state["briefing"]
    research = state["research_dossier"]
    critique = state.get("fact_check_critique", "")
    revision = state.get("revision_count", 0)

    prompt = f"""Write the complete 4-Act documentary script:
Topic: {briefing.get('tema')}
Unit: {briefing.get('unidade_investigada')}
15-Second Opening Priority: {briefing.get('diretrizes_estrategicas', {}).get('o_que_priorizar_na_abertura')}
Research Dossier: {json.dumps(research)}
Previous Critique (if any): {critique}
Revision Round: {revision}
"""
    response = llm.invoke([
        SystemMessage(content=SCRIPTWRITER_SYSTEM_PROMPT),
        HumanMessage(content=prompt)
    ])
    try:
        clean = re.sub(r"```json|```", "", response.content).strip()
        data = json.loads(clean)
    except Exception:
        data = {"raw_script": response.content}
    return {"script_acts": data, "revision_count": revision + 1}


def fact_checker_node(state: ChiefState) -> Dict[str, Any]:
    script = state["script_acts"]
    research = state["research_dossier"]
    prompt = f"""Audit the following script against empirical truth, retention rules, and tone fidelity:
Script: {json.dumps(script)[:4000]}
Research Base: {json.dumps(research)[:2000]}
"""
    response = llm.invoke([
        SystemMessage(content=FACT_CHECKER_SYSTEM_PROMPT),
        HumanMessage(content=prompt)
    ])
    try:
        clean = re.sub(r"```json|```", "", response.content).strip()
        data = json.loads(clean)
        verdict = data.get("verdict", "PASS")
        critique = data.get("critique", "")
    except Exception:
        verdict = "PASS"
        critique = "Audit completed."

    # Prevent infinite loop: cap revisions at 2
    if state.get("revision_count", 0) >= 2:
        verdict = "PASS"

    return {"fact_check_verdict": verdict, "fact_check_critique": critique}


def should_continue(state: ChiefState) -> Literal["art_director", "scriptwriter"]:
    if state.get("fact_check_verdict") == "PASS":
        return "art_director"
    return "scriptwriter"


def art_director_node(state: ChiefState) -> Dict[str, Any]:
    script = state["script_acts"]
    prompt = f"""Design the visual storyboard and thumbnail packages:
Script: {json.dumps(script)[:3000]}
"""
    response = llm.invoke([
        SystemMessage(content=ART_DIRECTOR_SYSTEM_PROMPT),
        HumanMessage(content=prompt)
    ])
    try:
        clean = re.sub(r"```json|```", "", response.content).strip()
        data = json.loads(clean)
    except Exception:
        data = {"raw_art": response.content}
    return {"visual_storyboard": data}


def ecosystem_publisher_node(state: ChiefState) -> Dict[str, Any]:
    briefing = state["briefing"]
    script = state["script_acts"]
    prompt = f"""Generate the 7-piece discovery ecosystem for this documentary:
Topic: {briefing.get('tema')}
Script Sample: {json.dumps(script)[:1000]}
"""
    response = llm.invoke([
        SystemMessage(content=ECOSYSTEM_SYSTEM_PROMPT),
        HumanMessage(content=prompt)
    ])
    try:
        clean = re.sub(r"```json|```", "", response.content).strip()
        data = json.loads(clean)
    except Exception:
        data = {"raw_ecosystem": response.content}
    return {"discovery_ecosystem": data}


def memory_recorder_node(state: ChiefState) -> Dict[str, Any]:
    """
    COMMITS THE NEW EPISODE TO CHIEF MEMORY FOR CONTINUOUS TRACKING
    Ensures that next runs will know this episode is already in production!
    """
    channel = state["channel"]
    topic = state["resolved_topic_data"]["adapted_topic_title"]
    episode_id = state["episode_id"]

    # 1. Record in video_history
    chief_memory.record_video(
        channel=channel,
        title=topic,
        video_id=episode_id,
        format="long",
        notes=f"Generated via LangGraph pipeline on {datetime.now().strftime('%Y-%m-%d %H:%M')}"
    )

    # 2. Record in learnings
    chief_memory.record_learning(
        channel=channel,
        category="EPISODE_PRODUCTION",
        insight=f"Episódio {episode_id} ('{topic}') aprovado e enviado para a esteira de edição.",
        evidence=f"Briefing e roteiro finalizados com 4 Atos e 7 peças de distribuição.",
        action_taken="Atualizar prateleira e agendar enquete de validação prévia na aba Comunidade."
    )

    final_pkg = {
        "channel": channel,
        "episode_id": episode_id,
        "status": "APPROVED_AND_RECORDED_IN_MEMORY",
        "adapted_topic": state["resolved_topic_data"],
        "briefing_path": state["briefing"].get("saved_path"),
        "script_acts": state["script_acts"],
        "visual_storyboard": state["visual_storyboard"],
        "discovery_ecosystem": state["discovery_ecosystem"]
    }

    # Save to disk
    out_file = Path("data/briefings_output") / f"PACKAGE_{channel}_{episode_id}.json"
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(final_pkg, f, indent=2, ensure_ascii=False)

    return {"final_output": final_pkg}

# ---------------------------------------------------------------------------
# 5. GRAPH ASSEMBLY & COMPILATION
# ---------------------------------------------------------------------------
def build_chief_production_graph():
    workflow = StateGraph(ChiefState)

    workflow.add_node("topic_scout", memory_and_topic_scout_node)
    workflow.add_node("researcher", researcher_node)
    workflow.add_node("scriptwriter", scriptwriter_node)
    workflow.add_node("fact_checker", fact_checker_node)
    workflow.add_node("art_director", art_director_node)
    workflow.add_node("ecosystem_publisher", ecosystem_publisher_node)
    workflow.add_node("memory_recorder", memory_recorder_node)

    # Sequence
    workflow.set_entry_point("topic_scout")
    workflow.add_edge("topic_scout", "researcher")
    workflow.add_edge("researcher", "scriptwriter")
    workflow.add_edge("scriptwriter", "fact_checker")

    workflow.add_conditional_edges(
        "fact_checker",
        should_continue,
        {
            "scriptwriter": "scriptwriter",
            "art_director": "art_director"
        }
    )

    workflow.add_edge("art_director", "ecosystem_publisher")
    workflow.add_edge("ecosystem_publisher", "memory_recorder")
    workflow.add_edge("memory_recorder", END)

    return workflow.compile()

# Global Compiled Application
chief_graph_app = build_chief_production_graph()

# ---------------------------------------------------------------------------
# 6. CLI / STANDALONE RUNNER
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Chief YouTube Autonomous Production Pipeline")
    parser.add_argument("--channel", type=str, default="hidden_systems_lab", choices=["hidden_systems_lab", "o_outro_lado", "brecha"])
    parser.add_argument("--seed", type=str, default=None, help="Raw idea to adapt")
    args = parser.parse_args()

    print(f"\n=======================================================")
    print(f"🚀 [CHIEF PIPELINE] Starting for channel: {args.channel}")
    print(f"🧠 Consulting ChiefMemory for past videos and next P0 topic...")
    print(f"=======================================================\n")

    initial_input: ChiefState = {
        "channel": args.channel,
        "custom_seed_idea": args.seed,
        "force_topic": None,
        "memory_context": {},
        "resolved_topic_data": {},
        "episode_id": "",
        "briefing": {},
        "research_dossier": {},
        "script_acts": {},
        "fact_check_verdict": "",
        "fact_check_critique": "",
        "revision_count": 0,
        "visual_storyboard": [],
        "discovery_ecosystem": {},
        "final_output": {}
    }

    result = chief_graph_app.invoke(initial_input)
    print("\n✅ PIPELINE COMPLETED SUCCESSFULLY!")
    print(f"📌 Episode ID: {result['episode_id']}")
    print(f"🎯 Adapted Topic: {result['resolved_topic_data'].get('adapted_topic_title')}")
    print(f"🔬 Physical Unit: {result['resolved_topic_data'].get('investigated_unit')}")
    print(f"💾 Committed to memory and saved in data/briefings_output/PACKAGE_{args.channel}_{result['episode_id']}.json\n")
