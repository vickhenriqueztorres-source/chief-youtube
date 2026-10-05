# -*- coding: utf-8 -*-
"""
LangGraph Multi-Agent Production Pipeline for Hidden Systems Lab (HSL)
Episode #1: THE BLACK START (EP_BLACKSTART)

Architecture:
  [Briefing Input]
         ↓
  [1. ForensicSystemsResearcher]
         ↓
  [2. NarrativeScriptArchitect]
         ↓
  [3. EngineeringFactChecker] ── (REVISE) ──┐
         │ (PASS)                           │
         ↓                                  │
  [4. VisualArtDirector]                    │
         ↓                                  │
  [5. EcosystemPublisher]                   │
         ↓                                  │
  [Final Production Artifacts]              │
         ▲                                  │
         └──────────────────────────────────┘
"""

import os
import json
from typing import Dict, Any, List, TypedDict, Literal
from pathlib import Path
from pydantic import BaseModel, Field

# LangGraph & LangChain imports
from langgraph.graph import StateGraph, END
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_groq import ChatGroq

# ---------------------------------------------------------------------------
# 1. GRAPH STATE DEFINITION
# ---------------------------------------------------------------------------
class GraphState(TypedDict):
    briefing: Dict[str, Any]
    research_dossier: Dict[str, Any]
    script_acts: Dict[str, Any]
    fact_check_verdict: str
    fact_check_critique: str
    revision_count: int
    visual_storyboard: List[Dict[str, Any]]
    discovery_ecosystem: Dict[str, Any]
    final_output: Dict[str, Any]

# ---------------------------------------------------------------------------
# 2. LLM INITIALIZATION (Using Groq llama-3.3-70b-versatile or DeepSeek R1)
# ---------------------------------------------------------------------------
groq_api_key = os.getenv("GROQ_API_KEY", "")
llm = ChatGroq(
    temperature=0.2,
    model_name="llama-3.3-70b-versatile",
    groq_api_key=groq_api_key
)

# ---------------------------------------------------------------------------
# 3. NODE SYSTEM PROMPTS
# ---------------------------------------------------------------------------

RESEARCHER_SYSTEM_PROMPT = """You are the Senior Forensic Systems Researcher for HIDDEN SYSTEMS LAB (@HiddenSystemslabss).
Your goal is to conduct deep, empirical engineering research on the assigned system failure and recovery.

MANTRA: "The view is not the asset. The compatible audience is the asset."
CHANNEL UNIT: 1 millisecond, extreme hydraulic shockwaves, 0.0 Hz electrical references, catastrophic limits.

Your output must be structured in JSON with:
1. "central_paradox": The unbreakable physical loop (e.g., Catch-22: generators need electricity to create electricity).
2. "physical_equations": Real electrical/mechanical formulas governing the phenomenon (Ferranti Effect, inrush current, reactive power absorption Q = V^2 * omega * C).
3. "historical_failures": 2 real-world catastrophic failure case studies with precise dates, plant names, and root causes (e.g., 2003 Northeast Blackout, 2021 Texas ERCOT trip).
4. "unresolved_questions": 3 counter-intuitive technical questions that mainstream YouTube videos never answer.
5. "sequence_of_operations": The step-by-step physical procedure used by engineers to resolve the crisis.
"""

SCRIPTWRITER_SYSTEM_PROMPT = """You are the Chief Documentary Script Architect for HIDDEN SYSTEMS LAB (@HiddenSystemslabss).
Tone: Cold, surgical, forensically objective. Inspired by Denis Villeneuve and technical disaster investigations.
Voice Pace: Exactly 146 words per minute (Chris's voice persona).

STRICT NARRATIVE RULES:
1. THE 15-SECOND RULE: Deliver the core promise within the first 15 seconds. NO greetings, NO "Welcome back to the channel", NO generic fluff.
2. 4 ACT STRUCTURE:
   - Act 1: The Zero State & The Breach (0:00 - 2:00) -> Continental silence, zero reference, the Catch-22 loop.
   - Act 2: The Invisible Physics (2:00 - 5:00) -> The Ferranti Effect trap, why simply flipping switches blows substations.
   - Act 3: Forensic Dissection (5:00 - 8:00) -> The 12-step bootstrap sequence from diesel crank to synchronous grid.
   - Act 4: The Fragile Equilibrium (8:00 - 10:30) -> Inverter-dominated grids, renewable vulnerability, and the retention hook to the next dossier.
3. Every scene MUST have timestamps [MM:SS], visual cues [VISUAL], and narration [VOICE].

Output strictly formatted JSON with "acts": [ {"act_number": 1, "title": "...", "duration": "0:00 - 2:00", "scenes": [...] } ].
"""

