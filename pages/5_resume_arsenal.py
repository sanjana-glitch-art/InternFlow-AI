import streamlit as st
import requests
import json
from datetime import datetime

st.set_page_config(
    page_title="InternFlow AI – Resume Arsenal",
    page_icon="📂",
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
    --lav300: #d8b4fe;
    --lav400: #c084fc;
    --lav500: #a855f7;
    --bg:     #08080f;
    --bg2:    #0e0e1a;
    --bg3:    #131325;
    --txt:    #f1f0f8;
    --txt2:   #c4c2dc;
    --muted:  #7c7a9a;
    --faint:  #2d2b45;
    --bdr:    rgba(168,85,247,0.18);
    --bdr2:   rgba(168,85,247,0.38);
    --green:  #6ee7b7;
    --amber:  #fcd34d;
    --rose:   #fca5a5;
    --indigo: #a5b4fc;
}

.stApp {
    background: var(--bg) !important;
    font-family: 'Outfit', sans-serif;
    color: var(--txt);
}
.block-container {
    padding: 28px 48px 72px !important;
    max-width: 1280px !important;
    margin: 0 auto !important;
}

/* Inputs */
.stTextInput > div > div > input {
    background: rgba(255,255,255,0.03) !important;
    border: 1px solid rgba(168,85,247,0.22) !important;
    border-radius: 12px !important;
    color: var(--txt) !important;
    font-family: 'Outfit', sans-serif !important;
    font-size: 15px !important;
    padding: 10px 14px !important;
}
.stTextInput label, .stTextArea label, .stFileUploader label {
    color: var(--muted) !important;
    font-family: 'Outfit', sans-serif !important;
    font-size: 13px !important;
    font-weight: 500 !important;
}
.stTextArea > div > div > textarea {
    background: rgba(255,255,255,0.03) !important;
    border: 1px solid rgba(168,85,247,0.22) !important;
    border-radius: 12px !important;
    color: var(--txt) !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 13px !important;
}

/* Buttons */
.stButton > button {
    background: linear-gradient(135deg, #7c3aed, #6d28d9) !important;
    color: #fff !important;
    border: none !important;
    border-radius: 10px !important;
    font-family: 'Outfit', sans-serif !important;
    font-size: 14px !important;
    font-weight: 600 !important;
    padding: 9px 20px !important;
    height: auto !important;
    transition: all 0.2s !important;
}
.stButton > button:hover { opacity: 0.85 !important; transform: translateY(-1px) !important; }
.stButton > button[kind="secondary"] {
    background: rgba(168,85,247,0.07) !important;
    border: 1px solid rgba(168,85,247,0.28) !important;
    color: var(--lav300) !important;
}
.stButton > button[kind="secondary"]:hover { background: rgba(168,85,247,0.14) !important; }

/* Download button */
.stDownloadButton > button {
    background: rgba(110,231,183,0.1) !important;
    border: 1px solid rgba(110,231,183,0.3) !important;
    color: #6ee7b7 !important;
    border-radius: 10px !important;
    font-family: 'Outfit', sans-serif !important;
    font-size: 13px !important;
    font-weight: 600 !important;
    padding: 7px 16px !important;
    height: auto !important;
    transition: all 0.2s !important;
}
.stDownloadButton > button:hover {
    background: rgba(110,231,183,0.18) !important;
    transform: translateY(-1px) !important;
}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    background: rgba(255,255,255,0.02) !important;
    border-bottom: 1px solid var(--bdr) !important;
    gap: 4px !important;
}
.stTabs [data-baseweb="tab"] {
    font-family: 'Outfit', sans-serif !important;
    font-size: 14px !important;
    font-weight: 600 !important;
    color: var(--muted) !important;
    border-radius: 8px 8px 0 0 !important;
    padding: 10px 20px !important;
}
.stTabs [aria-selected="true"] {
    color: var(--lav300) !important;
    background: rgba(168,85,247,0.1) !important;
    border-bottom: 2px solid var(--lav400) !important;
}

