from openai import OpenAI
from typing import TypedDict, List, Optional
from langgraph.graph import StateGraph, END
import json
import re
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key=os.environ.get("NVIDIA_API_KEY", "YOUR_NVIDIA_API_KEY")
)

MODEL_DIAGNOSTIC = "nvidia/llama-3.3-nemotron-super-49b-v1"
MODEL_PROJECTS   = "nvidia/llama-3.1-nemotron-nano-8b-v1"
MODEL_REWRITE    = "nvidia/llama-3.3-nemotron-super-49b-v1"

# ── State ─────────────────────────────────────────────────────────────────────
class AgentState(TypedDict):
    job_description: str
    resume_text: str
    projects: List[dict]
    keywords_missing: List[str]
    keywords_present: List[str]
    match_score: float
    selected_projects: List[dict]
    tailored_resume: str
    diagnostic_report: str

# ── Helpers ───────────────────────────────────────────────────────────────────
def extract_json(raw: str, kind: str = "object"):
    raw = re.sub(r"```json", "", raw)
    raw = re.sub(r"```", "", raw)
    raw = re.sub(r"//[^\n]*", "", raw)
    raw = raw.strip()

    if kind == "object":
        start = raw.find("{")
        end   = raw.rfind("}") + 1
    else:
        start = raw.find("[")
        end   = raw.rfind("]") + 1

    if start < 0 or end <= start:
        return None

    candidate = raw[start:end]
    candidate = re.sub(r",\s*([}\]])", r"\1", candidate)

    try:
        return json.loads(candidate)
    except Exception:
        return None

def normalize(s: str) -> str:
    """Lowercase, strip punctuation for loose matching."""
    s = s.lower().strip()
    s = re.sub(r"[^a-z0-9\+\#\./ ]+", " ", s)
    return re.sub(r"\s+", " ", s).strip()

def keyword_in_resume(keyword: str, resume_text: str) -> bool:
    """Check if a keyword or its variants appear in the resume."""
    kw = normalize(keyword)
    resume = normalize(resume_text)

    # Direct match
    if kw in resume:
        return True

    # Synonym map for common abbreviations
    synonyms = {
        "machine learning": ["ml", "machine learning"],
        "ml": ["ml", "machine learning"],
        "deep learning": ["dl", "deep learning"],
        "natural language processing": ["nlp", "natural language processing"],
        "nlp": ["nlp", "natural language processing"],
        "computer vision": ["cv", "computer vision"],
        "cv": ["cv", "computer vision"],
        "large language model": ["llm", "large language model"],
        "llm": ["llm", "large language model"],
        "reinforcement learning": ["rl", "reinforcement learning"],
        "pytorch": ["pytorch", "torch"],
        "tensorflow": ["tensorflow", "tf", "keras"],
        "kubernetes": ["kubernetes", "k8s"],
        "amazon web services": ["aws", "amazon web services"],
        "aws": ["aws", "amazon web services"],
        "google cloud": ["gcp", "google cloud"],
        "gcp": ["gcp", "google cloud"],
        "ci/cd": ["ci/cd", "cicd", "continuous integration"],
        "restful api": ["rest", "restful", "api"],
        "api": ["api", "rest", "restful"],
    }
    for variant in synonyms.get(kw, []):
        if variant in resume:
            return True

    # Partial word match for compound terms (e.g. "scikit" matches "scikit-learn")
    words = kw.split()
    if len(words) >= 2:
        if all(w in resume for w in words):
            return True

    return False

