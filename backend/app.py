import streamlit as st
import requests

st.set_page_config(
    page_title="InternFlow AI",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;500;600;700;800&family=DM+Sans:wght@300;400;500&family=DM+Mono:wght@400;500&display=swap');

#MainMenu{visibility:hidden;}footer{visibility:hidden;}header{visibility:hidden;}
[data-testid="collapsedControl"]{display:none;}
* {box-sizing:border-box;margin:0;padding:0;}

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

.stApp {
  background: var(--black) !important;
  font-family: var(--font-body);
  color: var(--white);
}
.block-container { padding: 0 !important; max-width: 100% !important; }

/* noise overlay */
.stApp::before {
  content: '';
  position: fixed;
  inset: 0;
  background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)' opacity='0.03'/%3E%3C/svg%3E");
  pointer-events: none;
  z-index: 0;
}

.wrap { max-width: 1140px; margin: 0 auto; padding: 0 48px; position: relative; z-index: 1; }

/* NAV */
.nav {
  padding: 28px 0;
  display: flex;
  align-items: center;
  justify-content: space-between;
  border-bottom: 1px solid var(--border);
}
.nav-logo {
  font-family: var(--font-display);
  font-size: 20px;
  font-weight: 800;
  color: var(--white);
  letter-spacing: -0.5px;
}
.nav-logo span { color: var(--green); }
.nav-badge {
  font-family: var(--font-mono);
  font-size: 11px;
  color: var(--green);
  background: var(--green-dim);
  border: 1px solid rgba(118,185,0,0.25);
  border-radius: 100px;
  padding: 5px 14px;
  letter-spacing: 0.08em;
}

/* HERO */
.hero { padding: 120px 0 80px; }
.hero-tag {
  font-family: var(--font-mono);
  font-size: 12px;
  color: var(--green);
  letter-spacing: 0.2em;
  text-transform: uppercase;
  margin-bottom: 32px;
  display: flex;
  align-items: center;
  gap: 12px;
}
.hero-tag::before {
  content: '';
  display: block;
  width: 32px;
  height: 1px;
  background: var(--green);
}
.hero-h1 {
  font-family: var(--font-display);
  font-size: clamp(52px, 7vw, 96px);
  font-weight: 800;
  line-height: 1.0;
  letter-spacing: -3px;
  color: var(--white);
  margin-bottom: 32px;
}
.hero-h1 em {
  font-style: normal;
  color: var(--green);
}
.hero-sub {
  font-size: 20px;
  font-weight: 300;
  line-height: 1.75;
  color: var(--muted);
  max-width: 560px;
  margin-bottom: 52px;
}
.hero-sub strong { color: var(--white); font-weight: 500; }

/* STATS */
.stats {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  border: 1px solid var(--border);
  border-radius: 16px;
  overflow: hidden;
  margin: 64px 0;
  background: var(--card);
}
.stat {
  padding: 32px 28px;
  border-right: 1px solid var(--border);
  text-align: center;
}
.stat:last-child { border-right: none; }
.stat-n {
  font-family: var(--font-display);
  font-size: 44px;
  font-weight: 800;
  color: var(--green);
  line-height: 1;
  margin-bottom: 8px;
}
.stat-l {
  font-size: 13px;
  color: var(--muted);
  line-height: 1.5;
}

/* SECTION */
.sec { padding: 96px 0; }
.sec-tag {
  font-family: var(--font-mono);
  font-size: 11px;
  color: var(--green);
  letter-spacing: 0.2em;
  text-transform: uppercase;
  margin-bottom: 20px;
}
.sec-h {
  font-family: var(--font-display);
  font-size: clamp(36px, 4vw, 56px);
  font-weight: 800;
  letter-spacing: -1.5px;
  color: var(--white);
  line-height: 1.1;
  margin-bottom: 16px;
}
.sec-h em { font-style: normal; color: var(--green); }
.sec-sub { font-size: 17px; color: var(--muted); font-weight: 300; max-width: 520px; line-height: 1.7; }

