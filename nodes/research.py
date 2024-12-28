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

@tool
def search(query: str) -> str:
    """
    Searches for the given query using the Google SERP API 
    and returns the top 2 search results.

    Parameters:
    query (str): The search query

    Returns:
    str: Formatted search results as a string
    """
    url = "https://google.serper.dev/search"

    # Prepare the payload with the search query and number of results
    payload = json.dumps({
        "q": query,
        "num": 2
    })

    # Set the necessary headers, including the API key
    headers = {
        'X-API-KEY': os.getenv("X-API-KEY"),
        'Content-Type': 'application/json'
    }

    # Make the API request to fetch search results
    response = requests.request("POST", url, headers=headers, data=payload).json()["organic"]

    # Initialize an empty list to store formatted results
    string = []

    # Iterate over each result and format the title, snippet, and link
    for result in response:
        string.append(f"{result['title']}\n{result['snippet']}\n{result['link']}\n\n")

    # Return the formatted string with all results
    return f"Search results for '{query}':\n\n" + "\n".join(string)



def researcher(state: GraphState):
    market_researcher_prompt_template="""
        You are a web search agent tasked with conducting thorough research on a specific topic. 
            topic : {TOPIC}
        Your findings will be used by a blog post writer to create an engaging and informative article. 
        Follow these instructions to ensure your output is valuable:
            Understanding the Topic: Research the given topic comprehensively. Understand its main aspects, subtopics, and related discussions.

            Sources and Credibility: Use up-to-date and reputable sources. Prioritize authoritative websites, recent publications, and credible platforms. Avoid using unverifiable or biased sources.

            Structure Your Output: Organize your findings clearly with headings, subheadings, and bullet points for readability. Include:

                Overview: A concise summary of the topic.
                Key Points: Main arguments, facts, or perspectives on the topic.
                Supporting Data: Relevant statistics, quotes, or case studies to enhance credibility.
                Trends and Insights: Current trends or emerging insights related to the topic.
                Relevant Questions: Common questions people ask about the topic to help shape the blog's FAQ or discussion sections.
                Resources and Links: Include links to the most useful sources for further reference.
            Content Style: Use neutral, formal language with an emphasis on clarity and conciseness. Avoid unnecessary jargon unless explaining technical terms.

            Adaptability: Include suggestions for tailoring the content to different audiences (e.g., beginners, industry experts, or general readers) if applicable.

            Focus Areas (if provided): If specific areas of focus are mentioned, ensure they are covered in detail.

            Remember your output will used by the blog post writer to create an engaging and informative article.
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


def researcher_to_tool(state:GraphState)->str:
    message=state["messages"][-1].tool_calls

    if message:
        return "TOOL_CALL"
    else:
        return "NO_TOOL_CALL"



researcher_tool=ToolNode([DuckDuckGoSearchResults(api_wrapper=DuckDuckGoSearchAPIWrapper())])







