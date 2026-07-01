# styles.py

def get_css(T: dict) -> str:
    return f"""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;700;800&family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@500;600;700&display=swap');

  /* ── Base ── */
  html, body, [class*="css"] {{
    font-family: 'Inter', sans-serif !important;
    color: {T['text']} !important;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    text-rendering: optimizeLegibility;
    font-feature-settings: "cv11", "ss01";
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
  [data-testid="collapsedControl"] {{ display: none !important; }}
  button[kind="header"] {{ display: none !important; }}
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
  [data-testid="stSidebar"] p,
  [data-testid="stSidebar"] span,
  [data-testid="stSidebar"] div,
  [data-testid="stSidebar"] label {{
    color: {T['text']} !important;
  }}
  [data-testid="stSidebar"] .stSelectbox > div > div {{
    background: {T['surface2']} !important;
    border-color: {T['border']} !important;
    color: {T['text']} !important;
    border-radius: 6px !important;
  }}
  [data-testid="stSidebar"] .stSelectbox svg {{ fill: {T['muted']} !important; }}
  [data-testid="stSidebar"] button {{
    background: {T['surface2']} !important;
    border: 1px solid {T['border']} !important;
    color: {T['text']} !important;
    border-radius: 6px !important;
    text-align: left !important;
    width: 100% !important;
    padding: 10px 12px !important;
    font-size: 12px !important;
    margin-bottom: 4px !important;
    white-space: nowrap !important;
    overflow: hidden !important;
    text-overflow: ellipsis !important;
    font-family: 'JetBrains Mono', monospace !important;
  }}
  [data-testid="stSidebar"] button:hover {{
    border-color: {T['accent']} !important;
    color: {T['accent']} !important;
  }}

  /* ── Main block ── */
  .main .block-container {{
    padding: 0px 48px 60px !important;
    max-width: 1180px !important;
    background-color: {T['bg']} !important;
  }}

  /* ── Cards ── */
  .card {{
    background: {T['surface']} !important;
    border: 1px solid {T['border']} !important;
    border-radius: 10px !important;
    padding: 28px !important;
    margin-bottom: 20px !important;
  }}
  .card p, .card li, .card span, .card div {{ color: {T['text']} !important; }}
  .card h1, .card h2, .card h3 {{ color: {T['text']} !important; font-family:'Space Grotesk', sans-serif !important; }}
  .card strong {{ color: {T['text']} !important; }}

  /* ── Markdown typography inside report cards ── */
  .card p {{
    font-size: 14.5px !important;
    line-height: 1.75 !important;
    margin-bottom: 12px !important;
  }}
  .card ul, .card ol {{
    padding-left: 20px !important;
    margin-bottom: 14px !important;
  }}
  .card li {{
    font-size: 14.5px !important;
    line-height: 1.75 !important;
    margin-bottom: 7px !important;
  }}
  .card h1, .card h2, .card h3 {{
    font-weight: 700 !important;
    letter-spacing: -0.01em !important;
    margin-top: 20px !important;
    margin-bottom: 10px !important;
  }}
  .card h3 {{ font-size: 16px !important; }}
  .card h2 {{ font-size: 18px !important; }}
  .card strong {{ font-weight: 700 !important; }}

  /* ── Report tag (signature structural device) ── */
  .report-tag {{
    display: inline-flex;
    align-items: center;
    gap: 6px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 10.5px;
    font-weight: 700;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: {T['accent']};
    background: {T['surface2']};
    border: 1px solid {T['border']};
    border-radius: 4px;
    padding: 4px 10px;
    margin-bottom: 16px;
  }}
  .report-tag::before {{
    content: '';
    width: 6px; height: 6px;
    border-radius: 50%;
    background: {T['accent']};
    flex-shrink: 0;
  }}

  /* ── Hero ── */
  .hero {{
    padding: 44px 0 36px;
    border-bottom: 1px solid {T['border']};
    margin-bottom: 36px;
    background-image: radial-gradient(rgba(115, 137, 126, 0.18) 1px, transparent 1px);
    background-size: 26px 26px;
    background-position: -8px -8px;
  }}

  .hero-eyebrow {{
    display: inline-flex;
    align-items: center;
    gap: 8px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 11.5px;
    font-weight: 700;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: {T['accent']};
    margin-bottom: 18px;
  }}
  .hero-eyebrow::before {{
    content: '';
    width: 7px; height: 7px;
    background: {T['accent']};
    display: inline-block;
  }}

  .hero-title {{
    font-family: 'Space Grotesk', sans-serif;
    font-size: clamp(32px, 4.2vw, 46px);
    font-weight: 700;
    color: {T['text']};
    line-height: 1.14;
    margin: 0 0 18px;
    letter-spacing: -0.025em;
  }}

  .hero-title span {{ color: {T['accent']}; font-weight: 700; }}

  .hero-sub {{
    font-size: 16.5px;
    color: #a9bdb3;
    line-height: 1.75;
    max-width: 600px;
    margin: 0;
    font-weight: 400;
  }}

  .accent-text {{
    color: {T['text']};
    font-weight: 600;
  }}

  /* ── Feature grid (spec sheet) ── */
  .feature-grid {{
    display: grid;
    grid-template-columns: repeat(5, 1fr);
    gap: 1px;
    margin-top: 36px;
    background: {T['border']};
    border: 1px solid {T['border']};
    border-radius: 10px;
    overflow: hidden;
  }}

  @media (max-width: 900px) {{
    .feature-grid {{ grid-template-columns: repeat(2, 1fr); }}
  }}

  .feature-chip {{
    background: {T['surface']};
    padding: 20px 18px;
  }}

  .feature-chip-icon {{ font-size: 22px; margin-bottom: 10px; }}
  .feature-chip-title {{
    font-family: 'JetBrains Mono', monospace;
    font-size: 11.5px; font-weight: 700; letter-spacing: 0.04em;
    text-transform: uppercase;
    color: {T['text']}; margin-bottom: 6px;
  }}
  .feature-chip-desc {{ font-size: 12.5px; color: #8ea198; line-height: 1.6; }}

  /* ── Input labels ── */
  .input-label {{
    font-family: 'JetBrains Mono', monospace;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: {T['muted']};
    margin-bottom: 8px;
  }}

  /* ── Text area ── */
  .stTextArea textarea {{
    background: {T['surface']} !important;
    border: 1px solid {T['border']} !important;
    border-radius: 8px !important;
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
    border: 1.5px dashed {T['border']} !important;
    border-radius: 8px !important;
    padding: 8px !important;
  }}
  [data-testid="stFileUploader"] * {{ color: {T['text']} !important; }}
  [data-testid="stFileUploader"]:hover {{ border-color: {T['accent']} !important; }}

  /* ── Primary button — solid, not gradient ── */
  .stButton > button {{
    background: {T['accent']} !important;
    color: #0b1210 !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 700 !important;
    font-size: 14.5px !important;
    padding: 13px 26px !important;
    width: 100% !important;
    font-family: 'JetBrains Mono', monospace !important;
    letter-spacing: 0.01em !important;
    transition: filter 0.15s !important;
  }}
  .stButton > button:hover {{ filter: brightness(1.12) !important; }}

  /* ── Tabs ── */
  .stTabs [data-baseweb="tab-list"] {{
    background: {T['surface']} !important;
    border-radius: 8px !important;
    padding: 4px !important;
    gap: 2px !important;
    border: 1px solid {T['border']} !important;
  }}
  .stTabs [data-baseweb="tab"] {{
    background: transparent !important;
    border-radius: 6px !important;
    color: {T['muted']} !important;
    font-weight: 600 !important;
    font-size: 13.5px !important;
    padding: 9px 18px !important;
    border: none !important;
  }}
  .stTabs [aria-selected="true"] {{
    background: {T['accent']} !important;
    color: #0b1210 !important;
  }}
  .stTabs [data-baseweb="tab-panel"] {{ padding: 24px 0 0 !important; background: transparent !important; }}

  /* ── Radial gauge (signature element) ── */
  .gauge-wrap {{
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 20px 0 4px;
  }}
  .gauge {{
    position: relative;
    width: 156px; height: 156px;
    border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
  }}
  .gauge::before {{
    content: '';
    position: absolute;
    top: -2px; left: 50%;
    width: 3px; height: 10px;
    background: {T['muted']};
    transform: translateX(-50%);
  }}
  .gauge-inner {{
    width: 122px; height: 122px;
    border-radius: 50%;
    display: flex; flex-direction: column;
    align-items: center; justify-content: center;
  }}
  .gauge-value {{
    font-family: 'JetBrains Mono', monospace;
    font-size: 38px; font-weight: 700;
    line-height: 1;
  }}
  .gauge-max {{
    font-family: 'JetBrains Mono', monospace;
    font-size: 11px; font-weight: 600;
    color: {T['muted']}; margin-top: 4px;
  }}
  .gauge-caption {{
    font-family: 'JetBrains Mono', monospace;
    font-size: 10.5px; font-weight: 700;
    letter-spacing: 0.12em; text-transform: uppercase;
    color: {T['muted']}; margin-top: 14px;
  }}

  /* ── Progress / status ── */
  div[data-testid="stStatusWidget"],
  div[data-baseweb="block"] [data-testid="stExpander"] {{
    background: {T['surface']} !important;
    border: 1px solid {T['border']} !important;
    border-radius: 8px !important;
  }}
  .stProgress > div > div > div > div {{ background: {T['accent']} !important; }}
  .stProgress > div > div {{ background: {T['surface2']} !important; }}

  /* ── Sidebar section headers ── */
  .sb-header {{
    font-family: 'JetBrains Mono', monospace !important;
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
    font-size: 12.5px; color: {T['muted']}; line-height: 1.5;
  }}
  .how-step:last-child {{ border-bottom: none; }}
  .how-num {{
    width: 18px; height: 18px;
    background: {T['accent']};
    color: #0b1210; font-size: 10px; font-weight: 800;
    font-family: 'JetBrains Mono', monospace;
    display: flex; align-items: center; justify-content: center;
    flex-shrink: 0; margin-top: 1px;
    border-radius: 3px;
  }}

  /* ── Download button ── */
  [data-testid="stDownloadButton"] > button {{
    background: {T['surface2']} !important;
    color: {T['accent']} !important;
    border: 1px solid {T['accent']} !important;
    border-radius: 6px !important;
    font-weight: 600 !important;
    margin-top: 12px !important;
    width: auto !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 12.5px !important;
  }}

  /* ── Tech / keyword badges ── */
  .tech-badge {{
    display: inline-block;
    background: {T['surface2']};
    border: 1px solid {T['border']};
    border-radius: 4px;
    padding: 4px 9px;
    font-size: 11px; font-weight: 600;
    color: {T['muted']};
    margin: 3px 3px 3px 0;
    font-family: 'JetBrains Mono', monospace;
  }}

  .kw-found {{
    display: inline-block;
    background: #052e16; color: #4ade80; border: 1px solid #1d5b3a;
    border-radius: 4px; padding: 5px 11px; font-size: 12.5px; font-weight: 600;
    margin: 4px 4px 4px 0; font-family: 'JetBrains Mono', monospace;
  }}
  .kw-missing {{
    display: inline-block;
    background: #3a0d0d; color: #f87171; border: 1px solid #6b1f1f;
    border-radius: 4px; padding: 5px 11px; font-size: 12.5px; font-weight: 600;
    margin: 4px 4px 4px 0; font-family: 'JetBrains Mono', monospace;
  }}

  hr {{ border-color: {T['border']} !important; }}

  /* ── Info / explainer box ── */
  .info-box {{
    background: {T['surface2']};
    border: 1px solid {T['border']};
    border-left: 3px solid {T['accent']};
    border-radius: 6px;
    padding: 14px 18px;
    margin-bottom: 20px;
    font-size: 13.5px;
    color: {T['muted']};
    line-height: 1.6;
  }}
  .info-box strong {{ color: {T['text']} !important; }}
</style>
"""