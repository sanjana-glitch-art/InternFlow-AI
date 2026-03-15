import streamlit as st
import requests

st.set_page_config(
    page_title="InternFlow AI – Jobs",
    page_icon="💼",
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
    --bg:     #08080f;
    --txt:    #f1f0f8;
    --txt2:   #c4c2dc;
    --muted:  #7c7a9a;
    --faint:  #2d2b45;
    --bdr:    rgba(168,85,247,0.18);
    --bdr2:   rgba(168,85,247,0.38);
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
    transition: border-color 0.2s !important;
}
.stTextInput > div > div > input:focus {
    border-color: rgba(168,85,247,0.55) !important;
}
.stTextInput label {
    color: var(--muted) !important;
    font-family: 'Outfit', sans-serif !important;
    font-size: 13px !important;
    font-weight: 500 !important;
}
.stSelectbox > div > div {
    background: rgba(255,255,255,0.03) !important;
    border: 1px solid rgba(168,85,247,0.22) !important;
    border-radius: 12px !important;
    color: var(--txt) !important;
}
.stSelectbox label {
    color: var(--muted) !important;
    font-family: 'Outfit', sans-serif !important;
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
.stButton > button:hover {
    opacity: 0.85 !important;
    transform: translateY(-1px) !important;
}
.stButton > button[kind="secondary"] {
    background: rgba(168,85,247,0.07) !important;
    border: 1px solid rgba(168,85,247,0.28) !important;
    color: var(--lav300) !important;
}
.stButton > button[kind="secondary"]:hover {
    background: rgba(168,85,247,0.14) !important;
}

/* Nav */
.nav-logo {
    font-family: 'Outfit', sans-serif;
    font-size: 21px;
    font-weight: 800;
    background: linear-gradient(135deg, #c4b5fd, #a78bfa);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
.nav-tagline {
    font-family: 'JetBrains Mono', monospace;
    font-size: 10px;
    color: var(--faint);
    letter-spacing: 0.12em;
    margin-top: 2px;
}

/* Divider */
.div {
    border: none;
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(168,85,247,0.2), transparent);
    margin: 18px 0;
}

/* Page header */
.page-hd {
    font-family: 'Instrument Serif', serif;
    font-size: clamp(30px, 3.5vw, 46px);
    font-weight: 400;
    color: var(--txt);
    letter-spacing: -1px;
    margin: 0 0 5px;
    line-height: 1.1;
}
.page-hd em { font-style: italic; color: var(--lav300); }
.page-sub { font-size: 15px; color: var(--muted); font-weight: 300; }
.page-sub span { color: var(--lav300); font-weight: 500; }

/* Search wrap */
.search-wrap {
    background: rgba(255,255,255,0.015);
    border: 1px solid rgba(168,85,247,0.14);
    border-radius: 16px;
    padding: 22px 24px 16px;
    margin-bottom: 10px;
}

/* Result count */
.result-count {
    font-family: 'JetBrains Mono', monospace;
    font-size: 12px;
    color: var(--muted);
    margin-bottom: 14px;
}
.result-count span { color: var(--lav400); font-weight: 700; }

/* Job card */
.jcard {
    background: rgba(255,255,255,0.022);
    border: 1px solid var(--bdr);
    border-radius: 18px;
    padding: 22px 26px 16px;
    margin-bottom: 12px;
    position: relative;
    overflow: hidden;
    transition: border-color 0.22s, transform 0.18s, box-shadow 0.22s;
}
.jcard:hover {
    border-color: var(--bdr2);
    transform: translateY(-2px);
    box-shadow: 0 8px 40px rgba(168,85,247,0.08);
}
.jcard::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(168,85,247,0.28), transparent);
}
.jcard-top-pick {
    border-color: rgba(168,85,247,0.42) !important;
    background: rgba(168,85,247,0.05) !important;
}

/* Card layout */
.jcard-inner {
    display: flex;
    align-items: flex-start;
    justify-content: space-between;
    gap: 20px;
}
.jcard-body { flex: 1; min-width: 0; }
.jcard-sidebar {
    display: flex;
    flex-direction: column;
    align-items: flex-end;
    gap: 10px;
    flex-shrink: 0;
}

