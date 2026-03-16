import streamlit as st
import requests
from datetime import datetime

st.set_page_config(
    page_title="InternFlow AI – Resume Arsenal",
    page_icon="📂",
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
  --black: #030305; --card: #0e0e1c; --card2: #12121e;
  --border: rgba(118,185,0,0.15); --green: #76B900;
  --green-dim: rgba(118,185,0,0.08); --white: #f0efe8; --muted: #6b6b80;
  --font-display: 'Syne', sans-serif; --font-body: 'DM Sans', sans-serif;
  --font-mono: 'DM Mono', monospace;
}

.stApp { background: var(--black) !important; font-family: var(--font-body); color: var(--white); }
.block-container { padding: 0 !important; max-width: 100% !important; }
.wrap { max-width: 1000px; margin: 0 auto; padding: 0 48px; }

.nav { padding: 24px 0; display: flex; align-items: center; justify-content: space-between; border-bottom: 1px solid var(--border); margin-bottom: 40px; }
.nav-logo { font-family: var(--font-display); font-size: 18px; font-weight: 800; color: var(--white); }
.nav-logo span { color: var(--green); }

.page-h { font-family: var(--font-display); font-size: clamp(28px,3vw,44px); font-weight: 800; letter-spacing:-1px; color: var(--white); margin-bottom: 4px; }
.page-h em { font-style: normal; color: var(--green); }
.page-sub { font-size: 15px; color: var(--muted); font-weight: 300; margin-bottom: 32px; }

