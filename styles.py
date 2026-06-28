# styles.py

def get_css(T: dict) -> str:
    return f"""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;600&display=swap');

  /* ── Base ── */
  html, body, [class*="css"] {{
    font-family: 'Inter', sans-serif !important;
    color: {T['text']} !important;
  }}

  .stApp {{
    background-color: {T['bg']} !important;
  }}

  /* ── Hide Streamlit chrome ── */
  #MainMenu {{ visibility: hidden !important; }}
  footer {{ visibility: hidden !important; }}
  [data-testid="stToolbar"] {{ display: none !important; }}
  [data-testid="stDecoration"] {{ display: none !important; }}
  [data-testid="stStatusWidget"] {{ display: none !important; }}
  header[data-testid="stHeader"] {{ display: none !important; }}

  /* ── Sidebar ── */
  [data-testid="stSidebar"] > div:first-child {{
    background-color: {T['surface']} !important;
    border-right: 1px solid {T['border']} !important;
    padding-top: 24px !important;
  }}

/* Force sidebar always visible */
  [data-testid="collapsedControl"] {{
    display: none !important;
    visibility: hidden !important;
    width: 0 !important;
    height: 0 !important;
  }}

  button[kind="header"] {{
    display: none !important;
  }}

  /* Ensure sidebar has width */
  section[data-testid="stSidebar"] {{
    min-width: 280px !important;
    width: 280px !important;
    transform: none !important;
  }}

  section[data-testid="stSidebar"][aria-expanded="false"] {{
    min-width: 280px !important;
    margin-left: 0 !important;
    transform: none !important;
  }}

  /* Sidebar text */
  [data-testid="stSidebar"] p,
  [data-testid="stSidebar"] span,
  [data-testid="stSidebar"] div,
  [data-testid="stSidebar"] label {{
    color: {T['text']} !important;
  }}

  /* Sidebar selectbox */
  [data-testid="stSidebar"] .stSelectbox > div > div {{
    background: {T['surface2']} !important;
    border-color: {T['border']} !important;
    color: {T['text']} !important;
  }}

  [data-testid="stSidebar"] .stSelectbox svg {{
    fill: {T['muted']} !important;
  }}

  /* Sidebar buttons */
  [data-testid="stSidebar"] button {{
    background: {T['surface2']} !important;
    border: 1px solid {T['border']} !important;
    color: {T['text']} !important;
    border-radius: 8px !important;
    text-align: left !important;
    width: 100% !important;
    padding: 10px 12px !important;
    font-size: 12px !important;
    margin-bottom: 4px !important;
    white-space: nowrap !important;
    overflow: hidden !important;
    text-overflow: ellipsis !important;
  }}

  [data-testid="stSidebar"] button:hover {{
    border-color: {T['accent']} !important;
    color: {T['accent']} !important;
  }}

  /* ── Main block ── */
  .main .block-container {{
    padding: 32px 48px 60px !important;
    max-width: 1200px !important;
    background-color: {T['bg']} !important;
  }}

  /* ── Cards ── */
  .card {{
    background: {T['surface']} !important;
    border: 1px solid {T['border']} !important;
    border-radius: 14px !important;
    padding: 28px !important;
    margin-bottom: 20px !important;
  }}

  .card p, .card li, .card span, .card div {{
    color: {T['text']} !important;
  }}

  /* ── Hero ── */
  .hero {{
    padding: 40px 0 36px;
    border-bottom: 1px solid {T['border']};
    margin-bottom: 36px;
  }}

  .hero-eyebrow {{
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 0.16em;
    text-transform: uppercase;
    color: {T['accent']};
    margin-bottom: 12px;
  }}

  .hero-title {{
    font-size: 40px;
    font-weight: 800;
    color: {T['text']};
    line-height: 1.15;
    margin: 0 0 14px;
    letter-spacing: -0.02em;
  }}

  .hero-title span {{
    background: linear-gradient(135deg, {T['accent']}, {T['accent2']});
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
  }}

  .hero-sub {{
    font-size: 16px;
    color: {T['muted']};
    line-height: 1.6;
    max-width: 560px;
    margin: 0;
  }}

  /* ── Feature chips ── */
  .feature-grid {{
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 14px;
    margin-top: 36px;
  }}

  .feature-chip {{
    background: {T['surface']};
    border: 1px solid {T['border']};
    border-radius: 12px;
    padding: 22px 16px;
    text-align: center;
  }}

  .feature-chip-icon {{ font-size: 28px; margin-bottom: 10px; }}
  .feature-chip-title {{ font-size: 13px; font-weight: 700; color: {T['text']}; margin-bottom: 5px; }}
  .feature-chip-desc {{ font-size: 12px; color: {T['muted']}; line-height: 1.5; }}

  /* ── Input labels ── */
  .input-label {{
    font-size: 12px;
    font-weight: 700;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: {T['muted']};
    margin-bottom: 8px;
  }}

  /* ── Text area ── */
  .stTextArea textarea {{
    background: {T['surface']} !important;
    border: 1px solid {T['border']} !important;
    border-radius: 10px !important;
    color: {T['text']} !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 14px !important;
  }}

  .stTextArea textarea:focus {{
    border-color: {T['accent']} !important;
    box-shadow: 0 0 0 3px {T['accent']}22 !important;
  }}

  /* ── File uploader ── */
  [data-testid="stFileUploader"] {{
    background: {T['surface']} !important;
    border: 2px dashed {T['border']} !important;
    border-radius: 10px !important;
    padding: 8px !important;
  }}

  [data-testid="stFileUploader"] * {{
    color: {T['text']} !important;
  }}

  [data-testid="stFileUploader"]:hover {{
    border-color: {T['accent']} !important;
  }}

  /* ── Analyse button ── */
  .stButton > button {{
    background: linear-gradient(135deg, {T['accent']}, {T['accent2']}) !important;
    color: #fff !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 700 !important;
    font-size: 15px !important;
    padding: 14px 28px !important;
    width: 100% !important;
    transition: opacity 0.2s !important;
  }}

  .stButton > button:hover {{
    opacity: 0.88 !important;
  }}

  /* ── Tabs ── */
  .stTabs [data-baseweb="tab-list"] {{
    background: {T['surface']} !important;
    border-radius: 12px !important;
    padding: 5px !important;
    gap: 4px !important;
    border: 1px solid {T['border']} !important;
  }}

  .stTabs [data-baseweb="tab"] {{
    background: transparent !important;
    border-radius: 8px !important;
    color: {T['muted']} !important;
    font-weight: 600 !important;
    font-size: 14px !important;
    padding: 9px 20px !important;
    border: none !important;
  }}

  .stTabs [aria-selected="true"] {{
    background: linear-gradient(135deg, {T['accent']}, {T['accent2']}) !important;
    color: #fff !important;
  }}

  .stTabs [data-baseweb="tab-panel"] {{
    padding: 24px 0 0 !important;
    background: transparent !important;
  }}

  /* ── Score ring ── */
  .score-wrap {{
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 28px 0;
  }}

  .score-ring {{
    width: 148px;
    height: 148px;
    border-radius: 50%;
    border: 8px solid;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 44px;
    font-weight: 800;
    font-family: 'JetBrains Mono', monospace;
    margin-bottom: 12px;
  }}

  .score-label {{
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: {T['muted']};
  }}

  /* ── Progress steps ── */
  .progress-wrap {{
    background: {T['surface']};
    border: 1px solid {T['border']};
    border-radius: 14px;
    padding: 24px 28px;
    margin-bottom: 28px;
  }}

  .progress-title {{
    font-size: 12px;
    font-weight: 700;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: {T['muted']};
    margin-bottom: 18px;
  }}

  .pstep {{
    display: flex;
    align-items: center;
    gap: 14px;
    padding: 10px 0;
    font-size: 14px;
    color: {T['muted']};
    border-bottom: 1px solid {T['border']};
  }}

  .pstep:last-child {{ border-bottom: none; }}

  .pstep-dot {{
    width: 30px; height: 30px;
    border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-size: 13px; font-weight: 700; flex-shrink: 0;
    background: {T['surface2']};
    border: 1px solid {T['border']};
    color: {T['muted']};
  }}

  .pstep-dot.done {{ background: #052e16; border-color: #22c55e; color: #22c55e; }}
  .pstep-dot.active {{ background: #1e1b4b; border-color: {T['accent']}; color: {T['accent']}; animation: pulse 1.2s infinite; }}
  .pstep.active-text {{ color: {T['text']}; font-weight: 600; }}
  .pstep.done-text {{ color: #4ade80; }}

  @keyframes pulse {{
    0%, 100% {{ box-shadow: 0 0 0 0 {T['accent']}55; }}
    50% {{ box-shadow: 0 0 0 6px {T['accent']}00; }}
  }}

  /* ── Sidebar section headers ── */
  .sb-header {{
    font-size: 10px !important;
    font-weight: 700 !important;
    letter-spacing: 0.14em !important;
    text-transform: uppercase !important;
    color: {T['muted']} !important;
    padding: 16px 0 8px !important;
    border-top: 1px solid {T['border']} !important;
    margin-top: 8px !important;
  }}

  .sb-header.first {{ border-top: none !important; padding-top: 0 !important; }}

  /* ── How to use ── */
  .how-step {{
    display: flex; gap: 12px; align-items: flex-start;
    padding: 10px 0;
    border-bottom: 1px solid {T['border']};
    font-size: 13px; color: {T['muted']}; line-height: 1.5;
  }}
  .how-step:last-child {{ border-bottom: none; }}
  .how-num {{
    width: 22px; height: 22px; border-radius: 50%;
    background: linear-gradient(135deg, {T['accent']}, {T['accent2']});
    color: #fff; font-size: 11px; font-weight: 800;
    display: flex; align-items: center; justify-content: center;
    flex-shrink: 0; margin-top: 1px;
  }}

  /* ── Download button ── */
  [data-testid="stDownloadButton"] > button {{
    background: {T['surface2']} !important;
    color: {T['accent']} !important;
    border: 1px solid {T['accent']} !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
    margin-top: 12px !important;
    width: auto !important;
  }}

  /* ── Tech badges ── */
  .tech-badge {{
    display: inline-block;
    background: {T['surface2']};
    border: 1px solid {T['border']};
    border-radius: 20px;
    padding: 4px 10px;
    font-size: 11px; font-weight: 600;
    color: {T['muted']};
    margin: 3px 3px 3px 0;
    font-family: 'JetBrains Mono', monospace;
  }}

  /* ── Markdown inside cards ── */
  .card h1, .card h2, .card h3 {{ color: {T['text']} !important; }}
  .card strong {{ color: {T['text']} !important; }}
  .card ul, .card ol {{ color: {T['text']} !important; }}
</style>
"""