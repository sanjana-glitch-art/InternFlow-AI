import streamlit as st
import requests
from datetime import datetime, timezone

st.set_page_config(
    page_title="InternFlow AI – Jobs",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="collapsed"
)

API = "http://127.0.0.1:8000"

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500&family=DM+Mono:wght@400;500&display=swap');

#MainMenu{visibility:hidden;}footer{visibility:hidden;}header{visibility:hidden;}
[data-testid="collapsedControl"]{display:none;}
* {box-sizing:border-box;}

:root {
  --black: #030305; --card: #0e0e1c; --border: rgba(118,185,0,0.15);
  --green: #76B900; --green-dim: rgba(118,185,0,0.08);
  --white: #f0efe8; --muted: #6b6b80;
  --font-display: 'Syne', sans-serif;
  --font-body: 'DM Sans', sans-serif;
  --font-mono: 'DM Mono', monospace;
}

.stApp { background: var(--black) !important; font-family: var(--font-body); color: var(--white); }
.block-container { padding: 0 !important; max-width: 100% !important; }
.wrap { max-width: 1100px; margin: 0 auto; padding: 0 48px; }

.nav { padding: 24px 0; display: flex; align-items: center; justify-content: space-between; border-bottom: 1px solid var(--border); margin-bottom: 40px; }
.nav-logo { font-family: var(--font-display); font-size: 18px; font-weight: 800; color: var(--white); }
.nav-logo span { color: var(--green); }

.page-h { font-family: var(--font-display); font-size: clamp(28px,3vw,44px); font-weight: 800; letter-spacing:-1px; color: var(--white); margin-bottom: 4px; }
.page-h em { font-style: normal; color: var(--green); }
.page-sub { font-size: 15px; color: var(--muted); font-weight: 300; margin-bottom: 32px; }

.job-card {
  background: var(--card); border: 1px solid var(--border);
  border-radius: 14px; padding: 24px 28px; margin-bottom: 12px;
  transition: border-color 0.2s, transform 0.2s;
}
.job-card:hover { border-color: rgba(118,185,0,0.35); transform: translateY(-2px); }
.job-title { font-family: var(--font-display); font-size: 17px; font-weight: 700; color: var(--white); margin-bottom: 4px; }
.job-company { font-size: 14px; color: var(--green); font-weight: 500; margin-bottom: 4px; }
.job-location { font-size: 13px; color: var(--muted); margin-bottom: 10px; }
.job-desc { font-size: 13px; color: var(--muted); line-height: 1.6; margin-bottom: 12px; }
.job-tags { display: flex; flex-wrap: wrap; gap: 6px; margin-bottom: 14px; }
.tag { font-family: var(--font-mono); font-size: 10px; padding: 3px 10px; border-radius: 100px; background: var(--green-dim); color: var(--green); border: 1px solid rgba(118,185,0,0.2); }
.tag-gray { font-family: var(--font-mono); font-size: 10px; padding: 3px 10px; border-radius: 100px; background: rgba(255,255,255,0.03); color: var(--muted); border: 1px solid rgba(255,255,255,0.06); }
.count-badge { font-family: var(--font-mono); font-size: 12px; color: var(--green); background: var(--green-dim); border: 1px solid rgba(118,185,0,0.2); border-radius: 100px; padding: 4px 14px; display: inline-block; margin-bottom: 20px; }

