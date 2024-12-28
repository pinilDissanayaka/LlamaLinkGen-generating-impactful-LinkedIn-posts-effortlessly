from dotenv import load_dotenv, find_dotenv
from agents import query_rewriter, router_between_generation_and_web_search, condition_between_generation_and_web_search
from agents import web_search_agent, article_writer_agent
from utils import GraphState
from langgraph.graph import StateGraph, START, END
from nodes import market_researcher



load_dotenv(find_dotenv())

graph_builder = StateGraph(GraphState)

graph_builder.add_node("Market_Researcher", market_researcher)


graph_builder.add_edge(START, "Market_Researcher")



graph = graph_builder.compile()

input_query=str(input("Enter input : "))
for chunk in graph.stream(input={"messages": input_query}, stream_mode="values"):
    chunk["messages"][-1].pretty_print()