/* Card text */
.jbadge-row {
    display: flex;
    align-items: center;
    gap: 8px;
    margin-bottom: 8px;
    flex-wrap: wrap;
}
.jtitle {
    font-family: 'Outfit', sans-serif;
    font-size: 17px;
    font-weight: 700;
    color: var(--txt);
    margin-bottom: 4px;
    letter-spacing: -0.3px;
    line-height: 1.3;
}
.jcompany { font-size: 14px; color: var(--lav400); font-weight: 600; margin-bottom: 2px; }
.jloc { font-size: 13px; color: var(--muted); }
.jdesc { font-size: 13.5px; color: #6b7a99; margin-top: 10px; line-height: 1.65; }

/* Score ring */
.score-ring {
    width: 64px; height: 64px;
    border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    flex-direction: column;
    border: 2.5px solid;
    flex-shrink: 0;
}
.score-num {
    font-family: 'Instrument Serif', serif;
    font-size: 20px;
    line-height: 1;
}
.score-lbl {
    font-family: 'JetBrains Mono', monospace;
    font-size: 8px;
    letter-spacing: 0.05em;
    margin-top: 2px;
}

/* Score mini bars */
.score-breakdown { display: flex; flex-direction: column; gap: 5px; align-items: flex-end; }
.score-row { display: flex; align-items: center; gap: 6px; }
.score-key {
    font-family: 'JetBrains Mono', monospace;
    font-size: 10px;
    color: var(--faint);
    min-width: 38px;
    text-align: right;
}
.score-bar-bg {
    width: 50px; height: 3px;
    background: rgba(255,255,255,0.05);
    border-radius: 4px;
    overflow: hidden;
}
.score-bar-fill { height: 100%; border-radius: 4px; }
.score-val {
    font-family: 'JetBrains Mono', monospace;
    font-size: 10px;
    color: var(--lav300);
    min-width: 28px;
    text-align: right;
}

/* Badges & tags */
.rank-badge {
    display: inline-flex; align-items: center; gap: 4px;
    background: rgba(168,85,247,0.12);
    border: 1px solid rgba(168,85,247,0.28);
    border-radius: 6px;
    padding: 3px 9px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 10px;
    color: var(--lav400);
    letter-spacing: 0.05em;
}
.jtag {
    background: rgba(168,85,247,0.14);
    border: 1px solid rgba(168,85,247,0.28);
    color: var(--lav300);
    padding: 3px 10px; border-radius: 100px;
    font-size: 11px; font-family: 'JetBrains Mono', monospace;
    margin-right: 5px; display: inline-block; margin-top: 5px;
}
.jtag-gray {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.08);
    color: #6b7280;
    padding: 3px 10px; border-radius: 100px;
    font-size: 11px; font-family: 'JetBrains Mono', monospace;
    margin-right: 5px; display: inline-block; margin-top: 5px;
}
.jtag-saved {
    background: rgba(16,185,129,0.1);
    border: 1px solid rgba(16,185,129,0.28);
    color: #6ee7b7;
    padding: 3px 10px; border-radius: 100px;
    font-size: 11px; font-family: 'JetBrains Mono', monospace;
    display: inline-flex; align-items: center; gap: 4px; margin-right: 5px;
}
.jtag-tracked {
    background: rgba(99,102,241,0.1);
    border: 1px solid rgba(99,102,241,0.28);
    color: #a5b4fc;
    padding: 3px 10px; border-radius: 100px;
    font-size: 11px; font-family: 'JetBrains Mono', monospace;
    display: inline-flex; align-items: center; gap: 4px; margin-right: 5px;
}

/* Job link */
.job-link {
    color: var(--lav400);
    font-size: 12.5px;
    text-decoration: none;
    font-family: 'JetBrains Mono', monospace;
    transition: color 0.2s;
}
.job-link:hover { color: var(--lav300); }

