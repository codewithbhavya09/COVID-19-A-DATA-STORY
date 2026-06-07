"""
╔══════════════════════════════════════════════════════════════════════════════╗
║         HOW COVID-19 CHANGED THE WORLD: A DATA STORY                        ║
║         Main Application Entry Point                                         ║
║         app.py — Streamlit Multi-Page Narrative Application                  ║
╚══════════════════════════════════════════════════════════════════════════════╝

This is the main entry point. It sets up page configuration, loads shared
data, applies global CSS styling, and renders the sidebar navigation that
guides users through the narrative journey.
"""

import streamlit as st
import pandas as pd
import numpy as np
from pathlib import Path

# ─── Page Configuration ───────────────────────────────────────────────────────
st.set_page_config(
    page_title="COVID-19: A Data Story",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Global CSS Styling ────────────────────────────────────────────────────────
GLOBAL_CSS = """
<style>
  /* Import Google Fonts */
  @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,700;1,400&family=Source+Sans+3:wght@300;400;600&family=JetBrains+Mono:wght@400;700&display=swap');

  /* ── Root Variables ── */
  :root {
    --bg-primary:    #0a0e1a;
    --bg-secondary:  #111827;
    --bg-card:       #1a2235;
    --accent-red:    #e63946;
    --accent-amber:  #f4a261;
    --accent-teal:   #2a9d8f;
    --accent-blue:   #457b9d;
    --text-primary:  #f1f5f9;
    --text-muted:    #94a3b8;
    --border:        rgba(255,255,255,0.08);
    --font-display:  'Playfair Display', serif;
    --font-body:     'Source Sans 3', sans-serif;
    --font-mono:     'JetBrains Mono', monospace;
  }

  /* ── Base Reset ── */
  html, body, [class*="css"] {
    font-family: var(--font-body);
    background-color: var(--bg-primary);
    color: var(--text-primary);
  }

  /* ── Main Container ── */
  .main .block-container {
    padding: 2rem 3rem 4rem;
    max-width: 1200px;
  }

  /* ── Sidebar ── */
  section[data-testid="stSidebar"] {
    background: var(--bg-secondary);
    border-right: 1px solid var(--border);
  }
  section[data-testid="stSidebar"] .block-container {
    padding: 1.5rem 1rem;
  }

  /* ── Hero Title ── */
  .hero-title {
    font-family: var(--font-display);
    font-size: clamp(2.2rem, 4vw, 3.6rem);
    font-weight: 700;
    line-height: 1.15;
    color: var(--text-primary);
    margin-bottom: 0.25rem;
  }
  .hero-subtitle {
    font-family: var(--font-display);
    font-style: italic;
    font-size: 1.25rem;
    color: var(--accent-amber);
    margin-bottom: 1.5rem;
  }
  .hero-rule {
    border: none;
    border-top: 2px solid var(--accent-red);
    width: 80px;
    margin: 0 0 2rem 0;
  }

  /* ── Section Headers ── */
  .section-tag {
    font-family: var(--font-mono);
    font-size: 0.72rem;
    letter-spacing: 0.18em;
    color: var(--accent-teal);
    text-transform: uppercase;
    margin-bottom: 0.4rem;
  }
  .section-title {
    font-family: var(--font-display);
    font-size: 2rem;
    font-weight: 700;
    color: var(--text-primary);
    margin-bottom: 0.5rem;
  }

  /* ── Narrative Body Text ── */
  .narrative-text {
    font-size: 1.05rem;
    line-height: 1.85;
    color: #cbd5e1;
    max-width: 780px;
    margin-bottom: 1.5rem;
  }

  /* ── Insight Box ── */
  .insight-box {
    background: linear-gradient(135deg, rgba(230,57,70,0.12), rgba(42,157,143,0.08));
    border-left: 4px solid var(--accent-red);
    border-radius: 0 8px 8px 0;
    padding: 1.2rem 1.5rem;
    margin: 1.5rem 0;
  }
  .insight-box .insight-label {
    font-family: var(--font-mono);
    font-size: 0.68rem;
    letter-spacing: 0.15em;
    color: var(--accent-red);
    text-transform: uppercase;
    margin-bottom: 0.4rem;
  }
  .insight-box p {
    font-size: 0.97rem;
    line-height: 1.7;
    color: var(--text-primary);
    margin: 0;
  }

  /* ── Stat Cards ── */
  .stat-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
    gap: 1rem;
    margin: 1.5rem 0;
  }
  .stat-card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 1.2rem 1.4rem;
    text-align: center;
  }
  .stat-card .stat-value {
    font-family: var(--font-mono);
    font-size: 1.9rem;
    font-weight: 700;
    color: var(--accent-amber);
  }
  .stat-card .stat-label {
    font-size: 0.8rem;
    color: var(--text-muted);
    margin-top: 0.3rem;
    letter-spacing: 0.05em;
  }

  /* ── Timeline Marker ── */
  .timeline-item {
    display: flex;
    gap: 1.2rem;
    margin-bottom: 1.2rem;
    align-items: flex-start;
  }
  .timeline-dot {
    width: 14px;
    height: 14px;
    border-radius: 50%;
    background: var(--accent-red);
    margin-top: 4px;
    flex-shrink: 0;
    box-shadow: 0 0 8px rgba(230,57,70,0.6);
  }
  .timeline-content .timeline-date {
    font-family: var(--font-mono);
    font-size: 0.75rem;
    color: var(--accent-teal);
    margin-bottom: 0.2rem;
  }
  .timeline-content p {
    font-size: 0.93rem;
    color: #cbd5e1;
    margin: 0;
    line-height: 1.6;
  }

  /* ── Chapter Divider ── */
  .chapter-divider {
    display: flex;
    align-items: center;
    gap: 1rem;
    margin: 2.5rem 0;
  }
  .chapter-divider .line {
    flex: 1;
    height: 1px;
    background: var(--border);
  }
  .chapter-divider .chapter-num {
    font-family: var(--font-mono);
    font-size: 0.72rem;
    color: var(--text-muted);
    letter-spacing: 0.1em;
  }

  /* ── Streamlit overrides ── */
  h1, h2, h3 { font-family: var(--font-display) !important; }
  .stSelectbox label, .stRadio label { color: var(--text-muted) !important; font-size: 0.85rem !important; }
  div[data-testid="stMetric"] {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 1rem;
  }
  div[data-testid="stMetricValue"] { color: var(--accent-amber) !important; font-family: var(--font-mono) !important; }
  div[data-testid="stMetricLabel"] { color: var(--text-muted) !important; font-size: 0.8rem !important; }
  .stDataFrame { background: var(--bg-card) !important; }
  footer { visibility: hidden; }
  #MainMenu { visibility: hidden; }
</style>
"""
st.markdown(GLOBAL_CSS, unsafe_allow_html=True)


# ─── Data Loading ─────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    """
    Load the COVID-19 dataset from the local CSV file.
    Returns a cleaned, typed DataFrame ready for analysis.
    """
    data_path = Path(__file__).parent / "data" / "covid19_global_data.csv"
    df = pd.read_csv(data_path, parse_dates=["date"])
    df = df.sort_values(["country", "date"]).reset_index(drop=True)

    # Ensure numeric types
    numeric_cols = [
        "total_cases", "new_cases", "total_deaths", "new_deaths",
        "total_recovered", "active_cases", "total_vaccinations",
        "people_vaccinated", "people_fully_vaccinated", "population",
    ]
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    # Derived metrics
    df["mortality_rate"]       = (df["total_deaths"] / df["total_cases"].replace(0, np.nan)) * 100
    df["recovery_rate"]        = (df["total_recovered"] / df["total_cases"].replace(0, np.nan)) * 100
    df["cases_per_million"]    = (df["total_cases"] / df["population"].replace(0, np.nan)) * 1_000_000
    df["deaths_per_million"]   = (df["total_deaths"] / df["population"].replace(0, np.nan)) * 1_000_000
    df["vaccination_rate_pct"] = (df["people_fully_vaccinated"] / df["population"].replace(0, np.nan)) * 100

    return df


# ─── Session State Initialisation ─────────────────────────────────────────────
if "data_loaded" not in st.session_state:
    st.session_state.data_loaded = False

try:
    df = load_data()
    st.session_state.df = df
    st.session_state.data_loaded = True
except FileNotFoundError:
    st.error("⚠️  Dataset not found. Please ensure `data/covid19_global_data.csv` exists.")
    st.stop()


# ─── Sidebar Navigation ────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='text-align:center; padding: 0.5rem 0 1.5rem;'>
      <div style='font-family:"Playfair Display",serif; font-size:1.1rem; color:#f1f5f9; font-weight:700;'>COVID-19</div>
      <div style='font-family:"Playfair Display",serif; font-style:italic; font-size:0.85rem; color:#f4a261;'>A Data Story</div>
    </div>
    <hr style='border-color:rgba(255,255,255,0.08); margin-bottom:1.2rem;'/>
    """, unsafe_allow_html=True)

    CHAPTERS = {
        "🌍  Introduction":          "introduction",
        "🔬  Data Exploration":       "exploration",
        "📈  Global Impact":          "global_impact",
        "🗺️  Country Comparison":    "country_comparison",
        "🎬  Visual Storytelling":    "visual_storytelling",
        "💡  Key Findings":           "key_findings",
        "📋  Recommendations":        "recommendations",
    }

    selected_chapter = st.radio(
        "Navigate the story",
        list(CHAPTERS.keys()),
        label_visibility="collapsed",
    )

    st.markdown("""
    <hr style='border-color:rgba(255,255,255,0.08); margin:1.5rem 0 1rem;'/>
    <div style='font-family:"JetBrains Mono",monospace; font-size:0.68rem; color:#475569; text-align:center; line-height:1.8;'>
      DATA PERIOD<br>
      <span style='color:#94a3b8;'>Jan 2020 — Dec 2023</span><br><br>
      SOURCE<br>
      <span style='color:#94a3b8;'>Simulated · OWID-style</span>
    </div>
    """, unsafe_allow_html=True)

chapter_key = CHAPTERS[selected_chapter]


# ─── Chapter Router ────────────────────────────────────────────────────────────
# Each chapter lives in its own module (pages/) and receives the shared df.
from pages import (
    introduction,
    exploration,
    global_impact,
    country_comparison,
    visual_storytelling,
    key_findings,
    recommendations,
)

CHAPTER_MAP = {
    "introduction":       introduction,
    "exploration":        exploration,
    "global_impact":      global_impact,
    "country_comparison": country_comparison,
    "visual_storytelling":visual_storytelling,
    "key_findings":       key_findings,
    "recommendations":    recommendations,
}

CHAPTER_MAP[chapter_key].render(df)
