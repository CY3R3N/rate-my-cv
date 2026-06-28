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

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="RateMyCV",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={"Get help": None, "Report a bug": None, "About": None}
)

# ── Session state ──────────────────────────────────────────────────────────────
if "history"  not in st.session_state: st.session_state.history  = []
if "results"  not in st.session_state: st.session_state.results  = None
if "theme"    not in st.session_state: st.session_state.theme    = "dark"
if "model"    not in st.session_state: st.session_state.model    = "llama-3.3-70b-versatile"
if "running"  not in st.session_state: st.session_state.running  = False
if "step"     not in st.session_state: st.session_state.step     = -1

# ── Theme tokens ───────────────────────────────────────────────────────────────
THEMES = {
    "dark": {
        "bg":      "#0b0f1a",
        "surface": "#131929",
        "surface2":"#1a2236",
        "border":  "#1e2d45",
        "text":    "#e8edf5",
        "muted":   "#5a7090",
        "accent":  "#5b7fff",
        "accent2": "#8b5cf6",
    },
    "light": {
        "bg":      "#f0f4ff",
        "surface": "#ffffff",
        "surface2":"#e8edf8",
        "border":  "#c8d4f0",
        "text":    "#0b1730",
        "muted":   "#6b7fa8",
        "accent":  "#3d5fe0",
        "accent2": "#6d3fd6",
    },
}

T = THEMES[st.session_state.theme]
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
    if score >= 75: return "#22c55e", "#052e16"
    if score >= 50: return "#f59e0b", "#451a03"
    return "#ef4444", "#450a0a"

STEPS = [
    ("Parsing resume", "📄"),
    ("Chunking & embedding", "🔢"),
    ("Building vector index", "🗃️"),
    ("Running AI analysis", "🤖"),
]


# ── Sidebar ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(f"""
    <div style="padding-bottom:16px;border-bottom:1px solid {T['border']};margin-bottom:4px;">
      <div style="font-size:18px;font-weight:800;color:{T['text']};letter-spacing:-0.01em;">
        💼 RateMyCV
      </div>
      <div style="font-size:12px;color:{T['muted']};margin-top:4px;">
        RAG-powered resume analyser
      </div>
    </div>""", unsafe_allow_html=True)

    st.markdown(f'<div class="sb-header first">How to use</div>', unsafe_allow_html=True)
    st.markdown(f"""
    <div style="margin-bottom:4px;">
      <div class="how-step"><div class="how-num">1</div><span>Upload your resume (PDF or DOCX)</span></div>
      <div class="how-step"><div class="how-num">2</div><span>Paste the full job description</span></div>
      <div class="how-step"><div class="how-num">3</div><span>Click Analyse and wait ~15s</span></div>
      <div class="how-step"><div class="how-num">4</div><span>Review score, cover letter, gaps & prep</span></div>
    </div>""", unsafe_allow_html=True)

    st.markdown(f'<div class="sb-header">Settings</div>', unsafe_allow_html=True)

    theme_choice = st.selectbox(
        "Theme", ["dark", "light"],
        index=0 if st.session_state.theme == "dark" else 1
    )
    if theme_choice != st.session_state.theme:
        st.session_state.theme = theme_choice
        st.rerun()

    model_choice = st.selectbox(
        "Model",
        ["llama-3.3-70b-versatile", "llama-3.1-8b-instant", "mixtral-8x7b-32768"],
        index=["llama-3.3-70b-versatile", "llama-3.1-8b-instant", "mixtral-8x7b-32768"].index(st.session_state.model)
    )
    if model_choice != st.session_state.model:
        st.session_state.model = model_choice

    st.markdown(f'<div class="sb-header">Analysis history</div>', unsafe_allow_html=True)
    if not st.session_state.history:
        st.markdown(f'<div style="font-size:13px;color:{T["muted"]};padding:6px 0;">No analyses yet.</div>', unsafe_allow_html=True)
    else:
        for i, item in enumerate(reversed(st.session_state.history)):
            if st.button(
                f"📄 {item['filename']}  ·  {item['score']}/100  ·  {item['time']}",
                key=f"hist_{i}"
            ):
                st.session_state.results = item["results"]
                st.rerun()

    st.markdown(f'<div class="sb-header">Built with</div>', unsafe_allow_html=True)
    st.markdown("""
    <div>
      <span class="tech-badge">LangChain</span><span class="tech-badge">FAISS</span>
      <span class="tech-badge">HuggingFace</span><span class="tech-badge">Groq</span>
      <span class="tech-badge">Streamlit</span><span class="tech-badge">PyTorch</span>
    </div>""", unsafe_allow_html=True)

# ── Main body ──────────────────────────────────────────────────────────────────

# Hero
st.markdown(f"""
<div class="hero">
  <div class="hero-eyebrow">AI-Powered Career Tool</div>
  <h1 class="hero-title">Your resume, <span>analysed</span><br>against any job.</h1>
  <p class="hero-sub">
    Upload your resume and paste a job description. Get a match score,
    tailored cover letter, skill gaps, and interview prep in seconds.
  </p>
