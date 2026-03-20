import uuid

import markdown as md_lib
import requests
import streamlit as st
from datetime import datetime


def render_ai_assistant():

    # ── Page config ──────────────────────────────────────────────────────────────
    st.set_page_config(
        page_title="Ask Intelligence · EquiStat AI",
        page_icon="🟣",
        layout="centered",
    )

    # ── Custom CSS ────────────────────────────────────────────────────────────────
    st.markdown(
        """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:ital,opsz,wght@0,9..40,300;0,9..40,400;0,9..40,500;0,9..40,600;1,9..40,300&family=DM+Mono:wght@400;500&display=swap');

    /* ── Reset & base ── */
    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

    html, body, [data-testid="stAppViewContainer"], [data-testid="stApp"] {
        background: #f0f2f8 !important;
        font-family: 'DM Sans', sans-serif;
    }

    /* Hide Streamlit chrome */
    #MainMenu, header, footer,
    [data-testid="stToolbar"],
    [data-testid="stDecoration"],
    [data-testid="stStatusWidget"] { display: none !important; }

    [data-testid="stAppViewContainer"] > .main { padding: 0 !important; }
    .block-container { padding: 0 !important; max-width: 100% !important; }

    /* ── Outer wrapper – centres the card ── */
    .chat-page {
        min-height: 100vh;
        display: flex;
        align-items: center;
        justify-content: center;
        padding: 2rem 1rem;
        background: #eef0f7;
    }

    /* ── Chat card ── */
    .chat-card {
        width: 100%;
        max-width: 480px;
        background: #ffffff;
        border-radius: 24px;
        box-shadow: 0 8px 40px rgba(80, 60, 180, 0.10), 0 1px 4px rgba(0,0,0,0.06);
        display: flex;
        flex-direction: column;
        overflow: hidden;
        min-height: 640px;
    }

    /* ── Header ── */
    .chat-header {
        display: flex;
        align-items: center;
        gap: 12px;
        padding: 18px 22px 16px;
        border-bottom: 1px solid #f0f0f6;
        background: #fff;
    }

    .avatar-ring {
        width: 46px; height: 46px;
        border-radius: 14px;
        background: linear-gradient(135deg, #7c5cfc 0%, #5b8af5 100%);
        display: flex; align-items: center; justify-content: center;
        font-size: 22px;
        flex-shrink: 0;
        box-shadow: 0 3px 12px rgba(124,92,252,0.30);
    }

    .header-text { flex: 1; }
    .header-title {
        font-size: 15px; font-weight: 600; color: #1a1a2e;
        letter-spacing: -0.01em;
    }
    .header-sub {
        font-size: 12px; color: #888;
        font-weight: 400; margin-top: 1px;
    }

    .online-badge {
        display: flex; align-items: center; gap: 5px;
        font-size: 12px; font-weight: 500; color: #22c55e;
    }
    .online-dot {
        width: 8px; height: 8px; border-radius: 50%;
        background: #22c55e;
        box-shadow: 0 0 0 2px rgba(34,197,94,0.20);
        animation: pulse 2s ease-in-out infinite;
    }
    @keyframes pulse {
        0%, 100% { box-shadow: 0 0 0 2px rgba(34,197,94,0.20); }
        50%       { box-shadow: 0 0 0 5px rgba(34,197,94,0.10); }
    }

    /* ── Messages area ── */
    .messages-area {
        flex: 1;
        padding: 24px 20px 16px;
        display: flex;
        flex-direction: column;
        gap: 16px;
        overflow-y: auto;
        background: #f8f9fd;
    }

    /* ── Single message ── */
    .msg-row { display: flex; align-items: flex-end; gap: 10px; }
    .msg-row.user { flex-direction: row-reverse; }

    .msg-avatar {
        width: 32px; height: 32px; border-radius: 10px; flex-shrink: 0;
        background: linear-gradient(135deg, #7c5cfc 0%, #5b8af5 100%);
        display: flex; align-items: center; justify-content: center;
        font-size: 15px;
        box-shadow: 0 2px 8px rgba(124,92,252,0.20);
    }

    .msg-bubble {
        max-width: 78%;
        padding: 13px 16px;
        border-radius: 18px;
        font-size: 14px; line-height: 1.55;
        color: #2a2a3d;
        position: relative;
    }

    .msg-bubble.bot {
        background: #fff;
        border-bottom-left-radius: 5px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.06);
    }

    .msg-bubble.user {
        background: linear-gradient(135deg, #7c5cfc 0%, #6370f5 100%);
        color: #fff;
        border-bottom-right-radius: 5px;
        box-shadow: 0 3px 14px rgba(124,92,252,0.28);
    }

    .msg-time {
        font-size: 10px; color: #bbb;
        margin-top: 5px;
        padding: 0 4px;
        font-family: 'DM Mono', monospace;
    }
    .msg-row.user .msg-time { text-align: right; }

    .msg-col { display: flex; flex-direction: column; }
    .msg-row.user .msg-col { align-items: flex-end; }

    /* ── Quick-reply chips ── */
    .chips-wrapper {
        padding: 0 20px 14px;
        background: #f8f9fd;
        display: flex;
        gap: 8px;
        overflow-x: auto;
        scrollbar-width: none;
    }
    .chips-wrapper::-webkit-scrollbar { display: none; }

    .chip {
        display: inline-flex; align-items: center;
        padding: 7px 13px;
        border-radius: 20px;
        background: #fff;
        border: 1.5px solid #e8e4fd;
        font-size: 12px; font-weight: 500;
        color: #6b5cf6;
        white-space: nowrap;
        cursor: pointer;
        transition: background 0.15s, border-color 0.15s, transform 0.1s;
        box-shadow: 0 1px 4px rgba(0,0,0,0.05);
    }
    .chip:hover {
        background: #f3f0ff;
        border-color: #c4b5fd;
        transform: translateY(-1px);
    }

    /* ── Input bar ── */
    .input-bar {
        display: flex;
        align-items: center;
        gap: 10px;
        padding: 14px 18px 18px;
        background: #fff;
        border-top: 1px solid #f0f0f6;
    }

    .input-field {
        flex: 1;
        padding: 11px 16px;
        border-radius: 22px;
        border: 1.5px solid #e8e4fd;
        background: #f8f9fd;
        font-family: 'DM Sans', sans-serif;
        font-size: 14px;
        color: #2a2a3d;
        outline: none;
        transition: border-color 0.2s;
    }
    .input-field:focus { border-color: #7c5cfc; }
    .input-field::placeholder { color: #b0aec8; }

    .send-btn {
        width: 42px; height: 42px;
        border-radius: 50%;
        background: linear-gradient(135deg, #7c5cfc 0%, #6370f5 100%);
        border: none; cursor: pointer;
        display: flex; align-items: center; justify-content: center;
        box-shadow: 0 3px 12px rgba(124,92,252,0.35);
        transition: transform 0.15s, box-shadow 0.15s;
        flex-shrink: 0;
    }
    .send-btn:hover {
        transform: scale(1.07);
        box-shadow: 0 5px 18px rgba(124,92,252,0.45);
    }
    .send-btn svg { width: 18px; height: 18px; fill: #fff; }

    /* ── Typing indicator ── */
    .typing { display: flex; align-items: center; gap: 4px; padding: 4px 2px; }
    .typing span {
        width: 7px; height: 7px; border-radius: 50%;
        background: #c4b5fd;
        animation: bounce 1.2s ease-in-out infinite;
    }
    .typing span:nth-child(2) { animation-delay: 0.15s; }
    .typing span:nth-child(3) { animation-delay: 0.30s; }
    @keyframes bounce {
        0%, 80%, 100% { transform: translateY(0); }
        40%           { transform: translateY(-5px); }
    }

    /* ── Markdown inside bot bubbles ── */
    .msg-bubble.bot p { margin: 0 0 8px; }
    .msg-bubble.bot p:last-child { margin-bottom: 0; }
    .msg-bubble.bot ul, .msg-bubble.bot ol { margin: 6px 0 6px 18px; }
    .msg-bubble.bot li { margin-bottom: 3px; }
    .msg-bubble.bot h1, .msg-bubble.bot h2, .msg-bubble.bot h3 {
        font-size: 14px; font-weight: 600; margin: 8px 0 4px; color: #1a1a2e;
    }
    .msg-bubble.bot strong { color: #5b4fcf; }
    .msg-bubble.bot code {
        background: #f0eeff; padding: 1px 5px;
        border-radius: 4px; font-family: 'DM Mono', monospace; font-size: 12px;
    }
    .msg-bubble.bot pre {
        background: #f0eeff; padding: 10px;
        border-radius: 8px; overflow-x: auto; margin: 8px 0;
    }
    .msg-bubble.bot pre code { background: none; padding: 0; }
    .msg-bubble.bot table {
        border-collapse: collapse; font-size: 12px; margin: 8px 0; width: 100%;
    }
    .msg-bubble.bot th, .msg-bubble.bot td {
        border: 1px solid #e8e4fd; padding: 4px 8px;
    }
    .msg-bubble.bot th { background: #f0eeff; }
    .msg-bubble.bot a { color: #7c5cfc; text-decoration: underline; }
    </style>
    """,
        unsafe_allow_html=True,
    )

    # ── Session state ─────────────────────────────────────────────────────────────
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {
                "role": "bot",
                "text": "Hello! I'm your Gender Data Intelligence assistant. I can help you analyze Rwanda's gender statistics, identify trends, and uncover regional disparities. What would you like to explore today?",
                "time": "09:36 PM",
            }
        ]

    if "input_key" not in st.session_state:
        st.session_state.input_key = 0

    if "session_id" not in st.session_state:
        st.session_state.session_id = str(uuid.uuid4())

    CHIPS = [
        "Highest gap region?",
        "Show trend analysis",
        "Give me a summary",
        "Predict next year",
        "Compare provinces",
    ]

    # ── Chip click via query params trick ────────────────────────────────────────
    chip_clicked = st.query_params.get("chip", "")

    # ── Layout ────────────────────────────────────────────────────────────────────
    # Build the static HTML for the chat card (header + messages + chips + input shell)

    # messages HTML
    msgs_html = ""
    for msg in st.session_state.messages:
        role = msg["role"]
        if role == "bot":
            rendered = md_lib.markdown(
                msg["text"], extensions=["tables", "fenced_code"]
            )
            msgs_html += f"""
            <div class="msg-row">
                <div class="msg-avatar">🤖</div>
                <div class="msg-col">
                    <div class="msg-bubble bot">{rendered}</div>
                    <div class="msg-time">{msg["time"]}</div>
                </div>
            </div>"""
        else:
            msgs_html += f"""
            <div class="msg-row user">
                <div class="msg-avatar">👤</div>
                <div class="msg-col">
                    <div class="msg-bubble user">{msg["text"]}</div>
                    <div class="msg-time">{msg["time"]}</div>
                </div>
            </div>"""

    chips_html = "".join(f'<div class="chip">{c}</div>' for c in CHIPS)

    st.markdown(
        f"""
    <div class="chat-page">
    <div class="chat-card">

        <!-- Header -->
        <div class="chat-header">
        <div class="avatar-ring">🤖</div>
        <div class="header-text">
            <div class="header-title">Ask Intelligence</div>
            <div class="header-sub">Powered by EquiStat AI</div>
        </div>
        <div class="online-badge">
            <div class="online-dot"></div> Online
        </div>
        </div>

        <!-- Messages -->
        <div class="messages-area" id="msg-area">
        {msgs_html}
        </div>

        <!-- Quick chips -->
        <div class="chips-wrapper">
        {chips_html}
        </div>

    </div>
    </div>
    """,
        unsafe_allow_html=True,
    )

    # ── Input row (native Streamlit widgets styled below the card) ───────────────
    st.markdown(
        """
    <style>
    /* Pull the input row up to look like it's inside the card */
    [data-testid="stHorizontalBlock"] {
        max-width: 480px !important;
        margin: -2px auto 0 !important;
        background: #fff;
        border-top: 1px solid #f0f0f6;
        border-radius: 0 0 24px 24px;
        padding: 12px 18px 18px !important;
        box-shadow: 0 8px 40px rgba(80,60,180,0.10);
    }

    /* Text input */
    [data-testid="stTextInput"] input {
        border-radius: 22px !important;
        border: 1.5px solid #e8e4fd !important;
        background: #f8f9fd !important;
        font-family: 'DM Sans', sans-serif !important;
        font-size: 14px !important;
        padding: 11px 16px !important;
        color: #2a2a3d !important;
    }
    [data-testid="stTextInput"] input:focus {
        border-color: #7c5cfc !important;
        box-shadow: none !important;
    }
    [data-testid="stTextInput"] > label { display: none !important; }
    [data-testid="stTextInput"] { flex: 1 !important; }

    /* Send button */
    [data-testid="stHorizontalBlock"] [data-testid="stButton"] button {
        width: 44px !important; height: 44px !important;
        border-radius: 50% !important;
        background: linear-gradient(135deg, #7c5cfc 0%, #6370f5 100%) !important;
        color: white !important;
        font-size: 18px !important;
        padding: 0 !important;
        border: none !important;
        box-shadow: 0 3px 12px rgba(124,92,252,0.35) !important;
        display: flex !important; align-items: center !important; justify-content: center !important;
    }
    [data-testid="stHorizontalBlock"] [data-testid="stButton"] button:hover {
        transform: scale(1.07) !important;
        box-shadow: 0 5px 18px rgba(124,92,252,0.45) !important;
    }
    </style>
    """,
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns([10, 1])
    with col1:
        user_input = st.text_input(
            label="msg",
            placeholder="Ask about trends, gaps, forecasts…",
            key=f"input_{st.session_state.input_key}",
            label_visibility="collapsed",
        )
    with col2:
        send = st.button("➤", key="send_btn")

    # ── Handle send ───────────────────────────────────────────────────────────────
    def add_message(text: str, role: str = "user"):
        now = datetime.now().strftime("%I:%M %p")
        st.session_state.messages.append({"role": role, "text": text, "time": now})

    if send and user_input.strip():
        add_message(user_input.strip(), "user")
        with st.spinner("Thinking…"):
            try:
                resp = requests.post(
                    "http://localhost:8000/api",
                    json={
                        "message": user_input.strip(),
                        "session_id": st.session_state.session_id,
                    },
                    timeout=120,
                )
                if resp.status_code == 200:
                    answer = resp.json()["answer"]
                else:
                    answer = f"⚠️ The assistant returned an error (`{resp.status_code}`). Please try again."
            except requests.exceptions.ConnectionError:
                answer = "⚠️ Could not reach the AI backend. Make sure the API server is running on `localhost:8000`."
            except requests.exceptions.Timeout:
                answer = "⚠️ The request timed out. The AI is taking too long to respond — try a simpler question."
        add_message(answer, "bot")
        st.session_state.input_key += 1
        st.rerun()
