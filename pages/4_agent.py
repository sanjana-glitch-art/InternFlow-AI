import streamlit as st
import requests
import json
import re
import difflib

st.set_page_config(
    page_title="InternFlow AI – Nemotron Agent",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&family=Outfit:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500;700&display=swap');

#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
[data-testid="collapsedControl"] {display: none;}
* { box-sizing: border-box; }

:root {
    --lav300: #d8b4fe; --lav400: #c084fc; --lav500: #a855f7;
    --bg: #08080f; --bg2: #0e0e1a; --bg3: #131325;
    --txt: #f1f0f8; --txt2: #c4c2dc; --muted: #7c7a9a; --faint: #2d2b45;
    --bdr: rgba(168,85,247,0.18); --bdr2: rgba(168,85,247,0.38);
    --green: #6ee7b7; --amber: #fcd34d; --rose: #fca5a5; --indigo: #a5b4fc;
}

.stApp { background: var(--bg) !important; font-family: 'Outfit', sans-serif; color: var(--txt); }
.block-container { padding: 28px 48px 72px !important; max-width: 1400px !important; margin: 0 auto !important; }

/* Inputs */
.stTextArea > div > div > textarea {
    background: rgba(255,255,255,0.03) !important;
    border: 1px solid rgba(168,85,247,0.22) !important;
    border-radius: 12px !important;
    color: var(--txt) !important;
    font-family: 'Outfit', sans-serif !important;
    font-size: 14px !important;
}
.stTextArea label, .stTextInput label, .stSelectbox label {
    color: var(--muted) !important;
    font-family: 'Outfit', sans-serif !important;
    font-size: 13px !important; font-weight: 500 !important;
}
.stTextInput > div > div > input {
    background: rgba(255,255,255,0.03) !important;
    border: 1px solid rgba(168,85,247,0.22) !important;
    border-radius: 12px !important; color: var(--txt) !important;
    font-family: 'Outfit', sans-serif !important; font-size: 14px !important;
}
.stSelectbox > div > div {
    background: rgba(255,255,255,0.03) !important;
    border: 1px solid rgba(168,85,247,0.22) !important;
    border-radius: 12px !important; color: var(--txt) !important;
}

/* Buttons */
.stButton > button {
    background: linear-gradient(135deg, #7c3aed, #6d28d9) !important;
    color: #fff !important; border: none !important; border-radius: 10px !important;
    font-family: 'Outfit', sans-serif !important; font-size: 14px !important;
    font-weight: 600 !important; padding: 9px 20px !important;
    height: auto !important; transition: all 0.2s !important;
}
.stButton > button:hover { opacity: 0.85 !important; transform: translateY(-1px) !important; }
.stButton > button[kind="secondary"] {
    background: rgba(168,85,247,0.07) !important;
    border: 1px solid rgba(168,85,247,0.28) !important; color: var(--lav300) !important;
}
.stDownloadButton > button {
    background: rgba(110,231,183,0.1) !important;
    border: 1px solid rgba(110,231,183,0.3) !important;
    color: #6ee7b7 !important; border-radius: 10px !important;
    font-family: 'Outfit', sans-serif !important; font-size: 13px !important;
    font-weight: 600 !important; padding: 8px 18px !important; height: auto !important;
}
.stDownloadButton > button:hover { background: rgba(110,231,183,0.18) !important; }

/* Nav */
.nav-logo {
    font-family: 'Outfit', sans-serif; font-size: 21px; font-weight: 800;
    background: linear-gradient(135deg, #c4b5fd, #a78bfa);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;
}
.nav-tagline { font-family: 'JetBrains Mono', monospace; font-size: 10px; color: var(--faint); letter-spacing: 0.12em; margin-top: 2px; }

/* Divider */
.div { border: none; height: 1px; background: linear-gradient(90deg, transparent, rgba(168,85,247,0.2), transparent); margin: 20px 0; }

/* Page header */
.page-hd { font-family: 'Instrument Serif', serif; font-size: clamp(28px,3.5vw,44px); font-weight: 400; color: var(--txt); letter-spacing: -1px; margin: 0 0 5px; line-height: 1.1; }
.page-hd em { font-style: italic; color: var(--lav300); }
.page-sub { font-size: 15px; color: var(--muted); font-weight: 300; }
.page-sub span { color: var(--lav300); font-weight: 500; }

/* Job banner */
.job-banner {
    background: rgba(168,85,247,0.05);
    border: 1px solid rgba(168,85,247,0.28);
    border-radius: 16px; padding: 18px 24px; margin-bottom: 4px;
    position: relative; overflow: hidden;
}
.job-banner::before {
    content: ''; position: absolute; top: 0; left: 0; right: 0; height: 1px;
    background: linear-gradient(90deg, transparent, rgba(168,85,247,0.4), transparent);
}
.jb-title { font-size: 18px; font-weight: 700; color: var(--txt); margin-bottom: 4px; }
.jb-company { font-size: 14px; color: var(--lav400); font-weight: 600; }
.jb-desc { font-size: 13px; color: var(--muted); margin-top: 8px; line-height: 1.6; }

/* Input panel */
.input-panel {
    background: rgba(255,255,255,0.018);
    border: 1px solid var(--bdr);
    border-radius: 16px; padding: 22px 24px;
}

/* Run button wrapper */
.run-wrap {
    background: rgba(168,85,247,0.04);
    border: 1px solid rgba(168,85,247,0.2);
    border-radius: 16px; padding: 24px; text-align: center; margin: 8px 0;
}

/* ── Results ── */
/* Section header */
.res-sec {
    display: flex; align-items: center; gap: 10px;
    margin: 28px 0 16px;
}
.res-sec-icon {
    width: 36px; height: 36px; border-radius: 10px;
    display: flex; align-items: center; justify-content: center;
    font-size: 18px; flex-shrink: 0;
}
.res-sec-title { font-family: 'Outfit', sans-serif; font-size: 20px; font-weight: 700; color: var(--txt); }
.res-sec-sub { font-size: 13px; color: var(--muted); margin-top: 1px; }

/* ATS Score ring */
.ats-wrap { text-align: center; padding: 20px 0; }
.ats-ring {
    width: 120px; height: 120px; border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    flex-direction: column; border: 4px solid; margin: 0 auto 12px;
}
.ats-num { font-family: 'Instrument Serif', serif; font-size: 36px; line-height: 1; }
.ats-lbl { font-family: 'JetBrains Mono', monospace; font-size: 9px; letter-spacing: 0.1em; margin-top: 3px; }
.ats-verdict { font-size: 14px; font-weight: 600; margin-top: 8px; }

/* Keyword pills */
.kw-section { margin-bottom: 16px; }
.kw-cat { font-family: 'JetBrains Mono', monospace; font-size: 10px; text-transform: uppercase; letter-spacing: 0.12em; margin-bottom: 8px; }
.kw-present {
    display: inline-flex; align-items: center; gap: 5px;
    background: rgba(110,231,183,0.1); border: 1px solid rgba(110,231,183,0.3);
    color: #6ee7b7; padding: 4px 12px; border-radius: 100px;
    font-size: 12px; font-family: 'JetBrains Mono', monospace; margin: 3px;
}
.kw-missing {
    display: inline-flex; align-items: center; gap: 5px;
    background: rgba(252,165,165,0.08); border: 1px solid rgba(252,165,165,0.3);
    color: #fca5a5; padding: 4px 12px; border-radius: 100px;
    font-size: 12px; font-family: 'JetBrains Mono', monospace; margin: 3px;
}

/* Info card */
.info-card {
    background: rgba(255,255,255,0.022);
    border: 1px solid var(--bdr); border-radius: 14px;
    padding: 18px 22px; margin-bottom: 10px; position: relative; overflow: hidden;
}
.info-card::before {
    content: ''; position: absolute; top: 0; left: 0; right: 0; height: 1px;
    background: linear-gradient(90deg, transparent, rgba(168,85,247,0.2), transparent);
}

/* Project card */
.proj-card {
    background: rgba(255,255,255,0.02);
    border: 1px solid var(--bdr); border-radius: 16px;
    padding: 20px 24px; margin-bottom: 12px; position: relative; overflow: hidden;
}
.proj-card::before {
    content: ''; position: absolute; top: 0; left: 0; bottom: 0; width: 3px;
    background: linear-gradient(180deg, #a855f7, #7c3aed);
}
.proj-num {
    font-family: 'JetBrains Mono', monospace; font-size: 10px;
    color: var(--lav400); letter-spacing: 0.1em; margin-bottom: 6px;
}
.proj-name { font-family: 'Outfit', sans-serif; font-size: 17px; font-weight: 700; color: var(--txt); margin-bottom: 8px; }
.proj-step {
    display: flex; align-items: flex-start; gap: 10px;
    background: rgba(255,255,255,0.025); border-radius: 8px;
    padding: 8px 12px; margin-bottom: 6px;
}
.proj-step-num {
    background: rgba(168,85,247,0.25); color: var(--lav300);
    width: 22px; height: 22px; border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-family: 'JetBrains Mono', monospace; font-size: 10px;
    flex-shrink: 0; font-weight: 700;
}
.proj-step-text { font-size: 13px; color: var(--txt2); line-height: 1.6; }

/* Side by side diff */
.diff-panel {
    background: rgba(255,255,255,0.018);
    border: 1px solid var(--bdr); border-radius: 14px;
    padding: 16px 18px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 12px; line-height: 1.8;
    max-height: 420px; overflow-y: auto;
    white-space: pre-wrap;
    color: var(--txt2);
}
.diff-add { background: rgba(110,231,183,0.15); color: #6ee7b7; display: block; }
.diff-rem { background: rgba(252,165,165,0.1); color: #fca5a5; display: block; text-decoration: line-through; opacity: 0.6; }
.diff-neu { display: block; }

/* Resume render (white doc) */
.resume-render {
    background: #ffffff; border-radius: 14px;
    padding: 36px 44px; max-height: 500px; overflow-y: auto;
    font-family: 'Georgia', serif; font-size: 13px;
    color: #1a1a1a; line-height: 1.75;
    box-shadow: 0 4px 40px rgba(0,0,0,0.5);
}
.resume-render h1 { font-size: 21px; font-weight: 700; color: #111; margin: 0 0 3px; text-align: center; }
.resume-render h2 { font-size: 12px; font-weight: 700; color: #333; text-transform: uppercase; letter-spacing: 0.12em; border-bottom: 1.5px solid #ddd; padding-bottom: 3px; margin: 16px 0 7px; }
.resume-render h3 { font-size: 13px; font-weight: 700; color: #222; margin: 7px 0 2px; }
.resume-render p  { margin: 2px 0 5px; color: #333; }
.resume-render .contact-line { text-align: center; font-size: 11.5px; color: #555; margin-bottom: 12px; }
.resume-render ul { margin: 3px 0 7px 16px; padding: 0; }
.resume-render li { margin-bottom: 3px; color: #333; }

/* Weak bullet card */
.weak-bullet {
    background: rgba(252,165,165,0.05);
    border: 1px solid rgba(252,165,165,0.2);
    border-left: 3px solid #fca5a5;
    border-radius: 8px; padding: 10px 14px; margin-bottom: 8px;
}
.weak-bullet-text { font-size: 13px; color: var(--rose); font-family: 'JetBrains Mono', monospace; margin-bottom: 4px; }
.weak-bullet-fix { font-size: 12px; color: var(--muted); }

/* Readme box */
.readme-box {
    background: #0d1117; border: 1px solid #30363d;
    border-radius: 12px; padding: 20px 22px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 12px; color: #c9d1d9; line-height: 1.7;
    max-height: 360px; overflow-y: auto; white-space: pre-wrap;
}

/* Spinner override */
.stSpinner > div { border-color: var(--lav500) transparent transparent transparent !important; }

/* Processing overlay */
.processing-card {
    background: rgba(168,85,247,0.05);
    border: 1px solid rgba(168,85,247,0.25);
    border-radius: 16px; padding: 32px 24px; text-align: center;
}
.processing-title { font-family: 'Instrument Serif', serif; font-size: 22px; color: var(--txt); margin-bottom: 8px; }
.processing-sub { font-size: 14px; color: var(--muted); }
.step-item {
    display: flex; align-items: center; gap: 10px;
    padding: 8px 0; font-size: 13px; color: var(--muted);
}
.step-dot {
    width: 8px; height: 8px; border-radius: 50%;
    background: var(--faint); flex-shrink: 0;
}
.step-dot-active { background: var(--lav400); box-shadow: 0 0 8px rgba(192,132,252,0.6); }
.step-dot-done { background: var(--green); }
</style>
""", unsafe_allow_html=True)

API = "http://127.0.0.1:8000"

# ── Helpers ───────────────────────────────────────────────────────────────────
def try_parse_json(text):
    if not text or not isinstance(text, str):
        return {}
    cleaned = re.sub(r"^```(?:json)?\s*|\s*```$", "", text.strip(), flags=re.IGNORECASE)
    m = re.search(r"\{.*\}", cleaned, flags=re.DOTALL)
    if not m:
        return {}
    try:
        return json.loads(m.group(0))
    except Exception:
        return {}

def normalize_projects(selected, all_projects):
    if not selected:
        return []
    if isinstance(selected, list) and selected and isinstance(selected[0], dict):
        return [{"name": p.get("name",""), "description": p.get("description",""),
                 "rewritten_description": p.get("rewritten_description","")} for p in selected]
    if isinstance(selected, list) and selected and isinstance(selected[0], str):
        name_set = set(selected)
        out = [{"name": p.get("name",""), "description": p.get("description",""),
                "rewritten_description": ""} for p in (all_projects or []) if p.get("name") in name_set]
        return out or [{"name": n, "description": "", "rewritten_description": ""} for n in selected]
    return []

def text_to_resume_html(text):
    SECTIONS = {"education","experience","work experience","projects","skills",
                "technical skills","summary","objective","certifications",
                "publications","awards","leadership","activities","interests","languages"}
    lines = text.strip().splitlines()
    html  = ["<div class='resume-render'>"]
    first = True
    contact = []
    in_contact = True
    for raw in lines:
        line = raw.strip()
        if not line:
            continue
        lower = line.lower().rstrip(":").strip()
        if first:
            html.append("<h1>" + line + "</h1>")
            first = False
            continue
        if in_contact and len(line) < 100 and lower not in SECTIONS:
            contact.append(line)
            if len(contact) <= 3:
                continue
            else:
                in_contact = False
                html.append("<div class='contact-line'>" + " &nbsp;|&nbsp; ".join(contact) + "</div>")
                contact = []
                continue
        if contact:
            html.append("<div class='contact-line'>" + " &nbsp;|&nbsp; ".join(contact) + "</div>")
            contact = []
            in_contact = False
        if lower in SECTIONS or (line.isupper() and 3 < len(line) < 40):
            html.append("<h2>" + line.title() + "</h2>")
            continue
        if line.startswith(("•","-","·","*","–","▪")):
            html.append("<li>" + re.sub(r"^[•\-·*–▪]\s*", "", line) + "</li>")
            continue
        if re.match(r"^[A-Z][^a-z]{0,3}[A-Z]", line) and len(line) < 80 and "|" in line:
            html.append("<h3>" + line + "</h3>")
            continue
        html.append("<p>" + line + "</p>")
    if contact:
        html.append("<div class='contact-line'>" + " &nbsp;|&nbsp; ".join(contact) + "</div>")
    html.append("</div>")
    return "\n".join(html)

def generate_pdf_bytes(content, name="resume"):
    try:
        from fpdf import FPDF
        SECTIONS = {"education","experience","work experience","projects","skills",
                    "technical skills","summary","objective","certifications","awards","leadership"}
        pdf = FPDF(format="Letter")
        pdf.set_margins(18, 18, 18)
        pdf.add_page()
        lines = content.strip().splitlines()
        first = True
        for raw in lines:
            line = raw.strip()
            if not line:
                pdf.ln(2); continue
            lower = line.lower().rstrip(":").strip()
            if first:
                pdf.set_font("Helvetica","B",16)
                pdf.cell(0,8,line[:80], new_x="LMARGIN", new_y="NEXT",align="C")
                first = False; continue
            if lower in SECTIONS or (line.isupper() and 3 < len(line) < 40):
                pdf.ln(3); pdf.set_font("Helvetica","B",10)
                pdf.set_text_color(60,60,60)
                pdf.cell(0,6,line.upper(), new_x="LMARGIN", new_y="NEXT")
                pdf.set_draw_color(180,180,180)
                pdf.line(pdf.get_x(), pdf.get_y(), pdf.get_x()+174, pdf.get_y())
                pdf.ln(2); pdf.set_text_color(0,0,0); continue
            if line.startswith(("•","-","·","*","–","▪")):
                pdf.set_font("Helvetica","",9)
                pdf.multi_cell(0,5,"  • " + line.lstrip("•-·*–▪ ")[:200]); continue
            pdf.set_font("Helvetica","",9)
            pdf.multi_cell(0,5,line[:200])
        return bytes(pdf.output())
    except Exception:
        return content.encode("utf-8")

def build_diff_html(old_text, new_text):
    old_lines = old_text.splitlines()
    new_lines = new_text.splitlines()
    differ = difflib.unified_diff(old_lines, new_lines, lineterm="", n=2)
    parts = []
    for line in differ:
        if line.startswith("+++") or line.startswith("---") or line.startswith("@@"):
            continue
        if line.startswith("+"):
            parts.append("<span class='diff-add'>+ " + line[1:].strip() + "</span>")
        elif line.startswith("-"):
            parts.append("<span class='diff-rem'>- " + line[1:].strip() + "</span>")
        else:
            parts.append("<span class='diff-neu'>  " + line.strip() + "</span>")
    return "\n".join(parts) if parts else "<span style='color:var(--muted)'>No diff available — originals may be identical.</span>"

def score_color(s):
    if s >= 70: return "#6ee7b7", "rgba(16,185,129,0.13)", "rgba(16,185,129,0.5)"
    if s >= 50: return "#fcd34d", "rgba(245,158,11,0.1)",  "rgba(245,158,11,0.4)"
    return "#fca5a5", "rgba(239,68,68,0.08)", "rgba(239,68,68,0.35)"

def weak_bullets(resume_text):
    """Find weak bullet points (short, no metrics, start with was/is/helped)."""
    weak = []
    WEAK_STARTS = ("was ", "is ", "helped ", "assisted ", "worked on ", "did ", "made ", "created a ")
    for line in resume_text.splitlines():
        s = line.strip()
        if not s.startswith(("•","-","·","*","–","▪")):
            continue
        bullet = re.sub(r"^[•\-·*–▪]\s*", "", s)
        if len(bullet) < 40:
            weak.append((bullet, "Too short — add context, tools, and impact."))
        elif any(bullet.lower().startswith(w) for w in WEAK_STARTS):
            weak.append((bullet, "Avoid passive starts. Use strong action verbs like 'Built', 'Designed', 'Reduced'."))
        elif not any(c.isdigit() for c in bullet):
            weak.append((bullet, "No metrics found. Add numbers: % improvement, records processed, latency reduced."))
    return weak[:6]

# ── Session ───────────────────────────────────────────────────────────────────
if "agent_result"   not in st.session_state: st.session_state.agent_result   = None
if "agent_jd"       not in st.session_state: st.session_state.agent_jd       = ""
if "agent_resume"   not in st.session_state: st.session_state.agent_resume   = ""
if "diff_view"      not in st.session_state: st.session_state.diff_view      = "tailored"

profile      = st.session_state.get("profile", {})
selected_job = st.session_state.get("selected_job", None)
projects     = st.session_state.get("projects", [])

# ── Navbar ────────────────────────────────────────────────────────────────────
c1, c2, c3, c4, c5 = st.columns([3, 1, 1, 1, 1])
with c1:
    st.markdown(
        "<div class='nav-logo'>🚀 InternFlow AI</div>"
        "<div class='nav-tagline'>AI-POWERED CAREER PLATFORM</div>",
        unsafe_allow_html=True)
with c2:
    if st.button("📝 Profile",  use_container_width=True): st.switch_page("pages/2_onboarding.py")
with c3:
    if st.button("💼 Jobs",     use_container_width=True): st.switch_page("pages/3_jobs.py")
with c4:
    if st.button("🤖 Agent",    use_container_width=True, type="primary"): pass
with c5:
    if st.button("📂 Arsenal",  use_container_width=True): st.switch_page("pages/5_resume_arsenal.py")

st.markdown("<div class='div'></div>", unsafe_allow_html=True)

# ── Page header ───────────────────────────────────────────────────────────────
st.markdown(
    "<div class='page-hd'>Nemotron <em>Agent</em></div>"
    "<p class='page-sub'>Powered by <span>NVIDIA Nemotron + LangGraph</span> · "
    "Analyzes JD · Rewrites resume · Scores ATS fit</p>",
    unsafe_allow_html=True)

st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)

# ── Job banner ────────────────────────────────────────────────────────────────
if selected_job:
    locs = ", ".join(selected_job.get("locations", []))
    desc = selected_job.get("description", "")[:280]
    st.markdown(
        "<div class='job-banner'>"
        "<div class='jb-title'>" + selected_job.get("title","") + "</div>"
        "<div class='jb-company'>" + selected_job.get("company","") +
        " <span style='color:var(--faint)'>·</span> <span style='color:var(--muted)'>📍 " + locs + "</span></div>"
        "<div class='jb-desc'>" + desc + "…</div>"
        "</div>",
        unsafe_allow_html=True)
    default_jd = selected_job.get("description", "")
else:
    default_jd = ""

st.markdown("<div class='div'></div>", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# INPUT SECTION
# ═══════════════════════════════════════════════════════════════════════════════
in1, in2 = st.columns(2)

with in1:
    st.markdown(
        "<div style='font-size:15px;font-weight:700;color:var(--txt);margin-bottom:4px'>📋 Job Description</div>"
        "<div style='font-size:13px;color:var(--muted);margin-bottom:10px'>Paste the full JD for best keyword matching.</div>",
        unsafe_allow_html=True)
    jd_text = st.text_area(
        "jd_label", height=240,
        value=default_jd,
        placeholder="Paste the full job description here...\n\nInclude requirements, responsibilities, and preferred qualifications for best results.",
        label_visibility="collapsed",
        key="jd_input"
    )

with in2:
    st.markdown(
        "<div style='font-size:15px;font-weight:700;color:var(--txt);margin-bottom:4px'>📄 Your Resume</div>"
        "<div style='font-size:13px;color:var(--muted);margin-bottom:10px'>Auto-loaded from your profile. Or paste/edit below.</div>",
        unsafe_allow_html=True)

    saved_resume = st.session_state.get("resume_text", "")
    if not saved_resume:
        try:
            r = requests.get(API + "/resumes/", timeout=4)
            bases = r.json().get("base_resumes", [])
            if bases:
                saved_resume = bases[0].get("content", "")
        except Exception:
            pass

    resume_text = st.text_area(
        "res_label", height=240,
        value=saved_resume,
        placeholder="Your resume will auto-load from your profile.\nOr paste it here...",
        label_visibility="collapsed",
        key="resume_input"
    )

# ── Projects row ──────────────────────────────────────────────────────────────
st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)

pc1, pc2 = st.columns([3, 1])
with pc1:
    if projects:
        proj_names = ", ".join(p.get("name","") for p in projects[:5])
        st.markdown(
            "<div style='background:rgba(110,231,183,0.06);border:1px solid rgba(110,231,183,0.2);"
            "border-radius:10px;padding:10px 16px;font-size:13px;color:#6ee7b7'>"
            "✅ <b>" + str(len(projects)) + " projects</b> loaded from your profile: "
            "<span style='color:var(--muted)'>" + proj_names + "</span></div>",
            unsafe_allow_html=True)
    else:
        st.markdown(
            "<div style='background:rgba(252,165,165,0.05);border:1px solid rgba(252,165,165,0.2);"
            "border-radius:10px;padding:10px 16px;font-size:13px;color:#fca5a5'>"
            "⚠️ No projects loaded. <a href='pages/2_onboarding.py' style='color:#fca5a5'>Add them in Profile →</a></div>",
            unsafe_allow_html=True)

with st.expander("➕ Add extra projects for this run"):
    proj_input = st.text_area(
        "Extra projects (Name | Description, one per line)",
        height=90,
        placeholder="InternFlow AI | Built AI career platform with Nemotron + LangGraph\nIPL Dashboard | Flask + MySQL dashboard with advanced SQL analytics")
    if proj_input:
        for line in proj_input.strip().split("\n"):
            if "|" in line:
                parts = line.split("|", 1)
                projects = [{"name": parts[0].strip(), "description": parts[1].strip()}] + projects

st.markdown("<div class='div'></div>", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# RUN BUTTON
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown("<div class='run-wrap'>", unsafe_allow_html=True)
rc1, rc2, rc3 = st.columns([1, 2, 1])
with rc2:
    st.markdown(
        "<div style='font-size:13px;color:var(--muted);margin-bottom:10px;text-align:center'>"
        "🧠 Nemotron analyzes keywords → selects best projects → rewrites your resume → scores ATS fit"
        "</div>",
        unsafe_allow_html=True)
    run_btn = st.button("⚡ Run Nemotron Agent", type="primary", use_container_width=True, key="run_agent")
st.markdown("</div>", unsafe_allow_html=True)

# ── Validation & API call ─────────────────────────────────────────────────────
if run_btn:
    if not jd_text.strip():
        st.warning("Please paste a job description first.")
    elif not resume_text.strip():
        st.warning("Please add your resume text.")
    elif not projects:
        st.warning("Please add at least one project in your profile.")
    else:
        progress_placeholder = st.empty()
        with progress_placeholder.container():
            st.markdown(
                "<div class='processing-card'>"
                "<div class='processing-title'>🧠 Nemotron is thinking…</div>"
                "<div class='processing-sub'>Running LangGraph pipeline — this takes 15–60 seconds</div>"
                "<div style='margin-top:20px;max-width:300px;margin-left:auto;margin-right:auto'>"
                "<div class='step-item'><div class='step-dot step-dot-active'></div>Extracting JD keywords & scoring gaps</div>"
                "<div class='step-item'><div class='step-dot'></div>Selecting best-fit projects</div>"
                "<div class='step-item'><div class='step-dot'></div>Rewriting resume to match JD</div>"
                "<div class='step-item'><div class='step-dot'></div>Generating ATS report</div>"
                "</div></div>",
                unsafe_allow_html=True)

        try:
            payload = {
                "job_description": jd_text,
                "resume_text": resume_text,
                "projects": [{"name": p["name"], "description": p.get("description","")} for p in projects]
            }
            response = requests.post(API + "/agent/analyze", json=payload, timeout=600)
            progress_placeholder.empty()

            if response.status_code != 200:
                st.error("Agent failed: HTTP " + str(response.status_code))
                st.code(response.text)
                st.stop()

            raw = response.json()

            diagnostic = raw.get("diagnostic", {})
            if not diagnostic:
                diagnostic = try_parse_json(raw.get("diagnostic_report", ""))

            present_kw = raw.get("present_keywords", []) or diagnostic.get("present_keywords", []) or []
            missing_kw = raw.get("missing_keywords", []) or diagnostic.get("missing_keywords", []) or []
            jd_keywords = raw.get("jd_keywords", []) or diagnostic.get("jd_keywords", []) or []
            match_score = int(raw.get("match_score", 0) or diagnostic.get("match_score", 0) or 0)

            if jd_keywords and match_score == 0:
                match_score = int(round(100 * len(present_kw) / max(len(jd_keywords), 1)))

            sel_projects = normalize_projects(raw.get("selected_projects", []), projects)
            tailored_resume = raw.get("tailored_resume", "")

            st.session_state.agent_result = {
                "diagnostic": {
                    "match_score": match_score,
                    "present_keywords": present_kw,
                    "missing_keywords": missing_kw,
                    "jd_keywords": jd_keywords,
                },
                "selected_projects": sel_projects,
                "tailored_resume": tailored_resume,
            }

            st.session_state.agent_jd     = jd_text
            st.session_state.agent_resume = resume_text
            st.success("✅ Analysis complete! Scroll down to see your results.")

        except requests.exceptions.ConnectionError:
            progress_placeholder.empty()
            st.markdown(
                "<div style='background:rgba(239,68,68,0.08);border:1px solid rgba(239,68,68,0.3);"
                "border-radius:14px;padding:20px 24px'>"
                "<div style='font-size:16px;font-weight:700;color:#fca5a5;margin-bottom:8px'>❌ Backend not running</div>"
                "<div style='color:#9ca3af;font-size:13px'>Run: "
                "<code style='background:#111;border-radius:4px;padding:2px 8px;color:#6ee7b7'>"
                "cd backend &amp;&amp; uvicorn main:app --reload</code>"
                "</div></div>",
                unsafe_allow_html=True)
        except Exception as ex:
            progress_placeholder.empty()
            st.error("Agent error: " + str(ex))

# ═══════════════════════════════════════════════════════════════════════════════
# RESULTS
# ═══════════════════════════════════════════════════════════════════════════════
if st.session_state.agent_result:
    result       = st.session_state.agent_result
    diagnostic   = result.get("diagnostic", {})
    match_score  = int(diagnostic.get("match_score", 0) or 0)
    present_kw   = diagnostic.get("present_keywords", []) or []
    missing_kw   = diagnostic.get("missing_keywords", []) or []
    sel_projects = result.get("selected_projects", [])
    tailored     = result.get("tailored_resume", "")
    orig_resume  = st.session_state.agent_resume

    st.markdown("<div class='div'></div>", unsafe_allow_html=True)

    # ── Result tabs ───────────────────────────────────────────────────────────
    rtab1, rtab2, rtab3, rtab4 = st.tabs([
        "🎯  ATS Score",
        "🔑  Keywords",
        "🗂️  Projects",
        "📝  Resume",
    ])

    # ═══════════════════════════════════════════════════════════════
    # TAB A — ATS SCORE
    # ═══════════════════════════════════════════════════════════════
    with rtab1:
        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

        txt_col, bg_col, bdr_col = score_color(match_score)

        if match_score >= 70:
            verdict      = "🟢 Strong match — ready to apply!"
            verdict_col  = "#6ee7b7"
        elif match_score >= 50:
            verdict      = "🟡 Decent match — a few tweaks needed."
            verdict_col  = "#fcd34d"
        else:
            verdict      = "🔴 Significant gaps — tailoring recommended."
            verdict_col  = "#fca5a5"

        sc1, sc2, sc3 = st.columns([1, 1, 1])

        with sc1:
            st.markdown(
                "<div class='info-card' style='text-align:center;padding:28px'>"
                "<div style='color:var(--muted);font-size:12px;font-family:JetBrains Mono,monospace;"
                "text-transform:uppercase;letter-spacing:0.1em;margin-bottom:14px'>ATS Match Score</div>"
                "<div class='ats-ring' style='border-color:" + bdr_col + ";background:" + bg_col + "'>"
                "<div class='ats-num' style='color:" + txt_col + "'>" + str(match_score) + "</div>"
                "<div class='ats-lbl' style='color:" + txt_col + "'>/ 100</div>"
                "</div>"
                "<div class='ats-verdict' style='color:" + verdict_col + "'>" + verdict + "</div>"
                "</div>",
                unsafe_allow_html=True)

        with sc2:
            kw_total   = len(present_kw) + len(missing_kw)
            kw_covered = len(present_kw)
            kw_pct     = int(kw_covered / max(kw_total, 1) * 100)
            kw_col, kw_bg, kw_bdr = score_color(kw_pct)
            st.markdown(
                "<div class='info-card' style='text-align:center;padding:28px'>"
                "<div style='color:var(--muted);font-size:12px;font-family:JetBrains Mono,monospace;"
                "text-transform:uppercase;letter-spacing:0.1em;margin-bottom:14px'>Keyword Coverage</div>"
                "<div class='ats-ring' style='border-color:" + kw_bdr + ";background:" + kw_bg + "'>"
                "<div class='ats-num' style='color:" + kw_col + "'>" + str(kw_pct) + "%</div>"
                "<div class='ats-lbl' style='color:" + kw_col + "'>" + str(kw_covered) + "/" + str(kw_total) + "</div>"
                "</div>"
                "<div style='font-size:13px;color:var(--muted);margin-top:8px'>"
                + str(kw_covered) + " of " + str(kw_total) + " required keywords found"
                "</div>"
                "</div>",
                unsafe_allow_html=True)

        with sc3:
            weak = weak_bullets(tailored or orig_resume)
            wb_n  = len(weak)
            wb_col = "#6ee7b7" if wb_n == 0 else "#fcd34d" if wb_n <= 2 else "#fca5a5"
            st.markdown(
                "<div class='info-card' style='text-align:center;padding:28px'>"
                "<div style='color:var(--muted);font-size:12px;font-family:JetBrains Mono,monospace;"
                "text-transform:uppercase;letter-spacing:0.1em;margin-bottom:14px'>Weak Bullets Found</div>"
                "<div class='ats-ring' style='border-color:" + wb_col + "40;background:" + wb_col + "18'>"
                "<div class='ats-num' style='color:" + wb_col + "'>" + str(wb_n) + "</div>"
                "<div class='ats-lbl' style='color:" + wb_col + "'>BULLETS</div>"
                "</div>"
                "<div style='font-size:13px;color:var(--muted);margin-top:8px'>"
                + ("All bullets look strong! ✅" if wb_n == 0 else str(wb_n) + " bullets need improvement") +
                "</div>"
                "</div>",
                unsafe_allow_html=True)

        # Weak bullets detail
        if weak:
            st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)
            st.markdown(
                "<div style='font-size:16px;font-weight:700;color:var(--txt);margin-bottom:12px'>"
                "⚠️ Bullets to Improve</div>",
                unsafe_allow_html=True)
            for bullet, fix in weak:
                st.markdown(
                    "<div class='weak-bullet'>"
                    "<div class='weak-bullet-text'>\"" + bullet[:120] + "\"</div>"
                    "<div class='weak-bullet-fix'>💡 " + fix + "</div>"
                    "</div>",
                    unsafe_allow_html=True)

        # Formatting tips
        st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)
        st.markdown(
            "<div style='font-size:16px;font-weight:700;color:var(--txt);margin-bottom:12px'>"
            "📐 Formatting Checklist</div>",
            unsafe_allow_html=True)

        checks = [
            ("One page length",    len(orig_resume.split()) < 700,  "Keep under ~600 words for entry-level."),
            ("Has contact info",   any(x in orig_resume.lower() for x in ["@","linkedin","github","phone"]), "Add email, LinkedIn, and GitHub."),
            ("Has education",      "education" in orig_resume.lower(), "Add an Education section."),
            ("Has experience",     any(x in orig_resume.lower() for x in ["experience","intern","work"]), "Add work/internship experience."),
            ("Has skills section", "skill" in orig_resume.lower(), "Add a dedicated Skills section."),
            ("Has projects",       "project" in orig_resume.lower(), "Add a Projects section."),
            ("Uses bullet points", any(c in orig_resume for c in ["•","-","·"]), "Use bullet points for readability."),
            ("Has quantified impact", any(c.isdigit() for c in orig_resume), "Add at least a few numbers/metrics."),
        ]

        ch1, ch2 = st.columns(2)
        for i, (label, passed, tip) in enumerate(checks):
            col = ch1 if i % 2 == 0 else ch2
            icon = "✅" if passed else "❌"
            color = "#6ee7b7" if passed else "#fca5a5"
            with col:
                st.markdown(
                    "<div style='display:flex;align-items:flex-start;gap:10px;padding:8px 12px;"
                    "background:rgba(255,255,255,0.02);border-radius:8px;margin-bottom:6px'>"
                    "<span style='font-size:15px'>" + icon + "</span>"
                    "<div>"
                    "<div style='font-size:13px;font-weight:600;color:" + color + "'>" + label + "</div>"
                    + ("" if passed else "<div style='font-size:11px;color:var(--muted)'>" + tip + "</div>") +
                    "</div></div>",
                    unsafe_allow_html=True)

    # ═══════════════════════════════════════════════════════════════
    # TAB B — KEYWORDS
    # ═══════════════════════════════════════════════════════════════
    with rtab2:
        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

        kb1, kb2 = st.columns(2)

        with kb1:
            st.markdown(
                "<div class='info-card'>"
                "<div style='color:#6ee7b7;font-family:JetBrains Mono,monospace;font-size:11px;"
                "text-transform:uppercase;letter-spacing:0.12em;margin-bottom:12px'>"
                "✅ Keywords You Have (" + str(len(present_kw)) + ")</div>"
                "<div>" + "".join(["<span class='kw-present'>✓ " + k + "</span>" for k in present_kw]) + "</div>"
                "</div>",
                unsafe_allow_html=True)

        with kb2:
            st.markdown(
                "<div class='info-card'>"
                "<div style='color:#fca5a5;font-family:JetBrains Mono,monospace;font-size:11px;"
                "text-transform:uppercase;letter-spacing:0.12em;margin-bottom:12px'>"
                "❌ Keywords You're Missing (" + str(len(missing_kw)) + ")</div>"
                "<div>" + "".join(["<span class='kw-missing'>✗ " + k + "</span>" for k in missing_kw]) + "</div>"
                "</div>",
                unsafe_allow_html=True)

        # Categorise missing keywords
        if missing_kw:
            st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
            st.markdown(
                "<div style='font-size:16px;font-weight:700;color:var(--txt);margin-bottom:14px'>"
                "🗂️ Missing Keywords by Category</div>",
                unsafe_allow_html=True)

            TOOL_WORDS   = {"python","java","sql","spark","airflow","docker","kubernetes","terraform",
                            "pytorch","tensorflow","react","node","aws","gcp","azure","git","kafka",
                            "redis","postgresql","mongodb","fastapi","flask","langchain","scikit"}
            HARD_WORDS   = {"machine learning","deep learning","nlp","computer vision","data engineering",
                            "distributed systems","restful api","ci/cd","mlops","llm","rag","reinforcement"}
            SOFT_WORDS   = {"communication","collaboration","leadership","problem solving","teamwork",
                            "adaptability","ownership","cross-functional","stakeholder"}

            tools   = [k for k in missing_kw if k.lower() in TOOL_WORDS]
            hard    = [k for k in missing_kw if k.lower() in HARD_WORDS]
            soft    = [k for k in missing_kw if k.lower() in SOFT_WORDS]
            other   = [k for k in missing_kw if k not in tools and k not in hard and k not in soft]

            cats = [("🔧 Tools & Frameworks", tools), ("🧠 Hard Skills", hard + other), ("🤝 Soft Skills", soft)]
            for cat_label, items in cats:
                if items:
                    pills = "".join(["<span class='kw-missing'>✗ " + k + "</span>" for k in items])
                    st.markdown(
                        "<div style='margin-bottom:14px'>"
                        "<div style='font-size:12px;color:var(--muted);font-family:JetBrains Mono,monospace;"
                        "text-transform:uppercase;letter-spacing:0.1em;margin-bottom:8px'>" + cat_label + "</div>"
                        "<div>" + pills + "</div>"
                        "</div>",
                        unsafe_allow_html=True)

    # ═══════════════════════════════════════════════════════════════
    # TAB C — PROJECTS
    # ═══════════════════════════════════════════════════════════════
    with rtab3:
        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

        # ── JD-aware steps generator ──────────────────────────────────────
        def jd_steps_for_project(pname, pdesc, jd, missing):
            """Generate smart build steps using JD keywords + project context."""
            # Detect tech from JD + description
            txt  = (pname + " " + pdesc + " " + jd).lower()
            tech = []
            TECH_MAP = [
                ("pytorch",     ["Install PyTorch, set up CUDA env", "Load and preprocess dataset with DataLoaders",
                                 "Define model architecture (layers, activations)", "Train with optimizer + loss fn, log metrics",
                                 "Evaluate on test set, export model weights"]),
                ("tensorflow",  ["Set up TensorFlow + GPU environment", "Build data pipeline with tf.data API",
                                 "Define model with Keras Sequential/Functional API", "Train with callbacks (EarlyStopping, ModelCheckpoint)",
                                 "Save & serve model with TF Serving or TFLite"]),
                ("langchain",   ["Install LangChain, set up API keys (OpenAI/NVIDIA)", "Define prompt templates and chains",
                                 "Connect to vector store (Chroma/Pinecone) for RAG", "Build retrieval + generation pipeline",
                                 "Add memory, streaming, and evaluation with LangSmith"]),
                ("spark",       ["Set up PySpark environment (local or cluster)", "Ingest raw data into DataFrames / RDDs",
                                 "Write transformations (filter, join, aggregate)", "Optimize with partitioning and caching",
                                 "Output results to Parquet/Delta and validate"]),
                ("sql",         ["Design normalized schema (ERD + tables)", "Load sample dataset and run exploratory queries",
                                 "Build complex queries (CTEs, window functions, subqueries)", "Create indexes for query optimization",
                                 "Build dashboard or API layer on top of queries"]),
                ("flask",       ["Initialize Flask app with blueprints and config", "Build REST endpoints (GET/POST/DELETE)",
                                 "Connect to database (SQLAlchemy + migrations)", "Add auth (JWT or session-based)",
                                 "Containerize with Docker and deploy to Render/Railway"]),
                ("react",       ["Bootstrap with Vite + TypeScript", "Build component hierarchy and state management",
                                 "Connect to backend API with React Query / SWR", "Add routing, auth, and error boundaries",
                                 "Deploy to Vercel with CI/CD pipeline"]),
            ]
            for keyword, steps in TECH_MAP:
                if keyword in txt:
                    return steps

            # Fallback smart generic steps with missing keyword context
            kw_str = ", ".join(missing[:3]) if missing else "the required skills"
            return [
                "Set up project repository with README, .gitignore, and requirements.txt",
                "Design system architecture and data flow (include diagram in README)",
                "Implement core logic — incorporate " + kw_str + " where applicable",
                "Write unit tests, add error handling, and log performance metrics",
                "Deploy to GitHub Pages / Heroku / HuggingFace Spaces with live demo link",
            ]

        # ── Suggested new projects from JD ────────────────────────────────
        def suggest_new_projects(jd, missing_kw):
            """Generate 3 project ideas using JD + missing keywords."""
            txt = jd.lower()
            ideas = []

            if any(w in txt for w in ["nlp","language","text","llm","bert","transformer"]):
                ideas.append({
                    "name": "Semantic Job Match Engine",
                    "why":  "Directly matches NLP/LLM skills required in this role",
                    "desc": "Build a sentence-transformer based job-resume similarity scorer. Use FAISS for vector search over 1000+ job listings. Achieve <50ms query latency.",
                    "stack": "Python · SentenceTransformers · FAISS · FastAPI · Streamlit"
                })
            if any(w in txt for w in ["machine learning","ml","model","prediction","classification","regression"]):
                ideas.append({
                    "name": "End-to-End ML Pipeline",
                    "why":  "Shows full MLOps lifecycle — data to deployment",
                    "desc": "Train, evaluate, and deploy a classification model with experiment tracking (MLflow), feature store, REST API, and CI/CD with GitHub Actions.",
                    "stack": "Python · Scikit-learn · MLflow · FastAPI · Docker · GitHub Actions"
                })
            if any(w in txt for w in ["data engineer","pipeline","etl","spark","airflow","kafka"]):
                ideas.append({
                    "name": "Real-Time Data Pipeline",
                    "why":  "Proves data engineering fundamentals for this role",
                    "desc": "Stream live data via Kafka → process with PySpark → store in Delta Lake → visualize in a live dashboard. Process 10K+ events/sec.",
                    "stack": "Apache Kafka · PySpark · Delta Lake · Grafana · Docker"
                })
            if any(w in txt for w in ["generative","gen ai","llm","rag","langchain","openai","gpt"]):
                ideas.append({
                    "name": "RAG-Powered Document Assistant",
                    "why":  "GenAI + RAG is explicitly requested in this JD",
                    "desc": "Build a production RAG app: ingest PDFs → chunk + embed → store in ChromaDB → query with LangChain → stream responses via FastAPI.",
                    "stack": "LangChain · ChromaDB · FastAPI · OpenAI/NVIDIA API · Streamlit"
                })
            if any(w in txt for w in ["computer vision","cv","image","cnn","object detection","yolo"]):
                ideas.append({
                    "name": "Real-Time Object Detection System",
                    "why":  "Computer vision experience is key for this position",
                    "desc": "Fine-tune YOLOv8 on a custom dataset, deploy as a FastAPI endpoint with WebSocket streaming, and build a React frontend showing live detections.",
                    "stack": "YOLOv8 · PyTorch · FastAPI · WebSockets · React"
                })
            if any(w in txt for w in ["quant","trading","financial","time series","forecasting"]):
                ideas.append({
                    "name": "Algorithmic Trading Backtester",
                    "why":  "Demonstrates quant + time-series skills for this role",
                    "desc": "Build a backtesting engine: ingest OHLCV data → implement 3 strategies (MA crossover, RSI, ML-based) → calculate Sharpe ratio, max drawdown, win rate.",
                    "stack": "Python · Pandas · Backtrader · Plotly · yfinance"
                })

            # Always add one general-purpose suggestion if < 3
            if len(ideas) < 3:
                ideas.append({
                    "name": "Full-Stack Portfolio Dashboard",
                    "why":  "Shows breadth: backend, frontend, database, and deployment",
                    "desc": "Build a personal dashboard featuring " + (", ".join(missing_kw[:3]) if missing_kw else "your key skills") + ". REST API + React frontend + PostgreSQL + deployed on Railway.",
                    "stack": "FastAPI · React · PostgreSQL · Railway · Docker"
                })

            return ideas[:3]

        if not sel_projects:
            st.markdown(
                "<div style='background:rgba(252,211,77,0.06);border:1px solid rgba(252,211,77,0.2);"
                "border-radius:14px;padding:16px 20px;margin-bottom:20px'>"
                "<div style='color:#fcd34d;font-weight:700;margin-bottom:4px'>💡 No portfolio projects found</div>"
                "<div style='color:var(--muted);font-size:13px'>Add your projects in the Profile page for Nemotron to select from. "
                "In the meantime, here are 3 project ideas tailored to this JD:</div>"
                "</div>",
                unsafe_allow_html=True)

            suggested = suggest_new_projects(st.session_state.agent_jd, missing_kw)
            for idx, idea in enumerate(suggested):
                st.markdown(
                    "<div class='proj-card'>"
                    "<div class='proj-num'>SUGGESTED PROJECT " + str(idx + 1) + "</div>"
                    "<div class='proj-name'>" + idea["name"] + "</div>"
                    "<div style='display:inline-block;background:rgba(252,211,77,0.1);"
                    "border:1px solid rgba(252,211,77,0.3);color:#fcd34d;"
                    "padding:3px 10px;border-radius:6px;font-size:11px;"
                    "font-family:JetBrains Mono,monospace;margin-bottom:10px'>"
                    "⚡ " + idea["why"] + "</div>"
                    "<div style='font-size:13px;color:var(--txt2);margin-bottom:14px'>" + idea["desc"] + "</div>"
                    "<div style='font-size:11px;color:var(--muted);font-family:JetBrains Mono,monospace'>"
                    "🛠 " + idea["stack"] + "</div>"
                    "</div>",
                    unsafe_allow_html=True)
        else:
            # Header with suggested ideas button
            hdr1, hdr2 = st.columns([3, 1])
            with hdr1:
                st.markdown(
                    "<div style='font-size:13px;color:var(--muted);margin-bottom:18px'>"
                    "Nemotron selected these <b style='color:var(--lav300)'>" + str(len(sel_projects)) +
                    " projects</b> as the best fit for this role — with JD-aware build steps and GitHub READMEs.</div>",
                    unsafe_allow_html=True)
            with hdr2:
                show_suggestions = st.toggle("💡 Show new ideas", value=False, key="show_proj_suggestions")

            if show_suggestions:
                suggested = suggest_new_projects(st.session_state.agent_jd, missing_kw)
                st.markdown(
                    "<div style='font-size:14px;font-weight:700;color:var(--amber);margin-bottom:12px'>"
                    "💡 Additional Project Ideas from JD Analysis</div>",
                    unsafe_allow_html=True)
                for idea in suggested:
                    st.markdown(
                        "<div style='background:rgba(252,211,77,0.04);border:1px solid rgba(252,211,77,0.18);"
                        "border-radius:12px;padding:14px 18px;margin-bottom:10px'>"
                        "<div style='font-weight:700;color:var(--txt);margin-bottom:4px'>" + idea["name"] + "</div>"
                        "<div style='font-size:11px;color:#fcd34d;font-family:JetBrains Mono,monospace;margin-bottom:6px'>"
                        "⚡ " + idea["why"] + "</div>"
                        "<div style='font-size:13px;color:var(--muted);margin-bottom:6px'>" + idea["desc"] + "</div>"
                        "<div style='font-size:11px;color:var(--faint);font-family:JetBrains Mono,monospace'>"
                        "🛠 " + idea["stack"] + "</div>"
                        "</div>",
                        unsafe_allow_html=True)
                st.markdown("<div class='div'></div>", unsafe_allow_html=True)

            for idx, proj in enumerate(sel_projects):
                pname = proj.get("name", "Project " + str(idx + 1))
                pdesc = proj.get("rewritten_description") or proj.get("description", "")
                steps = jd_steps_for_project(pname, pdesc, st.session_state.agent_jd, missing_kw)

                # Detect tech stack from description
                tech_txt = (pname + " " + pdesc + " " + st.session_state.agent_jd).lower()
                stack_tags = [s for s in ["Python","PyTorch","TensorFlow","LangChain","Spark","SQL",
                              "FastAPI","React","Docker","AWS","HuggingFace","Scikit-learn",
                              "Kafka","Airflow","dbt","OpenAI","NVIDIA"] if s.lower() in tech_txt]

                stack_html = "".join(
                    "<span style='background:rgba(168,85,247,0.12);border:1px solid rgba(168,85,247,0.25);"
                    "color:var(--lav400);padding:2px 8px;border-radius:6px;font-size:10px;"
                    "font-family:JetBrains Mono,monospace;margin-right:4px'>" + t + "</span>"
                    for t in stack_tags[:6]
                ) if stack_tags else ""

                # Build README
                slug    = pname.lower().replace(" ","-")
                readme  = (
                    "# " + pname + "\n\n"
                    "> " + (pdesc[:200] if pdesc else "Built for the " + (selected_job.get("title","") if selected_job else "role")) + "\n\n"
                    "## 🚀 Overview\n" + (pdesc if pdesc else "Project description here.") + "\n\n"
                    "## 🛠 Tech Stack\n" + "\n".join(["- " + t for t in (stack_tags or ["Python"])]) + "\n\n"
                    "## ⚙️ Installation\n```bash\ngit clone https://github.com/yourusername/" + slug + "\n"
                    "cd " + slug + "\npip install -r requirements.txt\n```\n\n"
                    "## 📖 Usage\n```python\n# Quick start\npython main.py --config config.yaml\n```\n\n"
                    "## 📊 Results\n| Metric | Score |\n|--------|-------|\n"
                    "| Accuracy | XX% |\n| Latency | XXms |\n| Dataset | XXXX records |\n\n"
                    "## 🔗 Links\n- [Live Demo](https://your-demo-link)\n- [Report](./report.pdf)\n\n"
                    "## 📄 License\nMIT © " + (profile.get("name","") or "Your Name")
                )

                steps_html = ""
                for si, step in enumerate(steps):
                    steps_html += (
                        "<div class='proj-step'>"
                        "<div class='proj-step-num'>" + str(si + 1) + "</div>"
                        "<div class='proj-step-text'>" + step + "</div>"
                        "</div>"
                    )

                st.markdown(
                    "<div class='proj-card'>"
                    "<div class='proj-num'>PROJECT " + str(idx + 1) + " OF " + str(len(sel_projects)) + "</div>"
                    "<div class='proj-name'>" + pname + "</div>"
                    + ("<div style='margin-bottom:10px'>" + stack_html + "</div>" if stack_html else "") +
                    "<div style='font-size:13px;color:var(--muted);margin-bottom:14px'>" + (pdesc[:220] if pdesc else "") + "</div>"
                    "<div style='font-size:11px;color:var(--lav400);font-family:JetBrains Mono,monospace;"
                    "text-transform:uppercase;letter-spacing:0.1em;margin-bottom:10px'>📋 Build Steps</div>"
                    + steps_html +
                    "</div>",
                    unsafe_allow_html=True)

                with st.expander("📄 GitHub README for " + pname):
                    st.markdown("<div class='readme-box'>" + readme + "</div>", unsafe_allow_html=True)
                    st.download_button(
                        label="⬇️ Download README.md",
                        data=readme,
                        file_name="README_" + pname.replace(" ","_") + ".md",
                        mime="text/markdown",
                        key="readme_dl_" + str(idx)
                    )

    # ═══════════════════════════════════════════════════════════════
    # TAB D — RESUME
    # ═══════════════════════════════════════════════════════════════
    with rtab4:
        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

        if not tailored:
            st.info("No tailored resume generated yet.")
        else:
            # View toggle
            vt1, vt2, vt3 = st.columns([1, 1, 4])
            with vt1:
                view_type = "tailored"
                if st.button("📄 Tailored", key="view_tailored",
                             type="primary" if st.session_state.diff_view == "tailored" else "secondary",
                             use_container_width=True):
                    st.session_state.diff_view = "tailored"
                    st.rerun()
            with vt2:
                if st.button("🔀 Diff View", key="view_diff",
                             type="primary" if st.session_state.diff_view == "diff" else "secondary",
                             use_container_width=True):
                    st.session_state.diff_view = "diff"
                    st.rerun()

            st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)

            if st.session_state.diff_view == "tailored":
                # Side-by-side
                r1, r2 = st.columns(2)
                with r1:
                    st.markdown(
                        "<div style='font-size:13px;font-weight:600;color:var(--muted);"
                        "font-family:JetBrains Mono,monospace;text-transform:uppercase;"
                        "letter-spacing:0.1em;margin-bottom:10px'>ORIGINAL</div>",
                        unsafe_allow_html=True)
                    st.markdown(text_to_resume_html(orig_resume), unsafe_allow_html=True)

                with r2:
                    st.markdown(
                        "<div style='font-size:13px;font-weight:600;color:#6ee7b7;"
                        "font-family:JetBrains Mono,monospace;text-transform:uppercase;"
                        "letter-spacing:0.1em;margin-bottom:10px'>✨ TAILORED BY NEMOTRON</div>",
                        unsafe_allow_html=True)
                    st.markdown(text_to_resume_html(tailored), unsafe_allow_html=True)

            else:
                # Diff view
                st.markdown(
                    "<div style='font-size:12px;color:var(--muted);margin-bottom:10px'>"
                    "<span style='color:#6ee7b7'>Green lines</span> = added &nbsp;·&nbsp; "
                    "<span style='color:#fca5a5'>Red lines</span> = removed &nbsp;·&nbsp; "
                    "White = unchanged</div>",
                    unsafe_allow_html=True)
                diff_html = build_diff_html(orig_resume, tailored)
                st.markdown("<div class='diff-panel'>" + diff_html + "</div>", unsafe_allow_html=True)

            # Action row
            st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)
            act1, act2, act3, act4 = st.columns([2, 2, 2, 2])

            with act1:
                pdf_data = generate_pdf_bytes(tailored, profile.get("name","resume"))
                fname    = (profile.get("name","resume") + "_tailored_resume.pdf").replace(" ","_")
                st.download_button("⬇️ Download PDF", data=pdf_data, file_name=fname,
                                   mime="application/pdf", use_container_width=True)

            with act2:
                company_name = selected_job.get("company","Company") if selected_job else "Company"
                job_title_str = selected_job.get("title","Role") if selected_job else "Role"
                if st.button("💾 Save to Arsenal", use_container_width=True, type="secondary"):
                    try:
                        requests.post(API + "/resumes/company", json={
                            "company":         company_name,
                            "job_title":       job_title_str,
                            "tailored_content": tailored,
                            "base_resume_name": "default"
                        }, timeout=10)
                        st.success("✅ Saved to Resume Arsenal!")
                    except Exception as ex:
                        st.error("Could not save: " + str(ex))

            with act3:
                if st.button("📄 Generate LaTeX PDF →", type="primary", use_container_width=True):
                    st.session_state.resume_for_pdf  = tailored
                    st.session_state.profile_for_pdf = profile
                    st.switch_page("pages/7_resume_output.py")

            with act4:
                if st.button("📋 Copy to Clipboard", use_container_width=True, type="secondary"):
                    st.code(tailored, language=None)