</div>""", unsafe_allow_html=True)

# ── Inputs stacked vertically, button below JD ────────────────────────────────
st.markdown(f'<div class="input-label">Upload Resume</div>', unsafe_allow_html=True)
uploaded_file = st.file_uploader("Resume", type=["pdf", "docx"], label_visibility="collapsed")

st.markdown(f'<div class="input-label" style="margin-top:20px;">Job Description</div>', unsafe_allow_html=True)
job_description = st.text_area(
    "JD", height=200,
    placeholder="Paste the full job description here...",
    label_visibility="collapsed"
)

# Button aligned to right under JD
_, btn_col = st.columns([3, 1])
with btn_col:
    run_button = st.button("Analyse Application →")

# ── Landing chips ──────────────────────────────────────────────────────────────
if not st.session_state.running and not st.session_state.results:
    st.markdown(f"""
    <div class="feature-grid">
      <div class="feature-chip">
        <div class="feature-chip-icon">📊</div>
        <div class="feature-chip-title">Match Score</div>
        <div class="feature-chip-desc">0–100 score with strengths and gaps</div>
      </div>
      <div class="feature-chip">
        <div class="feature-chip-icon">✉️</div>
        <div class="feature-chip-title">Cover Letter</div>
        <div class="feature-chip-desc">Tailored to the role, grounded in your CV</div>
      </div>
      <div class="feature-chip">
        <div class="feature-chip-icon">🔍</div>
        <div class="feature-chip-title">Skill Gaps</div>
        <div class="feature-chip-desc">What's missing and how to fix it</div>
      </div>
      <div class="feature-chip">
        <div class="feature-chip-icon">🎯</div>
        <div class="feature-chip-title">Interview Prep</div>
        <div class="feature-chip-desc">Likely questions with answer frameworks</div>
      </div>
    </div>""", unsafe_allow_html=True)

# ── Pipeline ───────────────────────────────────────────────────────────────────
if run_button:
    if not uploaded_file or not job_description.strip():
        st.warning("Please upload a resume and paste a job description.")
    else:
        st.session_state.running = True
        st.session_state.results = None

        step_labels = [
            "Parsing resume...",
            "Chunking & embedding...",
            "Building vector index...",
            "Running AI analysis...",
        ]

        progress_bar = st.progress(0, text=step_labels[0])
        status       = st.status("Processing your application", expanded=True)

        with status:
            st.write("📄 Parsing resume...")
            suffix = ".pdf" if uploaded_file.name.endswith(".pdf") else ".docx"
            with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
                tmp.write(uploaded_file.read())
                tmp_path = tmp.name
            raw     = parse_resume(tmp_path)
            cleaned = clean_text(raw)
            progress_bar.progress(25, text=step_labels[1])

            st.write("🔢 Chunking & embedding...")
            chunks   = chunk_text(cleaned)
            embedder = load_embedder()
            progress_bar.progress(50, text=step_labels[2])

            st.write("🗃️ Building vector index...")
            vs   = build_vector_store(chunks, embedder)
            hits = search_vector_store(vs, job_description)
            ctx  = "\n\n".join(hits)
            llm  = load_llm()
            os.unlink(tmp_path)
            progress_bar.progress(75, text=step_labels[3])

            st.write("🤖 Running AI analysis...")
            score_text     = get_match_score(llm, ctx, job_description)
            cover_text     = get_cover_letter(llm, ctx, job_description)
            gap_text       = get_gap_analysis(llm, ctx, job_description)
            interview_text = get_interview_prep(llm, ctx, job_description)
            progress_bar.progress(100, text="Done!")
            status.update(label="Analysis complete ✅", state="complete", expanded=False)

        score = extract_score(score_text)
        bundle = {
            "score_text": score_text, "cover_text": cover_text,
            "gap_text": gap_text, "interview_text": interview_text,
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
    ring_color, ring_bg = score_colors(score)

    st.markdown("<div style='margin-top:20px;'></div>", unsafe_allow_html=True)

    tab1, tab2, tab3, tab4 = st.tabs([
        "📊  Match Score", "✉️  Cover Letter",
        "🔍  Skill Gaps",  "🎯  Interview Prep",
    ])

    with tab1:
        c1, c2 = st.columns([1, 2], gap="large")
        with c1:
            st.markdown(f"""
            <div class="card" style="text-align:center;">
              <div class="score-wrap">
                <div class="score-ring"
                  style="color:{ring_color};border-color:{ring_color};background:{ring_bg};">
                  {score}
                </div>
                <div class="score-label">out of 100</div>
              </div>
            </div>""", unsafe_allow_html=True)
        with c2:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown(r["score_text"])
            st.markdown('</div>', unsafe_allow_html=True)

    with tab2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown(r["cover_text"])
        st.markdown('</div>', unsafe_allow_html=True)
        st.download_button(
            "⬇️  Download Cover Letter",
            data=r["cover_text"],
            file_name="cover_letter.txt",
            mime="text/plain"
        )

    with tab3:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown(r["gap_text"])
        st.markdown('</div>', unsafe_allow_html=True)

    with tab4:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown(r["interview_text"])
        st.markdown('</div>', unsafe_allow_html=True)