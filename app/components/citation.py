# app/components/citation.py
import streamlit as st


def format_apa(paper: dict) -> str:
    """Generate APA 7th edition citation string."""
    authors = paper.get("authors", "Unknown")
    if isinstance(authors, list):
        if len(authors) == 1:
            authors_str = authors[0]
        elif len(authors) == 2:
            authors_str = f"{authors[0]}, & {authors[1]}"
        else:
            authors_str = ", ".join(authors[:-1]) + f", & {authors[-1]}"
    else:
        authors_str = authors

    year   = paper.get("year", "n.d.")
    title  = paper.get("title", "Untitled")
    venue  = paper.get("venue", "")
    doi    = paper.get("doi", "")

    apa = f"{authors_str} ({year}). {title}."
    if venue:
        apa += f" *{venue}*."
    if doi:
        apa += f" https://doi.org/{doi}"
    return apa


def render_citations(papers: list, quotes: list = None):
    """Render a list of cited papers as styled citation blocks."""
    if not papers:
        return

    st.markdown("**Sources**")
    for i, paper in enumerate(papers):
        quote = quotes[i] if quotes and i < len(quotes) else None
        apa   = format_apa(paper)

        html = '<div class="citation-block">'
        if quote:
            html += f'<div class="quote">"{quote}"</div>'
        html += f'<div class="apa">{apa}</div>'
        html += '</div>'
        st.markdown(html, unsafe_allow_html=True)


def render_inline_badge(paper: dict) -> str:
    """Return a short inline reference string, e.g. (Gerschewski, 2020)."""
    authors = paper.get("authors", ["Unknown"])
    if isinstance(authors, list) and authors:
        last_name = authors[0].split(",")[0]
    else:
        last_name = str(authors).split(",")[0]
    year = paper.get("year", "n.d.")
    return f"({last_name}, {year})"
