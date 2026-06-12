from typing import Annotated
from typing import TypedDict
from langgraph.graph import StateGraph,START,END
from langgraph.graph.message import add_messages
from langchain_groq import ChatGroq
from langchain_mistralai import ChatMistralAI
import os
from dotenv import load_dotenv
from langchain_tavily import TavilySearch
from rich import print

load_dotenv()


class State(TypedDict):
    # Messages have the type "list". The `add_messages` function
    # in the annotation defines how this state key should be updated
    # (in this case, it appends messages to the list, rather than overwriting them)

    messages:Annotated[list,add_messages]


graph_builder =StateGraph(State)



llm=ChatMistralAI(model="mistral-small-2506")


#node functionality 

def chat_node(state:State):
    return {"messages":[llm.invoke(state["messages"])]}

#adding nodes

graph_builder.add_node("llmchatbot",chat_node)


## add edges

graph_builder.add_edge(START,"llmchatbot")
graph_builder.add_edge("llmchatbot",END)

#compile teh graph 

graph=graph_builder.compile()

#visualize the graph 
from IPython.display import Image, display

# try:
#     png_data = graph.get_graph().draw_mermaid_png()

#     with open("graph.png", "wb") as f:
#         f.write(png_data)

# except Exception:
#     pass  

# response=graph.invoke({"messages":"hey "})
# print(response["messages"][-1].content)

# for event in graph.stream({"messages":"how are you "}):
#     for values in event.values():
#         print(values['messages'][-1].content)

#tool
tool=TavilySearch(max_result=5)
# results=tool.invoke("latest news on ai ")
# print(results)


#custom tool
def multiply(a:int,b:int)->int:
    """
    multiply a and b 
    args:
    a:first int 
    b: second int 
    return :
    multiplication of a and b in int 
    """
    return a*b

tools=[tool,multiply]
 
llm_with_tools=llm.bind_tools(tools)

# results=llm_with_tools.invoke("latest news on war in 2026")
# print(results)

#binding is just tell the which tools do you have 

#now tool call 
from langgraph.prebuilt import ToolNode
from langgraph.prebuilt import tools_condition

# #node definitaion
# def tool_calling_llm(state:State):
#     return {"messages":[llm_with_tools.invoke(state["messages"])]}

# #graph


# builder=StateGraph(State)

# builder.add_node("tool_calling_llm",tool_calling_llm)
# builder.add_node("tools",ToolNode(tools))


# # add edges

# builder.add_edge(START,"tool_calling_llm")
# builder.add_conditional_edges("tool_calling_llm",
#     # If the latest message (result) from assistant is a tool call -> tools_condition routes to tools
#     # If the latest message (result) from assistant is a not a tool call -> tools_condition routes to END

#     tools_condition

# )
# builder.add_edge("tools",END)

# builder_compile=builder.compile()

# result=builder_compile.invoke({"messages":"what is 2*3"})
# print(result )

#ReAct Agent 


# #node definitaion
# def tool_calling_llm(state:State):
#     return {"messages":[llm_with_tools.invoke(state["messages"])]}

# #graph


# builder=StateGraph(State)

# builder.add_node("tool_calling_llm",tool_calling_llm)
# builder.add_node("tools",ToolNode(tools))


# # add edges

# builder.add_edge(START,"tool_calling_llm")
# builder.add_conditional_edges("tool_calling_llm",
#     # If the latest message (result) from assistant is a tool call -> tools_condition routes to tools
#     # If the latest message (result) from assistant is a not a tool call -> tools_condition routes to END

#     tools_condition

# )
# builder.add_edge("tools","tool_calling_llm")

# builder_compile=builder.compile()

# result=builder_compile.invoke({"messages":"what is 2*3 and give me latest news on ai "})
# print(result )


#Adding memory to AgenticGraph 

# from langgraph.checkpoint.memory import MemorySaver


# memory=MemorySaver()


# #node definitaion
# def tool_calling_llm(state:State):
#     return {"messages":[llm_with_tools.invoke(state["messages"])]}

# #graph


# builder=StateGraph(State)

# builder.add_node("tool_calling_llm",tool_calling_llm)
# builder.add_node("tools",ToolNode(tools))


# # add edges

# builder.add_edge(START,"tool_calling_llm")
# builder.add_conditional_edges("tool_calling_llm",
#     # If the latest message (result) from assistant is a tool call -> tools_condition routes to tools
#     # If the latest message (result) from assistant is a not a tool call -> tools_condition routes to END

#     tools_condition

# )
# builder.add_edge("tools","tool_calling_llm")

# builder_compile=builder.compile(checkpointer=memory)

# config={"configurable":{"thread_id":"1"}}


# result=builder_compile.invoke({"messages":"my name is raghav  "},config=config)
# print(result['messages'][-1].content )

# result1=builder_compile.invoke({"messages":"so what is my name "},config=config)
# print(result1['messages'][-1].content )


#Streaming
# Methods: .stream() and astream()

# These methods are sync and async methods for streaming back results.
# Additional parameters in streaming modes for graph state

# values : This streams the full state of the graph after each node is called.
# updates : This streams updates to the state of the graph after each node is called.
