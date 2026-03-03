# app/main.py
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import streamlit as st
from app.utils.styling import apply_styles
from app.utils.session import init_session
from src.ingestion.catalog_loader import PaperCatalog

# ── Page config ────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Research Copilot",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded",
)

apply_styles()
init_session()

CATALOG_PATH = "C:/Users/LENOVO/Documents/Papers/paper_catalog.json"

@st.cache_resource
def load_catalog():
    return PaperCatalog(CATALOG_PATH)

catalog = load_catalog()
all_papers = catalog.papers

# ── Sidebar ────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 📚 Research Copilot")
    st.markdown("---")
    st.markdown("**Navigate**")
    st.page_link("main.py",             label="🏠 Home")
    st.page_link("pages/1_Chat.py",     label="💬 Chat")
    st.page_link("pages/2_Papers.py",   label="📄 Papers")
    st.page_link("pages/3_Analytics.py",label="📊 Analytics")
    st.page_link("pages/4_Settings.py", label="⚙️ Settings")
    st.markdown("---")
    st.caption(f"**{len(all_papers)} papers** indexed")
    st.caption(f"**{st.session_state.token_usage['input'] + st.session_state.token_usage['output']:,}** tokens used")

# ── Header ─────────────────────────────────────────────────────────────────
st.markdown("""
<div class="main-header">
    <h1>📚 Research Copilot</h1>
    <p>AI-powered assistant for political science academic research</p>
</div>
""", unsafe_allow_html=True)

# ── Metrics row ────────────────────────────────────────────────────────────
c1, c2, c3, c4 = st.columns(4)

all_topics  = [t for p in all_papers for t in p.get("topics", [])]
unique_topics = len(set(all_topics))
years = sorted(set(p["year"] for p in all_papers if p.get("year")))

with c1:
    st.markdown('<div class="metric-card"><div class="value">19</div><div class="label">Academic Papers</div></div>', unsafe_allow_html=True)
with c2:
    st.markdown(f'<div class="metric-card"><div class="value">{unique_topics}</div><div class="label">Unique Topics</div></div>', unsafe_allow_html=True)
with c3:
    st.markdown(f'<div class="metric-card"><div class="value">{len(years)}</div><div class="label">Years Covered</div></div>', unsafe_allow_html=True)
with c4:
    n_queries = len(st.session_state.query_history)
    st.markdown(f'<div class="metric-card"><div class="value">{n_queries}</div><div class="label">Queries Today</div></div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── Navigation cards ───────────────────────────────────────────────────────
st.markdown('<div class="section-title">Sections</div>', unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.info("**💬 Chat**\n\nAsk questions about the papers. Get answers with APA citations and confidence scores.")
with col2:
    st.info("**📄 Papers**\n\nBrowse all 19 papers. Search by title, author, or topic. View abstracts.")
with col3:
    st.info("**📊 Analytics**\n\nVisualizations: papers by year, topic distribution, query history.")
with col4:
    st.info("**⚙️ Settings**\n\nConfigure the model, prompt strategy, and API keys.")

# ── Recent queries ─────────────────────────────────────────────────────────
if st.session_state.query_history:
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="section-title">Recent Queries</div>', unsafe_allow_html=True)
    for q in reversed(st.session_state.query_history[-5:]):
        st.markdown(
            f'<div style="padding:0.5rem 0.75rem;border-left:3px solid #4A90D9;margin-bottom:0.4rem;font-size:0.9rem">'
            f'<strong>{q["timestamp"]}</strong> &nbsp;·&nbsp; {q["strategy"]} &nbsp;·&nbsp; {q["question"][:80]}...'
            f'</div>',
            unsafe_allow_html=True,
        )
