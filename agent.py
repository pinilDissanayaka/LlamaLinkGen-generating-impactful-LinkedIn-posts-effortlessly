import os
from typing import Annotated, Sequence, TypedDict
from langchain_core.messages import BaseMessage, AIMessage, HumanMessage, ToolMessage
from langgraph.prebuilt import ToolNode, create_react_agent
from langgraph.graph import add_messages, StateGraph, START, END
from langchain_community.tools import DuckDuckGoSearchResults
from langchain_core.tools import tool
from langchain_groq.chat_models import ChatGroq
from dotenv import load_dotenv, find_dotenv
from langchain_experimental.utilities import PythonREPL
from agents import query_rewriter
from utils import GraphState


load_dotenv(find_dotenv())



'''load_dotenv(find_dotenv())

os.environ["GROQ_API_KEY"]=os.getenv("GROQ_API_KEY")


llm=ChatGroq(
    model_name="llama-3.3-70b-versatile",
    temperature=0.7
)






class GraphState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]


research_agent=create_react_agent(
    llm,
    tools=[DuckDuckGoSearchResults()],
    state_modifier="""
    You are best at researching a topic. 
    You should do a thorough research. 
    Your output will be used by a chart generator agent to visually display the data. 
    Hence you should provide accurate data. 
    Also specify the chart types like barchart, pie chart etc. 
    that will effectively display the data. 
    The chart generator may ask for more information, 
    so be prepared to do further research and provide it.
    """
)




def research_node(state: GraphState):
    return_message=research_agent.invoke(state)

    return {
        "messages": return_message["messages"][-1].content,
    }


def write_log_node(state: GraphState):
    data = state["messages"][-1].content
    """
    Write a log of the previous interaction to a file named 'log.txt'.
    """
    with open("log.txt", "w") as log_file:
        log_file.write(data)

'''




graph_builder = StateGraph(GraphState)

graph_builder.add_node("re_writer", query_rewriter)


graph_builder.add_edge(START, "re_writer")


graph = graph_builder.compile()

input_query=str(input("Enter input : "))
for chunk in graph.stream(input={"messages": input_query}, stream_mode="values"):
    chunk["messages"][-1].pretty_print()