/* DIFFERENTIATORS */
.diff-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 2px;
  margin-top: 56px;
  background: var(--border);
  border-radius: 20px;
  overflow: hidden;
}
.diff-card {
  background: var(--card);
  padding: 40px 32px;
  position: relative;
  transition: background 0.25s;
}
.diff-card:hover { background: #12121f; }
.diff-num {
  font-family: var(--font-mono);
  font-size: 11px;
  color: rgba(118,185,0,0.4);
  letter-spacing: 0.15em;
  margin-bottom: 24px;
}
.diff-icon { font-size: 32px; margin-bottom: 16px; display: block; }
.diff-title {
  font-family: var(--font-display);
  font-size: 20px;
  font-weight: 700;
  color: var(--white);
  margin-bottom: 10px;
  letter-spacing: -0.5px;
}
.diff-body {
  font-size: 15px;
  color: var(--muted);
  line-height: 1.7;
  font-weight: 300;
}

/* FLOW */
.flow {
  display: flex;
  align-items: center;
  gap: 0;
  margin-top: 56px;
  background: var(--card);
  border: 1px solid var(--border);
  border-radius: 16px;
  overflow: hidden;
}
.flow-step {
  flex: 1;
  padding: 32px 28px;
  border-right: 1px solid var(--border);
  text-align: center;
}
.flow-step:last-child { border-right: none; }
.flow-n {
  font-family: var(--font-mono);
  font-size: 11px;
  color: var(--green);
  margin-bottom: 12px;
  letter-spacing: 0.1em;
}
.flow-ico { font-size: 28px; margin-bottom: 10px; display: block; }
.flow-title {
  font-size: 15px;
  font-weight: 600;
  color: var(--white);
  margin-bottom: 6px;
  font-family: var(--font-display);
}
.flow-desc { font-size: 13px; color: var(--muted); line-height: 1.5; }

/* TEAM */
.team-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 16px;
  margin-top: 56px;
}
.team-card {
  background: var(--card);
  border: 1px solid var(--border);
  border-radius: 16px;
  padding: 28px 24px;
  text-align: center;
  transition: border-color 0.25s, transform 0.25s;
}
.team-card:hover { border-color: rgba(118,185,0,0.4); transform: translateY(-4px); }
.team-av {
  width: 64px;
  height: 64px;
  border-radius: 50%;
  background: var(--green-dim);
  border: 2px solid rgba(118,185,0,0.3);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 26px;
  margin: 0 auto 16px;
}
.team-name {
  font-family: var(--font-display);
  font-size: 17px;
  font-weight: 700;
  color: var(--white);
  margin-bottom: 4px;
}
.team-role { font-size: 13px; color: var(--green); margin-bottom: 16px; line-height: 1.4; }
.team-links { display: flex; gap: 8px; justify-content: center; }
.team-link {
  background: rgba(118,185,0,0.08);
  border: 1px solid rgba(118,185,0,0.2);
  border-radius: 6px;
  padding: 5px 12px;
  font-family: var(--font-mono);
  font-size: 11px;
  color: rgba(118,185,0,0.8);
  text-decoration: none;
}

/* CTA */
.cta-sec {
  padding: 120px 0;
  text-align: center;
  position: relative;
  z-index: 1;
}
.cta-glow {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 500px;
  height: 300px;
  background: radial-gradient(ellipse, rgba(118,185,0,0.08) 0%, transparent 70%);
  pointer-events: none;
}
.cta-h {
  font-family: var(--font-display);
  font-size: clamp(40px, 5vw, 72px);
  font-weight: 800;
  letter-spacing: -2px;
  color: var(--white);
  margin-bottom: 16px;
  line-height: 1.05;
}
.cta-h em { font-style: normal; color: var(--green); }
.cta-sub { font-size: 18px; color: var(--muted); font-weight: 300; margin-bottom: 48px; }

/* DIVIDER */
.divline {
  border: none;
  height: 1px;
  background: linear-gradient(90deg, transparent, rgba(118,185,0,0.2), transparent);
  margin: 0;
}

/* FOOTER */
.foot {
  border-top: 1px solid var(--border);
  padding: 28px 0;
  text-align: center;
  font-family: var(--font-mono);
  font-size: 12px;
  color: var(--muted);
}

