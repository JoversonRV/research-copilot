# app/components/chat_message.py
import streamlit as st


def render_user_message(text: str, timestamp: str = ""):
    st.markdown(
        f'<div class="user-bubble">{text}'
        f'<div style="font-size:0.7rem;opacity:0.7;text-align:right;margin-top:4px">{timestamp}</div>'
        f'</div>',
        unsafe_allow_html=True,
    )


def render_assistant_message(text: str, timestamp: str = ""):
    st.markdown(
        f'<div class="assistant-bubble">'
        f'<div class="bot-label">Research Copilot</div>'
        f'{text}'
        f'<div style="font-size:0.7rem;color:#9CA3AF;text-align:right;margin-top:6px">{timestamp}</div>'
        f'</div>',
        unsafe_allow_html=True,
    )


def render_typing_indicator():
    st.markdown(
        '<div class="assistant-bubble" style="width:70px">'
        '<div class="bot-label">Research Copilot</div>'
        '<span style="letter-spacing:4px;font-size:1.2rem">...</span>'
        '</div>',
        unsafe_allow_html=True,
    )
