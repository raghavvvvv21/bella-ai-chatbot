from dotenv import load_dotenv 
load_dotenv()

from langchain_mistralai import ChatMistralAI
model = ChatMistralAI(model="mistral-small-2506",temperature=0,max_tokens=100)
response = model.invoke("small poem on life")
print(response.content)