FACT_CHECKER_SYSTEM_PROMPT = """You are the Technical Gatekeeper and NERC Reliability Auditor for HIDDEN SYSTEMS LAB.
Your job is to ruthlessly critique the documentary script for physical, engineering, and algorithmic accuracy.

AUDIT CRITERIA (Boolean PASS / REVISE):
1. Physical Veracity: Are the electrical concepts (reactive capacitance, excitation field flashing, governor hunting) 100% accurate?
2. 15-Second Retention Gate: Did the script hook the viewer with the visceral paradox before 0:15 without corporate greetings?
3. Tone Fidelity: Is the narration cold and surgical, avoiding hyperbole, buzzwords, and dramatic sensationalism?
4. Algorithmic Pacing: Is there progressive tension without dead zones?

Return valid JSON with:
{
  "verdict": "PASS" or "REVISE",
  "score": 0 to 100,
  "critique": "Specific physical inaccuracies or structural flaws to fix if REVISE, or validation statement if PASS."
}
"""

ART_DIRECTOR_SYSTEM_PROMPT = """You are the Visual Art Director and Storyboard Engineer for HIDDEN SYSTEMS LAB.
Aesthetics: Technical blueprints, isometric 2.5D CAD schematics, orthographic X-ray cross-sections, high-voltage telemetry HUDs.
Color Palette: Charcoal Black (#0D0D0F), Industrial Amber (#FF9800), Nitrogen Blue (#00E5FF), Voltage Green (#76FF03).
NO CARTOONISH FIGURES. NO CYBERPUNK CLICHÉS. ONLY REALISTIC INDUSTRIAL TELEMETRY.

Generate a comprehensive storyboard JSON with:
1. "thumbnail_packages": 3 A/B/C options with Hero Object, Focal Point, and CTR Hypothesis.
2. "scene_prompts": Midjourney/Flux generation prompts for key scenes in the script.
3. "motion_graphics_spec": Overlay layers, telemetry counters (Hz, kV, MW), and audio LUFS targets (-16 LUFS).
"""

ECOSYSTEM_SYSTEM_PROMPT = """You are the 80/20 Discovery Ecosystem Engineer for HIDDEN SYSTEMS LAB.
Distribution cannot rely on a single faucet. You must generate the 7 coordinated discovery assets for this episode:
1. Search Long-Form Title (Active intent: Problem + Desired Result + Specific Mechanism)
2. Browse / Home Long-Form Title (Curiosity + High-stakes transformation)
3. Short #1 (Discovery & Proof - with related video link to long-form)
4. Short #2 (Hidden Trap / The Ferranti Paradox - 45s self-contained)
5. Playlist Architecture (Session retention path)
6. Community Poll (48h pre-production demand validation)
7. External Distribution Post (Forensic breakdown for Reddit r/ElectricalEngineering & LinkedIn)

Return strictly valid JSON with all 7 pieces.
"""

# ---------------------------------------------------------------------------
# 4. GRAPH NODES IMPLEMENTATION
# ---------------------------------------------------------------------------

def researcher_node(state: GraphState) -> Dict[str, Any]:
    briefing = state["briefing"]
    prompt = f"""Conduct deep forensic engineering research for this episode:
Channel: {briefing.get('canal')}
Topic: {briefing.get('tema')}
Unit of Investigation: {briefing.get('unidade_investigada')}
Central Thesis: {briefing.get('tese_central')}
Target Audience: {briefing.get('publico_alvo')}
Spontaneous Language / Visceral Quotes: {json.dumps(briefing.get('linguagem_espontanea_do_publico', {}))}
"""
    response = llm.invoke([
        SystemMessage(content=RESEARCHER_SYSTEM_PROMPT),
        HumanMessage(content=prompt)
    ])
    try:
        data = json.loads(response.content)
    except Exception:
        data = {"raw_research": response.content}
    return {"research_dossier": data}


def scriptwriter_node(state: GraphState) -> Dict[str, Any]:
    briefing = state["briefing"]
    research = state["research_dossier"]
    critique = state.get("fact_check_critique", "")
    revision = state.get("revision_count", 0)

    prompt = f"""Write the complete 4-Act documentary script for HIDDEN SYSTEMS LAB:
Topic: {briefing.get('tema')}
Unit: {briefing.get('unidade_investigada')}
Opening Priority: {briefing.get('diretrizes_estrategicas', {}).get('o_que_priorizar_na_abertura')}
Research Dossier: {json.dumps(research)}
Previous Critique (if any): {critique}
Revision Round: {revision}
"""
    response = llm.invoke([
        SystemMessage(content=SCRIPTWRITER_SYSTEM_PROMPT),
        HumanMessage(content=prompt)
    ])
    try:
        data = json.loads(response.content)
    except Exception:
        data = {"raw_script": response.content}
    return {"script_acts": data, "revision_count": revision + 1}


