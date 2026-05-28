import streamlit as st
from dotenv import load_dotenv

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser

from langchain_mistralai import ChatMistralAI

from pydantic import BaseModel
from typing import Optional, List


# ================= LOAD ENV =================
load_dotenv()


# ================= PYDANTIC MODEL =================
class Movie(BaseModel):
    title: str
    release_year: Optional[int]
    genre: List[str]
    director: Optional[str]
    rating: Optional[float]
    summary: str


# ================= PARSER =================
parser = PydanticOutputParser(
    pydantic_object=Movie
)


# ================= MODEL =================
model = ChatMistralAI(
    model="mistral-small-2506"
)


# ================= PROMPT =================
prompt = ChatPromptTemplate.from_messages([
    (
        'system',
        """
Extract Movie information from paragraph.

{format_instructions}
"""
    ),
    (
        'human',
        "{movie_data}"
    )
])


# ================= STREAMLIT UI =================
st.set_page_config(
    page_title="Movie Information Extractor",
    page_icon="🎬",
    layout="centered"
)

st.title("🎬 Movie Information Extractor")

st.markdown(
    "Paste movie-related content below and extract structured movie information using AI."
)

st.divider()


# ================= TEXT INPUT =================
movie_text = st.text_area(
    "Enter Movie Content",
    height=300,
    placeholder="Paste movie paragraph here..."
)


# ================= BUTTON =================
if st.button("Extract Information"):

    if movie_text.strip() == "":
        st.warning("Please enter some movie content.")
    else:

        with st.spinner("Extracting movie information..."):

            final_prompt = prompt.invoke({
                "movie_data": movie_text,
                "format_instructions": parser.get_format_instructions()
            })

            response = model.invoke(final_prompt)

            parsed_output = parser.parse(response.content)

        st.success("Extraction Completed")

        st.subheader("Extracted Information")

        st.json(
            parsed_output.model_dump()
        )