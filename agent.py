from dotenv import load_dotenv, find_dotenv
from agents import query_rewriter, router_between_generation_and_web_search, condition_between_generation_and_web_search
from agents import web_search_agent, article_writer_agent
from utils import GraphState
from langgraph.graph import StateGraph, START, END



load_dotenv(find_dotenv())

graph_builder = StateGraph(GraphState)

graph_builder.add_node("Query_rewriter", query_rewriter)
graph_builder.add_node("Router_between_generation_and_web_search", router_between_generation_and_web_search)
graph_builder.add_node("Web_search", web_search_agent)
graph_builder.add_node("Content_writer", article_writer_agent)

graph_builder.add_edge(START, "Router_between_generation_and_web_search")

graph_builder.add_conditional_edges(
    "Router_between_generation_and_web_search",
    condition_between_generation_and_web_search,
    {"web_search": "Query_rewriter", "generate": END}
)

graph_builder.add_edge("Query_rewriter", "Web_search")

graph_builder.add_edge("Web_search", "Content_writer")

graph = graph_builder.compile()

input_query=str(input("Enter input : "))
for chunk in graph.stream(input={"messages": input_query}, stream_mode="values"):
    chunk["messages"][-1].pretty_print()

