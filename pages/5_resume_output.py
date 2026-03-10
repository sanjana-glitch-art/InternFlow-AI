import streamlit as st
import requests
import subprocess
import os
import tempfile
import json

st.set_page_config(
    page_title="InternFlow AI – Resume PDF",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    [data-testid="collapsedControl"] {display: none;}

    .stApp { background: #0f0f0f; color: #fff; }
    .nav-logo { color: #76B900; font-size: 22px; font-weight: 900; }

    .section-title {
        color: #76B900;
        font-size: 20px;
        font-weight: 700;
        margin-bottom: 4px;
        margin-top: 24px;
    }
    .section-desc { color: #888; font-size: 14px; margin-bottom: 16px; }

    .status-card {
        background: #1a1a1a;
        border: 1px solid #2a2a2a;
        border-radius: 12px;
        padding: 20px 24px;
        margin-bottom: 16px;
        text-align: center;
    }
    .latex-box {
        background: #111;
        border: 1px solid #333;
        border-radius: 8px;
        padding: 16px;
        font-family: 'Courier New', monospace;
        font-size: 12px;
        color: #76B900;
        overflow-x: auto;
    }
    .step-badge {
        background: #76B900;
        color: #000;
        width: 28px;
        height: 28px;
        border-radius: 50%;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        font-weight: 900;
        font-size: 14px;
        margin-right: 10px;
    }
</style>
""", unsafe_allow_html=True)

NVIDIA_API_KEY = os.environ.get("NVIDIA_API_KEY", "")
API = "http://127.0.0.1:8000"

# ── Navbar ────────────────────────────────────────────────────────────────────
col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
with col1:
    st.markdown("<div class='nav-logo'>🚀 InternFlow AI</div>", unsafe_allow_html=True)
with col2:
    if st.button("📝 Profile", use_container_width=True):
        st.switch_page("pages/2_onboarding.py")
with col3:
    if st.button("💼 Jobs", use_container_width=True):
        st.switch_page("pages/3_jobs.py")
with col4:
    if st.button("🤖 AI Agent", use_container_width=True):
        st.switch_page("pages/4_agent.py")

st.markdown("---")

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("<h1 style='color:#fff'>📄 Generate Your Resume PDF</h1>", unsafe_allow_html=True)
st.markdown("<p style='color:#888'>Nemotron generates a LaTeX resume — strictly 1 page, ATS-friendly, ready to download.</p>", unsafe_allow_html=True)

# ── Check for resume from agent page ─────────────────────────────────────────
resume_content = st.session_state.get("resume_for_pdf", "")
profile = st.session_state.get("profile_for_pdf", st.session_state.get("profile", {}))
selected_job = st.session_state.get("selected_job", {})

if not resume_content:
    st.warning("⚠️ No tailored resume found. Go back to the AI Agent page first, or paste your resume below.")
    resume_content = st.text_area("Paste your resume content here",
        height=200,
        placeholder="Paste your resume text here to generate a LaTeX PDF...")
    profile = st.session_state.get("profile", {})

if resume_content:
    st.success("✅ Resume content loaded! Ready to generate PDF.")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"**Name:** {profile.get('name', 'Not set')}")
        st.markdown(f"**Email:** {profile.get('email', 'Not set')}")
        st.markdown(f"**Phone:** {profile.get('phone', 'Not set')}")
    with col2:
        st.markdown(f"**University:** {profile.get('university', 'Not set')}")
        st.markdown(f"**Degree:** {profile.get('degree', 'Not set')}")
        st.markdown(f"**LinkedIn:** {profile.get('linkedin', 'Not set')}")

st.markdown("---")

# ── Generate LaTeX ────────────────────────────────────────────────────────────
st.markdown("<div class='section-title'>⚡ Generate LaTeX Resume</div>", unsafe_allow_html=True)
st.markdown("<div class='section-desc'>Nemotron will convert your resume into a clean, 1-page LaTeX format.</div>", unsafe_allow_html=True)

if "latex_code" not in st.session_state:
    st.session_state.latex_code = ""

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    gen_btn = st.button("🧠 Generate LaTeX with Nemotron", type="primary",
        use_container_width=True, disabled=not resume_content)

if gen_btn and resume_content:
    with st.spinner("Nemotron is crafting your LaTeX resume..."):
        try:
            from openai import OpenAI
            client = OpenAI(
                base_url="https://integrate.api.nvidia.com/v1",
                api_key="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"
            )

            name = profile.get("name", "Your Name")
            email = profile.get("email", "email@example.com")
            phone = profile.get("phone", "+1 (000) 000-0000")
            linkedin = profile.get("linkedin", "")
            github = profile.get("github", "")
            university = profile.get("university", "")
            degree = profile.get("degree", "")
            graduation = profile.get("graduation", "")
            job_title = selected_job.get("title", "Software Engineer Intern") if selected_job else "Software Engineer Intern"
            company = selected_job.get("company", "") if selected_job else ""

            prompt = f"""You are an expert LaTeX resume writer. Convert the following resume content into a clean, professional, strictly 1-page LaTeX resume.

REQUIREMENTS:
- Use the moderncv or a clean custom LaTeX template
- Strictly 1 page — adjust font sizes and spacing to fit
- ATS-friendly (no tables, no columns for main content, no graphics)
- Use this exact personal info in the header:
  Name: {name}
  Email: {email}
  Phone: {phone}
  LinkedIn: {linkedin}
  GitHub: {github}
  University: {university}
  Degree: {degree}
  Graduation: {graduation}
- Sections: Summary, Education, Experience, Projects, Skills
- Bold company names and job titles
- Use bullet points (\\item) for experience and projects
- No colors except black
- Output ONLY the complete LaTeX code, nothing else, no explanation, no markdown backticks

RESUME CONTENT TO CONVERT:
{resume_content}

Output the complete compilable LaTeX code:"""

            response = client.chat.completions.create(
                model="nvidia/llama-3.3-nemotron-super-49b-v1",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=3000,
                temperature=0.3
            )

            latex_raw = response.choices[0].message.content.strip()

            # Clean up any markdown backticks if model added them
            if latex_raw.startswith("```"):
                latex_raw = latex_raw.split("\n", 1)[1]
            if latex_raw.endswith("```"):
                latex_raw = latex_raw.rsplit("```", 1)[0]

            st.session_state.latex_code = latex_raw.strip()
            st.success("✅ LaTeX generated!")

        except Exception as e:
            st.error(f"LaTeX generation failed: {e}")
            st.info("Make sure your NVIDIA_API_KEY is set as an environment variable.")

# ── Show LaTeX + Download Options ────────────────────────────────────────────
if st.session_state.latex_code:
    st.markdown("---")
    st.markdown("<div class='section-title'>📋 Your LaTeX Code</div>", unsafe_allow_html=True)

    # Show/edit LaTeX
    edited_latex = st.text_area("LaTeX Code (you can edit this)",
        value=st.session_state.latex_code,
        height=400,
        label_visibility="collapsed")
    st.session_state.latex_code = edited_latex

    col1, col2 = st.columns(2)

    with col1:
        # Download raw .tex file
        st.download_button(
            label="⬇️ Download .tex File",
            data=st.session_state.latex_code,
            file_name=f"{profile.get('name', 'resume').replace(' ', '_')}_resume.tex",
            mime="text/plain",
            use_container_width=True
        )

    with col2:
        # Try to compile to PDF locally
        if st.button("📄 Compile to PDF", use_container_width=True, type="primary"):
            with st.spinner("Compiling LaTeX to PDF..."):
                try:
                    with tempfile.TemporaryDirectory() as tmpdir:
                        tex_path = os.path.join(tmpdir, "resume.tex")
                        pdf_path = os.path.join(tmpdir, "resume.pdf")

                        with open(tex_path, "w") as f:
                            f.write(st.session_state.latex_code)

                        result = subprocess.run(
                            ["pdflatex", "-interaction=nonstopmode", "-output-directory", tmpdir, tex_path],
                            capture_output=True, text=True, timeout=30
                        )

                        if os.path.exists(pdf_path):
                            with open(pdf_path, "rb") as f:
                                pdf_bytes = f.read()
                            st.session_state.pdf_bytes = pdf_bytes
                            st.success("✅ PDF compiled successfully!")
                        else:
                            st.warning("pdflatex not found locally. Use the Overleaf option below!")
                            st.code(result.stdout[-500:] if result.stdout else "No output")

                except FileNotFoundError:
                    st.warning("pdflatex is not installed locally.")
                except Exception as e:
                    st.error(f"Compilation error: {e}")

    # Download PDF if compiled
    if "pdf_bytes" in st.session_state:
        st.download_button(
            label="⬇️ Download PDF Resume",
            data=st.session_state.pdf_bytes,
            file_name=f"{profile.get('name', 'resume').replace(' ', '_')}_resume.pdf",
            mime="application/pdf",
            use_container_width=True,
            type="primary"
        )

    st.markdown("---")

    # ── Overleaf Option ───────────────────────────────────────────────────────
    st.markdown("<div class='section-title'>🍃 Compile on Overleaf (Recommended)</div>", unsafe_allow_html=True)
    st.markdown("<div class='section-desc'>If pdflatex isn't installed locally, use Overleaf — free and instant.</div>", unsafe_allow_html=True)

    st.markdown("""
    <div style='background:#1a1a1a;border:1px solid #2a2a2a;border-radius:12px;padding:20px'>
        <div style='margin-bottom:12px'>
            <span class='step-badge'>1</span>
            <span style='color:#ccc'>Click <b style='color:#76B900'>Download .tex File</b> above</span>
        </div>
        <div style='margin-bottom:12px'>
            <span class='step-badge'>2</span>
            <span style='color:#ccc'>Go to <a href='https://www.overleaf.com/project' target='_blank' style='color:#76B900'>overleaf.com</a> → New Project → Upload</span>
        </div>
        <div style='margin-bottom:12px'>
            <span class='step-badge'>3</span>
            <span style='color:#ccc'>Upload your .tex file → Click <b style='color:#76B900'>Compile</b></span>
        </div>
        <div>
            <span class='step-badge'>4</span>
            <span style='color:#ccc'>Download the PDF → Apply! 🚀</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.link_button("🍃 Open Overleaf", "https://www.overleaf.com/project",
        use_container_width=False)

    st.markdown("---")

    # ── Track Application ─────────────────────────────────────────────────────
    st.markdown("<div class='section-title'>✅ Track This Application</div>", unsafe_allow_html=True)
    st.markdown("<div class='section-desc'>Save this to your applications tracker.</div>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        track_company = st.text_input("Company", value=selected_job.get("company", "") if selected_job else "")
        track_title = st.text_input("Job Title", value=selected_job.get("title", "") if selected_job else "")
    with col2:
        track_location = st.text_input("Location", value=', '.join(selected_job.get("locations", [])) if selected_job else "")
        track_url = st.text_input("Job URL", value=selected_job.get("url", "") if selected_job else "")

    if st.button("✅ Mark as Applied", type="primary"):
        try:
            requests.post(f"{API}/applications", json={
                "job_id": selected_job.get("id", "manual") if selected_job else "manual",
                "company": track_company,
                "job_title": track_title,
                "location": track_location,
                "url": track_url,
                "resume_used": f"Tailored for {track_company}",
                "status": "Applied"
            })
            st.success(f"✅ Tracked! Good luck at {track_company}! 🚀")
            st.balloons()
        except:
            st.error("Could not save — is the backend running?")

# ── Empty state ───────────────────────────────────────────────────────────────
elif not resume_content:
    st.markdown("""
    <div style='text-align:center;padding:60px 20px'>
        <div style='font-size:64px'>📄</div>
        <h3 style='color:#888'>No resume loaded yet</h3>
        <p style='color:#555'>Go back to the AI Agent page, run the analysis, then click "Generate PDF Resume"</p>
    </div>
    """, unsafe_allow_html=True)
    if st.button("← Go to AI Agent", type="primary"):
        st.switch_page("pages/4_agent.py")