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


load_dotenv(find_dotenv())

os.environ["GROQ_API_KEY"]=os.getenv("GROQ_API_KEY")


llm=ChatGroq(
    model_name="llama-3.3-70b-versatile",
    temperature=0.7
)


class GraphState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]
    context: str