# ── Node 1: Keyword Diagnostic ────────────────────────────────────────────────
def keyword_diagnostic_node(state: AgentState) -> AgentState:
    """
    Extract JD keywords then check each one against the RESUME TEXT directly.
    This ensures keyword matching is based on actual resume content.
    """
    jd     = state["job_description"][:7000]
    resume = state["resume_text"]

    # Step 1: Extract JD keywords using Nemotron
    prompt = f"""You are an ATS keyword extraction engine.

Extract the 15 most important technical keywords from this JOB DESCRIPTION only.
Focus on: programming languages, frameworks, tools, cloud platforms, domain skills.
Avoid generic words like: communication, teamwork, motivated, fast-paced.

JOB DESCRIPTION:
{jd}

Return ONLY valid JSON, no explanation:
{{
  "jd_keywords": ["keyword1", "keyword2", "keyword3"]
}}"""

    response = client.chat.completions.create(
        model=MODEL_DIAGNOSTIC,
        messages=[
            {"role": "system", "content": "Return ONLY valid JSON. No markdown, no commentary."},
            {"role": "user",   "content": prompt}
        ],
        temperature=0.0,
        max_tokens=400
    )

    raw  = response.choices[0].message.content.strip()
    data = extract_json(raw, "object")
    jd_keywords = []
    if data and isinstance(data, dict):
        jd_keywords = [str(k).strip() for k in data.get("jd_keywords", []) if str(k).strip()]

    # Step 2: Check each keyword against the ACTUAL resume text
    present_keywords = []
    missing_keywords = []

    for kw in jd_keywords:
        if keyword_in_resume(kw, resume):
            present_keywords.append(kw)
        else:
            missing_keywords.append(kw)

    # Step 3: Calculate match score
    match_score = round(100 * len(present_keywords) / max(len(jd_keywords), 1))

    state["keywords_present"]  = present_keywords
    state["keywords_missing"]  = missing_keywords
    state["match_score"]       = float(match_score)
    state["diagnostic_report"] = json.dumps({
        "jd_keywords":      jd_keywords,
        "present_keywords": present_keywords,
        "missing_keywords": missing_keywords,
        "match_score":      match_score,
    })

    return state

# ── Node 2: Project Selector ──────────────────────────────────────────────────
def project_selector_node(state: AgentState) -> AgentState:
    """
    Select the 3 most relevant projects from the portfolio for this specific JD.
    Uses the full project list and scores by relevance, NOT just first 3.
    """
    projects = state.get("projects") or []
    if not projects:
        state["selected_projects"] = []
        return state

    jd              = state["job_description"][:5000]
    missing_kw      = state.get("keywords_missing", [])
    missing_kw_str  = ", ".join(missing_kw[:10]) if missing_kw else "None"

    # Build compact project list with index
    project_list = []
    for i, p in enumerate(projects[:30]):
        name = (p.get("name") or "").strip()
        desc = (p.get("description") or "").strip()[:400]
        if name:
            project_list.append(f'{i}. "{name}": {desc}')

    projects_text = "\n".join(project_list)

    prompt = f"""You are a technical recruiter selecting the best portfolio projects for a job application.

TASK: From the PROJECT LIST below, select the TOP 3 projects that best match the JOB DESCRIPTION.

SELECTION RULES:
1. Read ALL projects carefully before deciding
2. Select projects with the strongest technical match to the JD
3. Prefer projects that demonstrate tools, frameworks, or domains mentioned in the JD
4. Prefer projects that help cover the MISSING KEYWORDS
5. Do NOT always pick the first 3 — pick the MOST RELEVANT 3
6. Return ONLY the exact project names from the list

JOB DESCRIPTION:
{jd}

MISSING KEYWORDS TO COVER:
{missing_kw_str}

PROJECT LIST:
{projects_text}

Return ONLY valid JSON array with exactly 3 project names:
["Exact Project Name 1", "Exact Project Name 2", "Exact Project Name 3"]"""

    response = client.chat.completions.create(
        model=MODEL_PROJECTS,
        messages=[
            {"role": "system", "content": "Return ONLY a valid JSON array. No markdown, no commentary."},
            {"role": "user",   "content": prompt}
        ],
        temperature=0.1,
        max_tokens=200
    )

    raw            = response.choices[0].message.content.strip()
    selected_names = extract_json(raw, "array")

    if selected_names and isinstance(selected_names, list):
        # Match by exact name first, then fuzzy
        project_lookup = {p["name"]: p for p in projects if p.get("name")}
        matched = []
        for name in selected_names:
            if name in project_lookup:
                matched.append(project_lookup[name])
            else:
                # fuzzy: find closest name
                for pname, proj in project_lookup.items():
                    if normalize(name) in normalize(pname) or normalize(pname) in normalize(name):
                        if proj not in matched:
                            matched.append(proj)
                            break

        # Backfill if fewer than 3 matched
        if len(matched) < min(3, len(projects)):
            used_names = {p["name"] for p in matched}
            for p in projects:
                if p.get("name") not in used_names:
                    matched.append(p)
                if len(matched) >= min(3, len(projects)):
                    break

        state["selected_projects"] = matched[:3]
    else:
        # Fallback: pick 3 most relevant by keyword overlap
        scored = []
        jd_lower = jd.lower()
        for p in projects:
            desc  = (p.get("description","") + " " + p.get("name","")).lower()
            score = sum(1 for kw in (missing_kw + state.get("keywords_present",[])) if normalize(kw) in desc)
            scored.append((score, p))
        scored.sort(key=lambda x: x[0], reverse=True)
        state["selected_projects"] = [p for _, p in scored[:3]]

    return state