/* Empty state */
.empty-state { text-align: center; padding: 80px 20px; }
.empty-icon { font-size: 48px; margin-bottom: 16px; }
.empty-title {
    font-family: 'Instrument Serif', serif;
    font-size: 28px; color: var(--txt2); margin-bottom: 8px;
}
.empty-sub { font-size: 15px; color: var(--muted); }
</style>
""", unsafe_allow_html=True)

API = "http://127.0.0.1:8000"

# ── Helpers ───────────────────────────────────────────────────────────────────
def score_color(pct):
    if pct >= 70:
        return "#6ee7b7", "rgba(16,185,129,0.13)", "rgba(16,185,129,0.48)"
    elif pct >= 45:
        return "#fcd34d", "rgba(245,158,11,0.10)", "rgba(245,158,11,0.38)"
    else:
        return "#fca5a5", "rgba(239,68,68,0.08)", "rgba(239,68,68,0.32)"

def bar_color(pct):
    if pct >= 70: return "#6ee7b7"
    if pct >= 45: return "#fcd34d"
    return "#fca5a5"

import re

def norm(s: str) -> str:
    s = (s or "").lower()
    s = s.replace("–", "-").replace("—", "-").replace("&", " and ")
    s = re.sub(r"[^a-z0-9\+\#\.\-/ ]+", " ", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s


def keyword_variants(term: str):
    t = norm(term)
    mapping = {
        "ml": {"ml", "machine learning"},
        "dl": {"dl", "deep learning"},
        "cv": {"cv", "computer vision"},
        "nlp": {"nlp", "natural language processing"},
        "llm": {"llm", "large language model", "large language models"},
        "aws": {"aws", "amazon web services"},
        "api": {"api", "apis", "rest api", "restful api"},
        "ci/cd": {"ci/cd", "ci cd", "cicd"},
        "systemverilog": {"systemverilog", "system verilog"},
        "rtl": {"rtl", "rtl design"},
    }
    return mapping.get(t, {t})


def compute_skill_match(job, profile):
    skills = profile.get("skills", []) or []
    if not skills:
        return 0

    text = norm((job.get("description", "") or "") + " " + (job.get("title", "") or ""))
    matched = 0

    for s in skills:
        variants = keyword_variants(s)
        if any(v in text for v in variants):
            matched += 1

    score = round(100 * matched / max(len(skills), 1))
    return min(score, 100)


def compute_resume_fit(job, profile):
    roles = profile.get("target_roles", []) or []
    text = norm((job.get("title", "") or "") + " " + (job.get("description", "") or ""))

    role_hits = 0
    for role in roles:
        role_tokens = [tok for tok in norm(role).split() if len(tok) > 2]
        if role_tokens and sum(tok in text for tok in role_tokens) >= max(1, len(role_tokens) // 2):
            role_hits += 1

    base = round(100 * role_hits / max(len(roles), 1)) if roles else 0

    student_bonus = 0
    if any(x in text for x in ["intern", "internship", "new grad", "entry level", "student"]):
        student_bonus += 15

    loc_bonus = 0
    preferred_locations = [norm(x) for x in profile.get("preferred_locations", []) or []]
    job_locs = " ".join(norm(x) for x in job.get("locations", []) or [])
    if preferred_locations and any(loc in job_locs for loc in preferred_locations):
        loc_bonus = 10

    return min(base + student_bonus + loc_bonus, 100)


def agent_rec_score(sm, rf):
    return min(round(sm * 0.65 + rf * 0.35), 100)

def agent_rec_score(sm, rf):
    return min(int(sm * 0.6 + rf * 0.4), 99)

def sort_jobs(jobs, mode, profile):
    scored = []
    for j in jobs:
        sm = compute_skill_match(j, profile)
        rf = compute_resume_fit(j, profile)
        ar = agent_rec_score(sm, rf)
        scored.append((j, sm, rf, ar))
    if mode == "Skill Match":
        scored.sort(key=lambda x: x[1], reverse=True)
    elif mode == "Resume Fit":
        scored.sort(key=lambda x: x[2], reverse=True)
    else:
        scored.sort(key=lambda x: x[3], reverse=True)
    return scored

def build_breakdown(sm, rf, ar):
    rows = [("skill", sm), ("fit", rf), ("agent", ar)]
    parts = ["<div class='score-breakdown'>"]
    for key, val in rows:
        col = bar_color(val)
        parts.append(
            "<div class='score-row'>"
            "<span class='score-key'>" + key + "</span>"
            "<div class='score-bar-bg'>"
            "<div class='score-bar-fill' style='width:" + str(val) + "%;background:" + col + ";'></div>"
            "</div>"
            "<span class='score-val'>" + str(val) + "%</span>"
            "</div>"
        )
    parts.append("</div>")
    return "".join(parts)

# ── Session state ─────────────────────────────────────────────────────────────
if "saved_jobs"   not in st.session_state: st.session_state.saved_jobs   = set()
if "tracked_jobs" not in st.session_state: st.session_state.tracked_jobs = set()
if "sort_mode"    not in st.session_state: st.session_state.sort_mode    = "Agent Recommendation"

profile = st.session_state.get("profile", {})

# ── Navbar ────────────────────────────────────────────────────────────────────
c1, c2, c3, c4, c5 = st.columns([3, 1, 1, 1, 1])
with c1:
    st.markdown(
    "<a href='/' target='_self' style='text-decoration:none'>"
    "<div class='nav-logo'>🚀 InternFlow AI</div>"
    "<div class='nav-tagline'>AI-POWERED CAREER PLATFORM</div>"
    "</a>",
    unsafe_allow_html=True
)
with c2:
    if st.button("📝 Profile", use_container_width=True):
        st.switch_page("pages/2_onboarding.py")
with c3:
    if st.button("💼 Jobs", use_container_width=True, type="primary"):
        pass
with c4:
    if st.button("🤖 AI Agent", use_container_width=True):
        st.switch_page("pages/4_agent.py")
with c5:
    if st.button("✅ Tracker", use_container_width=True):
        st.switch_page("pages/5_resume_arsenal.py")

st.markdown("<div class='div'></div>", unsafe_allow_html=True)

# ── Page Header ───────────────────────────────────────────────────────────────
if profile.get("name"):
    roles_str = ", ".join(profile.get("target_roles", [])[:3]) or "your roles"
    st.markdown(
        "<div class='page-hd'>Internship <em>Listings</em></div>"
        "<p class='page-sub'>Hey <span>" + profile["name"] + "</span>"
        " — ranked for: <span>" + roles_str + "</span></p>",
        unsafe_allow_html=True
    )
else:
    st.markdown(
        "<div class='page-hd'>Internship <em>Listings</em></div>"
        "<p class='page-sub'>Browse and analyze live internship listings ranked for your profile.</p>",
        unsafe_allow_html=True
    )

st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

# ── Search & Filters ──────────────────────────────────────────────────────────
ROLE_OPTIONS = [
    "Any Role",
    "ML Engineer", "Data Scientist", "Data Analyst", "Data Engineer",
    "AI Engineer", "Research Engineer", "Software Engineer", "Backend Engineer",
    "Frontend Engineer", "Full Stack Engineer", "Computer Vision Engineer",
    "NLP Engineer", "Quantitative Analyst", "Product Manager", "DevOps Engineer",
    "Cloud Engineer", "Security Engineer", "iOS Engineer", "Android Engineer",
    "GenAI Engineer", "Robotics Engineer", "Embedded Systems Engineer",
]

US_LOCATIONS = [
    "Any Location (USA)",
    "Remote",
    "San Francisco, CA", "New York, NY", "Seattle, WA", "Austin, TX",
    "Boston, MA", "Los Angeles, CA", "Chicago, IL", "San Jose, CA",
    "Denver, CO", "Atlanta, GA", "Washington, DC", "Raleigh, NC",
    "Dallas, TX", "Pittsburgh, PA", "Portland, OR", "San Diego, CA",
    "Philadelphia, PA", "Minneapolis, MN", "Nashville, TN",
]

sc1, sc2, sc3, sc4 = st.columns([3, 2, 1, 1])
with sc1:
    role_choice    = st.selectbox("🔍 Role / Keywords", ROLE_OPTIONS, index=0)
    custom_search  = st.text_input("Or type custom keywords", placeholder="e.g. Generative AI, LLM, PyTorch")
with sc2:
    location_choice = st.selectbox("📍 Location (USA)", US_LOCATIONS, index=0)
with sc3:
    limit = st.selectbox("Show", [25, 50, 100], index=0)
with sc4:
    st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)
    st.button("Search", use_container_width=True, type="primary")

# Build API params from dropdown choices
search   = custom_search if custom_search else ("" if role_choice == "Any Role" else role_choice)
location = "" if location_choice == "Any Location (USA)" else location_choice

# ── Sort Bar ──────────────────────────────────────────────────────────────────
st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)
sort_options = ["Agent Recommendation", "Skill Match", "Resume Fit"]
sort_icons   = ["🤖", "🎯", "📄"]
s1, s2, s3, _ = st.columns([1, 1, 1, 5])
for col, opt, icon in zip([s1, s2, s3], sort_options, sort_icons):
    with col:
        btn_type = "primary" if st.session_state.sort_mode == opt else "secondary"
        if st.button(icon + " " + opt, key="sort_" + opt, use_container_width=True, type=btn_type):
            st.session_state.sort_mode = opt
            st.rerun()

st.markdown("<div class='div'></div>", unsafe_allow_html=True)

# ── Fetch & Render ────────────────────────────────────────────────────────────
try:
    params = {"limit": limit}
    if search:
        params["search"] = search
    if location:
        params["location"] = location

    response = requests.get(API + "/jobs", params=params, timeout=10)
    data = response.json()
    jobs = data.get("jobs", [])

    if not jobs:
        st.markdown(
            "<div class='empty-state'>"
            "<div class='empty-icon'>🔭</div>"
            "<div class='empty-title'>No internships found</div>"
            "<div class='empty-sub'>Try different keywords or a broader location.</div>"
            "</div>",
            unsafe_allow_html=True
        )
        st.stop()

    scored_jobs = sort_jobs(jobs, st.session_state.sort_mode, profile)

    saved_count  = len(st.session_state.saved_jobs)
    count_suffix = (" &nbsp;·&nbsp; <span>" + str(saved_count) + "</span> saved") if saved_count else ""
    st.markdown(
        "<div class='result-count'>"
        "<span>" + str(len(jobs)) + "</span> internships &nbsp;·&nbsp; "
        "sorted by <span>" + st.session_state.sort_mode + "</span>"
        + count_suffix +
        "</div>",
        unsafe_allow_html=True
    )

    # ── Job Cards ─────────────────────────────────────────────────────────────
    for rank, (job, skill_match, resume_fit, agent_rec) in enumerate(scored_jobs, 1):
        # Use rank as key suffix to guarantee uniqueness across duplicate listings
        job_id     = str(rank) + "-" + job.get("id", str(rank))
        is_saved   = job_id in st.session_state.saved_jobs
        is_tracked = job_id in st.session_state.tracked_jobs

        if st.session_state.sort_mode == "Skill Match":
            primary_score, score_label = skill_match, "SKILL"
        elif st.session_state.sort_mode == "Resume Fit":
            primary_score, score_label = resume_fit, "FIT"
        else:
            primary_score, score_label = agent_rec, "MATCH"

        txt_col, bg_col, bdr_col = score_color(primary_score)
        locations_str = ", ".join(job.get("locations", []))[:45]
        desc_preview  = job.get("description", "")[:220].strip()
        desc_tail     = "…" if len(job.get("description", "")) > 220 else ""

        card_class   = "jcard jcard-top-pick" if rank == 1 else "jcard"
        job_title    = job.get("title", "—")
        job_company  = job.get("company", "")
        sponsorship  = job.get("sponsorship", "")
        terms        = job.get("terms", [])
        spons_html   = ("<span class='jtag'>" + sponsorship + "</span>") if sponsorship else ""
        terms_html   = "".join(["<span class='jtag-gray'>" + t + "</span>" for t in terms[:4]])
        saved_html   = "<span class='jtag-saved'>✓ Saved</span>" if is_saved else ""
        tracked_html = "<span class='jtag-tracked'>📋 Tracked</span>" if is_tracked else ""
        breakdown    = build_breakdown(skill_match, resume_fit, agent_rec)

        if rank == 1:
            rank_html = "<span class='rank-badge'>🥇 TOP PICK</span>"
        elif rank == 2:
            rank_html = "<span class='rank-badge'>🥈 #2</span>"
        elif rank == 3:
            rank_html = "<span class='rank-badge'>🥉 #3</span>"
        else:
            rank_html = ""

        st.markdown(
            "<div class='" + card_class + "'>"
            "<div class='jcard-inner'>"
            "<div class='jcard-body'>"
            "<div class='jbadge-row'>" + rank_html + saved_html + tracked_html + "</div>"
            "<div class='jtitle'>" + job_title + "</div>"
            "<div class='jcompany'>" + job_company + " <span style='color:#2d2b45'>·</span> "
            "<span class='jloc'>📍 " + locations_str + "</span></div>"
            "<div class='jdesc'>" + desc_preview + desc_tail + "</div>"
            "<div style='margin-top:8px'>" + spons_html + terms_html + "</div>"
            "</div>"
            "<div class='jcard-sidebar'>"
            "<div class='score-ring' style='color:" + txt_col + ";background:" + bg_col + ";border-color:" + bdr_col + ";'>"
            "<div class='score-num' style='color:" + txt_col + "'>" + str(primary_score) + "%</div>"
            "<div class='score-lbl' style='color:" + txt_col + "'>" + score_label + "</div>"
            "</div>"
            + breakdown +
            "</div>"
            "</div>"
            "</div>",
            unsafe_allow_html=True
        )

        b1, b2, b3, b4 = st.columns([2, 2, 2, 4])

        with b1:
            if st.button("🤖 Analyze with Agent", key="analyze_" + job_id, type="primary", use_container_width=True):
                st.session_state.selected_job = job
                st.switch_page("pages/4_agent.py")

        with b2:
            save_label = "★ Saved" if is_saved else "☆ Save Job"
            if st.button(save_label, key="save_" + job_id, use_container_width=True, type="secondary"):
                if is_saved:
                    st.session_state.saved_jobs.discard(job_id)
                else:
                    st.session_state.saved_jobs.add(job_id)
                st.rerun()

        with b3:
            track_label = "📋 Tracked" if is_tracked else "📋 Track"
            if st.button(track_label, key="track_" + job_id, use_container_width=True, type="secondary"):
                if not is_tracked:
                    try:
                        requests.post(API + "/applications", json={
                            "job_id":    job.get("id"),
                            "company":   job.get("company"),
                            "job_title": job.get("title"),
                            "location":  locations_str,
                            "url":       job.get("url", "")
                        }, timeout=5)
                        st.session_state.tracked_jobs.add(job_id)
                        st.success("Tracked " + job.get("company", "") + "!")
                        st.rerun()
                    except Exception:
                        st.error("Could not track — is the backend running?")
                else:
                    st.info("Already in your tracker.")

        with b4:
            url = job.get("url", "#")
            st.markdown(
                "<div style='padding-top:9px'>"
                "<a href='" + url + "' target='_blank' class='job-link'>🔗 View original posting →</a>"
                "</div>",
                unsafe_allow_html=True
            )

        st.markdown("<div style='height:2px'></div>", unsafe_allow_html=True)

except requests.exceptions.ConnectionError:
    st.markdown(
        "<div style='background:rgba(239,68,68,0.08);border:1px solid rgba(239,68,68,0.3);"
        "border-radius:14px;padding:24px 28px;margin:20px 0'>"
        "<div style='font-size:17px;font-weight:700;color:#fca5a5;margin-bottom:10px'>❌ Backend not running</div>"
        "<div style='color:#9ca3af;font-size:14px;line-height:1.9'>"
        "Open a <b style='color:#f1f0f8'>second terminal</b> in your project folder and run:<br>"
        "<code style='background:#111;border:1px solid #2d2d2d;border-radius:8px;padding:10px 16px;"
        "display:inline-block;margin-top:10px;color:#6ee7b7;font-size:13px;letter-spacing:0.02em'>"
        "cd backend &amp;&amp; uvicorn main:app --reload"
        "</code><br><br>"
        "<span style='color:#6b7280'>Keep that terminal open, then refresh this page. "
        "Jobs will appear once the backend is live on port 8000.</span>"
        "</div>"
        "</div>",
        unsafe_allow_html=True
    )
except Exception as e:
    st.error("Something went wrong: " + str(e))