.resume-card {
  background: var(--card);
  border: 1px solid var(--border);
  border-radius: 14px;
  padding: 24px 28px;
  margin-bottom: 12px;
  transition: border-color 0.2s;
}
.resume-card:hover { border-color: rgba(118,185,0,0.35); }
.resume-name { font-family: var(--font-display); font-size: 17px; font-weight: 700; color: var(--white); margin-bottom: 4px; }
.resume-meta { font-family: var(--font-mono); font-size: 11px; color: var(--green); opacity: 0.8; margin-bottom: 8px; letter-spacing: 0.05em; }
.resume-preview { font-family: var(--font-mono); font-size: 12px; color: var(--muted); line-height: 1.6; background: #07070f; border: 1px solid rgba(118,185,0,0.1); border-radius: 8px; padding: 14px 16px; margin-top: 10px; white-space: pre-wrap; max-height: 120px; overflow: hidden; }
.badge {
  display: inline-block; padding: 3px 10px; border-radius: 100px;
  font-family: var(--font-mono); font-size: 10px; margin-right: 6px;
}
.badge-base { background: var(--green-dim); border: 1px solid rgba(118,185,0,0.25); color: var(--green); }
.badge-company { background: rgba(168,85,247,0.08); border: 1px solid rgba(168,85,247,0.2); color: #c084fc; }

.empty-state {
  text-align: center; padding: 80px 20px;
  background: var(--card); border: 1px dashed var(--border);
  border-radius: 16px; margin-top: 24px;
}
.empty-ico { font-size: 48px; margin-bottom: 16px; }
.empty-title { font-family: var(--font-display); font-size: 20px; font-weight: 700; color: var(--white); margin-bottom: 8px; }
.empty-sub { font-size: 14px; color: var(--muted); line-height: 1.6; }

.divline { border: none; height: 1px; background: linear-gradient(90deg, transparent, rgba(118,185,0,0.15), transparent); margin: 32px 0; }

.stButton > button {
  background: var(--green) !important; color: #000 !important;
  border: none !important; border-radius: 8px !important;
  font-family: var(--font-display) !important; font-size: 13px !important;
  font-weight: 700 !important; padding: 8px 18px !important;
  height: auto !important; transition: opacity 0.2s !important;
}
.stButton > button:hover { opacity: 0.85 !important; }
.stButton > button[kind="secondary"] {
  background: transparent !important; color: var(--green) !important;
  border: 1px solid rgba(118,185,0,0.25) !important;
}
label { color: var(--muted) !important; font-size: 13px !important; }
.stTabs [data-baseweb="tab"] { font-family: var(--font-body) !important; color: var(--muted) !important; }
.stTabs [aria-selected="true"] { color: var(--green) !important; border-bottom-color: var(--green) !important; }
</style>
""", unsafe_allow_html=True)

# ── Navbar ────────────────────────────────────────────────────────────────────
st.markdown("<div class='wrap'>", unsafe_allow_html=True)
n1, n2, n3, n4, n5 = st.columns([3, 1, 1, 1, 1])
with n1:
    st.markdown("<div class='nav-logo'>Intern<span>Flow</span> AI</div>", unsafe_allow_html=True)
with n2:
    if st.button("📝 Profile",  use_container_width=True): st.switch_page("pages/2_onboarding.py")
with n3:
    if st.button("💼 Jobs",     use_container_width=True): st.switch_page("pages/3_jobs.py")
with n4:
    if st.button("🤖 Agent",    use_container_width=True): st.switch_page("pages/4_agent.py")
with n5:
    if st.button("📂 Arsenal",  type="primary", use_container_width=True): pass
st.markdown("</div>", unsafe_allow_html=True)

st.markdown("""
<div class='wrap'>
  <div class='page-h'>Resume <em>Arsenal</em></div>
  <p class='page-sub'>All your resume versions — base and company-tailored — in one place.</p>
</div>
""", unsafe_allow_html=True)

st.markdown("<div class='wrap'>", unsafe_allow_html=True)

# ── Fetch resumes ─────────────────────────────────────────────────────────────
try:
    resp = requests.get(f"{API}/resumes/", timeout=5)
    data = resp.json()
    base_resumes    = data.get("base_resumes", data.get("resumes", []))
    company_resumes = data.get("company_resumes", [])
except Exception:
    base_resumes    = []
    company_resumes = []

tab1, tab2 = st.tabs([f"📄 Base Resumes ({len(base_resumes)})", f"🏢 Company-Tailored ({len(company_resumes)})"])

# ── Tab 1: Base Resumes ───────────────────────────────────────────────────────
with tab1:
    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

    # Add base resume manually
    with st.expander("➕ Add Base Resume"):
        bname = st.text_input("Resume Name", placeholder="e.g. ML Engineer Base Resume")
        bcontent = st.text_area("Resume Content", height=120, placeholder="Paste your resume text here...")
        btags = st.text_input("Tags (comma-separated)", placeholder="e.g. ML, Data Science, Python")
        if st.button("Save Base Resume", type="primary"):
            if bname and bcontent:
                try:
                    requests.post(f"{API}/resumes/base", json={
                        "name": bname,
                        "content": bcontent,
                        "tags": [t.strip() for t in btags.split(",") if t.strip()]
                    }, timeout=5)
                    st.success("✅ Saved!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Could not save: {e}")
            else:
                st.warning("Please fill in name and content.")

    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

    if not base_resumes:
        st.markdown("""
        <div class='empty-state'>
          <div class='empty-ico'>📄</div>
          <div class='empty-title'>No base resumes yet</div>
          <div class='empty-sub'>Upload your resume in the Profile page<br>or add one manually above.</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        for resume in base_resumes:
            rid     = resume.get("id","")
            rname   = resume.get("name","Unnamed Resume")
            content = resume.get("content","")
            tags    = resume.get("tags",[]) or []
            created = resume.get("created_at","")

            tag_html = "".join([f"<span class='badge badge-base'>{t}</span>" for t in tags])
            preview  = content[:300].replace("<","&lt;").replace(">","&gt;")

            st.markdown(f"""
            <div class='resume-card'>
              <div class='resume-name'>{rname}</div>
              <div class='resume-meta'>BASE RESUME · {len(content):,} chars</div>
              <div>{tag_html}</div>
              <div class='resume-preview'>{preview}{"..." if len(content) > 300 else ""}</div>
            </div>
            """, unsafe_allow_html=True)

            col_dl, col_del, col_sp = st.columns([2, 2, 4])
            with col_dl:
                st.download_button(
                    "⬇️ Download",
                    data=content,
                    file_name=f"{rname.replace(' ','_')}.txt",
                    mime="text/plain",
                    key=f"dl_base_{rid}",
                    use_container_width=True
                )
            with col_del:
                if st.button("🗑 Delete", key=f"del_base_{rid}", use_container_width=True):
                    try:
                        requests.delete(f"{API}/resumes/base/{rid}", timeout=5)
                        st.rerun()
                    except Exception:
                        st.error("Could not delete.")

# ── Tab 2: Company Resumes ────────────────────────────────────────────────────
with tab2:
    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

    if not company_resumes:
        st.markdown("""
        <div class='empty-state'>
          <div class='empty-ico'>🏢</div>
          <div class='empty-title'>No tailored resumes yet</div>
          <div class='empty-sub'>Run the AI Agent on a job and click<br>"Save to Arsenal" to store tailored versions here.</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("🤖 Go to AI Agent →", type="primary"):
            st.switch_page("pages/4_agent.py")
    else:
        for resume in company_resumes:
            rid      = resume.get("id","")
            company  = resume.get("company","Unknown Company")
            job_title= resume.get("job_title","Unknown Role")
            content  = resume.get("tailored_content") or resume.get("content","")
            created  = resume.get("created_at","")

            preview = (content[:300] if content else "").replace("<","&lt;").replace(">","&gt;")

            st.markdown(f"""
            <div class='resume-card'>
              <div class='resume-name'>{job_title}</div>
              <div class='resume-meta'>TAILORED FOR · {company.upper()}</div>
              <div><span class='badge badge-company'>{company}</span><span class='badge badge-base'>{len(content):,} chars</span></div>
              <div class='resume-preview'>{preview}{"..." if len(content) > 300 else ""}</div>
            </div>
            """, unsafe_allow_html=True)

            col_dl, col_sp = st.columns([2, 6])
            with col_dl:
                st.download_button(
                    "⬇️ Download",
                    data=content,
                    file_name=f"{company.replace(' ','_')}_{job_title.replace(' ','_')}_resume.txt",
                    mime="text/plain",
                    key=f"dl_co_{rid}",
                    use_container_width=True
                )

st.markdown("<hr class='divline'>", unsafe_allow_html=True)

# ── Stats ─────────────────────────────────────────────────────────────────────
total = len(base_resumes) + len(company_resumes)
st.markdown(f"""
<div style='display:grid;grid-template-columns:repeat(3,1fr);gap:16px;margin-bottom:40px'>
  <div style='background:var(--card);border:1px solid var(--border);border-radius:12px;padding:20px;text-align:center'>
    <div style='font-family:var(--font-display);font-size:36px;font-weight:800;color:var(--green);line-height:1'>{len(base_resumes)}</div>
    <div style='font-size:13px;color:var(--muted);margin-top:4px'>Base Resumes</div>
  </div>
  <div style='background:var(--card);border:1px solid var(--border);border-radius:12px;padding:20px;text-align:center'>
    <div style='font-family:var(--font-display);font-size:36px;font-weight:800;color:var(--green);line-height:1'>{len(company_resumes)}</div>
    <div style='font-size:13px;color:var(--muted);margin-top:4px'>Tailored Versions</div>
  </div>
  <div style='background:var(--card);border:1px solid var(--border);border-radius:12px;padding:20px;text-align:center'>
    <div style='font-family:var(--font-display);font-size:36px;font-weight:800;color:var(--green);line-height:1'>{total}</div>
    <div style='font-size:13px;color:var(--muted);margin-top:4px'>Total in Arsenal</div>
  </div>
</div>
""", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)