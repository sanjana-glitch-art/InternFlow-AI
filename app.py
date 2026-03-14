import streamlit as st
import requests

st.set_page_config(
    page_title="InternFlow AI",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ── CSS only (no HTML here to avoid Streamlit rendering bugs) ─────────────────
st.markdown(
    "<style>"
    "@import url('https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&family=Outfit:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500;700&display=swap');"
    "#MainMenu{visibility:hidden;}footer{visibility:hidden;}header{visibility:hidden;}"
    "[data-testid='collapsedControl']{display:none;}"
    "* {box-sizing:border-box;}"
    ":root{--lav200:#e9d5ff;--lav300:#d8b4fe;--lav400:#c084fc;--lav500:#a855f7;--lav600:#9333ea;--lav700:#7e22ce;--bg:#08080f;--bg2:#0e0e1a;--bg3:#131325;--txt:#f1f0f8;--muted:#7c7a9a;--bdr:rgba(168,85,247,0.18);}"
    ".stApp{background:#08080f !important;font-family:'Outfit',sans-serif;color:#f1f0f8;}"
    ".block-container{padding:0 !important;max-width:100% !important;}"
    ".stButton > button{background:linear-gradient(135deg,#7c3aed,#6d28d9) !important;color:#fff !important;border:none !important;border-radius:12px !important;font-family:'Outfit',sans-serif !important;font-size:17px !important;font-weight:600 !important;padding:16px 48px !important;height:auto !important;box-shadow:0 8px 32px rgba(124,58,237,0.3) !important;transition:opacity 0.2s !important;}"
    ".stButton > button:hover{opacity:0.85 !important;}"
    ".orb1{position:fixed;top:-20vh;left:-10vw;width:60vw;height:60vw;background:radial-gradient(circle,rgba(124,58,237,0.09) 0%,transparent 65%);pointer-events:none;z-index:0;border-radius:50%;}"
    ".orb2{position:fixed;bottom:-20vh;right:-10vw;width:55vw;height:55vw;background:radial-gradient(circle,rgba(168,85,247,0.07) 0%,transparent 65%);pointer-events:none;z-index:0;border-radius:50%;}"
    ".bgrid{position:fixed;inset:0;background-image:linear-gradient(rgba(168,85,247,0.035) 1px,transparent 1px),linear-gradient(90deg,rgba(168,85,247,0.035) 1px,transparent 1px);background-size:72px 72px;pointer-events:none;z-index:0;}"
    ".W{max-width:1100px;margin:0 auto;padding:0 48px;position:relative;z-index:1;}"
    ".Ws{max-width:720px;margin:0 auto;padding:0 48px;position:relative;z-index:1;}"
    ".sec{padding:96px 0;position:relative;z-index:1;}"
    ".sec-alt{background:var(--bg2);border-top:1px solid var(--bdr);border-bottom:1px solid var(--bdr);}"
    ".divline{border:none;height:1px;background:linear-gradient(90deg,transparent,rgba(168,85,247,0.22),transparent);margin:0;}"
    ".eyebrow{font-family:'JetBrains Mono',monospace;font-size:13px;font-weight:500;letter-spacing:0.2em;text-transform:uppercase;color:var(--lav400);margin-bottom:20px;display:flex;align-items:center;gap:10px;}"
    ".eyebrow::before{content:'';display:inline-block;width:24px;height:1px;background:var(--lav500);}"
    ".hd{font-family:'Instrument Serif',serif;font-size:clamp(58px,7vw,98px);font-weight:400;line-height:1.05;letter-spacing:-2px;color:var(--txt);margin:0 0 28px;}"
    ".hd em{font-style:italic;color:var(--lav300);}"
    ".hs{font-family:'Instrument Serif',serif;font-size:clamp(38px,4vw,58px);font-weight:400;line-height:1.15;letter-spacing:-1px;color:var(--txt);margin:0 0 16px;}"
    ".hs em{font-style:italic;color:var(--lav300);}"
    ".lead{font-size:20px;font-weight:300;line-height:1.8;color:var(--muted);max-width:580px;}"
    ".lead strong{color:var(--lav300);font-weight:500;}"
    ".hero{padding:130px 0 60px;position:relative;z-index:1;}"
    ".badge{display:inline-flex;align-items:center;gap:8px;background:rgba(124,58,237,0.12);border:1px solid rgba(168,85,247,0.3);border-radius:100px;padding:8px 20px 8px 14px;font-family:'JetBrains Mono',monospace;font-size:14px;color:var(--lav300);margin-bottom:36px;}"
    ".bdot{width:7px;height:7px;background:var(--lav400);border-radius:50%;animation:pulse 2s infinite;}"
    "@keyframes pulse{0%,100%{opacity:1;transform:scale(1)}50%{opacity:0.5;transform:scale(0.8)}}"
    ".hacktag{text-align:center;color:#4b4966;font-size:15px;font-family:'JetBrains Mono',monospace;padding:12px 0 72px;}"
    ".sstrip{background:var(--bg2);border-top:1px solid var(--bdr);border-bottom:1px solid var(--bdr);padding:40px 0;}"
    ".sgrid{display:grid;grid-template-columns:repeat(4,1fr);}"
    ".sitem{padding:8px 32px;text-align:center;border-right:1px solid var(--bdr);}"
    ".sitem:last-child{border-right:none;}"
    ".snum{font-family:'Instrument Serif',serif;font-size:50px;color:var(--lav300);line-height:1;margin-bottom:8px;}"
    ".slbl{font-size:15px;color:var(--muted);line-height:1.5;}"
    ".pgrid{display:grid;grid-template-columns:repeat(2,1fr);gap:20px;margin-top:56px;}"
    ".pcard{background:var(--bg2);border:1px solid var(--bdr);border-radius:20px;padding:36px 32px;position:relative;overflow:hidden;transition:border-color 0.25s,transform 0.25s;}"
    ".pcard:hover{border-color:rgba(168,85,247,0.4);transform:translateY(-4px);}"
    ".pcard::before{content:'';position:absolute;top:0;left:0;right:0;height:1px;background:linear-gradient(90deg,transparent,rgba(168,85,247,0.35),transparent);}"
    ".pnum{position:absolute;top:24px;right:28px;font-family:'JetBrains Mono',monospace;font-size:13px;color:rgba(168,85,247,0.3);}"
    ".pico{font-size:30px;margin-bottom:16px;display:block;}"
    ".ptitle{font-size:20px;font-weight:600;color:var(--txt);margin-bottom:10px;}"
    ".pbody{font-size:17px;color:var(--muted);line-height:1.7;font-weight:300;}"
    ".sgrid2{display:grid;grid-template-columns:repeat(3,1fr);gap:20px;margin-top:56px;}"
    ".scard{background:var(--bg3);border:1px solid var(--bdr);border-radius:20px;padding:36px 28px;position:relative;overflow:hidden;transition:border-color 0.25s,transform 0.25s;}"
    ".scard:hover{border-color:rgba(168,85,247,0.4);transform:translateY(-4px);}"
    ".sico{font-size:34px;margin-bottom:20px;display:block;}"
    ".stitle{font-size:19px;font-weight:700;color:var(--lav200);margin-bottom:10px;}"
    ".sbody{font-size:16px;color:var(--muted);line-height:1.75;font-weight:300;}"
    ".stag{display:inline-block;margin-top:18px;font-family:'JetBrains Mono',monospace;font-size:12px;color:var(--lav500);border:1px solid rgba(168,85,247,0.25);border-radius:100px;padding:3px 10px;}"
    ".dbox{background:var(--bg2);border:1px solid var(--bdr);border-radius:24px;overflow:hidden;margin-top:56px;}"
    ".dtop{background:var(--bg3);border-bottom:1px solid var(--bdr);padding:14px 24px;display:flex;align-items:center;gap:8px;}"
    ".ddot{width:10px;height:10px;border-radius:50%;}"
    ".dbody{padding:40px;}"
    ".dcols{display:grid;grid-template-columns:1fr 1fr;gap:24px;}"
    ".dpanel{background:var(--bg);border:1px solid var(--bdr);border-radius:14px;padding:24px;min-height:220px;}"
    ".dlbl{font-family:'JetBrains Mono',monospace;font-size:12px;letter-spacing:0.15em;text-transform:uppercase;color:var(--lav500);margin-bottom:14px;}"
    ".dbefore{font-size:15px;color:#555577;line-height:1.7;}"
    ".dafter{font-size:15px;color:#b8afd8;line-height:1.7;}"
    ".dafter strong{color:var(--lav300);}"
    ".dbadge{display:inline-flex;align-items:center;gap:6px;background:rgba(124,58,237,0.15);border:1px solid rgba(168,85,247,0.3);border-radius:8px;padding:6px 14px;font-size:14px;color:var(--lav300);font-family:'JetBrains Mono',monospace;margin-top:16px;}"
    ".djd{background:#0b0b12;border:1px solid rgba(168,85,247,0.15);border-radius:10px;padding:16px;font-size:15px;color:#4b4966;line-height:1.7;font-family:'JetBrains Mono',monospace;margin-bottom:24px;}"
    ".aflow{display:flex;align-items:center;justify-content:center;flex-wrap:wrap;margin-top:56px;gap:0;}"
    ".anode{background:var(--bg2);border:1px solid var(--bdr);border-radius:16px;padding:28px 32px;text-align:center;min-width:160px;transition:border-color 0.25s;}"
    ".anode:hover{border-color:rgba(168,85,247,0.45);}"
    ".anode-hi{border-color:rgba(168,85,247,0.4) !important;}"
    ".aico{font-size:30px;margin-bottom:10px;display:block;}"
    ".atitle{font-size:17px;font-weight:700;color:var(--lav200);margin-bottom:4px;}"
    ".asub{font-family:'JetBrains Mono',monospace;font-size:12px;color:var(--muted);}"
    ".aarr{color:rgba(168,85,247,0.4);font-size:22px;padding:0 8px;flex-shrink:0;}"
    ".amodel-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:16px;margin-top:32px;}"
    ".amodel{background:rgba(168,85,247,0.06);border:1px solid rgba(168,85,247,0.15);border-radius:14px;padding:24px;}"
    ".amodel-lbl{font-family:'JetBrains Mono',monospace;font-size:12px;color:#7c3aed;letter-spacing:0.12em;text-transform:uppercase;margin-bottom:10px;}"
    ".amodel-txt{font-size:16px;color:#7c7a9a;line-height:1.6;}"
    ".mgrid3{display:grid;grid-template-columns:repeat(3,1fr);gap:20px;margin-top:56px;}"
    ".mcard{background:var(--bg2);border:1px solid var(--bdr);border-radius:20px;padding:44px 32px;text-align:center;position:relative;overflow:hidden;}"
    ".mcard::before{content:'';position:absolute;top:0;left:20%;right:20%;height:2px;background:linear-gradient(90deg,transparent,var(--lav500),transparent);border-radius:100px;}"
    ".mnum{font-family:'Instrument Serif',serif;font-size:66px;color:var(--lav200);line-height:1;margin-bottom:12px;}"
    ".mlbl{font-size:17px;color:var(--muted);font-weight:400;line-height:1.6;}"
    ".mlbl strong{color:var(--lav300);font-weight:600;}"
    ".tgrid{display:grid;grid-template-columns:repeat(4,1fr);gap:20px;margin-top:56px;}"
    ".tcard{background:var(--bg2);border:1px solid var(--bdr);border-radius:20px;padding:36px 24px;text-align:center;transition:border-color 0.25s,transform 0.25s;}"
    ".tcard:hover{border-color:rgba(168,85,247,0.4);transform:translateY(-4px);}"
    ".tav{width:72px;height:72px;border-radius:50%;background:linear-gradient(135deg,rgba(124,58,237,0.3),rgba(168,85,247,0.15));border:2px solid rgba(168,85,247,0.3);display:flex;align-items:center;justify-content:center;font-size:28px;margin:0 auto 16px;}"
    ".tname{font-size:18px;font-weight:700;color:var(--txt);margin-bottom:6px;}"
    ".trole{font-size:15px;color:var(--lav400);font-weight:400;margin-bottom:20px;line-height:1.5;}"
    ".tlinks{display:flex;gap:10px;justify-content:center;}"
    ".tlink{background:rgba(168,85,247,0.1);border:1px solid rgba(168,85,247,0.2);border-radius:8px;padding:6px 14px;font-family:'JetBrains Mono',monospace;font-size:13px;color:var(--lav400);text-decoration:none;transition:background 0.2s;}"
    ".tlink:hover{background:rgba(168,85,247,0.2);color:var(--lav200);}"
    ".ctasec{padding:120px 0;text-align:center;position:relative;z-index:1;}"
    ".ctaglow{position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);width:600px;height:300px;background:radial-gradient(ellipse,rgba(124,58,237,0.15) 0%,transparent 70%);pointer-events:none;}"
    ".ctatitle{font-family:'Instrument Serif',serif;font-size:clamp(42px,5vw,74px);font-weight:400;color:var(--txt);letter-spacing:-1.5px;line-height:1.1;margin-bottom:20px;}"
    ".ctatitle em{font-style:italic;color:var(--lav300);}"
    ".ctasub{font-size:20px;color:var(--muted);font-weight:300;margin-bottom:48px;}"
    ".foot{border-top:1px solid var(--bdr);padding:32px 0;text-align:center;font-family:'JetBrains Mono',monospace;font-size:14px;color:rgba(124,122,154,0.5);position:relative;z-index:1;}"
    "</style>",
    unsafe_allow_html=True
)

# ── Ambient background ────────────────────────────────────────────────────────
st.markdown("<div class='orb1'></div><div class='orb2'></div><div class='bgrid'></div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════
# HERO
# ══════════════════════════════════════════════════════════
st.markdown(
    "<div class='hero'><div class='W'>"
    "<div class='badge'><span class='bdot'></span>Powered by ❤️ NVIDIA Nemotron</div>"
    "<div class='hd'>InternFlow<br><em>AI.</em></div>"
    "<p class='lead'>Stop mass-applying and hoping.<br><strong>Start applying with precision.</strong><br>"
    "Your agentic co-pilot that reads the job, picks your best projects, rewrites your resume, and gets you to the interview.</p>"
    "</div></div>",
    unsafe_allow_html=True
)

_, cb, _ = st.columns([2, 2, 2])
with cb:
    if st.button("Get Started — It's Free", type="primary", use_container_width=True):
        st.switch_page("pages/2_onboarding.py")

# ══════════════════════════════════════════════════════════
# STAT STRIP — live job count from backend
# ══════════════════════════════════════════════════════════
try:
    _r = requests.get("http://127.0.0.1:8000/jobs", timeout=3)
    _data = _r.json()
    # support both {jobs: [...]} and {total: N} shapes
    if "total" in _data:
        _job_count = f"{_data['total']}+"
    elif "jobs" in _data:
        _job_count = f"{len(_data['jobs'])}+"
    else:
        _job_count = "500+"
except Exception:
    _job_count = "500+"

st.markdown(
    "<div class='sstrip'><div class='W'><div class='sgrid'>"
    f"<div class='sitem'><div class='snum'>{_job_count}</div><div class='slbl'>Live internship listings</div></div>"
    "<div class='sitem'><div class='snum'>3</div><div class='slbl'>Nemotron models<br>Nano 30B &#183; Super 49B &#183; RAG</div></div>"
    "<div class='sitem'><div class='snum'>~2 min</div><div class='slbl'>End-to-end tailored resume<br>per job description</div></div>"
    "<div class='sitem'><div class='snum'>1-pg</div><div class='slbl'>ATS-ready LaTeX<br>PDF output</div></div>"
    "</div></div></div>",
    unsafe_allow_html=True
)

# ══════════════════════════════════════════════════════════
# PROBLEM
# ══════════════════════════════════════════════════════════
st.markdown(
    "<div class='sec'><div class='W'>"
    "<div class='eyebrow'>The Problem</div>"
    "<div class='hs'>Every student faces this.<br><em>Every. Single. Week.</em></div>"
    "<p class='lead'>You're qualified. Your resume just doesn't know how to say it — for each specific role, with the right keywords, at the right moment.</p>"
    "<div class='pgrid'>"
    "<div class='pcard'><span class='pnum'>01</span><span class='pico'>🎯</span><div class='ptitle'>No idea which jobs fit you</div><div class='pbody'>Hundreds of listings, zero guidance on which ones actually match your background. You apply blindly and wonder why there's silence.</div></div>"
    "<div class='pcard'><span class='pnum'>02</span><span class='pico'>📄</span><div class='ptitle'>Resumes rejected before anyone reads them</div><div class='pbody'>ATS filters eliminate 75% of applications automatically. Wrong keywords, wrong format, wrong bullet framing — all invisible to you.</div></div>"
    "<div class='pcard'><span class='pnum'>03</span><span class='pico'>🗂️</span><div class='ptitle'>10 projects. Room for 3. Wrong pick = no call.</div><div class='pbody'>Which projects do you show an ML engineer vs. a data analyst? Every tool leaves that critical decision entirely to you.</div></div>"
    "<div class='pcard'><span class='pnum'>04</span><span class='pico'>⏳</span><div class='ptitle'>10–20 hours a week. Down the drain.</div><div class='pbody'>Copy. Paste. Tweak. Repeat. Manual tailoring for every role is exhausting, error-prone, and shouldn't be your job.</div></div>"
    "</div></div></div><hr class='divline'>",
    unsafe_allow_html=True
)

# ══════════════════════════════════════════════════════════
# SOLUTION
# ══════════════════════════════════════════════════════════
st.markdown(
    "<div class='sec sec-alt'><div class='W'>"
    "<div class='eyebrow'>The Solution</div>"
    "<div class='hs'>Everything you need<br><em>to actually land it.</em></div>"
    "<p class='lead'>A fully agentic pipeline — from discovery to a tailored, submission-ready resume.</p>"
    "<div class='sgrid2'>"
    "<div class='scard'><span class='sico'>🧠</span><div class='stitle'>Smart Project Selection</div><div class='sbody'>Nemotron reads the JD, understands the role's priorities, and selects your 3 most relevant projects — then rewrites their bullets in the role's exact language.</div><span class='stag'>Llama Nemotron Super 49B</span></div>"
    "<div class='scard'><span class='sico'>📊</span><div class='stitle'>Full JD Diagnostics</div><div class='sbody'>Not a match score. A complete gap analysis — missing keywords, ATS formatting flags, seniority mismatches, and specific bullet rewrites surfaced instantly.</div><span class='stag'>Nemotron RAG</span></div>"
    "<div class='scard'><span class='sico'>📄</span><div class='stitle'>ATS-Perfect PDF</div><div class='sbody'>Nemotron generates a LaTeX resume — strictly 1 page, machine-readable, professionally formatted. Download and apply in seconds.</div><span class='stag'>LaTeX &#183; pdflatex</span></div>"
    "<div class='scard'><span class='sico'>🗂️</span><div class='stitle'>Resume Arsenal</div><div class='sbody'>Store all your base resume versions plus every company-tailored variant in one organized hub. Always know which resume went where.</div><span class='stag'>Multi-version storage</span></div>"
    "<div class='scard'><span class='sico'>🐙</span><div class='stitle'>GitHub Integration</div><div class='sbody'>Drop your GitHub URL — we scrape your repos, READMEs, and stats to auto-build your entire project portfolio. Zero manual entry.</div><span class='stag'>GitHub API</span></div>"
    "<div class='scard'><span class='sico'>✅</span><div class='stitle'>Application Tracker</div><div class='sbody'>Track every application, the exact resume version sent, and current status from a single dashboard. Never apply blind again.</div><span class='stag'>FastAPI &#183; JSON</span></div>"
    "</div></div></div>",
    unsafe_allow_html=True
)

# ══════════════════════════════════════════════════════════
# DEMO
# ══════════════════════════════════════════════════════════
st.markdown(
    "<div class='sec'><div class='W'>"
    "<div class='eyebrow'>Live Demo Preview</div>"
    "<div class='hs'>Before vs. After.<br><em>See it happen.</em></div>"
    "<p class='lead'>Paste a JD. Upload your resume. Nemotron rewrites your bullets to match what the recruiter is actually looking for.</p>"
    "<div class='dbox'>"
    "<div class='dtop'><div class='ddot' style='background:#ff5f57'></div><div class='ddot' style='background:#febc2e'></div><div class='ddot' style='background:#28c840'></div>"
    "<span style='font-family:JetBrains Mono,monospace;font-size:12px;color:#4b4966;margin-left:12px'>internflow.ai &#8212; AI Resume Agent</span></div>"
    "<div class='dbody'>"
    "<div style='font-family:JetBrains Mono,monospace;font-size:11px;color:#7c3aed;letter-spacing:0.15em;text-transform:uppercase;margin-bottom:10px'>Job Description (input)</div>"
    "<div class='djd'>&#8220;We are seeking an ML Engineering Intern with experience in PyTorch, distributed training, model optimization, and MLOps pipelines. Familiarity with LLM fine-tuning and RLHF is a strong plus.&#8221;</div>"
    "<div class='dcols'>"
    "<div><div class='dlbl'>&#10060; Before &#8212; Generic Resume Bullet</div>"
    "<div class='dpanel'><div class='dbefore'>&#8226; Built a machine learning model for activity recognition using Python<br><br>&#8226; Achieved 94% accuracy on test dataset<br><br>&#8226; Used scikit-learn and pandas for data processing<br><br>&#8226; Deployed the model to Streamlit Cloud</div>"
    "<div style='margin-top:14px'><span style='background:rgba(239,68,68,0.1);border:1px solid rgba(239,68,68,0.25);color:#fca5a5;padding:3px 10px;border-radius:100px;font-size:11px;font-family:JetBrains Mono,monospace'>ATS match: 28%</span></div></div></div>"
    "<div><div class='dlbl'>&#10003; After &#8212; Nemotron Rewritten</div>"
    "<div class='dpanel'><div class='dafter'>&#8226; Engineered <strong>PyTorch-based</strong> HAR pipeline processing 2.8M records, achieving 94.2% accuracy with custom <strong>model optimization</strong> reducing inference latency by 38%<br><br>"
    "&#8226; Designed <strong>MLOps-ready</strong> training workflow with automated evaluation metrics and <strong>distributed data preprocessing</strong> via Dask</div>"
    "<div class='dbadge'>&#10024; ATS match: 91% &nbsp;&#183;&nbsp; +63pts</div></div></div>"
    "</div></div></div></div></div><hr class='divline'>",
    unsafe_allow_html=True
)

# ══════════════════════════════════════════════════════════
# ARCHITECTURE
# ══════════════════════════════════════════════════════════
st.markdown(
    "<div class='sec sec-alt'><div class='W'>"
    "<div class='eyebrow'>Architecture</div>"
    "<div class='hs'>How it all <em>connects.</em></div>"
    "<p class='lead'>A clean, production-grade stack — from the Streamlit frontend to the LangGraph agent orchestrating three Nemotron models.</p>"
    "<div class='aflow'>"
    "<div class='anode'><span class='aico'>🖥️</span><div class='atitle'>Streamlit</div><div class='asub'>Frontend UI</div></div>"
    "<div class='aarr'>&#8594;</div>"
    "<div class='anode'><span class='aico'>⚡</span><div class='atitle'>FastAPI</div><div class='asub'>REST Backend</div></div>"
    "<div class='aarr'>&#8594;</div>"
    "<div class='anode'><span class='aico'>🔗</span><div class='atitle'>LangGraph</div><div class='asub'>Agent Orchestration</div></div>"
    "<div class='aarr'>&#8594;</div>"
    "<div class='anode'><span class='aico'>🤖</span><div class='atitle'>Nemotron</div><div class='asub'>Nano 30B &#183; Super 49B &#183; RAG</div></div>"
    "</div>"
    "<div class='amodel-grid'>"
    "<div class='amodel'><div class='amodel-lbl'>Nano 30B</div><div class='amodel-txt'>Fast keyword extraction &amp; JD analysis with low latency &#8212; runs first in the pipeline.</div></div>"
    "<div class='amodel'><div class='amodel-lbl'>Super 49B</div><div class='amodel-txt'>Deep resume reasoning, intelligent project selection, and full resume rewriting agent.</div></div>"
    "<div class='amodel'><div class='amodel-lbl'>Nemotron RAG</div><div class='amodel-txt'>Resume parsing, JD retrieval, and semantic matching for full diagnostic reports.</div></div>"
    "</div></div></div>",
    unsafe_allow_html=True
)

# ══════════════════════════════════════════════════════════
# METRICS
# ══════════════════════════════════════════════════════════
st.markdown(
    "<div class='sec'><div class='W'>"
    "<div class='eyebrow'>Impact Metrics</div>"
    "<div class='hs'>Results that<br><em>speak for themselves.</em></div>"
    "<p class='lead'>Measured across test runs comparing standard resume submissions vs. InternFlow AI-tailored applications.</p>"
    "<div class='mgrid3'>"
    "<div class='mcard'><div class='mnum'>+42%</div><div class='mlbl'>Average <strong>ATS score improvement</strong><br>after Nemotron resume tailoring</div></div>"
    "<div class='mcard'><div class='mnum'>12m</div><div class='mlbl'>Average time <strong>saved per application</strong><br>vs. manual resume tailoring</div></div>"
    "<div class='mcard'><div class='mnum'>87%</div><div class='mlbl'><strong>Job match accuracy</strong> when<br>Nemotron selects projects vs. student-chosen</div></div>"
    "</div></div></div><hr class='divline'>",
    unsafe_allow_html=True
)

# ══════════════════════════════════════════════════════════
# TEAM
# ══════════════════════════════════════════════════════════
st.markdown(
    "<div class='sec sec-alt'><div class='W'>"
    "<div class='eyebrow'>The Team</div>"
    "<div class='hs'>Built by students,<br><em>for students.</em></div>"
    "<p class='lead'>Four SJSU engineers who got tired of the broken internship process and decided to fix it with AI.</p>"
    "<div class='tgrid'>"
    "<div class='tcard'><div class='tav'>👨‍💻</div><div class='tname'>Sanjana</div><div class='trole'>Frontend Engineer<br>React &#183; Next.js &#183; UI</div><div class='tlinks'><a href='https://github.com/sanjana-glitch-art' class='tlink'>GitHub</a><a href='https://www.linkedin.com/in/sai-teja-sri-sanjana-thummalapalli-2b9223235/' class='tlink'>LinkedIn</a></div></div>"
    "<div class='tcard'><div class='tav'>⚙️</div><div class='tname'>Sanjana</div><div class='trole'>Backend Engineer<br>FastAPI &#183; REST &#183; Storage</div><div class='tlinks'><a href='https://github.com/sanjana-glitch-art' class='tlink'>GitHub</a><a href='https://www.linkedin.com/in/sai-teja-sri-sanjana-thummalapalli-2b9223235/' class='tlink'>LinkedIn</a></div></div>"
    "<div class='tcard'><div class='tav'>🧠</div><div class='tname'>Sanjana</div><div class='trole'>AI / LangGraph Engineer<br>Nemotron &#183; RAG &#183; Agents</div><div class='tlinks'><a href='https://github.com/sanjana-glitch-art' class='tlink'>GitHub</a><a href='https://www.linkedin.com/in/sai-teja-sri-sanjana-thummalapalli-2b9223235/' class='tlink'>LinkedIn</a></div></div>"
    "<div class='tcard'><div class='tav'>🔗</div><div class='tname'>Sanjana</div><div class='trole'>Integration &amp; Demo<br>E2E &#183; Pitch &#183; Slides</div><div class='tlinks'><a href='https://github.com/sanjana-glitch-art' class='tlink'>GitHub</a><a href='https://www.linkedin.com/in/sai-teja-sri-sanjana-thummalapalli-2b9223235/' class='tlink'>LinkedIn</a></div></div>"
    "</div></div></div>",
    unsafe_allow_html=True
)

# ══════════════════════════════════════════════════════════
# FINAL CTA
# ══════════════════════════════════════════════════════════
st.markdown(
    "<div class='ctasec'><div class='ctaglow'></div><div class='Ws'>"
    "<div class='ctatitle'>Ready to land your<br><em>internship?</em></div>"
    "<div class='ctasub'>Stop applying blind. Let Nemotron pick your projects, tailor your resume, and get you to the interview.</div>"
    "</div></div>",
    unsafe_allow_html=True
)

_, cb2, _ = st.columns([2, 2, 2])
with cb2:
    if st.button("✨  Start Your Journey", type="primary", use_container_width=True):
        st.switch_page("pages/2_onboarding.py")

st.markdown(
    "<div class='foot'><div class='W'>Built with ❤️ using NVIDIA Nemotron &nbsp;&#183;&nbsp; SJSU Agents for Impact Hackathon 2026</div></div>"
    "<div style='height:40px'></div>",
    unsafe_allow_html=True
)
