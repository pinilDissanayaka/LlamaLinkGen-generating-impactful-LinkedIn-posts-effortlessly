from langchain_core.prompts import PromptTemplate
from utils import llm, GraphState
from datetime import datetime
from langchain_core.runnables import RunnablePassthrough
from  langchain_core.output_parsers import JsonOutputParser, StrOutputParser
from langchain_community.tools import DuckDuckGoSearchResults
from langchain_community.utilities import DuckDuckGoSearchAPIWrapper
from langchain_core.messages import AIMessage, ToolMessage, HumanMessage



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

    llm_with_tools = llm.bind_tools([DuckDuckGoSearchResults(api_wrapper=DuckDuckGoSearchAPIWrapper())])


    market_researcher_chain = (
        {"LINKEDIN_ACCOUNT_DESCRIPTION": RunnablePassthrough(), "CURRENT_DATE":RunnablePassthrough()} |
        market_researcher_prompt |
        llm_with_tools 
    )


    market_researcher_chain_response = market_researcher_chain.invoke(
        {"LINKEDIN_ACCOUNT_DESCRIPTION" : message, "CURRENT_DATE": current_date}
    )

    return {
        "messages": market_researcher_chain_response
    }






