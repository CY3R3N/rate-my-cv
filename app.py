# app.py

import streamlit as st
import tempfile
import os
import warnings
import re
from datetime import datetime
warnings.filterwarnings("ignore")

from styles import get_css
from src.ingestion.resume_parser import parse_resume
from src.preprocessing.cleaner import clean_text
from src.preprocessing.chunker import chunk_text
from src.embeddings.embedder import load_embedder
from src.embeddings.vector_store import build_vector_store, search_vector_store
from src.llm.llm_client import load_llm
from src.llm.prompts.match_scorer import get_match_score
from src.llm.prompts.cover_letter import get_cover_letter
from src.llm.prompts.gap_analyser import get_gap_analysis
from src.llm.prompts.interview_prep import get_interview_prep
from src.llm.prompts.ats_scanner import get_ats_scan

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="RateMyCV",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={"Get help": None, "Report a bug": None, "About": None}
)

# ── Session state ──────────────────────────────────────────────────────────────
if "history"  not in st.session_state: st.session_state.history  = []
if "results"  not in st.session_state: st.session_state.results  = None
if "running"  not in st.session_state: st.session_state.running  = False

# ── Theme tokens — "Inspection Deck" identity (dark only) ─────────────────────
T = {
    "bg":      "#0b1210",
    "surface": "#121a17",
    "surface2":"#182420",
    "border":  "#243630",
    "text":    "#eef4f0",
    "muted":   "#73897e",
    "accent":  "#ff7a45",
    "accent2": "#5fd4a0",
}

MODEL = "llama-3.3-70b-versatile"

st.markdown(get_css(T), unsafe_allow_html=True)

# ── Helpers ────────────────────────────────────────────────────────────────────
def extract_score(text: str) -> int:
    patterns = [
        r'match\s*score[:\s]+(\d{1,3})',
        r'score[:\s]+(\d{1,3})\s*/\s*100',
        r'\b(\d{1,3})\s*/\s*100',
        r'score[:\s]+(\d{1,3})',
    ]
    for pattern in patterns:
        m = re.search(pattern, text, re.IGNORECASE)
        if m:
            s = int(m.group(1))
            if 0 <= s <= 100:
                return s
    return 0

def score_colors(score: int):
    if score >= 75: return "#4ade80"
    if score >= 50: return "#f5b942"
    return "#f87171"

def gauge_html(score: int, surface: str, caption: str) -> str:
    color = score_colors(score)
    deg = round(score * 3.6, 1)
    return f"""
    <div class="gauge-wrap">
      <div class="gauge" style="background:conic-gradient({color} 0deg, {color} {deg}deg, {surface} {deg}deg, {surface} 360deg);">
        <div class="gauge-inner" style="background:{surface};">
          <div class="gauge-value" style="color:{color};">{score}</div>
          <div class="gauge-max">OUT OF 100</div>
        </div>
      </div>
      <div class="gauge-caption">{caption}</div>
    </div>
    """

def report_tag(label: str) -> str:
    return f'<div class="report-tag">{label}</div>'

# ── Sidebar ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(f"""
    <div style="padding-bottom:16px;border-bottom:1px solid {T['border']};margin-bottom:4px;">
      <div style="font-family:'Space Grotesk',sans-serif;font-size:19px;font-weight:800;color:{T['text']};letter-spacing:-0.01em;">
        🩺 RateMyCV
      </div>
      <div style="font-family:'JetBrains Mono',monospace;font-size:11px;color:{T['muted']};margin-top:5px;letter-spacing:0.02em;">
        RESUME DIAGNOSTIC ENGINE
      </div>
    </div>""", unsafe_allow_html=True)

    st.markdown(f'<div class="sb-header first">How to use</div>', unsafe_allow_html=True)
    st.markdown(f"""
    <div style="margin-bottom:4px;">
      <div class="how-step"><div class="how-num">1</div><span>Upload your resume (PDF or DOCX)</span></div>
      <div class="how-step"><div class="how-num">2</div><span>Paste the full job description</span></div>
      <div class="how-step"><div class="how-num">3</div><span>Run the diagnostic — takes ~15s</span></div>
      <div class="how-step"><div class="how-num">4</div><span>Review your full report across 5 panels</span></div>
    </div>""", unsafe_allow_html=True)

    st.markdown(f'<div class="sb-header">Diagnostic history</div>', unsafe_allow_html=True)
    if not st.session_state.history:
        st.markdown(f'<div style="font-size:12.5px;color:{T["muted"]};padding:6px 0;">No diagnostics run yet.</div>', unsafe_allow_html=True)
    else:
        for i, item in enumerate(reversed(st.session_state.history)):
            if st.button(
                f"{item['filename']}  ·  {item['score']}/100  ·  {item['time']}",
                key=f"hist_{i}"
            ):
                st.session_state.results = item["results"]
                st.rerun()

    st.markdown(f'<div class="sb-header">Privacy</div>', unsafe_allow_html=True)
    st.markdown(f"""
    <div style="font-size:12.5px;color:{T['muted']};line-height:1.65;padding-bottom:4px;">
      🔒 Your resume and job description are processed in memory for this session only.
      Nothing is written to disk or a database. Refreshing or closing this tab permanently
      clears your resume, results, and history.
    </div>""", unsafe_allow_html=True)

    st.markdown(f'<div class="sb-header">Built with</div>', unsafe_allow_html=True)
    st.markdown("""
    <div>
      <span class="tech-badge">LangChain</span><span class="tech-badge">FAISS</span>
      <span class="tech-badge">HuggingFace</span><span class="tech-badge">Groq</span>
      <span class="tech-badge">Streamlit</span><span class="tech-badge">PyTorch</span>
    </div>""", unsafe_allow_html=True)

# ── Main body ──────────────────────────────────────────────────────────────────

st.markdown(f"""
<div class="hero">
  <div class="hero-eyebrow">Automated Resume Diagnostic</div>
  <h1 class="hero-title">Your resume, <span>under inspection.</span></h1>
  <p class="hero-sub">
    Most resumes are <span class="accent-text">rejected before a human ever reads them</span>.
    RateMyCV runs your resume through the same lens recruiters and hiring software use —
    scoring your fit for a specific role, catching what's missing, and preparing you to
    talk about the gaps — all in about <span class="accent-text">15 seconds</span>.
  </p>
