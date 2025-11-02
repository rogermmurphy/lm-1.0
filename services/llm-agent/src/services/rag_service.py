"""
LLM Agent Service - RAG Service
Retrieval Augmented Generation using ChromaDB
Extracted from POC 00 - Tested and Validated
"""
import chromadb
from chromadb.config import Settings
from typing import List, Dict, Optional
from ..config import settings


class RAGService:
    """RAG service for retrieving relevant context from ChromaDB"""
    
    def __init__(self):
        """Initialize ChromaDB client (lazy connection)"""
        self.client = None
        self.collection_name = "education"
    
    def _get_client(self):
        """Lazy load ChromaDB client"""
        if self.client is None:
            try:
                self.client = chromadb.HttpClient(
                    host=settings.CHROMADB_HOST,
                    port=settings.CHROMADB_PORT,
                    settings=Settings(allow_reset=True)
                )
            except Exception as e:
                print(f"Warning: Could not connect to ChromaDB: {e}")
                return None
        return self.client
    
    def search_content(
        self,
        query: str,
        collection_name: Optional[str] = None,
        n_results: int = 3
    ) -> Dict:
        """
        Search for relevant content in ChromaDB
        
        Args:
            query: Search query
            collection_name: Collection to search (default: education)
            n_results: Number of results to return
            
        Returns:
            Dictionary with documents, metadatas, distances
        """
        try:
            client = self._get_client()
            if not client:
                return {"documents": [[]], "metadatas": [[]], "distances": [[]]}
            
            coll_name = collection_name or self.collection_name
            collection = client.get_or_create_collection(coll_name)
            
            results = collection.query(
                query_texts=[query],
                n_results=n_results
            )
            
            return results
        except Exception as e:
            print(f"Error searching content: {e}")
            return {
                "documents": [[]],
                "metadatas": [[]],
                "distances": [[]]
            }
    
    def get_context_for_query(
        self,
        query: str,
        n_results: int = 3
    ) -> tuple[str, List[Dict]]:
        """
        Get formatted context and sources for a query
        
        Args:
            query: User question
            n_results: Number of context chunks to retrieve
            
        Returns:
            Tuple of (context_text, sources_list)
        """
        search_results = self.search_content(query, n_results=n_results)
        
        documents = search_results['documents'][0] if search_results['documents'] else []
        metadatas = search_results['metadatas'][0] if search_results['metadatas'] else []
        distances = search_results['distances'][0] if search_results['distances'] else []
        
        if not documents:
            return "", []
        
        # Format context
        context = "\n\n---\n\n".join(documents)
        
        # Format sources
        sources = []
        for i, metadata in enumerate(metadatas):
            sources.append({
                "source": metadata.get("source", "Unknown"),
                "relevance_score": 1 - distances[i] if i < len(distances) else 0,
                "chunk_index": metadata.get("chunk_index", i)
            })
        
        return context, sources
    
    def add_document(
        self,
        text: str,
        metadata: Dict,
        collection_name: Optional[str] = None
    ) -> str:
        """
        Add a document to the vector database
        
        Args:
            text: Document text
            metadata: Document metadata
            collection_name: Collection name
            
        Returns:
            Document ID
        """
        try:
            client = self._get_client()
            if not client:
                raise Exception("ChromaDB not available")
            
            coll_name = collection_name or self.collection_name
            collection = client.get_or_create_collection(coll_name)
            
            # Generate ID
            doc_id = f"doc_{metadata.get('user_id', 'unknown')}_{metadata.get('material_id', 0)}"
            
            collection.add(
                documents=[text],
                metadatas=[metadata],
                ids=[doc_id]
            )
            
            return doc_id
        except Exception as e:
            raise Exception(f"Failed to add document: {e}")