.stButton > button { background: var(--green) !important; color: #000 !important; border: none !important; border-radius: 8px !important; font-family: var(--font-display) !important; font-size: 13px !important; font-weight: 700 !important; padding: 8px 20px !important; height: auto !important; transition: opacity 0.2s !important; }
.stButton > button:hover { opacity: 0.85 !important; }
.stButton > button[kind="secondary"] { background: transparent !important; color: var(--green) !important; border: 1px solid rgba(118,185,0,0.25) !important; font-size: 12px !important; }
.stTextInput > div > div > input { background: #0a0a14 !important; border: 1px solid rgba(118,185,0,0.2) !important; border-radius: 10px !important; color: var(--white) !important; }
.stSelectbox > div > div { background: #0a0a14 !important; border: 1px solid rgba(118,185,0,0.2) !important; border-radius: 10px !important; color: var(--white) !important; }
label { color: var(--muted) !important; font-size: 13px !important; }
</style>
""", unsafe_allow_html=True)

def is_active(job: dict) -> bool:
    if job.get("active") is False:
        return False
    date_updated = job.get("date_updated") or job.get("date_posted") or ""
    if date_updated:
        try:
            if isinstance(date_updated, (int, float)):
                ts = datetime.fromtimestamp(date_updated, tz=timezone.utc)
            else:
                ts = datetime.fromisoformat(str(date_updated).replace("Z","+00:00"))
            if (datetime.now(timezone.utc) - ts).days > 90:
                return False
        except Exception:
            pass
    return True

# ── Navbar ────────────────────────────────────────────────────────────────────
st.markdown("<div class='wrap'>", unsafe_allow_html=True)
n1, n2, n3, n4, n5 = st.columns([3, 1, 1, 1, 1])
with n1:
    st.markdown("<div class='nav-logo'>Intern<span>Flow</span> AI</div>", unsafe_allow_html=True)
with n2:
    if st.button("📝 Profile", use_container_width=True): st.switch_page("pages/2_onboarding.py")
with n3:
    if st.button("💼 Jobs", type="primary", use_container_width=True): pass
with n4:
    if st.button("📂 Arsenal", use_container_width=True): st.switch_page("pages/5_resume_arsenal.py")
with n5:
    name = st.session_state.get("profile",{}).get("name","")
    if name:
        st.markdown(f"<div style='font-size:13px;color:var(--muted);padding-top:10px;text-align:right'>👋 {name}</div>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

st.markdown("""
<div class='wrap'>
  <div class='page-h'>Internship <em>Listings</em></div>
  <p class='page-sub'>Live openings from Simplify Jobs — active listings only.</p>
</div>
""", unsafe_allow_html=True)

# ── Filters ───────────────────────────────────────────────────────────────────
st.markdown("<div class='wrap'>", unsafe_allow_html=True)

# Role dropdown — maps display name to search keyword
ROLE_OPTIONS = {
    "All Roles":                "",
    "Machine Learning Engineer":"machine learning",
    "Data Scientist":           "data scientist",
    "Data Analyst":             "data analyst",
    "Data Engineer":            "data engineer",
    "AI Engineer":              "ai engineer",
    "Software Engineer":        "software engineer",
    "Backend Engineer":         "backend",
    "Computer Vision":          "computer vision",
    "NLP Engineer":             "nlp",
    "Research Scientist":       "research scientist",
    "GenAI Engineer":           "generative ai",
    "Quantitative Analyst":     "quantitative",
}

f1, f2, f3, f4 = st.columns([2, 2, 2, 1])
with f1:
    selected_role = st.selectbox("🎯 Role", list(ROLE_OPTIONS.keys()), index=0)
with f2:
    search = st.text_input("🔍 Search", placeholder="e.g. Google, PyTorch, Remote")
with f3:
    location = st.text_input("📍 Location", placeholder="e.g. San Francisco, Remote")
with f4:
    limit = st.selectbox("Show", [25, 50, 100], index=0)

# Build search query — combine role keyword + custom search
role_keyword = ROLE_OPTIONS[selected_role]
combined_search = " ".join(filter(None, [role_keyword, search])).strip()

# ── Fetch jobs ────────────────────────────────────────────────────────────────
try:
    params = {"limit": limit * 2}
    if combined_search: params["search"] = combined_search
    if location:        params["location"] = location

    resp = requests.get(f"{API}/jobs/", params=params, timeout=10)
    data = resp.json()
    all_jobs = data.get("jobs", data if isinstance(data, list) else [])
    active_jobs = [j for j in all_jobs if is_active(j)][:limit]

    st.markdown(f"<div class='count-badge'>🟢 {len(active_jobs)} active listings{' · ' + selected_role if selected_role != 'All Roles' else ''}</div>", unsafe_allow_html=True)

    if not active_jobs:
        st.info("No active listings found. Try a different role or search term.")

    for job in active_jobs:
        title       = job.get("title","Unknown Role")
        company     = job.get("company","Unknown Company")
        locations   = ", ".join(job.get("locations",[]))
        desc        = (job.get("description","") or "")[:220]
        url         = job.get("url","#")
        terms       = job.get("terms",[]) or []
        sponsorship = job.get("sponsorship","")

        st.markdown(f"""
        <div class='job-card'>
          <div class='job-title'>{title}</div>
          <div class='job-company'>{company}</div>
          <div class='job-location'>📍 {locations if locations else "Location not specified"}</div>
          <div class='job-desc'>{desc}{"..." if len(job.get("description","") or "") > 220 else ""}</div>
          <div class='job-tags'>
            {"<span class='tag'>" + sponsorship + "</span>" if sponsorship else ""}
            {"".join([f"<span class='tag-gray'>{t}</span>" for t in terms])}
          </div>
        </div>
        """, unsafe_allow_html=True)

        b1, b2, _ = st.columns([2, 2, 4])
        with b1:
            if st.button("🤖 Analyse with AI", key=f"ai_{job.get('id',title+company)}", type="primary"):
                st.session_state.selected_job = job
                st.switch_page("pages/4_agent.py")
        with b2:
            st.markdown(f"<a href='{url}' target='_blank' style='display:inline-block;margin-top:8px;font-size:12px;color:var(--green);text-decoration:none;font-family:var(--font-mono)'>🔗 View Posting →</a>", unsafe_allow_html=True)

        st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)

except requests.exceptions.ConnectionError:
    st.error("❌ Cannot connect to backend. Run: `cd backend && python -m uvicorn main:app --reload`")
except Exception as e:
    st.error(f"Something went wrong: {e}")

st.markdown("</div>", unsafe_allow_html=True)