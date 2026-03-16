import streamlit as st
import requests
import PyPDF2
import io
import re
import os
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(
    page_title="InternFlow AI – Setup",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="collapsed"
)

API = "http://127.0.0.1:8000"
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN", "")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500&family=DM+Mono:wght@400;500&display=swap');

#MainMenu{visibility:hidden;}footer{visibility:hidden;}header{visibility:hidden;}
[data-testid="collapsedControl"]{display:none;}
* {box-sizing:border-box;}

:root {
  --black: #030305;
  --dark: #080810;
  --card: #0e0e1c;
  --border: rgba(118,185,0,0.15);
  --green: #76B900;
  --green-dim: rgba(118,185,0,0.08);
  --white: #f0efe8;
  --muted: #6b6b80;
  --font-display: 'Syne', sans-serif;
  --font-body: 'DM Sans', sans-serif;
  --font-mono: 'DM Mono', monospace;
}

.stApp { background: var(--black) !important; font-family: var(--font-body); color: var(--white); }
.block-container { padding: 0 !important; max-width: 100% !important; }
.wrap { max-width: 860px; margin: 0 auto; padding: 0 48px; }

.nav { padding: 24px 0; display: flex; align-items: center; justify-content: space-between; border-bottom: 1px solid var(--border); margin-bottom: 56px; }
.nav-logo { font-family: var(--font-display); font-size: 18px; font-weight: 800; color: var(--white); }
.nav-logo span { color: var(--green); }

.page-h { font-family: var(--font-display); font-size: clamp(32px, 4vw, 52px); font-weight: 800; letter-spacing: -1.5px; color: var(--white); margin-bottom: 8px; }
.page-h em { font-style: normal; color: var(--green); }
.page-sub { font-size: 16px; color: var(--muted); font-weight: 300; margin-bottom: 48px; }

.step-card {
  background: var(--card);
  border: 1px solid var(--border);
  border-radius: 16px;
  padding: 32px;
  margin-bottom: 24px;
  position: relative;
  overflow: hidden;
}
.step-card::before {
  content: '';
  position: absolute;
  top: 0; left: 0; right: 0;
  height: 1px;
  background: linear-gradient(90deg, transparent, rgba(118,185,0,0.3), transparent);
}
.step-label { font-family: var(--font-mono); font-size: 10px; color: var(--green); letter-spacing: 0.2em; text-transform: uppercase; margin-bottom: 6px; }
.step-title { font-family: var(--font-display); font-size: 18px; font-weight: 700; color: var(--white); margin-bottom: 4px; }
.step-desc { font-size: 13px; color: var(--muted); margin-bottom: 20px; }

.proj-row {
  background: rgba(118,185,0,0.04);
  border: 1px solid rgba(118,185,0,0.18);
  border-left: 3px solid var(--green);
  border-radius: 10px;
  padding: 12px 16px;
  margin-bottom: 8px;
}
.proj-name { font-size: 14px; font-weight: 600; color: var(--white); margin-bottom: 3px; }
.proj-meta { font-family: var(--font-mono); font-size: 11px; color: var(--green); opacity: 0.7; margin-bottom: 4px; }
.proj-desc { font-size: 12px; color: var(--muted); line-height: 1.5; }

