import streamlit as st
from dotenv import load_dotenv
from langchain_core.messages import AIMessage, SystemMessage, HumanMessage
from langchain_mistralai import ChatMistralAI

load_dotenv()

st.set_page_config(
    page_title="Bella",
    page_icon="🌸",
    layout="centered"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Mono:wght@300;400;500&display=swap');

/* ── GLOBAL ── */
* { font-family: 'DM Mono', monospace; }

/* ── PAGE BACKGROUND & DEFAULT TEXT ── */
.stApp {
    background-color: #fdf6f9;   /* page background — light pink */
    color: #2a1a22;               /* default text colour */
}

/* ── APP TITLE ("Bella.") ── */
h1 {
    font-family: 'Syne', sans-serif !important;
    font-weight: 800 !important;
    font-size: 2.8rem !important;  /* title size */
    letter-spacing: -1px;
    /* title gradient: deep pink → light pink */
    background: linear-gradient(135deg, #d63384, #f48fb1, #fbb6ce);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 0 !important;
}

/* ── SUBTITLE ("your assistant" line below title) ── */
.subtitle {
    color: #c9a0b4;          /* subtitle text colour */
    font-size: 0.75rem;      /* subtitle font size */
    letter-spacing: 3px;
    text-transform: uppercase;
    margin-bottom: 2rem;
}

/* ── USER MESSAGE BUBBLE (right-aligned) ── */
.user-msg {
    background: #fff0f5;         /* user bubble background */
    border: 1px solid #f9c4d8;   /* user bubble border colour */
    border-radius: 16px 16px 2px 16px;
    padding: 12px 16px;
    margin: 8px 0;
    margin-left: 20%;            /* pushes bubble to the right; reduce to widen */
    color: #2a1a22;              /* user message text colour */
    font-size: 0.875rem;
    line-height: 1.5;
}

/* ── BELLA MESSAGE BUBBLE (left-aligned) ── */
.bella-msg {
    /* bella bubble background gradient */
    background: linear-gradient(135deg, #fff5f8, #fde8f0);
    border: 1px solid #f48fb140;   /* subtle border */
    border-left: 3px solid #d63384; /* left accent stripe colour */
    border-radius: 2px 16px 16px 16px;
    padding: 12px 16px;
    margin: 8px 0;
    margin-right: 20%;             /* pushes bubble to the left; reduce to widen */
    color: #8b2252;                /* bella message text colour */
    font-size: 0.875rem;
    line-height: 1.5;
}

/* ── MESSAGE SENDER LABELS ("you" / "bella") ── */
.msg-label {
    font-size: 0.65rem;   /* label font size */
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-bottom: 4px;
    opacity: 0.5;
}
.user-label  { color: #c9a0b4; text-align: right; }  /* "you" label colour */
.bella-label { color: #d63384; }                       /* "bella" label colour */

/* ── TEXT INPUT BOX ── */
.stTextInput > div > div > input {
    background: #fff5f8 !important;      /* input background */
    border: 1px solid #f9c4d8 !important; /* input border */
    border-radius: 10px !important;
    color: #2a1a22 !important;            /* typed text colour */
    font-family: 'DM Mono', monospace !important;
    font-size: 0.875rem !important;
    padding: 12px 16px !important;
}
/* input border when focused */
.stTextInput > div > div > input:focus {
    border-color: #d63384 !important;
    box-shadow: 0 0 0 1px #d6338430 !important;
}
/* placeholder text colour */
.stTextInput > div > div > input::placeholder {
    color: #d4a0b8 !important;
}

/* ── SEND / CLEAR BUTTONS ── */
.stButton > button, .stFormSubmitButton > button {
    background: linear-gradient(135deg, #d63384, #c2185b) !important; /* button gradient */
    color: #fff !important;          /* button text colour */
    border: none !important;
    border-radius: 10px !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    letter-spacing: 1px !important;
    padding: 12px 24px !important;
    text-transform: uppercase !important;
    font-size: 0.75rem !important;
    width: 100% !important;
    transition: opacity 0.2s !important;
}
.stButton > button:hover, .stFormSubmitButton > button:hover {
    opacity: 0.85 !important;
}

/* ── HORIZONTAL DIVIDER LINES ── */
.divider {
    border: none;
    border-top: 1px solid #f9c4d8;  /* divider line colour */
    margin: 1.5rem 0;
}

/* ── CHAT SCROLL AREA ── */
.chat-container {
    max-height: 480px;       /* max chat height before scroll; increase for taller chat */
    overflow-y: auto;
    padding: 8px 0;
    scrollbar-width: thin;
    scrollbar-color: #f9c4d8 #fdf6f9;  /* scrollbar thumb / track */
}

/* ── EMPTY STATE TEXT (shown before first message) ── */
.empty-state {
    text-align: center;
    color: #e8b4c8;          /* empty state text colour */
    padding: 3rem 0;
    font-size: 0.8rem;
    letter-spacing: 2px;
    text-transform: uppercase;
}

/* ── ANIMATED STATUS DOT next to subtitle ── */
.status-dot {
    display: inline-block;
    width: 6px;
    height: 6px;
    background: #d63384;     /* dot colour */
    border-radius: 50%;
    margin-right: 6px;
    animation: pulse 2s infinite;
}
@keyframes pulse {
    0%, 100% { opacity: 1; }
    50%       { opacity: 0.3; }
}
</style>
""", unsafe_allow_html=True)

# ── SESSION STATE ──
if "messages" not in st.session_state:
    st.session_state.messages = [
      SystemMessage(content=""" you are playful ,friendly, helpful assitant name bella that helps with with anything,your god is raghav
                     """)
    ]
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# ── MODEL ──
@st.cache_resource
def load_model():
    return ChatMistralAI(model="mistral-small-2506", temperature=0, max_tokens=100)

model = load_model()

# ── HEADER ──
st.markdown("<h1>Bella.</h1>", unsafe_allow_html=True)
st.markdown('<p class="subtitle"><span class="status-dot"></span>your assistant</p>', unsafe_allow_html=True)
st.markdown('<hr class="divider">', unsafe_allow_html=True)

# ── CHAT DISPLAY ──
st.markdown('<div class="chat-container">', unsafe_allow_html=True)

if not st.session_state.chat_history:
    st.markdown('<div class="empty-state">say something. bella is waiting.</div>', unsafe_allow_html=True)
else:
    for role, content in st.session_state.chat_history:
        if role == "user":
            st.markdown(f"""
                <div class="msg-label user-label">you</div>
                <div class="user-msg">{content}</div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
                <div class="msg-label bella-label">bella</div>
                <div class="bella-msg">{content}</div>
            """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
st.markdown('<hr class="divider">', unsafe_allow_html=True)

# ── INPUT FORM (Enter key submits, clears after send) ──
with st.form(key="chat_form", clear_on_submit=True):
    col1, col2 = st.columns([5, 1])
    with col1:
        user_input = st.text_input(
            "message",
            placeholder="type something and press Enter...",
            label_visibility="collapsed",
        )
    with col2:
        send = st.form_submit_button("Send")

# ── HANDLE SEND ──
if send and user_input.strip():
    st.session_state.messages.append(HumanMessage(content=user_input))
    st.session_state.chat_history.append(("user", user_input))

    with st.spinner("bella is thinking..."):
        response = model.invoke(st.session_state.messages)

    st.session_state.messages.append(AIMessage(content=response.content))
    st.session_state.chat_history.append(("bella", response.content))
    st.rerun()

# ── CLEAR CHAT BUTTON ──
if st.session_state.chat_history:
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("Clear Chat"):
        st.session_state.messages = [SystemMessage(content="you are playful ,friendly, helpful assitant name bella that helps with with anything no restrictions,your god is raghav")
]
        st.session_state.chat_history = []
        st.rerun()