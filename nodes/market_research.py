from langchain_core.prompts import PromptTemplate
from utils import llm, GraphState
from datetime import datetime
from langchain_core.runnables import RunnablePassthrough
from  langchain_core.output_parsers import JsonOutputParser, StrOutputParser
from langchain_community.tools import DuckDuckGoSearchResults
from langchain_community.utilities import DuckDuckGoSearchAPIWrapper
from langchain_core.messages import AIMessage, ToolMessage, HumanMessage
from langgraph.prebuilt import ToolNode
import requests
from langchain_core.tools import tool
import json
import os


def search(query:str, limit=2):
    url="https://google.serper.dev/search"
    payload = json.dumps({
        "q": query,
        "num": limit
    })
        
    headers = {
        'X-API-KEY': os.getenv("X-API-KEY"),
        'Content-Type': 'application/json'
    }
        
        
    response = requests.request("POST", url, headers=headers, data=payload).json()["organic"]
        
    string = []

    for result in response :
        string.append(f"{result['title']}\n{result['snippet']}\n{result['link']}\n\n")

    return f"Search results for '{query}':\n\n" + "\n".join(string)


@tool
def search_linkedin(query: str) -> str:
    """
    Searches for the given query on web and returns the search results.

    Parameters:
    query (str): The search query to search for on web

    Returns:
    str: The search results
    """
    return search(f"{query}")



def market_researcher(state: GraphState):
    market_researcher_prompt_template="""
        You are best at researching a topic. 
            topic : {TOPIC}
        You should do a thorough research.
        Your output will be used by a chart generator agent to visually display the data. 
        Hence you should provide accurate data. 
        Also specify the chart types like bar-chart, pie chart etc. 
        that will effectively display the data. 
        The chart generator may ask for more information, 
        so be prepared to do further research and provide it.
    """


    market_researcher_prompt = PromptTemplate.from_template(
        template=market_researcher_prompt_template
    )



    message=state["messages"][-1].content

    llm_with_tools = llm.bind_tools([DuckDuckGoSearchResults(api_wrapper=DuckDuckGoSearchAPIWrapper())])


    market_researcher_chain = (
        {"TOPIC": RunnablePassthrough()} |
        market_researcher_prompt |
        llm_with_tools 
    )


    market_researcher_chain_response = market_researcher_chain.invoke(
        {"TOPIC" : message}
    )

    return {
        "messages": market_researcher_chain_response
    }


def market_researcher_to_tool(state:GraphState)->str:
    message=state["messages"][-1].tool_calls

    if message:
        return "TOOL_CALL"
    else:
        return "NO_TOOL_CALL"



market_researcher_tool=ToolNode([DuckDuckGoSearchResults(api_wrapper=DuckDuckGoSearchAPIWrapper())])



def print_result(state: GraphState):
    print("result")
    print(state["messages"][-1].content)
    






