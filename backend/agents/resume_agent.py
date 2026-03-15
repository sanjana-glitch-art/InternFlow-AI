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

def normalize_text(s: str) -> str:
    s = (s or "").lower().strip()
    s = s.replace("–", "-").replace("—", "-")
    s = re.sub(r"[^a-z0-9\+\#\.\-/ ]+", " ", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s


def normalize_keyword(k: str) -> str:
    k = normalize_text(k)
    synonyms = {
        "llms": "llm",
        "large language models": "llm",
        "rest api": "api",
        "restful api": "api",
        "apis": "api",
        "ci cd": "ci/cd",
        "cicd": "ci/cd",
        "machine learning": "ml",
        "deep learning": "dl",
        "computer vision": "cv",
        "natural language processing": "nlp",
        "amazon web services": "aws",
        "docker containers": "docker",
        "k8s": "kubernetes",
        "system verilog": "systemverilog",
        "rtl design": "rtl",
        "verilog hdl": "verilog",
    }
    return synonyms.get(k, k)


def compute_keyword_overlap(jd_keywords: List[str], present_keywords: List[str]) -> int:
    jd_set = {normalize_keyword(x) for x in jd_keywords if x}
    present_set = {normalize_keyword(x) for x in present_keywords if x}
    if not jd_set:
        return 0
    score = round(100 * len(jd_set & present_set) / len(jd_set))
    return max(0, min(100, score))

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
        "You are an ATS keyword analysis engine. "
        "Return ONLY valid JSON. No markdown, no commentary, no extra text."
    )

    jd = truncate(state.get("job_description", ""), 7000)
    resume = truncate(state.get("resume_text", ""), 9000)

    prompt = f"""
Analyze the JOB DESCRIPTION and RESUME.

TASK:
1. Extract the 12 most important ATS keywords from the JOB DESCRIPTION only.
2. Keywords must be concrete and resume-usable:
   - programming languages
   - frameworks/tools
   - cloud/devops/platforms
   - domain skills
   - role-specific responsibilities
3. Avoid generic words like: team, communication, motivated, problem-solving, fast-paced.
4. Prefer exact ATS phrases from the JD where useful.
5. Compare those JD keywords against the RESUME.
6. Mark a keyword as "present" if it is explicitly present or clearly equivalent in the resume.
7. Mark all remaining JD keywords as "missing".

OUTPUT JSON SCHEMA EXACTLY:
{{
  "jd_keywords": ["keyword1", "keyword2", "keyword3"],
  "present_keywords": ["keyword1", "keyword2"],
  "missing_keywords": ["keyword3"],
  "keyword_categories": {{
    "languages": ["..."],
    "frameworks_tools": ["..."],
    "cloud_devops": ["..."],
    "domain": ["..."],
    "responsibilities": ["..."]
  }},
  "summary": "1-2 sentence diagnosis"
}}

RULES:
- Use only keywords from the JOB DESCRIPTION.
- Do not invent keywords not supported by the JD.
- Do not include duplicates.
- Keep keyword strings short and ATS-friendly.
- Return JSON only.

JOB DESCRIPTION:
{jd}

RESUME:
{resume}
""".strip()

    resp = client.chat.completions.create(
        model=MODEL_DIAGNOSTIC,
        messages=[
            {"role": "system", "content": SYSTEM_JSON_ONLY},
            {"role": "user", "content": prompt},
        ],
        temperature=0.0,
        max_tokens=650,
    )

    raw = get_message_text(resp)

    if raw is None:
        state["keywords_missing"] = []
        state["diagnostic_report"] = json.dumps({
            "jd_keywords": [],
            "present_keywords": [],
            "missing_keywords": [],
            "match_score": 0,
            "summary": "Model returned no output."
        })
        return state

    data = extract_first_json_object(raw)

    if not isinstance(data, dict):
        state["keywords_missing"] = []
        state["diagnostic_report"] = json.dumps({
            "jd_keywords": [],
            "present_keywords": [],
            "missing_keywords": [],
            "match_score": 0,
            "summary": raw[:500]
        })
        return state

    jd_keywords = data.get("jd_keywords", []) or []
    present_keywords = data.get("present_keywords", []) or []
    missing_keywords = data.get("missing_keywords", []) or []

    # normalize + dedupe
    jd_keywords = list(dict.fromkeys([str(x).strip() for x in jd_keywords if str(x).strip()]))
    present_keywords = list(dict.fromkeys([str(x).strip() for x in present_keywords if str(x).strip()]))
    missing_keywords = list(dict.fromkeys([str(x).strip() for x in missing_keywords if str(x).strip()]))

    # recompute missing if model output is inconsistent
    jd_norm = {normalize_keyword(x): x for x in jd_keywords}
    present_norm = {normalize_keyword(x) for x in present_keywords}
    corrected_present = [orig for norm, orig in jd_norm.items() if norm in present_norm]
    corrected_missing = [orig for norm, orig in jd_norm.items() if norm not in present_norm]

    match_score = compute_keyword_overlap(jd_keywords, corrected_present)

    final_report = {
        "jd_keywords": jd_keywords,
        "present_keywords": corrected_present,
        "missing_keywords": corrected_missing,
        "keyword_categories": data.get("keyword_categories", {}),
        "summary": data.get("summary", ""),
        "match_score": match_score,
    }

    state["keywords_missing"] = corrected_missing
    state["diagnostic_report"] = json.dumps(final_report, indent=2)
    return state


