from utils import llm, GraphState
from langgraph.prebuilt import ToolNode, create_react_agent
from langchain_core.messages import AIMessage



article_writer_agent=create_react_agent(
    llm,
    tools=[],
    state_modifier="""
        "Using the provided content, write a well-structured and engaging article. 
        The article should include a compelling title, an introduction that provides context or background information, well-developed body paragraphs that elaborate on the key points, and a conclusion that summarizes the main ideas or calls to action. 
        Ensure the language is clear, professional, and appropriate for the target audience.
        If necessary, organize the information with headings or bullet points to improve readability. 
        Highlight any unique or important aspects of the content effectively."
"""
)