from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel
from typing import Optional,List
from langchain_core.output_parsers import PydanticOutputParser
class Movie(BaseModel):
    title:str
    release_year:Optional[int]
    genre:List[str]
    director: Optional[str]
    rating:Optional[float]
    summary:str

parser=PydanticOutputParser(pydantic_object=Movie)


load_dotenv()
from langchain_mistralai import ChatMistralAI
model = ChatMistralAI(model="mistral-small-2506")

prompt = ChatPromptTemplate.from_messages([
    ('system',"""
Extract Movie information from paragraph {format_instructions}
"""),('human',"{movie_data}")]
)

para=input("Give content")
final_prompt=prompt.invoke(
    {"movie_data":para,
    'format_instructions':parser.get_format_instructions()}
    
)
response=model.invoke(final_prompt)
print("AI:",response.content)