from dotenv import load_dotenv, find_dotenv
from utils import GraphState
from langgraph.graph import StateGraph, START, END
from nodes import researcher, researcher_to_tool, researcher_tool, writer



load_dotenv(find_dotenv())

graph_builder = StateGraph(GraphState)

graph_builder.add_node("Researcher", researcher)
graph_builder.add_node("Researcher_Tool", researcher_tool)
graph_builder.add_node("Writer", writer)


graph_builder.set_entry_point("Researcher")

graph_builder.add_conditional_edges(
    "Researcher",
    researcher_to_tool,
    {
        "TOOL_CALL": "Researcher_Tool",
        "NO_TOOL_CALL": END
    }
)

graph_builder.add_edge("Researcher_Tool", "Researcher")

graph_builder.add_edge("Researcher", "Writer")

graph_builder.add_edge("Writer", END)


graph = graph_builder.compile()



input_query=str(input("Enter input : "))
for chunk in graph.stream(input={"messages": input_query}, stream_mode="values"):
    chunk["messages"][-1].pretty_print()

