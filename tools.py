
from crewai.tools import tool
from typing import List
import os,re
import requests

@tool
def web_search_tool(query:str)->List[dict]:
    """
    Web Search Tool.
    Use this tool to search the web for information about jobs, companies, or anything else.
    Args:
        query:str
          The query to search the web for.
    Returns:
        A list of web search results in markdown format.
    
     """

    url = "https://api.firecrawl.dev/v2/search"

    payload = {
    "query": query,
    "sources": [
        "web"
    ],
    "categories": [],
    "limit": 5,
    "scrapeOptions": {
        "onlyMainContent": True,
        "maxAge": 172800000,
        "parsers": [
        "pdf"
        ],
        "formats": [
        "markdown"
        ]
    }
    }

    headers = {
        "Authorization": f"Bearer {os.getenv("FIRECRAWL_API_KEY")}",
        "Content-Type": "application/json"
    }

    response = requests.post(url, json=payload, headers=headers)

    if not response.json()['success']:
        return "Error occured while using web_search_tool"

    results = response.json()['data']['web']
    cleaned_chunks = []
    for result in results:
        title = result.get('title') or result.get('metadata', {}).get('title', 'No Title')
        url = result.get('url') or result.get('metadata', {}).get('sourceURL', 'No URL')
        description = result.get('description') or result.get('metadata', {}).get('description', '')
        
        markdown_content = result.get('markdown', '')
        cleaned_markdown_content = re.sub(r'\n{3,}', '\n\n', markdown_content).strip()
        
        cleaned_result = {
            "title": title,
            "url": url,
            "description": description,
            "markdown": cleaned_markdown_content
        }
        cleaned_chunks.append(cleaned_result)

    return cleaned_chunks