/* BUTTON OVERRIDE */
.stButton > button {
  background: var(--green) !important;
  color: #000 !important;
  border: none !important;
  border-radius: 10px !important;
  font-family: var(--font-display) !important;
  font-size: 16px !important;
  font-weight: 700 !important;
  padding: 14px 40px !important;
  height: auto !important;
  letter-spacing: -0.3px !important;
  transition: opacity 0.2s !important;
}
.stButton > button:hover { opacity: 0.85 !important; }
</style>
""", unsafe_allow_html=True)

# ── Live job count ──────────────────────────────────────────────────────────
try:
    r = requests.get("http://127.0.0.1:8000/jobs/", params={"limit": 100}, timeout=3)
    d = r.json()
    job_count = f"{len(d.get('jobs', d if isinstance(d, list) else []))}+"
except Exception:
    job_count = "500+"

# ── NAV ─────────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class='wrap'>
  <div class='nav'>
    <div class='nav-logo'>Intern<span>Flow</span> AI</div>
    <div class='nav-badge'>⚡ NVIDIA Nemotron · SJSU 2026</div>
  </div>
</div>
""", unsafe_allow_html=True)

# ── HERO ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class='wrap'>
  <div class='hero'>
    <div class='hero-tag'>Agents for Impact · Hackathon 2026</div>
    <div class='hero-h1'>Land your<br>internship<br>with <em>AI.</em></div>
    <p class='hero-sub'>
      Stop applying blindly. InternFlow scrapes your GitHub, diagnoses every JD,
      selects your <strong>best projects</strong>, and rewrites your resume — powered by NVIDIA Nemotron.
    </p>
  </div>
</div>
""", unsafe_allow_html=True)

_, cb, _ = st.columns([2, 2, 2])
with cb:
    if st.button("🚀 Get Started — It's Free", type="primary", use_container_width=True):
        st.switch_page("pages/2_onboarding.py")

# ── STATS ────────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class='wrap'>
  <div class='stats'>
    <div class='stat'><div class='stat-n'>{job_count}</div><div class='stat-l'>Live internship listings</div></div>
    <div class='stat'><div class='stat-n'>3</div><div class='stat-l'>Nemotron agents running in pipeline</div></div>
    <div class='stat'><div class='stat-n'>&lt;30s</div><div class='stat-l'>Resume tailored per job</div></div>
    <div class='stat'><div class='stat-n'>1-pg</div><div class='stat-l'>ATS-ready LaTeX PDF output</div></div>
  </div>
</div>
<hr class='divline'>
""", unsafe_allow_html=True)

# ── DIFFERENTIATORS ──────────────────────────────────────────────────────────
st.markdown("""
<div class='wrap'>
  <div class='sec'>
    <div class='sec-tag'>What makes us different</div>
    <div class='sec-h'>Three things no other<br>platform <em>does.</em></div>
    <p class='sec-sub'>Every other tool helps you find jobs. We help you land them.</p>
    <div class='diff-grid'>
      <div class='diff-card'>
        <div class='diff-num'>01 / GITHUB INTEGRATION</div>
        <span class='diff-icon'>🐙</span>
        <div class='diff-title'>Automatic Project Import</div>
        <div class='diff-body'>Drop your GitHub URL. We scrape every repo — READMEs, languages, stars — and build your full project portfolio automatically. Zero manual entry.</div>
      </div>
      <div class='diff-card'>
        <div class='diff-num'>02 / JD DIAGNOSTICS</div>
        <span class='diff-icon'>📊</span>
        <div class='diff-title'>Full Gap Analysis</div>
        <div class='diff-body'>Not just a score. Nemotron extracts every required keyword from the JD, shows exactly what's missing from your resume, and tells you how to fix it.</div>
      </div>
      <div class='diff-card'>
        <div class='diff-num'>03 / SMART SELECTION</div>
        <span class='diff-icon'>🧠</span>
        <div class='diff-title'>AI Project Selection</div>
        <div class='diff-body'>Have 10 projects but room for 3? Nemotron reads the JD and picks the most relevant ones — then rewrites them in the exact language recruiters want to see.</div>
      </div>
    </div>
  </div>
</div>
<hr class='divline'>
""", unsafe_allow_html=True)

