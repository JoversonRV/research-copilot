# app/pages/4_Settings.py
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))

import streamlit as st
from dotenv import load_dotenv
from app.utils.styling import apply_styles
from app.utils.session import init_session, clear_chat

load_dotenv(os.path.join(os.path.dirname(__file__), "../../.env"))

st.set_page_config(page_title="Settings | Research Copilot", page_icon="⚙️", layout="wide")
apply_styles()
init_session()

# ── Header ─────────────────────────────────────────────────────────────────
st.markdown("""
<div class="main-header">
    <h1>⚙️ Settings</h1>
    <p>Configure your Research Copilot environment.</p>
</div>
""", unsafe_allow_html=True)

# ── API Keys ───────────────────────────────────────────────────────────────
st.markdown('<div class="section-title">API Keys</div>', unsafe_allow_html=True)

ant_key = os.getenv("ANTHROPIC_API_KEY", "")
voy_key = os.getenv("VOYAGE_API_KEY", "not set")

col1, col2 = st.columns(2)
with col1:
    masked_ant = f"{ant_key[:12]}...{ant_key[-4:]}" if len(ant_key) > 16 else "(not set)"
    st.markdown(f"""
    <div class="paper-card">
        <div class="paper-id">Anthropic</div>
        <div class="paper-title">Claude API Key</div>
        <div class="paper-meta">{masked_ant}</div>
    </div>
    """, unsafe_allow_html=True)
    st.caption("Used for: Chat responses (all strategies)")

with col2:
    masked_voy = f"{voy_key[:8]}..." if len(voy_key) > 8 else "(not set)"
    st.markdown(f"""
    <div class="paper-card">
        <div class="paper-id">Voyage AI</div>
        <div class="paper-title">Embeddings API Key</div>
        <div class="paper-meta">{masked_voy}</div>
    </div>
    """, unsafe_allow_html=True)
    st.caption("Used for: Vector search (ingestion pipeline)")

st.info("To update API keys, edit the `.env` file at `ResearchAssistant/.env`")

# ── Model settings ─────────────────────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)
st.markdown('<div class="section-title">Model Configuration</div>', unsafe_allow_html=True)

col3, col4 = st.columns(2)
with col3:
    model = st.selectbox(
        "Claude Model",
        ["claude-sonnet-4-6", "claude-opus-4-6", "claude-haiku-4-5-20251001"],
        index=0,
        help="claude-sonnet-4-6 is the default — best balance of quality and speed.",
    )
    st.caption("Applied on next query.")

with col4:
    default_strategy = st.selectbox(
        "Default Prompt Strategy",
        ["V1 - Basic", "V2 - Structured JSON", "V3 - Few-Shot", "V4 - Chain of Thought"],
        index=int(["V1 - Basic","V2 - Structured JSON","V3 - Few-Shot","V4 - Chain of Thought"]
                  .index(st.session_state.get("active_strategy","V1 - Basic"))),
    )
    st.session_state.active_strategy = default_strategy

# ── Retrieval settings ─────────────────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)
st.markdown('<div class="section-title">Retrieval Settings</div>', unsafe_allow_html=True)

col5, col6 = st.columns(2)
with col5:
    top_k = st.slider("Default sources per query (top-k)", 1, 5, 3)
    st.caption("Number of papers retrieved as context for each question.")
with col6:
    st.markdown("**Papers Directory**")
    st.code("C:/Users/LENOVO/Documents/Papers/", language=None)
    st.caption("Source folder for PDF ingestion.")

# ── Session management ─────────────────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)
st.markdown('<div class="section-title">Session</div>', unsafe_allow_html=True)

col7, col8 = st.columns(2)
with col7:
    st.metric("Chat messages", len(st.session_state.messages))
    st.metric("Queries logged", len(st.session_state.query_history))
with col8:
    st.metric("Input tokens used",  st.session_state.token_usage["input"])
    st.metric("Output tokens used", st.session_state.token_usage["output"])

st.markdown("<br>", unsafe_allow_html=True)
if st.button("🗑️ Clear all session data", type="secondary"):
    clear_chat()
    st.session_state.query_history = []
    st.session_state.token_usage   = {"input": 0, "output": 0}
    st.success("Session cleared.")
    st.rerun()

# ── About ──────────────────────────────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)
st.markdown('<div class="section-title">About</div>', unsafe_allow_html=True)
st.markdown("""
**Research Copilot** · v1.0

An AI-powered academic research assistant built with:
- **Claude** (Anthropic) — Language model for question answering
- **Voyage AI** — Academic embeddings for semantic search
- **LanceDB** — Vector store for document retrieval
- **Streamlit** — Web interface framework

**Corpus:** 19 political science papers on democratic backsliding, judicial independence, and institutional change.
""")
