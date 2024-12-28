from langchain_core.prompts import PromptTemplate
from datetime import datetime

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



print(datetime.now().strftime("%Y-%m-%d"))




