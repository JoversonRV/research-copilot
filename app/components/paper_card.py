# app/components/paper_card.py
import streamlit as st
from app.components.citation import format_apa


def render_paper_card(paper: dict, expanded: bool = False):
    """Render a paper as a styled card with optional abstract expansion."""
    topics  = paper.get("topics", [])
    authors = paper.get("authors", [])
    authors_str = "; ".join(authors) if isinstance(authors, list) else authors

    topic_tags = "".join(
        f'<span class="topic-tag">{t}</span>' for t in topics[:5]
    )

    card_html = f"""
    <div class="paper-card">
        <div class="paper-id">{paper.get('id','').upper()}</div>
        <div class="paper-title">{paper.get('title','Untitled')}</div>
        <div class="paper-meta">
            {authors_str} &nbsp;·&nbsp;
            {paper.get('year','n.d.')} &nbsp;·&nbsp;
            <em>{paper.get('venue','')}</em>
        </div>
        <div>{topic_tags}</div>
    </div>
    """
    st.markdown(card_html, unsafe_allow_html=True)

    if expanded:
        abstract = paper.get("abstract", "No abstract available.")
        with st.expander("Abstract & Citation", expanded=True):
            st.markdown(abstract)
            st.markdown("---")
            st.caption(f"**APA Citation:** {format_apa(paper)}")
            if paper.get("doi"):
                st.caption(f"**DOI:** https://doi.org/{paper['doi']}")


def render_paper_list(papers: list, show_abstracts: bool = False):
    """Render a list of paper cards."""
    if not papers:
        st.info("No papers match your current filters.")
        return
    for paper in papers:
        render_paper_card(paper, expanded=show_abstracts)
