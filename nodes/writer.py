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


def writer(state:GraphState):
    print("at the writer node")
    question=state["messages"][0].content
    context=state["messages"][1].content


    writer_prompt_template="""
            You are an AI assistant that synthesizes web search results to 
            create engaging and informative LinkedIn posts that are clear, 
            concise, and appealing to professionals on LinkedIn. 
            Make sure the tone is professional yet approachable, and include 
            actionable insights, tips, or thought-provoking points 
            that would resonate with the LinkedIn audience. 
            If you don't know, just say that you don't know.
            Only make direct references to material if provided in the context.
                Question: {QUESTION} 
                Context: {CONTEXT}
    """

    writer_prompt=PromptTemplate.from_template(writer_prompt_template)


    writer_chain=(
        {"QUESTION": RunnablePassthrough(), "CONTEXT": RunnablePassthrough()} |
        writer_prompt |
        llm 
    )

    writer_response=writer_chain.invoke({
        "QUESTION": question,
        "CONTEXT": context
    })

    return {
        "messages": writer_response.content
    }




