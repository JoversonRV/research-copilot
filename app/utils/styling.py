# app/utils/styling.py
import streamlit as st


ACADEMIC_CSS = """
<style>
/* ── Fonts & Base ─────────────────────────────────────────────── */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Merriweather:wght@400;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

/* ── Color Palette ────────────────────────────────────────────── */
:root {
    --navy:      #0D1B2A;
    --blue:      #1B4F8C;
    --lightblue: #4A90D9;
    --gold:      #C9A84C;
    --cream:     #F8F6F1;
    --bg:        #F2F4F8;
    --card:      #FFFFFF;
    --border:    #D9E0EA;
    --text:      #1A1A2A;
    --muted:     #6B7280;
    --success:   #28A745;
    --warning:   #FFC107;
}

/* ── Sidebar ──────────────────────────────────────────────────── */
[data-testid="stSidebar"] {
    background-color: var(--navy) !important;
}
[data-testid="stSidebar"] * {
    color: #E8EDF2 !important;
}
[data-testid="stSidebar"] .stMarkdown a {
    color: var(--lightblue) !important;
}

/* ── Main header ──────────────────────────────────────────────── */
.main-header {
    background: linear-gradient(135deg, var(--navy) 0%, var(--blue) 100%);
    color: white;
    padding: 2rem 2.5rem;
    border-radius: 12px;
    margin-bottom: 1.5rem;
}
.main-header h1 {
    font-family: 'Merriweather', serif;
    font-size: 2rem;
    margin: 0;
    font-weight: 700;
}
.main-header p {
    margin: 0.5rem 0 0;
    opacity: 0.85;
    font-size: 1rem;
}

/* ── Metric cards ─────────────────────────────────────────────── */
.metric-card {
    background: var(--card);
    border: 1px solid var(--border);
    border-top: 4px solid var(--lightblue);
    border-radius: 8px;
    padding: 1.25rem;
    text-align: center;
}
.metric-card .value {
    font-size: 2.2rem;
    font-weight: 700;
    color: var(--blue);
}
.metric-card .label {
    font-size: 0.85rem;
    color: var(--muted);
    margin-top: 0.25rem;
}

/* ── Chat bubbles ─────────────────────────────────────────────── */
.user-bubble {
    background: var(--blue);
    color: white;
    padding: 0.85rem 1.15rem;
    border-radius: 18px 18px 4px 18px;
    margin: 0.5rem 0 0.5rem 20%;
    font-size: 0.95rem;
    line-height: 1.5;
}
.assistant-bubble {
    background: var(--card);
    border: 1px solid var(--border);
    padding: 0.85rem 1.15rem;
    border-radius: 18px 18px 18px 4px;
    margin: 0.5rem 20% 0.5rem 0;
    font-size: 0.95rem;
    line-height: 1.6;
}
.assistant-bubble .bot-label {
    font-size: 0.75rem;
    font-weight: 600;
    color: var(--lightblue);
    margin-bottom: 0.4rem;
    letter-spacing: 0.05em;
    text-transform: uppercase;
}

/* ── Citation block ───────────────────────────────────────────── */
.citation-block {
    background: #EEF4FB;
    border-left: 4px solid var(--lightblue);
    padding: 0.75rem 1rem;
    border-radius: 0 8px 8px 0;
    margin: 0.4rem 0;
    font-size: 0.875rem;
    color: var(--text);
}
.citation-block .quote {
    font-style: italic;
    color: #374151;
    margin-bottom: 0.35rem;
}
.citation-block .apa {
    font-size: 0.8rem;
    color: var(--muted);
}

/* ── Paper card ───────────────────────────────────────────────── */
.paper-card {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 1.25rem;
    margin-bottom: 0.75rem;
    transition: box-shadow 0.2s;
}
.paper-card:hover {
    box-shadow: 0 4px 16px rgba(27,79,140,0.12);
    border-color: var(--lightblue);
}
.paper-card .paper-id {
    font-size: 0.72rem;
    font-weight: 600;
    color: var(--lightblue);
    text-transform: uppercase;
    letter-spacing: 0.08em;
}
.paper-card .paper-title {
    font-family: 'Merriweather', serif;
    font-size: 1rem;
    font-weight: 700;
    color: var(--navy);
    margin: 0.3rem 0;
    line-height: 1.4;
}
.paper-card .paper-meta {
    font-size: 0.82rem;
    color: var(--muted);
    margin-bottom: 0.5rem;
}
.topic-tag {
    display: inline-block;
    background: #EEF4FB;
    color: var(--blue);
    border: 1px solid #C3D9F5;
    border-radius: 20px;
    padding: 0.15rem 0.6rem;
    font-size: 0.75rem;
    margin: 0.15rem 0.15rem 0.15rem 0;
    font-weight: 500;
}

/* ── Section title ────────────────────────────────────────────── */
.section-title {
    font-family: 'Merriweather', serif;
    font-size: 1.4rem;
    color: var(--navy);
    border-bottom: 2px solid var(--lightblue);
    padding-bottom: 0.4rem;
    margin-bottom: 1rem;
}

/* ── Confidence badge ─────────────────────────────────────────── */
.badge-high   { background: #D4EDDA; color: #155724; padding: 2px 10px; border-radius: 20px; font-size: 0.78rem; font-weight: 600; }
.badge-medium { background: #FFF3CD; color: #856404; padding: 2px 10px; border-radius: 20px; font-size: 0.78rem; font-weight: 600; }
.badge-low    { background: #F8D7DA; color: #721C24; padding: 2px 10px; border-radius: 20px; font-size: 0.78rem; font-weight: 600; }
</style>
"""


def apply_styles():
    st.markdown(ACADEMIC_CSS, unsafe_allow_html=True)
