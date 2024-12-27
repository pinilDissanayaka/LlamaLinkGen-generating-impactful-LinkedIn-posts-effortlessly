from langchain_community.utilities import DuckDuckGoSearchAPIWrapper
from langchain_community.document_loaders import WebBaseLoader
from langchain.tools import tool
import json
import requests
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())



@tool
def web_search_tool(query: str) -> str:
    """
    This function performs a web search using the Google SERP API and returns the results as a string.

    Parameters:
    query (str): The search query

    Returns:
    str: The search results as a JSON string
    """
    url="https://google.serper.dev/search"
    payload = json.dumps({
    "q": query,
    "num": 5
    })
    
    headers = {
    'X-API-KEY': os.getenv("X-API-KEY"),
    'Content-Type': 'application/json'
    }
    
    # Make the API call
    web_search_response = requests.request("POST", url, headers=headers, data=payload)
    
    # Parse the response as JSON
    web_search_response = web_search_response.json()
    
    # Return the search results as a string
    return json.dumps(web_search_response)

@tool
def open_web_page(urls: list) -> str:
    """
    Loads and splits the content of web pages from the given URLs.

    Parameters:
    urls (list): A list of URLs to load the web pages from.

    Returns:
    str: The loaded and split content of the web pages.
    """
    # Initialize the web loader with the provided URLs
    web_loader = WebBaseLoader(urls)

    # Load and split the web pages
    loaded_web_page = web_loader.load_and_split()

    # Return the loaded web page content
    return loaded_web_page

    
print(open_web_page(["https://www.coursera.org/articles/history-of-ai"]))
