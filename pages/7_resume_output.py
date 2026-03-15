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

            prompt = fr"""
You are an expert LaTeX resume writer.

Generate a clean, professional, ATS-friendly, strictly one-page resume in LaTeX using a Jake's Resume style layout.

IMPORTANT OUTPUT RULES:
1. Output ONLY complete compilable LaTeX code.
2. Do NOT output markdown, backticks, explanations, notes, or any text outside the LaTeX source.
3. Do NOT fabricate experience, metrics, tools, responsibilities, dates, project results, or technologies.
4. You may rewrite bullet points for clarity, conciseness, impact, and ATS alignment, but must preserve factual accuracy.
5. Keep the resume to exactly one page.
6. Use concise bullets and compact spacing.
7. Use only black text.
8. Use no graphics, no icons, no images, no tables for the main content, and no multi-column body layout.
9. Use this exact section order: Summary, Education, Experience, Projects, Skills.
10. The final LaTeX must compile successfully with pdflatex.

CRITICAL LATEX SAFETY RULES:
1. Escape LaTeX special characters in all generated content:
   - & -> \&
   - % -> \%
   - _ -> \_
   - # -> \#
2. Do not output malformed commands or unmatched braces.
3. Do not leave placeholders like SUMMARY_TEXT, EXPERIENCE_ENTRIES, PROJECT_ENTRIES, or SKILLS_TEXT in the final output.
4. Use -- for date ranges, never Unicode dashes like – or —.
5. Every \resumeSubheading must have exactly 4 arguments.
6. Every \resumeProjectHeading must have exactly 2 arguments.
7. If a field is empty, output {{}} for that argument and never omit it.
8. Never let a macro consume the next LaTeX command as a missing argument.

HEADER INFORMATION TO USE EXACTLY:
Name: {name}
Email: {email}
Phone: {phone}
LinkedIn: {linkedin}
GitHub: {github}

EDUCATION INFORMATION TO USE EXACTLY:
University: {university}
Degree: {degree}
Graduation: {graduation}

PROJECT SELECTION RULES:
1. Include EXACTLY 3 projects in the Projects section.
2. Do NOT include fewer than 3 projects unless fewer than 3 projects exist in the input.
3. Select the 3 strongest and most technically significant projects from the resume content.
4. Prioritize projects that best demonstrate systems, software, ML, FPGA, RTL, embedded, architecture, optimization, deployment, or engineering depth.
5. Each selected project must appear as its own separate \resumeProjectHeading entry.
6. Do NOT merge multiple projects into one heading.
7. Do NOT compress all project bullets under a single project title.
8. Each of the 3 projects must have 2 or 3 concise bullets.
9. If page space is tight, shorten bullets before reducing the number of projects.
10. Prefer the most relevant and technically impressive projects rather than the most recent ones.

CONTENT RULES:
- Summary must be 2 to 3 lines maximum.
- Experience and project bullets must begin with strong action verbs.
- Use 2 to 4 bullets per experience or project.
- Prefer concise, technical, ATS-friendly bullets over long generic bullets.
- Keep project titles aligned consistently.
- Keep formatting consistent across all sections.
- Do not invent locations if none are provided.
- Do not invent tech stacks if none are provided.

EXPERIENCE ENTRY FORMAT:
Use exactly this format for every experience entry:
\resumeSubheading
  {{{{Company Name}}}}{{{{Date Range}}}}
  {{{{Job Title}}}}{{{{Location or {{}} if empty}}}}
\resumeItemListStart
  \resumeItem{{{{Bullet 1}}}}
  \resumeItem{{{{Bullet 2}}}}
  \resumeItem{{{{Bullet 3}}}}
\resumeItemListEnd

IMPORTANT:
- \resumeSubheading always requires 4 arguments.
- If location is missing, write:
  \resumeSubheading
    {{{{Open-Source Contributor}}}}{{{{}}}}
    {{{{Contributor}}}}{{{{}}}}

PROJECT ENTRY FORMAT:
Use exactly this format for every project entry:
\resumeProjectHeading
  {{{{\textbf{{{{Project Name}}}} $|$ \emph{{{{Tech Stack / Focus}}}}}}}}{{{{}}}}
\resumeItemListStart
  \resumeItem{{{{Bullet 1}}}}
  \resumeItem{{{{Bullet 2}}}}
  \resumeItem{{{{Bullet 3}}}}
\resumeItemListEnd

IMPORTANT:
- \resumeProjectHeading always requires exactly 2 arguments.
- If there is no date or right-side label, the second argument must still be {{}}.
- Output EXACTLY 3 separate project headings when at least 3 projects are present in the input.

SKILLS FORMAT:
Format skills exactly like this:
\textbf{{Languages}}: ... \\
\textbf{{Hardware / RTL}}: ... \\
\textbf{{ML / AI}}: ... \\
\textbf{{Tools / Platforms}}: ... \\
\textbf{{Concepts}}: ...

SUMMARY RULES:
- Write a concise professional summary tailored to the resume content.
- 2 to 3 lines maximum.
- Mention degree level, strongest technical areas, and target engineering profile.
- Keep it factual and ATS-friendly.

USE THIS EXACT LATEX TEMPLATE AND FILL IT CORRECTLY:

\documentclass[letterpaper,10pt]{{article}}

\usepackage[empty]{{fullpage}}
\usepackage{{titlesec}}
\usepackage{{enumitem}}
\usepackage[hidelinks]{{hyperref}}
\usepackage{{fancyhdr}}

\pagestyle{{fancy}}
\fancyhf{{}}
\renewcommand{{\headrulewidth}}{{0pt}}
\renewcommand{{\footrulewidth}}{{0pt}}

\addtolength{{\oddsidemargin}}{{-0.5in}}
\addtolength{{\evensidemargin}}{{-0.5in}}
\addtolength{{\textwidth}}{{1in}}
\addtolength{{\topmargin}}{{-0.6in}}
\addtolength{{\textheight}}{{1.2in}}

\urlstyle{{same}}
\raggedright
\setlength{{\tabcolsep}}{{0in}}

\titleformat{{\section}}{{
  \vspace{{-4pt}}\scshape\raggedright\large
}}{{}}{{0em}}{{}}[\titlerule \vspace{{-5pt}}]

\newcommand{{\resumeItem}}[1]{{
  \item\small{{#1 \vspace{{-2pt}}}}
}}

\newcommand{{\resumeSubheading}}[4]{{
  \vspace{{-2pt}}\item
    \begin{{tabular*}}{{0.97\textwidth}}[t]{{l@{{\extracolsep{{\fill}}}}r}}
      \textbf{{#1}} & #2 \\
      \textit{{\small #3}} & \textit{{\small #4}} \\
    \end{{tabular*}}\vspace{{-7pt}}
}}

\newcommand{{\resumeProjectHeading}}[2]{{
    \item
    \begin{{tabular*}}{{0.97\textwidth}}{{l@{{\extracolsep{{\fill}}}}r}}
      \small #1 & #2 \\
    \end{{tabular*}}\vspace{{-7pt}}
}}

\newcommand{{\resumeSubHeadingListStart}}{{\begin{{itemize}}[leftmargin=0.15in, label={{}}]}}
\newcommand{{\resumeSubHeadingListEnd}}{{\end{{itemize}}}}
\newcommand{{\resumeItemListStart}}{{\begin{{itemize}}[leftmargin=0.2in]}}
\newcommand{{\resumeItemListEnd}}{{\end{{itemize}}\vspace{{-5pt}}}}

\begin{{document}}

\begin{{center}}
    {{\Huge \textbf{{{name}}}}} \\ \vspace{{2pt}}
    {email} $|$ {phone} $|$ \href{{{linkedin}}}{{LinkedIn}} $|$ \href{{{github}}}{{GitHub}}
\end{{center}}

\section{{Summary}}
SUMMARY_TEXT

\section{{Education}}
\resumeSubHeadingListStart
  \resumeSubheading
    {{{university}}}{{{graduation}}}
    {{{degree}}}{{}}
\resumeSubHeadingListEnd

\section{{Experience}}
\resumeSubHeadingListStart
EXPERIENCE_ENTRIES
\resumeSubHeadingListEnd

\section{{Projects}}
\resumeSubHeadingListStart
PROJECT_ENTRIES
\resumeSubHeadingListEnd

\section{{Skills}}
\begin{{itemize}}[leftmargin=0.15in, label={{}}]
  \small{{\item {{
    SKILLS_TEXT
  }}}}
\end{{itemize}}

\end{{document}}

RESUME CONTENT TO CONVERT:
{resume_content}

Generate the final complete compilable LaTeX code only.
"""

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