# ── Node 3: Resume Rewriter ───────────────────────────────────────────────────
def resume_modifier_node(state: AgentState) -> AgentState:
    selected_text = "\n".join([
        f"- {p.get('name','')}: {p.get('description','')[:300]}"
        for p in state.get("selected_projects", [])
    ]) or "Use existing projects from resume."

    missing = ", ".join(state.get("keywords_missing", [])) or "None"

    prompt = f"""You are an expert ATS resume writer.

Rewrite the resume below to better match the job description while staying 100% truthful.

RULES:
- Return ONLY the rewritten resume text, no explanation, no markdown fences
- Do NOT fabricate experience, tools, metrics, or skills
- Keep the same overall structure
- Naturally incorporate missing keywords where truthful
- Rewrite bullet points to match JD language
- Highlight the selected projects prominently
- Keep it ATS-friendly and concise
- Use strong action verbs

JOB DESCRIPTION:
{state["job_description"][:5000]}

ORIGINAL RESUME:
{state["resume_text"][:8000]}

PROJECTS TO HIGHLIGHT:
{selected_text}

MISSING KEYWORDS TO ADD (only where truthful):
{missing}

Return the complete rewritten resume text only:"""

    response = client.chat.completions.create(
        model=MODEL_REWRITE,
        messages=[
            {"role": "system", "content": "You are a precise ATS resume rewriter. Output only the final resume text, no fences, no commentary."},
            {"role": "user",   "content": prompt}
        ],
        temperature=0.2,
        max_tokens=2000
    )

    raw = response.choices[0].message.content.strip()
    # Strip any accidental markdown fences
    if raw.startswith("```"): raw = raw.split("\n", 1)[1]
    if raw.endswith("```"):   raw = raw.rsplit("```", 1)[0]
    state["tailored_resume"] = raw.strip()
    return state

# ── Build pipeline ────────────────────────────────────────────────────────────
def build_agent():
    graph = StateGraph(AgentState)
    graph.add_node("keyword_diagnostic", keyword_diagnostic_node)
    graph.add_node("project_selector",   project_selector_node)
    graph.add_node("resume_modifier",    resume_modifier_node)
    graph.set_entry_point("keyword_diagnostic")
    graph.add_edge("keyword_diagnostic", "project_selector")
    graph.add_edge("project_selector",   "resume_modifier")
    graph.add_edge("resume_modifier",    END)
    return graph.compile()

# ── Entry point ───────────────────────────────────────────────────────────────
def run_resume_agent(job_description: str, resume_text: str, projects: List[dict] = None) -> dict:
    if projects is None:
        projects = []

    result = build_agent().invoke({
        "job_description": job_description or "",
        "resume_text":     resume_text     or "",
        "projects":        projects,
        "keywords_missing":  [],
        "keywords_present":  [],
        "match_score":       0.0,
        "selected_projects": [],
        "tailored_resume":   "",
        "diagnostic_report": ""
    })

    return {
        "status": "success",
        "diagnostic": {
            "missing_keywords": result.get("keywords_missing", []),
            "present_keywords": result.get("keywords_present", []),
            "match_score":      result.get("match_score", 0),
        },
        "present_keywords":  result.get("keywords_present", []),
        "missing_keywords":  result.get("keywords_missing", []),
        "match_score":       result.get("match_score", 0),
        "selected_projects": [
            {"name": p.get("name",""), "description": p.get("description","")}
            for p in result.get("selected_projects", [])
        ],
        "tailored_resume": result.get("tailored_resume", ""),
    }