/* Nav */
.nav-logo {
    font-family: 'Outfit', sans-serif;
    font-size: 21px; font-weight: 800;
    background: linear-gradient(135deg, #c4b5fd, #a78bfa);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
.nav-tagline {
    font-family: 'JetBrains Mono', monospace;
    font-size: 10px; color: var(--faint);
    letter-spacing: 0.12em; margin-top: 2px;
}

/* Divider */
.div {
    border: none; height: 1px;
    background: linear-gradient(90deg, transparent, rgba(168,85,247,0.2), transparent);
    margin: 18px 0;
}

/* Page header */
.page-hd {
    font-family: 'Instrument Serif', serif;
    font-size: clamp(28px, 3.5vw, 44px);
    font-weight: 400; color: var(--txt);
    letter-spacing: -1px; margin: 0 0 5px; line-height: 1.1;
}
.page-hd em { font-style: italic; color: var(--lav300); }
.page-sub { font-size: 15px; color: var(--muted); font-weight: 300; }
.page-sub span { color: var(--lav300); font-weight: 500; }

/* Section header */
.sec-hd {
    font-family: 'Outfit', sans-serif;
    font-size: 18px; font-weight: 700; color: var(--txt);
    margin: 0 0 4px; display: flex; align-items: center; gap: 8px;
}
.sec-sub { font-size: 13px; color: var(--muted); margin-bottom: 18px; }

/* Base resume card */
.base-card {
    background: rgba(168,85,247,0.04);
    border: 1px solid rgba(168,85,247,0.22);
    border-radius: 18px;
    padding: 24px 28px;
    position: relative; overflow: hidden;
}
.base-card::before {
    content: '';
    position: absolute; top: 0; left: 0; right: 0; height: 1px;
    background: linear-gradient(90deg, transparent, rgba(168,85,247,0.35), transparent);
}
.base-card-name {
    font-family: 'Outfit', sans-serif;
    font-size: 20px; font-weight: 700; color: var(--txt);
    margin-bottom: 6px;
}
.base-card-meta {
    font-family: 'JetBrains Mono', monospace;
    font-size: 11px; color: var(--muted);
    display: flex; gap: 16px; flex-wrap: wrap;
}
.base-card-meta span { display: flex; align-items: center; gap: 4px; }

/* Tailored resume card */
.tcard {
    background: rgba(255,255,255,0.022);
    border: 1px solid var(--bdr);
    border-radius: 16px;
    padding: 20px 24px;
    margin-bottom: 10px;
    position: relative; overflow: hidden;
    transition: border-color 0.2s, transform 0.18s;
}
.tcard:hover {
    border-color: var(--bdr2);
    transform: translateY(-1px);
}
.tcard::before {
    content: '';
    position: absolute; top: 0; left: 0; right: 0; height: 1px;
    background: linear-gradient(90deg, transparent, rgba(168,85,247,0.2), transparent);
}
.tcard-inner { display: flex; align-items: flex-start; justify-content: space-between; gap: 16px; }
.tcard-company {
    font-family: 'Outfit', sans-serif;
    font-size: 17px; font-weight: 700; color: var(--txt);
    margin-bottom: 3px;
}
.tcard-role { font-size: 14px; color: var(--lav400); font-weight: 600; margin-bottom: 6px; }
.tcard-date {
    font-family: 'JetBrains Mono', monospace;
    font-size: 11px; color: var(--muted);
}
.tcard-badge {
    display: inline-flex; align-items: center; gap: 4px;
    background: rgba(168,85,247,0.12);
    border: 1px solid rgba(168,85,247,0.28);
    border-radius: 6px; padding: 3px 9px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 10px; color: var(--lav400); letter-spacing: 0.05em;
}
.tcard-callback {
    background: rgba(110,231,183,0.1);
    border: 1px solid rgba(110,231,183,0.3);
    color: #6ee7b7;
}

/* Stat card */
.stat-card {
    background: rgba(255,255,255,0.022);
    border: 1px solid var(--bdr);
    border-radius: 16px;
    padding: 20px 22px;
    text-align: center;
}
.stat-num {
    font-family: 'Instrument Serif', serif;
    font-size: 38px; line-height: 1;
    margin-bottom: 6px;
}
.stat-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 10px; color: var(--muted);
    text-transform: uppercase; letter-spacing: 0.12em;
}

/* Keyword pill */
.kpill-hit {
    display: inline-flex; align-items: center; gap: 5px;
    background: rgba(110,231,183,0.1);
    border: 1px solid rgba(110,231,183,0.28);
    color: #6ee7b7;
    padding: 4px 12px; border-radius: 100px;
    font-size: 12px; font-family: 'JetBrains Mono', monospace;
    margin: 3px;
}
.kpill-miss {
    display: inline-flex; align-items: center; gap: 5px;
    background: rgba(252,165,165,0.08);
    border: 1px solid rgba(252,165,165,0.25);
    color: #fca5a5;
    padding: 4px 12px; border-radius: 100px;
    font-size: 12px; font-family: 'JetBrains Mono', monospace;
    margin: 3px;
}

/* Insight card */
.insight-card {
    background: rgba(255,255,255,0.018);
    border: 1px solid var(--bdr);
    border-radius: 16px;
    padding: 20px 24px;
    margin-bottom: 12px;
}
.insight-card-title {
    font-family: 'Outfit', sans-serif;
    font-size: 15px; font-weight: 700; color: var(--txt);
    margin-bottom: 10px; display: flex; align-items: center; gap: 8px;
}

/* Bar chart row */
.bar-row { display: flex; align-items: center; gap: 10px; margin-bottom: 8px; }
.bar-label { font-family: 'JetBrains Mono', monospace; font-size: 11px; color: var(--muted); min-width: 120px; }
.bar-bg { flex: 1; height: 6px; background: rgba(255,255,255,0.05); border-radius: 4px; overflow: hidden; }
.bar-fill { height: 100%; border-radius: 4px; }
.bar-val { font-family: 'JetBrains Mono', monospace; font-size: 11px; color: var(--lav300); min-width: 32px; text-align: right; }

/* Empty state */
.empty-wrap { text-align: center; padding: 48px 20px; }
.empty-icon { font-size: 44px; margin-bottom: 12px; }
.empty-title { font-family: 'Instrument Serif', serif; font-size: 24px; color: var(--txt2); margin-bottom: 6px; }
.empty-sub { font-size: 14px; color: var(--muted); }

/* Preview box */
.resume-render {
    background: #ffffff;
    border-radius: 14px;
    padding: 40px 48px;
    max-height: 560px;
    overflow-y: auto;
    font-family: 'Georgia', serif;
    font-size: 13.5px;
    color: #1a1a1a;
    line-height: 1.7;
    box-shadow: 0 4px 40px rgba(0,0,0,0.4);
}
.resume-render h1 {
    font-size: 22px; font-weight: 700; color: #111;
    margin: 0 0 4px; text-align: center; letter-spacing: -0.5px;
}
.resume-render h2 {
    font-size: 13px; font-weight: 700; color: #333;
    text-transform: uppercase; letter-spacing: 0.12em;
    border-bottom: 1.5px solid #ddd;
    padding-bottom: 4px; margin: 18px 0 8px;
}
.resume-render h3 { font-size: 13.5px; font-weight: 700; color: #222; margin: 8px 0 2px; }
.resume-render p  { margin: 2px 0 6px; color: #333; }
.resume-render .contact-line {
    text-align: center; font-size: 12px;
    color: #555; margin-bottom: 14px;
}
.resume-render ul { margin: 4px 0 8px 18px; padding: 0; }
.resume-render li { margin-bottom: 3px; color: #333; }
.resume-render .section { margin-bottom: 14px; }
</style>
""", unsafe_allow_html=True)

API = "http://127.0.0.1:8000"

# ── Resume helpers ────────────────────────────────────────────────────────────
def text_to_resume_html(text: str) -> str:
    """
    Convert plain resume text into a clean, formatted HTML resume view.
    Detects section headings, bullet points, and the name/contact header.
    """
    import re
    lines = text.strip().splitlines()
    html  = ["<div class='resume-render'>"]

    SECTION_KEYWORDS = {
        "education", "experience", "work experience", "projects", "skills",
        "technical skills", "summary", "objective", "certifications",
        "publications", "awards", "leadership", "activities", "interests",
        "volunteer", "languages", "honors",
    }

    first_line = True
    contact_lines = []
    in_contact = True

    for raw in lines:
        line = raw.strip()
        if not line:
            continue

        lower = line.lower().rstrip(":").strip()

        # First non-empty line = Name
        if first_line:
            html.append("<h1>" + line + "</h1>")
            first_line = False
            continue

        # Next few short lines before a section = contact info
        if in_contact and len(line) < 100 and lower not in SECTION_KEYWORDS:
            contact_lines.append(line)
            if len(contact_lines) <= 3:
                continue
            else:
                in_contact = False
                html.append("<div class='contact-line'>" + " &nbsp;|&nbsp; ".join(contact_lines) + "</div>")
                contact_lines = []
                continue

        # Flush remaining contact lines when we hit a section
        if contact_lines:
            html.append("<div class='contact-line'>" + " &nbsp;|&nbsp; ".join(contact_lines) + "</div>")
            contact_lines = []
            in_contact = False

        # Section heading detection
        if lower in SECTION_KEYWORDS or (line.isupper() and len(line) > 3 and len(line) < 40):
            html.append("<h2>" + line.title() + "</h2>")
            continue

        # Bullet points
        if line.startswith(("•", "-", "·", "*", "–", "▪")):
            bullet_text = re.sub(r"^[•\-·*–▪]\s*", "", line)
            html.append("<li>" + bullet_text + "</li>")
            continue

        # Lines that look like job/project titles (bold them)
        if re.match(r"^[A-Z][^a-z]{0,3}[A-Z]", line) and len(line) < 80 and "|" in line:
            html.append("<h3>" + line + "</h3>")
            continue

        # Regular paragraph line
        html.append("<p>" + line + "</p>")

    # Flush any remaining contact lines
    if contact_lines:
        html.append("<div class='contact-line'>" + " &nbsp;|&nbsp; ".join(contact_lines) + "</div>")

    html.append("</div>")
    return "\n".join(html)


def generate_pdf_bytes(content: str, person_name: str = "resume") -> bytes:
    """Generate a clean PDF from resume text using fpdf2."""
    try:
        from fpdf import FPDF

        class ResumePDF(FPDF):
            pass

        pdf = ResumePDF(format="Letter")
        pdf.set_margins(18, 18, 18)
        pdf.add_page()

        lines = content.strip().splitlines()

        SECTION_KEYWORDS = {
            "education", "experience", "work experience", "projects", "skills",
            "technical skills", "summary", "objective", "certifications",
            "publications", "awards", "leadership", "activities",
        }

        first_line = True
        for raw in lines:
            line = raw.strip()
            if not line:
                pdf.ln(2)
                continue

            lower = line.lower().rstrip(":").strip()

            if first_line:
                pdf.set_font("Helvetica", "B", 16)
                pdf.cell(0, 8, line[:80], new_x="LMARGIN", new_y="NEXT", align="C")
                first_line = False
                continue

            if lower in SECTION_KEYWORDS or (line.isupper() and 3 < len(line) < 40):
                pdf.ln(3)
                pdf.set_font("Helvetica", "B", 10)
                pdf.set_text_color(60, 60, 60)
                pdf.cell(0, 6, line.upper(), new_x="LMARGIN", new_y="NEXT")
                pdf.set_draw_color(180, 180, 180)
                pdf.line(pdf.get_x(), pdf.get_y(), pdf.get_x() + 174, pdf.get_y())
                pdf.ln(2)
                pdf.set_text_color(0, 0, 0)
                continue

            if line.startswith(("•", "-", "·", "*", "–", "▪")):
                pdf.set_font("Helvetica", "", 9)
                bullet = "  • " + line.lstrip("•-·*–▪ ")
                pdf.multi_cell(0, 5, bullet[:200])
                continue

            pdf.set_font("Helvetica", "", 9)
            pdf.multi_cell(0, 5, line[:200])

        return bytes(pdf.output())

    except ImportError:
        # fpdf2 not installed — return UTF-8 encoded text as fallback
        return content.encode("utf-8")
    except Exception:
        return content.encode("utf-8")

# ── Session state ─────────────────────────────────────────────────────────────
if "resume_previews" not in st.session_state:
    st.session_state.resume_previews = {}   # resume_id -> bool (expanded)
if "callback_flags"  not in st.session_state:
    st.session_state.callback_flags  = set()  # resume ids marked as got callback

# ── Navbar ────────────────────────────────────────────────────────────────────
c1, c2, c3, c4, c5 = st.columns([3, 1, 1, 1, 1])
with c1:
    st.markdown(
        "<div class='nav-logo'>🚀 InternFlow AI</div>"
        "<div class='nav-tagline'>AI-POWERED CAREER PLATFORM</div>",
        unsafe_allow_html=True
    )
with c2:
    if st.button("📝 Profile", use_container_width=True):
        st.switch_page("pages/2_onboarding.py")
with c3:
    if st.button("💼 Jobs", use_container_width=True):
        st.switch_page("pages/3_jobs.py")
with c4:
    if st.button("🤖 AI Agent", use_container_width=True):
        st.switch_page("pages/4_agent.py")
with c5:
    if st.button("📂 Arsenal", use_container_width=True, type="primary"):
        pass

st.markdown("<div class='div'></div>", unsafe_allow_html=True)

# ── Page Header ───────────────────────────────────────────────────────────────
st.markdown(
    "<div class='page-hd'>Resume <em>Arsenal</em></div>"
    "<p class='page-sub'>Your base resume, every tailored version, and insights on what's working.</p>",
    unsafe_allow_html=True
)

st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)

# ── Load data ─────────────────────────────────────────────────────────────────
try:
    resp = requests.get(API + "/resumes/", timeout=6)
    all_resumes = resp.json()
    base_resumes     = all_resumes.get("base_resumes", [])
    company_resumes  = all_resumes.get("company_resumes", [])
    backend_online   = True
except Exception:
    base_resumes    = []
    company_resumes = []
    backend_online  = False

# Also pull from session state as fallback
session_resume = st.session_state.get("resume_text", "")
session_profile = st.session_state.get("profile", {})

# ── Tabs ──────────────────────────────────────────────────────────────────────
tab1, tab2, tab3 = st.tabs([
    "📄  Base Resume",
    "🗂️  Tailored Resumes  (" + str(len(company_resumes)) + ")",
    "📊  Performance Insights",
])

# ═══════════════════════════════════════════════════════════════════════════════
# TAB 1 — BASE RESUME
# ═══════════════════════════════════════════════════════════════════════════════
with tab1:
    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

    if base_resumes:
        base = base_resumes[-1]   # most recent
        name       = base.get("name", "My Resume")
        content    = base.get("content", "")
        tags       = base.get("tags", [])
        resume_id  = base.get("id", "base-1")
        char_count = len(content)
        word_count = len(content.split())

        tags_html = "".join(
            "<span style='background:rgba(168,85,247,0.14);border:1px solid rgba(168,85,247,0.28);"
            "color:#d8b4fe;padding:3px 10px;border-radius:100px;font-size:11px;"
            "font-family:JetBrains Mono,monospace;margin-right:5px'>" + t + "</span>"
            for t in tags
        )

        st.markdown(
            "<div class='base-card'>"
            "<div class='base-card-name'>📄 " + name + "</div>"
            "<div class='base-card-meta'>"
            "<span>📝 " + str(word_count) + " words</span>"
            "<span>🔤 " + str(char_count) + " chars</span>"
            "<span>🏷️ " + str(len(tags)) + " tags</span>"
            "</div>"
            + ("<div style='margin-top:10px'>" + tags_html + "</div>" if tags else "") +
            "</div>",
            unsafe_allow_html=True
        )

        st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)

        # Actions row
        a1, a2, a3 = st.columns([1, 1, 3])
        with a1:
            preview_key = "prev_base_" + resume_id
            if preview_key not in st.session_state:
                st.session_state[preview_key] = False
            label = "🙈 Hide Preview" if st.session_state[preview_key] else "👁️ View Resume"
            if st.button(label, key="toggle_base", use_container_width=True, type="secondary"):
                st.session_state[preview_key] = not st.session_state[preview_key]
                st.rerun()
        with a2:
            pdf_bytes = generate_pdf_bytes(content, session_profile.get("name", "resume"))
            fname = (session_profile.get("name", "resume") + "_base_resume.pdf").replace(" ", "_")
            st.download_button(
                label="⬇️ Download PDF",
                data=pdf_bytes,
                file_name=fname,
                mime="application/pdf",
                use_container_width=True
            )

        if st.session_state.get("prev_base_" + resume_id, False):
            resume_html = text_to_resume_html(content)
            st.markdown(resume_html, unsafe_allow_html=True)

    elif session_resume:
        # Fallback: show from session state
        word_count = len(session_resume.split())
        st.markdown(
            "<div class='base-card'>"
            "<div class='base-card-name'>📄 Resume (from session)</div>"
            "<div class='base-card-meta'>"
            "<span>📝 " + str(word_count) + " words</span>"
            "<span>💾 Not yet saved to backend</span>"
            "</div>"
            "</div>",
            unsafe_allow_html=True
        )
        st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)
        with st.expander("👁️ Preview"):
            st.markdown(text_to_resume_html(session_resume), unsafe_allow_html=True)
    else:
        st.markdown(
            "<div class='empty-wrap'>"
            "<div class='empty-icon'>📭</div>"
            "<div class='empty-title'>No base resume yet</div>"
            "<div class='empty-sub'>Upload your resume in the Profile page — it'll appear here automatically.</div>"
            "</div>",
            unsafe_allow_html=True
        )

    st.markdown("<div class='div'></div>", unsafe_allow_html=True)

    # ── Replace / Upload New ──────────────────────────────────────────────────
    st.markdown("<div class='sec-hd'>🔄 Replace Base Resume</div>", unsafe_allow_html=True)
    st.markdown("<div class='sec-sub'>Upload a new version to replace your current base resume.</div>", unsafe_allow_html=True)

    import PyPDF2, io
    uploaded = st.file_uploader("Upload PDF resume", type=["pdf"], key="arsenal_upload")
    resume_name_input = st.text_input("Resume label", placeholder="e.g. ML Engineer Resume v2", value="My Base Resume")

    if uploaded and st.button("💾 Save as New Base Resume", type="primary"):
        try:
            pdf_reader = PyPDF2.PdfReader(io.BytesIO(uploaded.read()))
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
            st.session_state.resume_text = text

            if backend_online:
                requests.post(API + "/resumes/base", json={
                    "name": resume_name_input,
                    "content": text,
                    "tags": session_profile.get("target_roles", [])[:3]
                }, timeout=5)
                st.success("✅ Saved to backend! Refresh to see it above.")
            else:
                st.success("✅ Saved to session! Start the backend to persist it.")
            st.rerun()
        except Exception as ex:
            st.error("Could not parse PDF: " + str(ex))

    if not backend_online:
        st.markdown(
            "<div style='background:rgba(239,68,68,0.07);border:1px solid rgba(239,68,68,0.2);"
            "border-radius:12px;padding:14px 18px;margin-top:12px'>"
            "<span style='color:#fca5a5;font-size:13px'>⚠️ Backend offline — data saved to session only. "
            "Run <code style='background:#111;padding:2px 6px;border-radius:4px'>cd backend && uvicorn main:app --reload</code> to persist.</span>"
            "</div>",
            unsafe_allow_html=True
        )


# ═══════════════════════════════════════════════════════════════════════════════
# TAB 2 — TAILORED RESUMES
# ═══════════════════════════════════════════════════════════════════════════════
with tab2:
    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

    if not company_resumes:
        st.markdown(
            "<div class='empty-wrap'>"
            "<div class='empty-icon'>🗂️</div>"
            "<div class='empty-title'>No tailored resumes yet</div>"
            "<div class='empty-sub'>Run the AI Agent on a job to generate your first tailored resume.</div>"
            "</div>",
            unsafe_allow_html=True
        )
        if st.button("🤖 Go to AI Agent →", type="primary"):
            st.switch_page("pages/4_agent.py")
    else:
        # Sort newest first
        ordered = list(reversed(company_resumes))

        for i, res in enumerate(ordered):
            res_id      = res.get("id", "company-" + str(i))
            company     = res.get("company", "Unknown Company")
            job_title   = res.get("job_title", "Unknown Role")
            content     = res.get("tailored_content", "")
            created     = res.get("created_at", "")
            got_callback = res_id in st.session_state.callback_flags

            callback_badge = "<span class='tcard-badge tcard-callback'>✓ Got Callback</span>" if got_callback else ""
            idx_badge = "<span class='tcard-badge'>#" + str(i + 1) + "</span>"

            st.markdown(
                "<div class='tcard'>"
                "<div class='tcard-inner'>"
                "<div>"
                "<div style='display:flex;align-items:center;gap:8px;margin-bottom:6px'>"
                + idx_badge + callback_badge +
                "</div>"
                "<div class='tcard-company'>" + company + "</div>"
                "<div class='tcard-role'>" + job_title + "</div>"
                "<div class='tcard-date'>📅 " + (created if created else "Recently generated") + " &nbsp;·&nbsp; "
                "📝 " + str(len(content.split())) + " words</div>"
                "</div>"
                "</div>"
                "</div>",
                unsafe_allow_html=True
            )

            b1, b2, b3, b4, b5 = st.columns([2, 2, 2, 2, 3])

            with b1:
                preview_key = "prev_" + res_id
                if preview_key not in st.session_state:
                    st.session_state[preview_key] = False
                plabel = "🙈 Hide" if st.session_state[preview_key] else "👁️ Preview"
                if st.button(plabel, key="view_" + res_id + str(i), use_container_width=True, type="secondary"):
                    st.session_state[preview_key] = not st.session_state[preview_key]
                    st.rerun()

            with b2:
                t_pdf = generate_pdf_bytes(content, company)
                t_fname = (company + "_" + job_title + "_resume.pdf").replace(" ", "_")
                st.download_button(
                    label="⬇️ Download PDF",
                    data=t_pdf,
                    file_name=t_fname,
                    mime="application/pdf",
                    key="dl_" + res_id + str(i),
                    use_container_width=True
                )

            with b3:
                cb_label = "★ Callback!" if got_callback else "☆ Got Callback?"
                if st.button(cb_label, key="cb_" + res_id + str(i), use_container_width=True, type="secondary"):
                    if got_callback:
                        st.session_state.callback_flags.discard(res_id)
                    else:
                        st.session_state.callback_flags.add(res_id)
                    st.rerun()

            with b4:
                if st.button("🗑️ Delete", key="del_" + res_id + str(i), use_container_width=True, type="secondary"):
                    try:
                        requests.delete(API + "/resumes/company/" + res_id, timeout=5)
                        st.success("Deleted!")
                        st.rerun()
                    except Exception:
                        st.warning("Could not delete — remove manually or restart backend.")

            with b5:
                if st.button("📤 Send to PDF Generator →", key="pdf_" + res_id + str(i), use_container_width=True):
                    st.session_state.resume_for_pdf   = content
                    st.session_state.profile_for_pdf  = session_profile
                    st.switch_page("pages/7_resume_output.py")

            # Preview
            if st.session_state.get("prev_" + res_id, False):
                t_html = text_to_resume_html(content)
                st.markdown(t_html, unsafe_allow_html=True)

            st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
# TAB 3 — PERFORMANCE INSIGHTS
# ═══════════════════════════════════════════════════════════════════════════════
with tab3:
    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

    total_resumes    = len(company_resumes)
    callback_count   = len(st.session_state.callback_flags)
    callback_rate    = int((callback_count / max(total_resumes, 1)) * 100)
    base_count       = len(base_resumes)

    # ── Stats row ──────────────────────────────────────────────────────────────
    s1, s2, s3, s4 = st.columns(4)
    with s1:
        st.markdown(
            "<div class='stat-card'>"
            "<div class='stat-num' style='color:var(--lav300)'>" + str(total_resumes) + "</div>"
            "<div class='stat-label'>Tailored Resumes</div>"
            "</div>", unsafe_allow_html=True
        )
    with s2:
        st.markdown(
            "<div class='stat-card'>"
            "<div class='stat-num' style='color:#6ee7b7'>" + str(callback_count) + "</div>"
            "<div class='stat-label'>Callbacks Received</div>"
            "</div>", unsafe_allow_html=True
        )
    with s3:
        rate_color = "#6ee7b7" if callback_rate >= 30 else "#fcd34d" if callback_rate >= 10 else "#fca5a5"
        st.markdown(
            "<div class='stat-card'>"
            "<div class='stat-num' style='color:" + rate_color + "'>" + str(callback_rate) + "%</div>"
            "<div class='stat-label'>Callback Rate</div>"
            "</div>", unsafe_allow_html=True
        )
    with s4:
        st.markdown(
            "<div class='stat-card'>"
            "<div class='stat-num' style='color:var(--indigo)'>" + str(base_count) + "</div>"
            "<div class='stat-label'>Base Resumes</div>"
            "</div>", unsafe_allow_html=True
        )

    st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)

    if total_resumes == 0:
        st.markdown(
            "<div class='empty-wrap'>"
            "<div class='empty-icon'>📊</div>"
            "<div class='empty-title'>No data yet</div>"
            "<div class='empty-sub'>Generate tailored resumes and mark callbacks to see insights here.</div>"
            "</div>",
            unsafe_allow_html=True
        )
    else:
        col_a, col_b = st.columns(2)

        # ── Which resumes got callbacks ─────────────────────────────────────
        with col_a:
            st.markdown(
                "<div class='insight-card'>"
                "<div class='insight-card-title'>🏆 Callback Performance by Company</div>",
                unsafe_allow_html=True
            )

            if company_resumes:
                for res in company_resumes:
                    res_id    = res.get("id", "")
                    company   = res.get("company", "Unknown")
                    got_cb    = res_id in st.session_state.callback_flags
                    bar_w     = "100" if got_cb else "20"
                    bar_col   = "#6ee7b7" if got_cb else "rgba(168,85,247,0.3)"
                    label     = "✓ Callback" if got_cb else "No response"
                    label_col = "#6ee7b7" if got_cb else "#4b5563"

                    st.markdown(
                        "<div class='bar-row'>"
                        "<span class='bar-label'>" + company[:18] + "</span>"
                        "<div class='bar-bg'>"
                        "<div class='bar-fill' style='width:" + bar_w + "%;background:" + bar_col + "'></div>"
                        "</div>"
                        "<span style='font-family:JetBrains Mono,monospace;font-size:10px;color:" + label_col + ";min-width:80px;text-align:right'>" + label + "</span>"
                        "</div>",
                        unsafe_allow_html=True
                    )
            else:
                st.markdown("<p style='color:var(--muted);font-size:14px'>No tailored resumes yet.</p>", unsafe_allow_html=True)

            st.markdown("</div>", unsafe_allow_html=True)

        # ── Keyword analysis ────────────────────────────────────────────────
        with col_b:
            st.markdown(
                "<div class='insight-card'>"
                "<div class='insight-card-title'>🔑 Keyword Intelligence</div>",
                unsafe_allow_html=True
            )

            # Gather keywords from agent results if available
            agent_result = st.session_state.get("agent_result", {})
            diagnostic   = agent_result.get("diagnostic", {}) if agent_result else {}
            present_kw   = diagnostic.get("present_keywords", []) if diagnostic else []
            missing_kw   = diagnostic.get("missing_keywords", []) if diagnostic else []

            if present_kw or missing_kw:
                if present_kw:
                    st.markdown(
                        "<div style='font-family:JetBrains Mono,monospace;font-size:10px;"
                        "color:#6ee7b7;text-transform:uppercase;letter-spacing:0.1em;margin-bottom:8px'>"
                        "✅ Keywords that matched</div>",
                        unsafe_allow_html=True
                    )
                    pills = "".join(["<span class='kpill-hit'>✓ " + k + "</span>" for k in present_kw[:12]])
                    st.markdown("<div>" + pills + "</div>", unsafe_allow_html=True)

                if missing_kw:
                    st.markdown(
                        "<div style='font-family:JetBrains Mono,monospace;font-size:10px;"
                        "color:#fca5a5;text-transform:uppercase;letter-spacing:0.1em;margin:14px 0 8px'>"
                        "⚠️ Keywords you were missing</div>",
                        unsafe_allow_html=True
                    )
                    pills = "".join(["<span class='kpill-miss'>✗ " + k + "</span>" for k in missing_kw[:12]])
                    st.markdown("<div>" + pills + "</div>", unsafe_allow_html=True)
            else:
                st.markdown(
                    "<p style='color:var(--muted);font-size:14px'>"
                    "Run the AI Agent on a job to see keyword analysis here. "
                    "The agent identifies which keywords your resume has vs. what the job requires."
                    "</p>",
                    unsafe_allow_html=True
                )

            st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)

        # ── Tips based on data ──────────────────────────────────────────────
        st.markdown(
            "<div class='insight-card'>"
            "<div class='insight-card-title'>💡 Recommendations</div>",
            unsafe_allow_html=True
        )

        tips = []
        if total_resumes > 0 and callback_count == 0:
            tips.append("📌 No callbacks yet — try adding more missing keywords to your next tailored resume.")
        if total_resumes >= 3 and callback_rate < 20:
            tips.append("📌 Callback rate below 20% — consider rewriting your summary section to be more role-specific.")
        if missing_kw:
            top_missing = ", ".join(missing_kw[:3])
            tips.append("📌 Top missing keywords from last analysis: <b style='color:#fcd34d'>" + top_missing + "</b> — add these where truthful.")
        if callback_count > 0:
            tips.append("🎉 You're getting callbacks! Keep using similar language patterns in future resumes.")
        if total_resumes == 0:
            tips.append("📌 Generate your first tailored resume by clicking 🤖 AI Agent and selecting a job.")

        if not tips:
            tips.append("✅ Things look good! Keep tailoring per job and marking your callbacks for better insights.")

        for tip in tips:
            st.markdown(
                "<div style='display:flex;align-items:flex-start;gap:10px;margin-bottom:10px;"
                "padding:10px 14px;background:rgba(255,255,255,0.02);border-radius:10px;"
                "border-left:3px solid rgba(168,85,247,0.4)'>"
                "<span style='font-size:14px;color:var(--txt2);line-height:1.6'>" + tip + "</span>"
                "</div>",
                unsafe_allow_html=True
            )

        st.markdown("</div>", unsafe_allow_html=True)
