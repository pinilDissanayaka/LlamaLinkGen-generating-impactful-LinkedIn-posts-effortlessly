
from langchain_core.tools import tool   

@tool
def write_article(article_text: str):
    """
    Writes the provided article text to a file named using the article heading.

    Args:
        article_heading (str): The heading of the article, used to name the file.
        article_text (str): The text content of the article to be written to the file.
    """
    # Open a file with a name based on the article heading, ensuring no conflicts
    with open("article.txt", "w") as f:
        # Write the article text to the file
        f.write(article_text)
