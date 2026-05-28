import streamlit as st
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_mistralai import ChatMistralAI

load_dotenv()

st.set_page_config(
    page_title="Movie Extractor",
    page_icon="🎬",
    layout="centered"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Mono:wght@300;400;500&display=swap');

/* ── GLOBAL ── */
* { font-family: 'DM Mono', monospace; }

/* ── PAGE BACKGROUND & DEFAULT TEXT ── */
.stApp {
    background-color: #0d0d0d;   /* page background — deep dark */
    color: #f0f0f0;               /* default text colour */
}

/* ── TITLE ── */
h1 {
    font-family: 'Syne', sans-serif !important;
    font-weight: 800 !important;
    font-size: 2.8rem !important;
    letter-spacing: -1px;
    /* title gradient: gold → amber */
    background: linear-gradient(135deg, #f5c518, #ffdd57, #ffe082);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 0 !important;
}

/* ── SUBTITLE ── */
.subtitle {
    color: #666;              /* subtitle colour */
    font-size: 0.75rem;
    letter-spacing: 3px;
    text-transform: uppercase;
    margin-bottom: 2rem;
}

/* ── DIVIDER LINES ── */
.divider {
    border: none;
    border-top: 1px solid #1f1f1f;  /* divider colour */
    margin: 1.5rem 0;
}

/* ── TEXTAREA (content input) ── */
.stTextArea > div > div > textarea {
    background: #111 !important;          /* textarea background */
    border: 1px solid #2a2a2a !important; /* textarea border */
    border-radius: 10px !important;
    color: #f0f0f0 !important;            /* typed text colour */
    font-family: 'DM Mono', monospace !important;
    font-size: 0.85rem !important;
    line-height: 1.6 !important;
    padding: 14px 16px !important;
}
.stTextArea > div > div > textarea:focus {
    border-color: #f5c518 !important;                  /* border on focus */
    box-shadow: 0 0 0 1px #f5c51830 !important;
}
.stTextArea > div > div > textarea::placeholder {
    color: #444 !important;   /* placeholder text colour */
}

/* ── ANALYSE BUTTON ── */
.stButton > button {
    background: linear-gradient(135deg, #f5c518, #e6b800) !important; /* button gradient */
    color: #0d0d0d !important;       /* button text colour */
    border: none !important;
    border-radius: 10px !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    letter-spacing: 1px !important;
    padding: 12px 28px !important;
    text-transform: uppercase !important;
    font-size: 0.75rem !important;
    transition: opacity 0.2s !important;
}
.stButton > button:hover {
    opacity: 0.85 !important;
}

/* ── RESULT CARD (wraps extracted info) ── */
.result-card {
    background: #111;              /* result card background */
    border: 1px solid #1f1f1f;    /* result card border */
    border-top: 3px solid #f5c518; /* result card top accent colour */
    border-radius: 12px;
    padding: 24px 28px;
    margin-top: 1.5rem;
    line-height: 1.8;
    color: #e0e0e0;                /* result text colour */
    font-size: 0.875rem;
    white-space: pre-wrap;         /* preserves line breaks in AI output */
}

/* ── FIELD LABELS inside result (bold lines like "Movie Title:") ── */
.result-card strong {
    color: #f5c518;   /* highlight colour for bold labels */
}

/* ── SECTION LABEL above textarea ── */
.section-label {
    font-size: 0.65rem;
    letter-spacing: 3px;
    text-transform: uppercase;
    color: #555;           /* section label colour */
    margin-bottom: 6px;
}

/* ── STATUS DOT ── */
.status-dot {
    display: inline-block;
    width: 6px;
    height: 6px;
    background: #f5c518;   /* dot colour */
    border-radius: 50%;
    margin-right: 6px;
    animation: pulse 2s infinite;
}
@keyframes pulse {
    0%, 100% { opacity: 1; }
    50%       { opacity: 0.3; }
}

/* ── SPINNER TEXT ── */
.stSpinner > div {
    color: #f5c518 !important;   /* spinner text colour */
}
</style>
""", unsafe_allow_html=True)

# ── PROMPT TEMPLATE ──
prompt = ChatPromptTemplate.from_messages([
    ("system", """
You are an expert movie information extraction assistant.

Your task is to analyze unstructured movie-related content collected from multiple sources such as:
- articles
- reviews
- blogs
- social media
- movie databases
- news websites

Extract only the most useful and relevant information.

Focus on:
1. Movie title
2. Genre
3. Main cast
4. Director
5. Release year/date
6. Plot summary
7. Main themes
8. Sentiment or public opinion
9. Ratings or reviews if available
10. Important insights or trends

Rules:
- Keep summaries concise but informative.
- Ignore advertisements, spam, or irrelevant content.
- If information is missing, mention "Not Available".
- Ensure extracted information is factually consistent with the input.
- Output should be clean, structured, and easy to read.
- Prioritize important movie-related insights over unnecessary details.
"""),
    ("human", """
Analyze the following movie-related content and extract useful structured information.

Content:
{movie_data}

Provide:
- Movie Title
- Genre
- Cast
- Director
- Release Information
- Short Summary
- Public Sentiment
- Ratings (if available)
- Key Insights
""")
])

# ── MODEL ──
@st.cache_resource
def load_model():
    return ChatMistralAI(model="mistral-small-2506")

model = load_model()

# ── HEADER ──
st.markdown("<h1>🎬 CineExtract.</h1>", unsafe_allow_html=True)
st.markdown('<p class="subtitle"><span class="status-dot"></span>movie intelligence extractor</p>', unsafe_allow_html=True)
st.markdown('<hr class="divider">', unsafe_allow_html=True)

# ── INPUT ──
st.markdown('<p class="section-label">Paste movie-related content below</p>', unsafe_allow_html=True)
movie_data = st.text_area(
    "movie content",
    placeholder="Paste any movie-related content here — reviews, articles, plot descriptions, social media posts, news...",
    height=220,
    label_visibility="collapsed"
)

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    analyse = st.button("Analyse Content")

# ── HANDLE ANALYSE ──
if analyse:
    if not movie_data.strip():
        st.warning("Please paste some movie content first.")
    else:
        with st.spinner("Extracting movie intelligence..."):
            final_prompt = prompt.invoke({"movie_data": movie_data})
            response = model.invoke(final_prompt)

        st.markdown('<hr class="divider">', unsafe_allow_html=True)
        st.markdown('<p class="section-label">Extracted Information</p>', unsafe_allow_html=True)

        # Bold the field labels in output
        import re
        formatted = response.content
        formatted = re.sub(
            r'(-\s?(Movie Title|Genre|Cast|Director|Release Information|Short Summary|Public Sentiment|Ratings|Key Insights)[:\s]?)',
            r'**\1**',
            formatted
        )
        st.markdown(f'<div class="result-card">{formatted}</div>', unsafe_allow_html=True)