# -----------------------------------------------------------------------------
# Node 2: Select best projects for this specific JD
# -----------------------------------------------------------------------------
def project_selector_node(state: AgentState) -> AgentState:
    projects = state.get("projects") or []
    if not projects:
        state["selected_projects"] = []
        return state

    compact_projects = []
    for p in projects[:30]:
        name = (p.get("name") or "").strip()
        desc = (p.get("description") or "").strip()
        if name:
            compact_projects.append({
                "name": name,
                "description": desc[:500]
            })

    if not compact_projects:
        state["selected_projects"] = []
        return state

    projects_json = json.dumps(compact_projects, indent=2)
    jd = truncate(state.get("job_description", ""), 5000)
    missing_keywords = state.get("keywords_missing", []) or []

    prompt = f"""
You are selecting the best portfolio projects for a specific job application.

TASK:
Select the EXACT TOP 3 projects from the provided PROJECT LIST that best match the JOB DESCRIPTION.

SELECTION CRITERIA:
1. Strong technical relevance to the JD
2. Demonstrates similar tools, frameworks, architectures, or responsibilities
3. Shows engineering depth, implementation skill, or measurable outcomes
4. Prefer projects aligned with software engineering, ML, data, systems, FPGA, embedded, APIs, cloud, or automation if the JD emphasizes them
5. Prefer projects that can help cover missing JD keywords when truthful
6. Select ONLY from the provided project names
7. Do NOT invent or rename projects

OUTPUT JSON EXACTLY:
{{
  "selected_project_names": ["Exact Name 1", "Exact Name 2", "Exact Name 3"],
  "reasons": [
    "why project 1 matches",
    "why project 2 matches",
    "why project 3 matches"
  ]
}}

JOB DESCRIPTION:
{jd}

MISSING KEYWORDS:
{", ".join(missing_keywords) if missing_keywords else "None"}

PROJECT LIST:
{projects_json}
""".strip()

    resp = client.chat.completions.create(
        model=MODEL_PROJECTS,
        messages=[
            {
                "role": "system",
                "content": "Return ONLY valid JSON. No markdown. No commentary."
            },
            {"role": "user", "content": prompt}
        ],
        temperature=0.0,
        max_tokens=350,
    )

    raw = get_message_text(resp)

    if not raw:
        state["selected_projects"] = compact_projects[:3]
        return state

    data = extract_first_json_object(raw)

    if not isinstance(data, dict):
        state["selected_projects"] = compact_projects[:3]
        return state

    selected_names = data.get("selected_project_names", []) or []
    selected_names = [str(x).strip() for x in selected_names if str(x).strip()]

    selected_lookup = {p["name"]: p for p in compact_projects}
    selected_projects = [selected_lookup[name] for name in selected_names if name in selected_lookup]

    # backfill if model returns fewer than 3
    if len(selected_projects) < min(3, len(compact_projects)):
        used = {p["name"] for p in selected_projects}
        for p in compact_projects:
            if p["name"] not in used:
                selected_projects.append(p)
            if len(selected_projects) >= min(3, len(compact_projects)):
                break

    state["selected_projects"] = selected_projects[:3]
    return state

