# app/pages/1_Chat.py
import sys, os, json, re
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))

import streamlit as st
import anthropic
from dotenv import load_dotenv

from app.utils.styling import apply_styles
from app.utils.session import init_session, add_message, clear_chat, log_query
from app.components.chat_message import render_user_message, render_assistant_message, render_typing_indicator
from app.components.citation import render_citations, format_apa
from src.ingestion.catalog_loader import PaperCatalog
from src.rag.prompts import PromptStrategy, build_prompt

load_dotenv(os.path.join(os.path.dirname(__file__), "../../.env"))

st.set_page_config(page_title="Chat | Research Copilot", page_icon="💬", layout="wide")
apply_styles()
init_session()

CATALOG_PATH = "C:/Users/LENOVO/Documents/Papers/paper_catalog.json"
CLAUDE_MODEL = "claude-sonnet-4-6"

STRATEGY_OPTIONS = {
    "V1 - Basic":           PromptStrategy.V1_BASIC,
    "V2 - Structured JSON": PromptStrategy.V2_STRUCTURED,
    "V3 - Few-Shot":        PromptStrategy.V3_FEW_SHOT,
    "V4 - Chain of Thought":PromptStrategy.V4_CHAIN,
}

@st.cache_resource
def load_catalog():
    return PaperCatalog(CATALOG_PATH)

catalog = load_catalog()


# ── Retrieval ──────────────────────────────────────────────────────────────

def retrieve_papers(question: str, top_k: int = 3) -> list[dict]:
    """Keyword-based retrieval from catalog (upgradeable to vector search)."""
    q_words = {w for w in question.lower().split() if len(w) > 3}
    scored  = []
    for paper in catalog.papers:
        haystack = (
            paper["title"] + " " +
            paper.get("abstract", "") + " " +
            " ".join(paper.get("topics", []))
        ).lower()
        score = sum(1 for w in q_words if w in haystack)
        if score > 0:
            scored.append((score, paper))
    scored.sort(key=lambda x: x[0], reverse=True)
    return [p for _, p in scored[:top_k]]


def build_context(papers: list[dict]) -> str:
    parts = []
    for p in papers:
        authors = "; ".join(p["authors"]) if isinstance(p["authors"], list) else p["authors"]
        parts.append(
            f"[{p['id'].upper()}] {p['title']}\n"
            f"Authors: {authors} ({p['year']})\n"
            f"Venue: {p.get('venue','')}\n"
            f"Abstract: {p.get('abstract','')}\n"
            f"Topics: {', '.join(p.get('topics',[]))}"
        )
    return "\n\n---\n\n".join(parts)


# ── Claude call ────────────────────────────────────────────────────────────

def call_claude(prompt: str) -> tuple[str, int, int]:
    """Returns (response_text, input_tokens, output_tokens)."""
    client  = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
    message = client.messages.create(
        model=CLAUDE_MODEL,
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}],
    )
    raw         = message.content[0].text
    tokens_in   = message.usage.input_tokens
    tokens_out  = message.usage.output_tokens
    return raw, tokens_in, tokens_out


def parse_response(raw: str, strategy: PromptStrategy) -> tuple[str, list, str]:
    """
    Returns (display_text, citations_list, confidence).
    citations_list items are dicts with keys: paper, authors, year, quote.
    """
    if strategy == PromptStrategy.V2_STRUCTURED:
        try:
            match = re.search(r'\{.*\}', raw, re.DOTALL)
            if match:
                data = json.loads(match.group())
                return data.get("answer", raw), data.get("citations", []), data.get("confidence", "medium")
        except Exception:
            pass

    if strategy == PromptStrategy.V4_CHAIN:
        if "FINAL ANSWER:" in raw:
            return raw.split("FINAL ANSWER:", 1)[1].strip(), [], "high"

    return raw, [], "medium"


# ── Sidebar ────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 💬 Chat Settings")
    st.markdown("---")

    strategy_label = st.selectbox(
        "Prompt Strategy",
        options=list(STRATEGY_OPTIONS.keys()),
        index=0,
        help="Select how Claude reasons about your question.",
    )
    st.session_state.active_strategy = strategy_label

    top_k = st.slider("Sources to retrieve", min_value=1, max_value=5, value=3)

    st.markdown("---")
    if st.button("🗑️ Clear conversation", use_container_width=True):
        clear_chat()
        st.rerun()

    st.markdown("---")
    st.caption(f"**{len(st.session_state.messages)//2}** exchanges this session")
    st.caption(f"**{len(st.session_state.query_history)}** total queries")

# ── Header ─────────────────────────────────────────────────────────────────
st.markdown("""
<div class="main-header">
    <h1>💬 Research Chat</h1>
    <p>Ask questions about your 19 academic papers and get cited answers.</p>
</div>
""", unsafe_allow_html=True)

# ── Chat history ───────────────────────────────────────────────────────────
chat_container = st.container()

with chat_container:
    if not st.session_state.messages:
        st.markdown("""
        <div style="text-align:center;padding:3rem;color:#9CA3AF">
            <div style="font-size:3rem">📚</div>
            <div style="font-size:1.1rem;margin-top:0.5rem">Start a conversation about your papers</div>
            <div style="font-size:0.9rem;margin-top:0.3rem">
                Try: <em>"What is democratic backsliding?"</em> or
                <em>"How do courts resist authoritarian pressure?"</em>
            </div>
        </div>
        """, unsafe_allow_html=True)

    for msg in st.session_state.messages:
        if msg["role"] == "user":
            render_user_message(msg["content"], msg.get("timestamp", ""))
        else:
            render_assistant_message(msg["content"], msg.get("timestamp", ""))
            if msg.get("citations"):
                with st.expander(f"📎 {len(msg['citations'])} source(s)", expanded=False):
                    for cit in msg["citations"]:
                        quote   = cit.get("quote", "")
                        paper_info = {
                            "title":   cit.get("paper", ""),
                            "authors": cit.get("authors", ""),
                            "year":    cit.get("year", ""),
                            "doi":     "",
                        }
                        html = '<div class="citation-block">'
                        if quote:
                            html += f'<div class="quote">"{quote}"</div>'
                        html += f'<div class="apa">{format_apa(paper_info)}</div></div>'
                        st.markdown(html, unsafe_allow_html=True)

# ── Input ──────────────────────────────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)
with st.form("chat_form", clear_on_submit=True):
    col_input, col_btn = st.columns([5, 1])
    with col_input:
        user_input = st.text_input(
            "Your question",
            placeholder="Ask something about the papers...",
            label_visibility="collapsed",
        )
    with col_btn:
        submitted = st.form_submit_button("Send", use_container_width=True)

# ── Process query ──────────────────────────────────────────────────────────
if submitted and user_input.strip():
    strategy = STRATEGY_OPTIONS[strategy_label]
    add_message("user", user_input)

    with st.spinner("Searching papers and generating answer..."):
        papers  = retrieve_papers(user_input, top_k=top_k)
        context = build_context(papers)
        prompt  = build_prompt(strategy, context, user_input)

        try:
            raw, tok_in, tok_out = call_claude(prompt)
            answer, citations, confidence = parse_response(raw, strategy)

            # Confidence badge
            badge_class = f"badge-{confidence}"
            answer_with_badge = (
                f'<span class="{badge_class}">{confidence.upper()}</span><br><br>' + answer
            )

            add_message("assistant", answer_with_badge, citations=citations, strategy=strategy_label)
            log_query(user_input, strategy_label, len(papers), tok_in, tok_out)

        except Exception as e:
            add_message("assistant", f"Error calling Claude: {e}")

    st.rerun()
