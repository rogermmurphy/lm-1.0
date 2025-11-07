"""
Web Research Tools
Tools for searching the web, fetching URLs, and retrieving library documentation
Uses Firecrawl and Context7 APIs directly
"""
from langchain.tools import tool
import requests
import os
from typing import Optional
from lm_common.logging import get_logger

logger = get_logger(__name__)

# Get API keys from environment
FIRECRAWL_API_KEY = os.getenv("FIRECRAWL_API_KEY", "fc-f67a516b10704b3b8d510c1761568596")
CONTEXT7_API_KEY = os.getenv("CONTEXT7_API_KEY", "ctx7sk-ce9bd595-1c57-4cd4-a6fd-3577201868c6")


@tool
def search_web(query: str, limit: int = 5) -> str:
    """
    Search the web using Firecrawl search API.
    
    Use this when the user asks questions about current events, recent information,
    or topics not in your training data. Returns relevant search results.
    
    Args:
        query: Search query
        limit: Maximum number of results (default: 5)
    
    Returns:
        Formatted search results with titles, URLs, and content snippets
    """
    try:
        logger.info(f"Searching web for: {query}")
        
        url = "https://api.firecrawl.dev/v1/search"
        headers = {
            "Authorization": f"Bearer {FIRECRAWL_API_KEY}",
            "Content-Type": "application/json"
        }
        payload = {
            "query": query,
            "limit": limit,
            "scrapeOptions": {
                "formats": ["markdown"]
            }
        }
        
        response = requests.post(url, json=payload, headers=headers, timeout=30)
        response.raise_for_status()
        
        data = response.json()
        
        if not data.get("success") or not data.get("data"):
            return f"No results found for: {query}"
        
        results = []
        for i, item in enumerate(data["data"][:limit], 1):
            title = item.get("title", "No title")
            url = item.get("url", "No URL")
            markdown = item.get("markdown", "")
            
            # Get first 300 chars of content
            snippet = markdown[:300] + "..." if len(markdown) > 300 else markdown
            
            results.append(f"{i}. **{title}**\nURL: {url}\n{snippet}\n")
        
        return "\n".join(results)
        
    except requests.exceptions.Timeout:
        logger.error("Firecrawl search timed out")
        return "Search request timed out. Please try again with a more specific query."
    except requests.exceptions.RequestException as e:
        logger.error(f"Firecrawl search failed: {e}")
        return f"Search failed: {str(e)}"
    except Exception as e:
        logger.error(f"Unexpected error in search_web: {e}")
        return f"An error occurred while searching: {str(e)}"


@tool
def fetch_url(url: str) -> str:
    """
    Fetch and extract content from a specific URL using Firecrawl scrape API.
    
    Use this when you need to get the full content of a specific webpage,
    such as documentation, articles, or other web resources.
    
    Args:
        url: The URL to fetch
    
    Returns:
        Markdown content of the page
    """
    try:
        logger.info(f"Fetching URL: {url}")
        
        api_url = "https://api.firecrawl.dev/v1/scrape"
        headers = {
            "Authorization": f"Bearer {FIRECRAWL_API_KEY}",
            "Content-Type": "application/json"
        }
        payload = {
            "url": url,
            "formats": ["markdown"]
        }
        
        response = requests.post(api_url, json=payload, headers=headers, timeout=30)
        response.raise_for_status()
        
        data = response.json()
        
        if not data.get("success"):
            return f"Failed to fetch URL: {url}"
        
        markdown = data.get("data", {}).get("markdown", "")
        
        if not markdown:
            return f"No content found at URL: {url}"
        
        # Limit to first 5000 chars to avoid token overflow
        if len(markdown) > 5000:
            markdown = markdown[:5000] + "\n\n[Content truncated for length...]"
        
        return f"Content from {url}:\n\n{markdown}"
        
    except requests.exceptions.Timeout:
        logger.error("URL fetch timed out")
        return f"Request timed out while fetching: {url}"
    except requests.exceptions.RequestException as e:
        logger.error(f"URL fetch failed: {e}")
        return f"Failed to fetch URL: {str(e)}"
    except Exception as e:
        logger.error(f"Unexpected error in fetch_url: {e}")
        return f"An error occurred while fetching the URL: {str(e)}"


@tool
def get_documentation(library_name: str, topic: Optional[str] = None) -> str:
    """
    Get up-to-date documentation for a programming library or framework using Context7 API.
    
    Use this when the user asks about how to use a specific library, framework, or API.
    Examples: React, Next.js, Python libraries, etc.
    
    Args:
        library_name: Name of the library/framework (e.g., "react", "next.js", "fastapi")
        topic: Optional specific topic to focus on (e.g., "hooks", "routing")
    
    Returns:
        Relevant documentation for the library
    """
    try:
        logger.info(f"Fetching documentation for: {library_name}, topic: {topic}")
        
        # First, resolve the library ID
        resolve_url = "https://api.context7.io/v1/libraries/search"
        headers = {
            "Authorization": f"Bearer {CONTEXT7_API_KEY}",
            "Content-Type": "application/json"
        }
        
        response = requests.get(f"{resolve_url}?q={library_name}", headers=headers, timeout=15)
        response.raise_for_status()
        
        libraries = response.json()
        
        if not libraries or len(libraries) == 0:
            return f"No documentation found for library: {library_name}"
        
        # Get the first match
        library_id = libraries[0].get("id")
        
        if not library_id:
            return f"Could not resolve library ID for: {library_name}"
        
        # Now get the docs
        docs_url = "https://api.context7.io/v1/docs"
        payload = {
            "libraryId": library_id,
            "tokens": 3000  # Limit token count
        }
        
        if topic:
            payload["topic"] = topic
        
        response = requests.post(docs_url, json=payload, headers=headers, timeout=20)
        response.raise_for_status()
        
        data = response.json()
        documentation = data.get("documentation", "")
        
        if not documentation:
            return f"No documentation content available for {library_name}"
        
        result = f"Documentation for {library_name}"
        if topic:
            result += f" (topic: {topic})"
        result += f":\n\n{documentation}"
        
        return result
        
    except requests.exceptions.Timeout:
        logger.error("Documentation fetch timed out")
        return f"Request timed out while fetching documentation for: {library_name}"
    except requests.exceptions.RequestException as e:
        logger.error(f"Documentation fetch failed: {e}")
        return f"Failed to fetch documentation: {str(e)}"
    except Exception as e:
        logger.error(f"Unexpected error in get_documentation: {e}")
        return f"An error occurred while fetching documentation: {str(e)}"