# -----------------------------------------------------------------------------
# Node 3: Rewrite resume tailored to the JD
# -----------------------------------------------------------------------------
def resume_modifier_node(state: AgentState) -> AgentState:
    selected_projects = state.get("selected_projects") or []
    selected_projects_text = "\n".join(
        [f"- {p.get('name','')}: {p.get('description','')}" for p in selected_projects]
    ).strip() or "Use the strongest existing projects already present in the resume."

    missing_keywords = state.get("keywords_missing") or []
    missing_keywords_text = ", ".join(missing_keywords) if missing_keywords else "None"

    prompt = f"""
You are an expert ATS resume editor.

TASK:
Rewrite the resume so it is better aligned with the JOB DESCRIPTION while staying 100% truthful.

IMPORTANT RULES:
1. Return ONLY the rewritten resume text.
2. Do NOT use markdown fences.
3. Do NOT fabricate experience, projects, tools, metrics, dates, responsibilities, or achievements.
4. Keep the same overall resume structure and section order if possible.
5. Preserve the candidate's real background and strongest technical areas.
6. Make the writing ATS-friendly and concise.
7. Use strong action verbs.
8. Prefer technical, measurable, implementation-focused bullets.
9. Naturally incorporate relevant missing keywords ONLY when they are genuinely supported by the original resume or selected projects.
10. Highlight the selected projects prominently in the Projects section.
11. Keep exactly 3 selected projects if at least 3 are available.
12. If space is tight, shorten bullets instead of dropping the selected projects.

JOB DESCRIPTION:
{truncate(state.get("job_description", ""), 7000)}

ORIGINAL RESUME:
{truncate(state.get("resume_text", ""), 10000)}

SELECTED PROJECTS TO PRIORITIZE:
{selected_projects_text}

IMPORTANT MISSING KEYWORDS TO INCORPORATE IF TRUTHFUL:
{missing_keywords_text}

REWRITE GOALS:
- Match JD language more closely
- Improve summary
- Strengthen experience bullets
- Make projects more relevant to the target role
- Improve ATS keyword coverage
- Keep output professional and recruiter-friendly

Return only the final rewritten resume text.
""".strip()

    resp = client.chat.completions.create(
        model=MODEL_REWRITE,
        messages=[
            {
                "role": "system",
                "content": "You are a precise ATS resume rewriter. Output only the final resume text."
            },
            {"role": "user", "content": prompt}
        ],
        temperature=0.15,
        max_tokens=1800,
    )

    raw = get_message_text(resp)
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

    diagnostic_obj = {}
    raw_report = result.get("diagnostic_report", "")
    if isinstance(raw_report, str) and raw_report.strip():
        try:
            diagnostic_obj = json.loads(raw_report)
        except Exception:
            diagnostic_obj = {
                "jd_keywords": [],
                "present_keywords": [],
                "missing_keywords": result.get("keywords_missing", []),
                "match_score": 0,
                "summary": raw_report[:500],
            }

    selected_projects = result.get("selected_projects", []) or []

    return {
        "diagnostic_report": raw_report,
        "diagnostic": diagnostic_obj,
        "missing_keywords": diagnostic_obj.get("missing_keywords", result.get("keywords_missing", [])),
        "present_keywords": diagnostic_obj.get("present_keywords", []),
        "jd_keywords": diagnostic_obj.get("jd_keywords", []),
        "match_score": diagnostic_obj.get("match_score", 0),
        "selected_projects": selected_projects,
        "tailored_resume": result.get("tailored_resume", ""),
    }