.stButton > button {
  background: var(--green) !important; color: #000 !important;
  border: none !important; border-radius: 10px !important;
  font-family: var(--font-display) !important; font-size: 15px !important;
  font-weight: 700 !important; padding: 12px 32px !important;
  height: auto !important; transition: opacity 0.2s !important;
}
.stButton > button:hover { opacity: 0.85 !important; }
.stButton > button[kind="secondary"] {
  background: transparent !important; color: var(--green) !important;
  border: 1px solid rgba(118,185,0,0.3) !important;
}
.stTextInput > div > div > input {
  background: #0a0a14 !important; border: 1px solid rgba(118,185,0,0.2) !important;
  border-radius: 10px !important; color: var(--white) !important;
  font-family: var(--font-body) !important;
}
.stTextInput > div > div > input:focus {
  border-color: rgba(118,185,0,0.5) !important;
  box-shadow: 0 0 0 2px rgba(118,185,0,0.1) !important;
}
label { color: var(--muted) !important; font-size: 13px !important; }
.stMultiSelect > div { background: #0a0a14 !important; border: 1px solid rgba(118,185,0,0.2) !important; border-radius: 10px !important; }
.stFileUploader > div { background: #0a0a14 !important; border: 1px dashed rgba(118,185,0,0.3) !important; border-radius: 10px !important; }
.stTabs [data-baseweb="tab"] { font-family: var(--font-body) !important; color: var(--muted) !important; }
.stTabs [aria-selected="true"] { color: var(--green) !important; border-bottom-color: var(--green) !important; }
</style>
""", unsafe_allow_html=True)

# ── Session state ─────────────────────────────────────────────────────────────
if "profile"     not in st.session_state: st.session_state.profile     = {}
if "projects"    not in st.session_state: st.session_state.projects    = []
if "resume_text" not in st.session_state: st.session_state.resume_text = ""

# ── GitHub helper ─────────────────────────────────────────────────────────────
def gh_headers(accept="application/vnd.github.v3+json"):
    h = {"Accept": accept}
    if GITHUB_TOKEN:
        h["Authorization"] = f"token {GITHUB_TOKEN}"
    return h

# ── Navbar ────────────────────────────────────────────────────────────────────
st.markdown("<div class='wrap'>", unsafe_allow_html=True)
n1, n2, n3, n4 = st.columns([3, 1, 1, 1])
with n1:
    st.markdown("<div class='nav-logo'>Intern<span>Flow</span> AI</div>", unsafe_allow_html=True)
with n2:
    if st.button("📝 Profile", type="primary", use_container_width=True): pass
with n3:
    if st.button("💼 Jobs", use_container_width=True):
        st.switch_page("pages/3_jobs.py")
with n4:
    if st.button("📂 Arsenal", use_container_width=True):
        st.switch_page("pages/5_resume_arsenal.py")
st.markdown("</div>", unsafe_allow_html=True)

st.markdown("""
<div class='wrap'>
  <div class='page-h'>Let's set you <em>up.</em></div>
  <p class='page-sub'>Tell us about yourself so Nemotron can personalize everything.</p>
</div>
""", unsafe_allow_html=True)

st.markdown("<div class='wrap'>", unsafe_allow_html=True)

# ── STEP 1: Basic Info ────────────────────────────────────────────────────────
st.markdown("""
<div class='step-card'>
  <div class='step-label'>Step 01</div>
  <div class='step-title'>👤 Basic Information</div>
  <div class='step-desc'>This populates your resume header and personalizes AI output.</div>
</div>
""", unsafe_allow_html=True)

c1, c2 = st.columns(2)
with c1:
    name       = st.text_input("Full Name",           placeholder="e.g. Sreeram Achutuni",         value=st.session_state.profile.get("name",""))
    email      = st.text_input("Email",               placeholder="e.g. sreeram@sjsu.edu",          value=st.session_state.profile.get("email",""))
    phone      = st.text_input("Phone",               placeholder="e.g. +1 (408) 123-4567",         value=st.session_state.profile.get("phone",""))
with c2:
    university = st.text_input("University",          placeholder="e.g. San José State University", value=st.session_state.profile.get("university",""))
    degree     = st.text_input("Degree & Major",      placeholder="e.g. MS Data Analytics",         value=st.session_state.profile.get("degree",""))
    graduation = st.text_input("Expected Graduation", placeholder="e.g. May 2027",                  value=st.session_state.profile.get("graduation",""))

linkedin       = st.text_input("LinkedIn URL",       placeholder="https://linkedin.com/in/yourname", value=st.session_state.profile.get("linkedin",""))
github_profile = st.text_input("GitHub Profile URL", placeholder="https://github.com/yourusername",  value=st.session_state.profile.get("github",""))

role_options = ["ML Engineer","Data Scientist","Data Analyst","Data Engineer","AI Engineer",
                "Research Engineer","Software Engineer","Backend Engineer","Computer Vision Engineer",
                "NLP Engineer","Quantitative Analyst","GenAI Engineer"]
target_roles = st.multiselect("Target Roles", role_options,
    default=st.session_state.profile.get("target_roles",["ML Engineer","Data Scientist"]))

st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

# ── STEP 2: Resume Upload ──────────────────────────────────────────────────────
st.markdown("""
<div class='step-card'>
  <div class='step-label'>Step 02</div>
  <div class='step-title'>📄 Upload Your Resume</div>
  <div class='step-desc'>Upload as PDF — we parse it and use it as the base for all tailoring.</div>
</div>
""", unsafe_allow_html=True)

uploaded_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])
if uploaded_file:
    try:
        pdf_reader = PyPDF2.PdfReader(io.BytesIO(uploaded_file.read()))
        raw = [page.extract_text() or "" for page in pdf_reader.pages]
        raw_text = "\n".join(raw)
        raw_text = re.sub(r'-\n(\S)', r'\1', raw_text)
        raw_text = re.sub(r'(?<![.,:;])\n(?=[a-z(@/])', r' ', raw_text)
        raw_text = re.sub(r' {2,}', ' ', raw_text)
        raw_text = re.sub(r'\n{3,}', '\n\n', raw_text)
        st.session_state.resume_text = raw_text.strip()
        st.success(f"✅ Parsed {len(pdf_reader.pages)} page(s) — {len(raw_text):,} characters")
        with st.expander("Preview extracted text"):
            st.text(raw_text[:1200] + "..." if len(raw_text) > 1200 else raw_text)
        try:
            requests.post(f"{API}/resumes/base", json={
                "name": f"{name}'s Resume" if name else "Base Resume",
                "content": raw_text.strip(),
                "tags": target_roles[:3]
            }, timeout=5)
        except Exception:
            pass
    except Exception as e:
        st.error(f"Could not parse PDF: {e}")
elif st.session_state.resume_text:
    st.success("✅ Resume already loaded from this session.")

st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

# ── STEP 3: GitHub Projects ───────────────────────────────────────────────────
st.markdown("""
<div class='step-card'>
  <div class='step-label'>Step 03</div>
  <div class='step-title'>🐙 Import Projects from GitHub</div>
  <div class='step-desc'>We scrape your repos, READMEs, stars, and languages automatically. You can also add projects manually.</div>
</div>
""", unsafe_allow_html=True)

tab1, tab2 = st.tabs(["🐙 Import from GitHub", "✏️ Add Manually"])

with tab1:
    gh_url = st.text_input("GitHub Profile URL", placeholder="https://github.com/yourusername", key="gh_import_url")

    if not GITHUB_TOKEN:
        st.markdown("""
        <div style='background:rgba(252,211,77,0.06);border:1px solid rgba(252,211,77,0.2);
        border-radius:8px;padding:10px 14px;font-size:12px;color:#fcd34d;margin-bottom:10px'>
        ⚠️ No GitHub token found in .env — you may hit rate limits (60 req/hr).
        Add GITHUB_TOKEN to your .env for 5,000 req/hr.
        </div>
        """, unsafe_allow_html=True)

    if st.button("🔍 Scrape GitHub Projects"):
        if gh_url:
            with st.spinner("Fetching your repos..."):
                try:
                    username = gh_url.rstrip("/").split("/")[-1]
                    # Remove https://github.com/ prefix if present
                    if "github.com" in username:
                        username = username.split("github.com/")[-1].strip("/")

                    resp = requests.get(
                        f"https://api.github.com/users/{username}/repos?sort=updated&per_page=30",
                        headers=gh_headers(),
                        timeout=10
                    )

                    if resp.status_code == 200:
                        repos = resp.json()
                        imported = 0
                        existing = [p["name"] for p in st.session_state.projects]

                        for repo in repos:
                            if repo.get("fork"): continue
                            rname = repo["name"]
                            desc  = repo.get("description","") or ""
                            stars = repo.get("stargazers_count",0)
                            lang  = repo.get("language","Unknown") or "Unknown"

                            readme = ""
                            try:
                                rr = requests.get(
                                    f"https://api.github.com/repos/{username}/{rname}/readme",
                                    headers=gh_headers("application/vnd.github.v3.raw"),
                                    timeout=5
                                )
                                if rr.status_code == 200:
                                    readme = rr.text[:400]
                            except Exception:
                                pass

                            proj_desc = f"{desc}. " if desc else ""
                            proj_desc += f"Language: {lang}. Stars: {stars}."
                            if readme:
                                proj_desc += f" README: {readme[:300]}"

                            if rname not in existing and proj_desc.strip():
                                st.session_state.projects.append({
                                    "name":        rname,
                                    "description": proj_desc.strip(),
                                    "source":      "github",
                                    "language":    lang,
                                    "stars":       stars
                                })
                                imported += 1

                        st.success(f"✅ Imported {imported} projects from @{username}!")
                        st.rerun()

                    elif resp.status_code == 403:
                        st.error("❌ GitHub rate limit hit. Add GITHUB_TOKEN to your .env file to fix this.")
                    elif resp.status_code == 404:
                        st.error(f"❌ GitHub user '{username}' not found. Check the username.")
                    else:
                        st.error(f"❌ GitHub API error (status {resp.status_code}).")

                except Exception as e:
                    st.error(f"Scraping failed: {e}")
        else:
            st.warning("Please enter your GitHub URL.")

with tab2:
    pc1, pc2 = st.columns(2)
    with pc1:
        pname = st.text_input("Project Name", placeholder="e.g. PAMAP2 Activity Recognition")
    with pc2:
        plang = st.text_input("Tech Stack", placeholder="e.g. Python, PyTorch, Streamlit")
    pdesc = st.text_area("Description", height=80,
        placeholder="e.g. Built HAR system using Random Forest on 2.8M records achieving 94.2% accuracy.")
    if st.button("➕ Add Project"):
        if pname and pdesc:
            existing = [p["name"] for p in st.session_state.projects]
            if pname in existing:
                st.warning("Already exists.")
            else:
                st.session_state.projects.append({
                    "name":        pname,
                    "description": f"{pdesc} Tech: {plang}" if plang else pdesc,
                    "source":      "manual",
                    "language":    plang,
                    "stars":       0
                })
                st.success(f"✅ Added: {pname}")
                st.rerun()
        else:
            st.warning("Please fill in name and description.")

# ── Projects list ─────────────────────────────────────────────────────────────
if st.session_state.projects:
    st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)
    st.markdown(f"<div style='font-family:var(--font-mono);font-size:11px;color:var(--green);letter-spacing:0.15em;text-transform:uppercase;margin-bottom:12px'>Portfolio — {len(st.session_state.projects)} project(s)</div>", unsafe_allow_html=True)
    for i, p in enumerate(st.session_state.projects):
        col_p, col_rm = st.columns([10, 1])
        with col_p:
            badge = "🐙" if p.get("source") == "github" else "✏️"
            lang  = p.get("language","")
            stars = p.get("stars",0)
            desc  = p["description"][:140] + "..." if len(p["description"]) > 140 else p["description"]
            meta  = f"{lang}" + (f" · ⭐ {stars}" if stars > 0 else "")
            st.markdown(f"""
            <div class='proj-row'>
              <div class='proj-name'>{badge} {p['name']}</div>
              <div class='proj-meta'>{meta}</div>
              <div class='proj-desc'>{desc}</div>
            </div>
            """, unsafe_allow_html=True)
        with col_rm:
            st.markdown("<div style='height:18px'></div>", unsafe_allow_html=True)
            if st.button("✕", key=f"rm_{i}", use_container_width=True):
                st.session_state.projects.pop(i)
                st.rerun()
else:
    st.markdown("""
    <div style='background:rgba(118,185,0,0.03);border:1px dashed rgba(118,185,0,0.2);
    border-radius:10px;padding:20px;text-align:center;color:var(--muted);font-size:14px;margin-top:16px'>
    No projects yet — import from GitHub or add manually above.
    </div>
    """, unsafe_allow_html=True)

st.markdown("<div style='height:32px'></div>", unsafe_allow_html=True)

# ── Save & Continue ───────────────────────────────────────────────────────────
_, btn_col, _ = st.columns([1, 2, 1])
with btn_col:
    if st.button("💾 Save Profile & Browse Jobs →", type="primary", use_container_width=True):
        if not name:
            st.warning("Please enter your name.")
        elif not st.session_state.resume_text and not st.session_state.projects:
            st.warning("Please upload a resume or add at least one project.")
        else:
            st.session_state.profile = {
                "name": name, "email": email, "phone": phone,
                "university": university, "degree": degree, "graduation": graduation,
                "linkedin": linkedin, "github": github_profile,
                "target_roles": target_roles,
            }
            st.success("✅ Profile saved!")
            st.switch_page("pages/3_jobs.py")

st.markdown("</div>", unsafe_allow_html=True)