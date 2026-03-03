# app/pages/3_Analytics.py
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))

import streamlit as st
import pandas as pd
import altair as alt
from collections import Counter

from app.utils.styling import apply_styles
from app.utils.session import init_session
from src.ingestion.catalog_loader import PaperCatalog

st.set_page_config(page_title="Analytics | Research Copilot", page_icon="📊", layout="wide")
apply_styles()
init_session()

CATALOG_PATH = "C:/Users/LENOVO/Documents/Papers/paper_catalog.json"

@st.cache_resource
def load_catalog():
    return PaperCatalog(CATALOG_PATH)

catalog    = load_catalog()
all_papers = catalog.papers

# ── Header ─────────────────────────────────────────────────────────────────
st.markdown("""
<div class="main-header">
    <h1>📊 Analytics Dashboard</h1>
    <p>Visualize your paper collection and session statistics.</p>
</div>
""", unsafe_allow_html=True)

# ── Top metrics ────────────────────────────────────────────────────────────
all_topics = [t for p in all_papers for t in p.get("topics", [])]
all_years  = [p["year"] for p in all_papers if p.get("year")]
tok_in     = st.session_state.token_usage["input"]
tok_out    = st.session_state.token_usage["output"]

c1, c2, c3, c4 = st.columns(4)
with c1:
    st.markdown(f'<div class="metric-card"><div class="value">{len(all_papers)}</div><div class="label">Papers</div></div>', unsafe_allow_html=True)
with c2:
    st.markdown(f'<div class="metric-card"><div class="value">{len(set(all_topics))}</div><div class="label">Unique Topics</div></div>', unsafe_allow_html=True)
with c3:
    st.markdown(f'<div class="metric-card"><div class="value">{len(st.session_state.query_history)}</div><div class="label">Queries This Session</div></div>', unsafe_allow_html=True)
with c4:
    st.markdown(f'<div class="metric-card"><div class="value">{tok_in + tok_out:,}</div><div class="label">Tokens Used</div></div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── Row 1: Papers by year + Venue distribution ─────────────────────────────
col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="section-title">Papers by Year</div>', unsafe_allow_html=True)
    year_counts = Counter(all_years)
    df_years = pd.DataFrame(
        sorted(year_counts.items()), columns=["Year", "Count"]
    )
    chart = (
        alt.Chart(df_years)
        .mark_bar(color="#1B4F8C", cornerRadiusTopLeft=4, cornerRadiusTopRight=4)
        .encode(
            x=alt.X("Year:O", axis=alt.Axis(labelAngle=0)),
            y=alt.Y("Count:Q", axis=alt.Axis(tickMinStep=1)),
            tooltip=["Year", "Count"],
        )
        .properties(height=260)
    )
    st.altair_chart(chart, use_container_width=True)

with col2:
    st.markdown('<div class="section-title">Papers by Venue Type</div>', unsafe_allow_html=True)
    venue_types = []
    for p in all_papers:
        v = p.get("venue", "").lower()
        if "cambridge" in v or "oxford" in v or "chapter" in v or "book" in v or "handbook" in v:
            venue_types.append("Book Chapter")
        elif "working" in v or "wp" in v:
            venue_types.append("Working Paper")
        else:
            venue_types.append("Journal Article")
    venue_counts = Counter(venue_types)
    df_venues = pd.DataFrame(
        list(venue_counts.items()), columns=["Type", "Count"]
    )
    pie = (
        alt.Chart(df_venues)
        .mark_arc(innerRadius=50)
        .encode(
            theta=alt.Theta("Count:Q"),
            color=alt.Color("Type:N", scale=alt.Scale(
                domain=["Journal Article", "Book Chapter", "Working Paper"],
                range=["#1B4F8C", "#4A90D9", "#C9A84C"]
            )),
            tooltip=["Type", "Count"],
        )
        .properties(height=260)
    )
    st.altair_chart(pie, use_container_width=True)

# ── Row 2: Top topics ──────────────────────────────────────────────────────
st.markdown('<div class="section-title">Top 15 Topics</div>', unsafe_allow_html=True)
topic_counts = Counter(all_topics).most_common(15)
df_topics = pd.DataFrame(topic_counts, columns=["Topic", "Count"])

bars = (
    alt.Chart(df_topics)
    .mark_bar(color="#4A90D9", cornerRadiusTopRight=4, cornerRadiusBottomRight=4)
    .encode(
        y=alt.Y("Topic:N", sort="-x", axis=alt.Axis(labelLimit=250)),
        x=alt.X("Count:Q", axis=alt.Axis(tickMinStep=1)),
        tooltip=["Topic", "Count"],
    )
    .properties(height=380)
)
st.altair_chart(bars, use_container_width=True)

# ── Row 3: Token usage + Query history ────────────────────────────────────
col3, col4 = st.columns(2)

with col3:
    st.markdown('<div class="section-title">Token Usage</div>', unsafe_allow_html=True)
    if tok_in + tok_out == 0:
        st.info("No tokens used yet. Start chatting!")
    else:
        df_tok = pd.DataFrame(
            [{"Type": "Input", "Tokens": tok_in}, {"Type": "Output", "Tokens": tok_out}]
        )
        tok_chart = (
            alt.Chart(df_tok)
            .mark_bar(cornerRadiusTopLeft=4, cornerRadiusTopRight=4)
            .encode(
                x=alt.X("Type:N", axis=alt.Axis(labelAngle=0)),
                y=alt.Y("Tokens:Q"),
                color=alt.Color("Type:N", scale=alt.Scale(
                    domain=["Input", "Output"],
                    range=["#1B4F8C", "#C9A84C"]
                )),
                tooltip=["Type", "Tokens"],
            )
            .properties(height=220)
        )
        st.altair_chart(tok_chart, use_container_width=True)

with col4:
    st.markdown('<div class="section-title">Query History</div>', unsafe_allow_html=True)
    history = st.session_state.query_history
    if not history:
        st.info("No queries yet. Ask a question in the Chat page!")
    else:
        for i, q in enumerate(reversed(history[-8:])):
            st.markdown(
                f'<div style="padding:0.4rem 0.75rem;border-left:3px solid #4A90D9;'
                f'margin-bottom:0.35rem;font-size:0.85rem;background:#F8FAFC;border-radius:0 4px 4px 0">'
                f'<strong>{q["timestamp"]}</strong> · {q["strategy"]}<br>'
                f'<span style="color:#374151">{q["question"][:70]}{"..." if len(q["question"])>70 else ""}</span>'
                f'</div>',
                unsafe_allow_html=True,
            )
