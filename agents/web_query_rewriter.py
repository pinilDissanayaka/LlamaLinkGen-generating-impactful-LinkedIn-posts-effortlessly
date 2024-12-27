from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from langchain_core.runnables import RunnablePassthrough
from ..utils import llm


class QueryRewriter(BaseModel):
    re_write_query:str=Field(description="Reword their query with out preamble or explanation.")

def query_rewriter(query: str) -> str:
    prompt_template="""
        You are an expert at crafting web search queries for research questions.
        More often than not, a user will ask a basic question that they wish to learn more about; 
        however, it might not be in the best format. 
        Reword their query to be the most effective web search string possible.
        
            Question to transform: {QUESTION} 
        """

    prompt=ChatPromptTemplate.from_template(prompt_template)


    agent_llm=llm.with_structured_output(QueryRewriter)


    agent_chain=(
        {"QUESTION": RunnablePassthrough()}|
        prompt|
        agent_llm
    )

    agent_response=agent_chain.invoke({"QUESTION":query})

    rewrite_query=agent_response.re_write_query

    return rewrite_query




