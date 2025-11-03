"""
Content Service - Educational Content Integration
Provides access to educational content from various sources
"""
import wikipediaapi
from typing import List, Dict, Any, Optional


class ContentService:
    """Service for fetching educational content from external sources"""
    
    def __init__(self):
        """Initialize content service with Wikipedia API"""
        self.wiki = wikipediaapi.Wikipedia(
            language='en',
            extract_format=wikipediaapi.ExtractFormat.WIKI,
            user_agent='LittleMonsterGPA/1.0 (Educational Platform)'
        )
    
    def search_wikipedia(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        """
        Search Wikipedia for educational content
        
        Args:
            query: Search query
            limit: Maximum number of results (default: 5)
            
        Returns:
            List of search results with titles and summaries
        """
        try:
            # Get page
            page = self.wiki.page(query)
            
            if not page.exists():
                return []
            
            # Return page summary
            return [{
                'title': page.title,
                'summary': page.summary[:500] + '...' if len(page.summary) > 500 else page.summary,
                'url': page.fullurl,
                'source': 'Wikipedia'
            }]
            
        except Exception as e:
            print(f"Wikipedia search error: {e}")
            return []
    
    def get_wikipedia_article(self, title: str) -> Optional[Dict[str, Any]]:
        """
        Get full Wikipedia article content
        
        Args:
            title: Article title
            
        Returns:
            Article data with full content or None if not found
        """
        try:
            page = self.wiki.page(title)
            
            if not page.exists():
                return None
            
            return {
                'title': page.title,
                'summary': page.summary,
                'content': page.text,
                'url': page.fullurl,
                'categories': list(page.categories.keys())[:10],
                'sections': [section.title for section in page.sections],
                'source': 'Wikipedia'
            }
            
        except Exception as e:
            print(f"Wikipedia article error: {e}")
            return None
    
    def extract_key_concepts(self, text: str, max_concepts: int = 10) -> List[str]:
        """
        Extract key concepts from text (simple implementation)
        
        Args:
            text: Text to analyze
            max_concepts: Maximum concepts to return
            
        Returns:
            List of key concept phrases
        """
        # Simple implementation: extract capitalized phrases
        # In production, would use NLP/NER
        words = text.split()
        concepts = []
        
        for i, word in enumerate(words):
            if word and word[0].isupper() and len(word) > 3:
                concepts.append(word)
        
        # Remove duplicates and limit
        unique_concepts = list(dict.fromkeys(concepts))
        return unique_concepts[:max_concepts]
    
    def aggregate_content(self, topic: str) -> Dict[str, Any]:
        """
        Aggregate content from multiple sources
        
        Args:
            topic: Topic to search for
            
        Returns:
            Aggregated content from various sources
        """
        results = {
            'topic': topic,
            'sources': []
        }
        
        # Get Wikipedia content
        wiki_results = self.search_wikipedia(topic)
        if wiki_results:
            results['sources'].extend(wiki_results)
        
        # Could add more sources here (OpenLibrary, arXiv, etc.)
        # For Phase 9.6, Wikipedia provides solid foundation
        
        return results


# Singleton instance
_content_service = None

def get_content_service() -> ContentService:
    """Get singleton ContentService instance"""
    global _content_service
    if _content_service is None:
        _content_service = ContentService()
    return _content_service
