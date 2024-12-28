from utils import llm, GraphState
from langchain_core.runnables import RunnablePassthrough
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.messages import AIMessage


def chart_generator(state:GraphState)->GraphState:
    message=state["messages"][-1].content

    chart_generator_prompt_template="""
        Take the data and chart specifications provided by the researcher agent.
        If the provided data is insufficient to draw the chart, 
        ask for the missing details, being specific about what is needed. 
        Do not ask for information that is already provided. 
        You must ask for clarification or additional data at least once. 
        When asking any question to the researcher, include the phrase 
        QUESTION_TO_RESEARCHER in your response, 
        otherwise the researcher will not answer.
        Once you have enough information, return the Json data to be used 
        for the chart.
            provided_data: {PROVIDED_DATA}
        
    """

    chart_generator_prompt=PromptTemplate.from_template(
        template=chart_generator_prompt_template
    )

    chart_generator_chain=(
        {"PROVIDED_DATA" : RunnablePassthrough()} |
        chart_generator_prompt |
        llm  
    )

    chart_generator_response=chart_generator_chain.invoke(
        {"PROVIDED_DATA" : message}
    )

    return {
        "messages": AIMessage(content=chart_generator_response)
    }



