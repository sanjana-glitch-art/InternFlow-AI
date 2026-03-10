from openai import OpenAI
from typing import TypedDict, List, Dict, Any, Optional
from langgraph.graph import StateGraph, END
import json
import regex as re

# NVIDIA Nemotron via OpenAI-compatible API
client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key="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"
)
# Choose models (you can change these safely)
MODEL_DIAGNOSTIC = "nvidia/nemotron-3-nano-30b-a3b"
MODEL_PROJECTS = "nvidia/nemotron-3-nano-30b-a3b"
MODEL_REWRITE = "nvidia/nemotron-3-nano-30b-a3b"


# -----------------------------------------------------------------------------
# State shared across all agent nodes
# -----------------------------------------------------------------------------
class AgentState(TypedDict):
    job_description: str
    resume_text: str
    projects: List[dict]

    keywords_missing: List[str]
    selected_projects: List[dict]
    tailored_resume: str
    diagnostic_report: str


# -----------------------------------------------------------------------------
# Helpers
# -----------------------------------------------------------------------------
def truncate(s: str, max_chars: int) -> str:
    if not s:
        return ""
    return s[:max_chars]


def get_message_text(resp) -> Optional[str]:
    """
    NVIDIA/OpenAI-compatible responses sometimes put text in:
      - message.content
      - message.reasoning
      - message.reasoning_content
    We try all safely.
    """
    if not resp or not getattr(resp, "choices", None):
        return None

    msg = getattr(resp.choices[0], "message", None)
    if msg is None:
        return None

    # Standard content
    content = getattr(msg, "content", None)
    if isinstance(content, str) and content.strip():
        return content.strip()

    # Sometimes reasoning contains the textual output
    reasoning = getattr(msg, "reasoning", None)
    if isinstance(reasoning, str) and reasoning.strip():
        return reasoning.strip()

    reasoning_content = getattr(msg, "reasoning_content", None)
    if isinstance(reasoning_content, str) and reasoning_content.strip():
        return reasoning_content.strip()

    # Some providers may return list parts for content
    if isinstance(content, list):
        parts = []
        for p in content:
            if isinstance(p, dict) and p.get("type") == "text":
                parts.append(p.get("text", ""))
        joined = "\n".join([x for x in parts if x]).strip()
        return joined or None

    return None


def extract_first_json_object(text: str) -> Optional[Dict[str, Any]]:
    """
    Attempts to extract the first JSON object from a string.
    Handles:
      - ```json fences
      - extra leading/trailing text
    """
    if not text:
        return None

    # strip markdown fences
    cleaned = re.sub(r"^```(?:json)?\s*|\s*```$", "", text.strip(), flags=re.IGNORECASE)

    # find the first {...} block
    m = re.search(r"\{.*\}", cleaned, flags=re.DOTALL)
    if not m:
        return None

    candidate = m.group(0)

    try:
        return json.loads(candidate)
    except json.JSONDecodeError:
        return None


# -----------------------------------------------------------------------------
# Node 1: Extract keywords from JD and find gaps
# -----------------------------------------------------------------------------
def keyword_diagnostic_node(state: AgentState) -> AgentState:
    SYSTEM_JSON_ONLY = (
        "You MUST output ONLY valid JSON. "
        "No explanations, no reasoning, no markdown, no extra text."
    )

    jd = truncate(state.get("job_description", ""), 6000)
    resume = truncate(state.get("resume_text", ""), 8000)

    prompt = f"""
Extract the TOP 15 required keywords/skills from the JOB DESCRIPTION.
Compare them against the RESUME text.

Return JSON ONLY with this exact schema:
{{
  "jd_keywords": ["...15 strings..."],
  "missing_keywords": ["..."],
  "present_keywords": ["..."],
  "match_score": 0
}}

JOB DESCRIPTION:
{jd}

RESUME:
{resume}

Return ONLY the JSON object now.
""".strip()

    resp = client.chat.completions.create(
        model=MODEL_DIAGNOSTIC,
        messages=[
            {"role": "system", "content": SYSTEM_JSON_ONLY},
            {"role": "user", "content": prompt},
        ],
        temperature=0.0,
        max_tokens=350,
    )

    raw = get_message_text(resp)

    # If still nothing, do not crash the whole pipeline—fallback gracefully
    if raw is None:
        state["keywords_missing"] = []
        state["diagnostic_report"] = "Model returned no text (content/reasoning empty)."
        return state

    data = extract_first_json_object(raw)

    if not isinstance(data, dict):
        # Fallback if model didn't produce JSON
        state["keywords_missing"] = []
        state["diagnostic_report"] = raw
        return state

    state["keywords_missing"] = data.get("missing_keywords", []) or []
    state["diagnostic_report"] = json.dumps(data, indent=2)
    return state


