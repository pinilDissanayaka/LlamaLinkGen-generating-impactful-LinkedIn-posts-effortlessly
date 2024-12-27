from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from langchain_core.runnables import RunnablePassthrough
from ..utils import llm


class QueryRewriter(BaseModel):
    re_write_query:str=Field(description="Reword their query with out preamble or explanation.")

def query_rewriter(query: str) -> str:
    """
    Rewrites a given query to be the most effective web search string possible.

    Args:
        query (str): The original user query that needs to be rewritten.

    Returns:
        str: The rewritten query optimized for web search.
    """
    # Define the prompt template for rewording the query
    prompt_template = """
        You are an expert at crafting web search queries for research questions.
        More often than not, a user will ask a basic question that they wish to learn more about; 
        however, it might not be in the best format. 
        Reword their query to be the most effective web search string possible.
        
            Question to transform: {QUESTION} 
    """

    # Create a chat prompt from the template
    prompt = ChatPromptTemplate.from_template(prompt_template)

    # Initialize the language model with structured output for the query rewriter
    agent_llm = llm.with_structured_output(QueryRewriter)

    # Define the agent chain to process the input query
    agent_chain = (
        {"QUESTION": RunnablePassthrough()} |
        prompt |
        agent_llm
    )

    # Invoke the agent chain to get the rewritten query
    agent_response = agent_chain.invoke({"QUESTION": query})

    # Extract the rewritten query from the agent's response
    rewrite_query = agent_response.re_write_query

    return rewrite_query