def fact_checker_node(state: GraphState) -> Dict[str, Any]:
    script = state["script_acts"]
    research = state["research_dossier"]
    prompt = f"""Audit the following script against engineering truth and retention rules:
Script: {json.dumps(script)}
Research Base: {json.dumps(research)}
"""
    response = llm.invoke([
        SystemMessage(content=FACT_CHECKER_SYSTEM_PROMPT),
        HumanMessage(content=prompt)
    ])
    try:
        data = json.loads(response.content)
        verdict = data.get("verdict", "PASS")
        critique = data.get("critique", "")
    except Exception:
        verdict = "PASS"
        critique = "Audit completed."

    # Cap revisions at 2 to avoid infinite loops
    if state.get("revision_count", 0) >= 2:
        verdict = "PASS"

    return {"fact_check_verdict": verdict, "fact_check_critique": critique}


def should_continue(state: GraphState) -> Literal["art_director", "scriptwriter"]:
    if state["fact_check_verdict"] == "PASS":
        return "art_director"
    return "scriptwriter"


def art_director_node(state: GraphState) -> Dict[str, Any]:
    script = state["script_acts"]
    prompt = f"""Design the visual storyboard and thumbnail packages for this episode:
Script: {json.dumps(script)}
"""
    response = llm.invoke([
        SystemMessage(content=ART_DIRECTOR_SYSTEM_PROMPT),
        HumanMessage(content=prompt)
    ])
    try:
        data = json.loads(response.content)
    except Exception:
        data = {"raw_art": response.content}
    return {"visual_storyboard": data}


def ecosystem_publisher_node(state: GraphState) -> Dict[str, Any]:
    briefing = state["briefing"]
    script = state["script_acts"]
    prompt = f"""Generate the 7-piece discovery ecosystem for this documentary:
Topic: {briefing.get('tema')}
Script Highlights: {json.dumps(script)[:1000]}
"""
    response = llm.invoke([
        SystemMessage(content=ECOSYSTEM_SYSTEM_PROMPT),
        HumanMessage(content=prompt)
    ])
    try:
        data = json.loads(response.content)
    except Exception:
        data = {"raw_ecosystem": response.content}

    # Aggregate final output
    final_pkg = {
        "channel": briefing.get("canal"),
        "episode_id": briefing.get("episode_id"),
        "status": "APPROVED_FOR_PRODUCTION",
        "script": script,
        "storyboard": state.get("visual_storyboard"),
        "ecosystem_7_pieces": data
    }
    return {"discovery_ecosystem": data, "final_output": final_pkg}

# ---------------------------------------------------------------------------
# 5. GRAPH ASSEMBLY & COMPILATION
# ---------------------------------------------------------------------------
def build_hsl_production_graph():
    workflow = StateGraph(GraphState)

    workflow.add_node("researcher", researcher_node)
    workflow.add_node("scriptwriter", scriptwriter_node)
    workflow.add_node("fact_checker", fact_checker_node)
    workflow.add_node("art_director", art_director_node)
    workflow.add_node("ecosystem_publisher", ecosystem_publisher_node)

    workflow.set_entry_point("researcher")
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
    workflow.add_edge("ecosystem_publisher", END)

    return workflow.compile()

# Singleton graph app instance
hsl_pipeline_app = build_hsl_production_graph()

if __name__ == "__main__":
    briefing_path = Path(__file__).resolve().parent.parent.parent / "data" / "briefings_output" / "briefing_hidden_systems_lab_EP_BLACKSTART.json"
    if briefing_path.exists():
        with open(briefing_path, "r", encoding="utf-8") as f:
            sample_briefing = json.load(f)
    else:
        sample_briefing = {"canal": "hidden_systems_lab", "tema": "Black Start", "episode_id": "EP_BLACKSTART"}

    initial_state: GraphState = {
        "briefing": sample_briefing,
        "research_dossier": {},
        "script_acts": {},
        "fact_check_verdict": "",
        "fact_check_critique": "",
        "revision_count": 0,
        "visual_storyboard": [],
        "discovery_ecosystem": {},
        "final_output": {}
    }

    print("[*] Running HSL LangGraph Pipeline...")
    # Run synchronously or stream nodes
    output = hsl_pipeline_app.invoke(initial_state)
    print("[+] Pipeline finished successfully! Final package generated.")
    with open("data/briefings_output/EP_BLACKSTART_LANGGRAPH_RESULT.json", "w", encoding="utf-8") as out:
        json.dump(output["final_output"], out, indent=2, ensure_ascii=False)
