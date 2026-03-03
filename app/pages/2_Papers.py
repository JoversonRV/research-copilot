# app/pages/2_Papers.py
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))

import streamlit as st
from app.utils.styling import apply_styles
from app.utils.session import init_session
from app.components.paper_card import render_paper_card
from app.components.citation import format_apa
from src.ingestion.catalog_loader import PaperCatalog

st.set_page_config(page_title="Papers | Research Copilot", page_icon="📄", layout="wide")
apply_styles()
init_session()

CATALOG_PATH = "C:/Users/LENOVO/Documents/Papers/paper_catalog.json"

@st.cache_resource
def load_catalog():
    return PaperCatalog(CATALOG_PATH)

catalog   = load_catalog()
all_papers = catalog.papers

# Derived filter values
all_years   = sorted(set(p["year"] for p in all_papers if p.get("year")))
all_topics  = sorted(set(t for p in all_papers for t in p.get("topics", [])))
all_authors = sorted(set(
    a.split(",")[0].strip()
    for p in all_papers
    for a in (p["authors"] if isinstance(p["authors"], list) else [p["authors"]])
))

# ── Sidebar filters ────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🔍 Filters")
    st.markdown("---")

    search_query = st.text_input("Search", placeholder="Title, author, keyword...")

    year_range = st.slider(
        "Year range",
        min_value=min(all_years),
        max_value=max(all_years),
        value=(min(all_years), max(all_years)),
    )

    selected_topics = st.multiselect("Topics", options=all_topics)
    selected_authors = st.multiselect("Authors (last name)", options=all_authors)

    st.markdown("---")
    show_abstracts = st.toggle("Show abstracts", value=False)

    if st.button("Reset filters", use_container_width=True):
        st.rerun()

# ── Header ─────────────────────────────────────────────────────────────────
st.markdown("""
<div class="main-header">
    <h1>📄 Paper Browser</h1>
    <p>Browse, search, and filter your academic paper collection.</p>
</div>
""", unsafe_allow_html=True)

# ── Apply filters ──────────────────────────────────────────────────────────
filtered = all_papers

# Year filter
filtered = [p for p in filtered if year_range[0] <= (p.get("year") or 0) <= year_range[1]]

# Topic filter
if selected_topics:
    filtered = [
        p for p in filtered
        if any(t in p.get("topics", []) for t in selected_topics)
    ]

# Author filter
if selected_authors:
    filtered = [
        p for p in filtered
        if any(
            a_filter in (a if isinstance(a, str) else "".join(p.get("authors",[])))
            for a_filter in selected_authors
            for a in (p["authors"] if isinstance(p["authors"], list) else [p["authors"]])
        )
    ]

# Search query
if search_query.strip():
    q = search_query.lower()
    filtered = [
        p for p in filtered
        if q in p.get("title", "").lower()
        or q in p.get("abstract", "").lower()
        or q in " ".join(p.get("topics", [])).lower()
        or q in " ".join(p.get("authors", [])).lower()
    ]

# ── Results summary ────────────────────────────────────────────────────────
col_count, col_sort = st.columns([3, 1])
with col_count:
    st.markdown(f"**{len(filtered)}** paper(s) found")
with col_sort:
    sort_by = st.selectbox("Sort by", ["Year (newest)", "Year (oldest)", "Title A-Z"], label_visibility="collapsed")

if sort_by == "Year (newest)":
    filtered = sorted(filtered, key=lambda p: p.get("year", 0), reverse=True)
elif sort_by == "Year (oldest)":
    filtered = sorted(filtered, key=lambda p: p.get("year", 0))
elif sort_by == "Title A-Z":
    filtered = sorted(filtered, key=lambda p: p.get("title", ""))

st.markdown("---")

# ── Paper list ─────────────────────────────────────────────────────────────
if not filtered:
    st.warning("No papers match your current filters. Try adjusting the search or filters.")
else:
    for paper in filtered:
        render_paper_card(paper)

        if show_abstracts:
            with st.expander(f"Abstract — {paper['title'][:60]}...", expanded=False):
                st.markdown(paper.get("abstract", "No abstract available."))
                st.markdown("---")
                st.caption(f"**APA:** {format_apa(paper)}")
                if paper.get("doi"):
                    st.caption(f"**DOI:** https://doi.org/{paper['doi']}")