# -----------------------------------------------------------------------------
# Node 2: Select best projects for this specific JD
# -----------------------------------------------------------------------------
def project_selector_node(state: AgentState) -> AgentState:
    projects = state.get("projects") or []
    if not projects:
        state["selected_projects"] = []
        return state

    # Make project list compact (avoid huge prompts)
    compact_projects = []
    for p in projects[:30]:  # cap count
        name = (p.get("name") or "").strip()
        desc = (p.get("description") or "").strip()
        if name:
            compact_projects.append({"name": name, "description": desc[:400]})

    projects_text = "\n".join([f"- {p['name']}: {p['description']}" for p in compact_projects])

    prompt = f"""
Job Description:
{truncate(state.get("job_description", ""), 4500)}

Student Projects:
{projects_text}

Task:
Select the TOP 3 most relevant project NAMES for this role.

Return ONLY a JSON array of strings, exactly like:
["Project 1", "Project 2", "Project 3"]
""".strip()

    resp = client.chat.completions.create(
        model=MODEL_PROJECTS,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.0,
        max_tokens=120,
    )

    raw = get_message_text(resp)

    if not raw:
        state["selected_projects"] = compact_projects[:3]
        return state

    # extract json array
    m = re.search(r"\[.*\]", raw, flags=re.DOTALL)
    if not m:
        state["selected_projects"] = compact_projects[:3]
        return state

    try:
        selected_names = json.loads(m.group(0))
        if not isinstance(selected_names, list):
            raise ValueError("Not a list")
        selected_set = set([str(x) for x in selected_names])
        state["selected_projects"] = [p for p in compact_projects if p["name"] in selected_set][:3]
        if not state["selected_projects"]:
            state["selected_projects"] = compact_projects[:3]
    except Exception:
        state["selected_projects"] = compact_projects[:3]

    return state


# -----------------------------------------------------------------------------
# Node 3: Rewrite resume tailored to the JD
# -----------------------------------------------------------------------------
def resume_modifier_node(state: AgentState) -> AgentState:
    selected_projects = state.get("selected_projects") or []
    selected_projects_text = "\n".join(
        [f"- {p.get('name','')}: {p.get('description','')}" for p in selected_projects]
    ).strip() or "Use projects already in the resume."

    missing_keywords = ", ".join(state.get("keywords_missing") or []) or "None"

    prompt = f"""
You are an expert resume writer.

Job Description:
{truncate(state.get("job_description", ""), 6000)}

Original Resume:
{truncate(state.get("resume_text", ""), 9000)}

Selected Projects to highlight:
{selected_projects_text}

Missing keywords to naturally incorporate (only if truthful):
{missing_keywords}

Instructions:
- Keep the same structure and format
- Rewrite bullets to match JD language
- Highlight the selected projects prominently
- Keep ATS-friendly
- Do NOT fabricate experience or skills

Return the complete rewritten resume text only.
""".strip()

    resp = client.chat.completions.create(
        model=MODEL_REWRITE,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
        max_tokens=1400,
    )

    raw = get_message_text(resp)

    # fallback: if no output, keep original resume
    state["tailored_resume"] = raw.strip() if raw else state.get("resume_text", "")
    return state


# -----------------------------------------------------------------------------
# Build the LangGraph pipeline
# -----------------------------------------------------------------------------
def build_agent():
    graph = StateGraph(AgentState)

    graph.add_node("keyword_diagnostic", keyword_diagnostic_node)
    graph.add_node("project_selector", project_selector_node)
    graph.add_node("resume_modifier", resume_modifier_node)

    graph.set_entry_point("keyword_diagnostic")
    graph.add_edge("keyword_diagnostic", "project_selector")
    graph.add_edge("project_selector", "resume_modifier")
    graph.add_edge("resume_modifier", END)

    return graph.compile()


# -----------------------------------------------------------------------------
# Main function called by FastAPI
# -----------------------------------------------------------------------------
def run_resume_agent(job_description: str, resume_text: str, projects: List[dict] = None) -> dict:
    if projects is None:
        projects = []

    agent = build_agent()

    result = agent.invoke({
        "job_description": job_description or "",
        "resume_text": resume_text or "",
        "projects": projects,
        "keywords_missing": [],
        "selected_projects": [],
        "tailored_resume": "",
        "diagnostic_report": ""
    })

    return {
        "diagnostic_report": result.get("diagnostic_report", ""),
        "missing_keywords": result.get("keywords_missing", []),
        "selected_projects": [p.get("name", "") for p in result.get("selected_projects", [])],
        "tailored_resume": result.get("tailored_resume", ""),
    }