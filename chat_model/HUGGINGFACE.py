from dotenv import load_dotenv

from langchain_huggingface import (
    ChatHuggingFace,
    HuggingFaceEndpoint
)

load_dotenv()

llm = HuggingFaceEndpoint(
    repo_id="deepseek-ai/DeepSeek-R1-Distill-Llama-8B",
    task="text-generation"
)

model = ChatHuggingFace(llm=llm)

response = model.invoke("Who are you?")

print(response.content)