from langchain_community.utilities import DuckDuckGoSearchAPIWrapper
from langchain.tools import tool
from langchain_community.tools import DuckDuckGoSearchResults




def web_search_tool(query: str) -> str:
    """
    Perform a web search using the DuckDuckGo search engine.

    Args:
        query (str): The search query string.

    Returns:
        str: The search results.
    """
    # Initialize the API wrapper for DuckDuckGo
    api_wrapper = DuckDuckGoSearchAPIWrapper()

    # Create a search engine instance with the API wrapper
    search_engine = DuckDuckGoSearchResults(api_wrapper=api_wrapper)

    # Invoke the search engine with the given query and get results
    search_results = search_engine.invoke(input=query)

    return search_results



print(web_search_tool("Ai in 2025"))
