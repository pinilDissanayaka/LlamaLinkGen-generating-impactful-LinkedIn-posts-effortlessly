from utils import llm, GraphState
from langchain_core.messages import AIMessage, HumanMessage, ToolMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough    
from langchain_core.output_parsers import JsonOutputParser




def router_between_generation_and_web_search(state: GraphState):
    """
    Router that takes the user's question and determines whether to send it to the web search or generation stage.

    The router is a language model that returns a JSON with a single key 'choice' with a binary value 'web_search' or 'generate'.
    """
    message = state["messages"][-1].content

    # Define the prompt template
    prompt_template = """
    You are an expert at routing a user question to either the generation stage or web search. 
    Use the web search for questions that require more context for a better answer or recent events.
    Otherwise, you can skip and go straight to the generation phase to respond.
    You do not need to be stringent with the keywords in the question related to these topics.
    Give a binary choice 'web_search' or 'generate' based on the question. 
    Return the JSON with a single key 'choice' with no preamble or explanation. 
    
    Question to route: {QUESTION} 
    """

    # Create the chat prompt from the template
    prompt = ChatPromptTemplate.from_template(prompt_template)

    # Build the chain to process the input question
    chain = (
        {"QUESTION": RunnablePassthrough()} |
        prompt |
        llm |
        JsonOutputParser()
    )

    # Invoke the chain to get the response
    chain_response = chain.invoke({"QUESTION": message})

    # Return the response
    return {
        "router_state": AIMessage(content=chain_response['choice'])
    }


def condition_between_generation_and_web_search(state: GraphState):
    """
    Condition that takes the output of the router and
    determines which path to take in the graph.

    If the output of the router is 'web_search', then the condition
    returns 'web_search'. Otherwise, it returns 'generate'.
    """
    router_state = state["router_state"][-1].content

    print(router_state)

    if router_state == "web_search":
        # If the router says to web search, then go to the web search node
        return "web_search"
    else:
        # Otherwise, go to the generation node
        return "generate"






    