# ── HOW IT WORKS ─────────────────────────────────────────────────────────────
st.markdown("""
<div class='wrap'>
  <div class='sec'>
    <div class='sec-tag'>How it works</div>
    <div class='sec-h'>Four steps.<br><em>One outcome.</em></div>
    <div class='flow'>
      <div class='flow-step'>
        <div class='flow-n'>STEP 01</div>
        <span class='flow-ico'>📝</span>
        <div class='flow-title'>Set Up Profile</div>
        <div class='flow-desc'>Upload resume + connect GitHub. We do the rest.</div>
      </div>
      <div class='flow-step'>
        <div class='flow-n'>STEP 02</div>
        <span class='flow-ico'>💼</span>
        <div class='flow-title'>Browse Jobs</div>
        <div class='flow-desc'>Live listings from Simplify Jobs. Active only.</div>
      </div>
      <div class='flow-step'>
        <div class='flow-n'>STEP 03</div>
        <span class='flow-ico'>🤖</span>
        <div class='flow-title'>Run AI Agent</div>
        <div class='flow-desc'>3 Nemotron agents analyze, select, and rewrite.</div>
      </div>
      <div class='flow-step'>
        <div class='flow-n'>STEP 04</div>
        <span class='flow-ico'>📄</span>
        <div class='flow-title'>Download & Apply</div>
        <div class='flow-desc'>1-page ATS-perfect LaTeX PDF ready to submit.</div>
      </div>
    </div>
  </div>
</div>
<hr class='divline'>
""", unsafe_allow_html=True)

# ── TEAM ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class='wrap'>
  <div class='sec'>
    <div class='sec-tag'>The Team</div>
    <div class='sec-h'>Built by students,<br><em>for students.</em></div>
    <p class='sec-sub'>Four SJSU engineers who got tired of the broken internship process and built the tool they wished existed.</p>
    <div class='team-grid'>
      <div class='team-card'>
        <div class='team-av'>👨‍💻</div>
        <div class='team-name'>Teammate 1</div>
        <div class='team-role'>AI Engineer<br>Nemotron · LangGraph</div>
        <div class='team-links'>
          <a href='#' class='team-link'>GitHub</a>
          <a href='#' class='team-link'>LinkedIn</a>
        </div>
      </div>
      <div class='team-card'>
        <div class='team-av'>⚙️</div>
        <div class='team-name'>Teammate 2</div>
        <div class='team-role'>Backend Engineer<br>FastAPI · REST</div>
        <div class='team-links'>
          <a href='#' class='team-link'>GitHub</a>
          <a href='#' class='team-link'>LinkedIn</a>
        </div>
      </div>
      <div class='team-card'>
        <div class='team-av'>🎨</div>
        <div class='team-name'>Teammate 3</div>
        <div class='team-role'>Frontend Engineer<br>Streamlit · UI/UX</div>
        <div class='team-links'>
          <a href='#' class='team-link'>GitHub</a>
          <a href='#' class='team-link'>LinkedIn</a>
        </div>
      </div>
      <div class='team-card'>
        <div class='team-av'>🔗</div>
        <div class='team-name'>Teammate 4</div>
        <div class='team-role'>Integration & Demo<br>E2E · Pitch</div>
        <div class='team-links'>
          <a href='#' class='team-link'>GitHub</a>
          <a href='#' class='team-link'>LinkedIn</a>
        </div>
      </div>
    </div>
  </div>
</div>
<hr class='divline'>
""", unsafe_allow_html=True)

# ── CTA ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class='wrap'>
  <div class='cta-sec'>
    <div class='cta-glow'></div>
    <div class='cta-h'>Ready to land your<br><em>internship?</em></div>
    <p class='cta-sub'>Stop applying blind. Let Nemotron do the work.</p>
  </div>
</div>
""", unsafe_allow_html=True)

_, cb2, _ = st.columns([2, 2, 2])
with cb2:
    if st.button("✨ Start Your Journey", type="primary", use_container_width=True):
        st.switch_page("pages/2_onboarding.py")

st.markdown("""
<div class='foot'>
  <div class='wrap'>Built with ❤️ using NVIDIA Nemotron · SJSU Agents for Impact Hackathon 2026</div>
</div>
<div style='height:40px'></div>
""", unsafe_allow_html=True)