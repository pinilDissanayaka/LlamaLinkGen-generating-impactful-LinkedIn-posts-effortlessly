import os
from dotenv import load_dotenv, find_dotenv
from typing import Annotated, Sequence, TypedDict
from langchain_core.messages import BaseMessage
from langgraph.graph import add_messages
from langchain_groq.chat_models import ChatGroq

load_dotenv(find_dotenv())


os.environ["GROQ_API_KEY"]=os.getenv("GROQ_API_KEY")

llm=ChatGroq(
    model_name="llama-3.3-70b-versatile",
    temperature=0.7
)


class GraphState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]
    router_state: Annotated[Sequence[BaseMessage], add_messages]
    context: str


