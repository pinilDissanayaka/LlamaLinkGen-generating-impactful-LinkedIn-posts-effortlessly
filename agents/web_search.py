from langgraph.prebuilt import create_react_agent
from utils import llm
from agents.tools import web_search_tool, open_web_page

research_agent=create_react_agent(
    llm,
    tools=[web_search_tool, open_web_page],
    state_modifier="""
            You are best at researching a topic. 
            You should do a thorough research. 
            Your output will be used by a post generator agent. 
            Hence you should provide accurate data. 
    """
)