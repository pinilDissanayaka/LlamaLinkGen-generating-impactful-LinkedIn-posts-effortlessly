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
    Searches for the given query on LinkedIn and returns the search results.

    Parameters:
    query (str): The search query to search for on LinkedIn

    Returns:
    str: The search results
    """
    return search(f"site:linkedin.com {query}")



def market_researcher(state: GraphState):
    market_researcher_prompt_template="""
        You are an expert at Investigate the latest trends.
        Investigate the latest trends, hashtags, and competitor activities on 
        Linkedin specific to the industry of this Linkedin account. 
        Focus on gathering data that reveals what content performs well in the current year, 
        identifying patterns, preferences, and emerging trends. 

            Current date: {CURRENT_DATE}

        Description of the Linkedin account for which you are doing this research: 
            Linkedin Account Description : {LINKEDIN_ACCOUNT_DESCRIPTION}

        Find the most relevant topics, hashtags and trends to use the the posts for next week. 
    """


    market_researcher_prompt = PromptTemplate.from_template(
        template=market_researcher_prompt_template
    )



    current_date = datetime.now().strftime("%Y-%m-%d")
    message=state["messages"][-1].content

    llm_with_tools = llm.bind_tools([search_linkedin])


    market_researcher_chain = (
        {"LINKEDIN_ACCOUNT_DESCRIPTION": RunnablePassthrough(), "CURRENT_DATE":RunnablePassthrough()} |
        market_researcher_prompt |
        llm_with_tools 
    )


    market_researcher_chain_response = market_researcher_chain.invoke(
        {"LINKEDIN_ACCOUNT_DESCRIPTION" : message, "CURRENT_DATE": current_date}
    )

    print(market_researcher_chain_response)

    return {
        "messages": market_researcher_chain_response
    }


def market_researcher_to_tool(state:GraphState)->str:
    message=state["messages"][-1].tool_calls

    if message:
        return "TOOL_CALL"
    else:
        return "NO_TOOL_CALL"



market_researcher_tool=ToolNode([search_linkedin])
    






