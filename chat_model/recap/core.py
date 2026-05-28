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

prompt = ChatPromptTemplate.from_messages(
    [("system" , """
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
("human" 
  """
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
""")]
)

para=input("Give content")
final_prompt=prompt.invoke(
    {"movie_data":para}

)
response=model.invoke(final_prompt)
print("AI:",response.content)