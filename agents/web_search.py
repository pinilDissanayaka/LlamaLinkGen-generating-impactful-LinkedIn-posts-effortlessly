from utils import llm, GraphState
from agents.tools import web_search_tool, open_web_page
from langgraph.prebuilt import ToolNode, create_react_agent
from langchain_core.messages import AIMessage


llm_with_tools = llm.bind_tools([web_search_tool, open_web_page])


web_search_agent=create_react_agent(
    llm,
    tools=[web_search_tool],
    state_modifier="""
        You are best at researching a topic. 
        You should do a thorough research. 
        Your output will be used by a content writer agent to write a article, 
        blogs, posts or any other content. 
        Hence you should provide accurate content. 
"""
)