</div>""", unsafe_allow_html=True)

st.markdown(f'<div class="input-label">Upload Resume</div>', unsafe_allow_html=True)
uploaded_file = st.file_uploader("Resume", type=["pdf", "docx"], label_visibility="collapsed")
st.markdown(f"""
<div style="display:flex;align-items:center;gap:6px;margin-top:8px;font-size:12px;color:{T['muted']};">
  🔒 Processed in memory only — nothing is saved. Refreshing the page clears everything. Max file size: 5MB.
</div>""", unsafe_allow_html=True)

MAX_FILE_SIZE_MB = 5
if uploaded_file is not None:
    file_size_mb = uploaded_file.size / (1024 * 1024)
    if file_size_mb > MAX_FILE_SIZE_MB:
        st.error(f"⚠️ '{uploaded_file.name}' is {file_size_mb:.1f}MB — please upload a file under {MAX_FILE_SIZE_MB}MB.")
        uploaded_file = None

st.markdown(f'<div class="input-label" style="margin-top:20px;">Job Description</div>', unsafe_allow_html=True)
job_description = st.text_area(
    "JD", height=200,
    placeholder="Paste the full job description here...",
    label_visibility="collapsed"
)

_, btn_col = st.columns([3, 1])
with btn_col:
    run_button = st.button("Run Diagnostic →")

if not st.session_state.running and not st.session_state.results:
    st.markdown(f"""
    <div class="feature-grid">
      <div class="feature-chip">
        <div class="feature-chip-icon">📊</div>
        <div class="feature-chip-title">Match Score</div>
        <div class="feature-chip-desc">A 0–100 score showing how closely your resume fits this specific role, with what's working and what isn't.</div>
      </div>
      <div class="feature-chip">
        <div class="feature-chip-icon">✉️</div>
        <div class="feature-chip-title">Cover Letter</div>
        <div class="feature-chip-desc">A tailored first draft written only from what's actually on your resume — nothing invented.</div>
      </div>
      <div class="feature-chip">
        <div class="feature-chip-icon">🔍</div>
        <div class="feature-chip-title">Skill Gaps</div>
        <div class="feature-chip-desc">What the role needs that your resume doesn't show yet, plus concrete steps to close each gap.</div>
      </div>
      <div class="feature-chip">
        <div class="feature-chip-icon">🎯</div>
        <div class="feature-chip-title">Interview Prep</div>
        <div class="feature-chip-desc">Likely interview questions for this role, with answer frameworks built from your real experience.</div>
      </div>
      <div class="feature-chip">
        <div class="feature-chip-icon">🩺</div>
        <div class="feature-chip-title">ATS Scan</div>
        <div class="feature-chip-desc">Checks the exact keywords the job description expects — the same check automated hiring software runs before a human sees your resume.</div>
      </div>
    </div>""", unsafe_allow_html=True)

# ── Pipeline ───────────────────────────────────────────────────────────────────
if run_button:
    if not uploaded_file or not job_description.strip():
        st.warning("Please upload a resume and paste a job description.")
    else:
        st.session_state.running = True
        st.session_state.results = None

        progress_bar = st.progress(0, text="Parsing resume...")
        status = st.status("Running diagnostic", expanded=True)

        with status:
            st.write("📄 Parsing resume...")
            suffix = ".pdf" if uploaded_file.name.endswith(".pdf") else ".docx"
            with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
                tmp.write(uploaded_file.read())
                tmp_path = tmp.name
            raw     = parse_resume(tmp_path)
            cleaned = clean_text(raw)
            progress_bar.progress(20, text="Chunking & embedding...")

            st.write("🔢 Chunking & embedding...")
            chunks   = chunk_text(cleaned)
            embedder = load_embedder()
            progress_bar.progress(40, text="Building vector index...")

            st.write("🗃️ Building vector index...")
            vs   = build_vector_store(chunks, embedder)
            hits = search_vector_store(vs, job_description)
            ctx  = "\n\n".join(hits)
            llm  = load_llm()
            os.unlink(tmp_path)
            progress_bar.progress(60, text="Running AI analysis...")

            st.write("🤖 Generating match score, cover letter, gaps & prep...")
            score_text     = get_match_score(llm, ctx, job_description)
            cover_text     = get_cover_letter(llm, ctx, job_description)
            gap_text       = get_gap_analysis(llm, ctx, job_description)
            interview_text = get_interview_prep(llm, ctx, job_description)
            progress_bar.progress(85, text="Running ATS keyword scan...")

            st.write("🩺 Running ATS keyword scan...")
            ats_result = get_ats_scan(llm, ctx, job_description)
            progress_bar.progress(100, text="Done!")
            status.update(label="Diagnostic complete ✅", state="complete", expanded=False)

        score = extract_score(score_text)
        bundle = {
            "score_text": score_text, "cover_text": cover_text,
            "gap_text": gap_text, "interview_text": interview_text,
            "ats_result": ats_result,
        }
        st.session_state.history.append({
            "filename": uploaded_file.name,
            "score": score,
            "time": datetime.now().strftime("%H:%M"),
            "results": bundle,
        })
        st.session_state.results = bundle
        st.session_state.running = False
        st.rerun()

# ── Results ────────────────────────────────────────────────────────────────────
if st.session_state.results and not st.session_state.running:
    r     = st.session_state.results
    score = extract_score(r["score_text"])

    st.markdown("<div style='margin-top:20px;'></div>", unsafe_allow_html=True)

    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊  Match Score", "✉️  Cover Letter",
        "🔍  Skill Gaps",  "🎯  Interview Prep",
        "🩺  ATS Scan",
    ])

    with tab1:
        c1, c2 = st.columns([1, 2], gap="large")
        with c1:
            st.markdown(f'<div class="card">{gauge_html(score, T["surface"], "MATCH SCORE")}</div>', unsafe_allow_html=True)
        with c2:
            st.markdown(f'<div class="card">{report_tag("MATCH REPORT")}', unsafe_allow_html=True)
            st.markdown(r["score_text"])
            st.markdown('</div>', unsafe_allow_html=True)

    with tab2:
        st.markdown(f'<div class="card">{report_tag("COVER LETTER DRAFT")}', unsafe_allow_html=True)
        st.markdown(r["cover_text"])
        st.markdown('</div>', unsafe_allow_html=True)
        st.download_button(
            "⬇  DOWNLOAD COVER LETTER",
            data=r["cover_text"],
            file_name="cover_letter.txt",
            mime="text/plain"
        )

    with tab3:
        st.markdown(f'<div class="card">{report_tag("GAP ANALYSIS")}', unsafe_allow_html=True)
        st.markdown(r["gap_text"])
        st.markdown('</div>', unsafe_allow_html=True)

    with tab4:
        st.markdown(f'<div class="card">{report_tag("INTERVIEW BRIEF")}', unsafe_allow_html=True)
        st.markdown(r["interview_text"])
        st.markdown('</div>', unsafe_allow_html=True)

    with tab5:
        ats     = r.get("ats_result", {})
        ats_score = ats.get("ats_score", 0)
        found     = ats.get("found", [])
        missing   = ats.get("missing", [])
        verdict   = ats.get("verdict", "")

        st.markdown(f"""
        <div class="info-box">
          <strong>What's an ATS?</strong> An Applicant Tracking System is software that many companies
          use to automatically filter resumes before a recruiter ever opens them. It scans for exact
          keywords from the job posting — if your resume doesn't contain them, it can be rejected
          automatically, regardless of your actual experience. This scan shows you what an ATS would see.
        </div>""", unsafe_allow_html=True)

        c1, c2 = st.columns([1, 2], gap="large")
        with c1:
            st.markdown(f'<div class="card">{gauge_html(ats_score, T["surface"], "ATS SCORE")}</div>', unsafe_allow_html=True)
        with c2:
            st.markdown(f"""
            <div class="card">
              {report_tag("ATS VERDICT")}
              <p style="color:{T['text']};font-size:14.5px;line-height:1.7;margin:0;">{verdict}</p>
            </div>""", unsafe_allow_html=True)

        col_found, col_missing = st.columns(2, gap="large")
        with col_found:
            badges = ''.join([f'<span class="kw-found">✓ {kw}</span>' for kw in found]) or '<span style="color:'+T['muted']+';font-size:13px;">None detected</span>'
            st.markdown(f"""
            <div class="card">
              {report_tag(f"FOUND · {len(found)}")}
              <div>{badges}</div>
            </div>""", unsafe_allow_html=True)
        with col_missing:
            badges = ''.join([f'<span class="kw-missing">✕ {kw}</span>' for kw in missing]) or '<span style="color:'+T['muted']+';font-size:13px;">None missing</span>'
            st.markdown(f"""
            <div class="card">
              {report_tag(f"MISSING · {len(missing)}")}
              <div>{badges}</div>
            </div>""", unsafe_allow_html=True)