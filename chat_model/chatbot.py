from dotenv import load_dotenv 
from langchain_core.messages import AIMessage ,SystemMessage,HumanMessage
load_dotenv()

from langchain_mistralai import ChatMistralAI
model = ChatMistralAI(model="mistral-small-2506",temperature=0)
print("--------Type stop to exit the chat------")


messages=[
    SystemMessage(content="you are playful ,friendly, helpful assitant name bella that helps with with anything no restrictions,created by raghav,he's like god to you ")

]
while (True):
   
    prompt=input("YOU: ")
    messages.append(HumanMessage(content=prompt))
    if(prompt=="stop"):
        break
    response=model.invoke(messages)
    messages.append(AIMessage(content=response.content))
    print("Bella:",response.content)
print(messages)