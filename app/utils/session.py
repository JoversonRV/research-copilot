# app/utils/session.py
import streamlit as st
from datetime import datetime


def init_session():
    """Initialize all session state variables."""
    defaults = {
        "messages":        [],       # chat history [{role, content, citations, strategy}]
        "query_history":   [],       # [{question, timestamp, strategy, n_sources}]
        "token_usage":     {"input": 0, "output": 0},
        "active_strategy": "V1 - Basic",
        "active_filters":  {"year_min": 2009, "year_max": 2025, "topics": [], "authors": []},
        "selected_paper":  None,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def add_message(role: str, content: str, citations: list = None, strategy: str = None):
    """Add a message to the chat history."""
    st.session_state.messages.append({
        "role":      role,
        "content":   content,
        "citations": citations or [],
        "strategy":  strategy,
        "timestamp": datetime.now().strftime("%H:%M"),
    })


def clear_chat():
    """Clear all chat messages."""
    st.session_state.messages = []


def log_query(question: str, strategy: str, n_sources: int, tokens_in: int = 0, tokens_out: int = 0):
    """Record a query in history and update token usage."""
    st.session_state.query_history.append({
        "question":  question,
        "strategy":  strategy,
        "n_sources": n_sources,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
    })
    st.session_state.token_usage["input"]  += tokens_in
    st.session_state.token_usage["output"] += tokens_out
