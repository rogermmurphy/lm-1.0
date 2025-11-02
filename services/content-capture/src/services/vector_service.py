"""
Vector Service - Handles vector embeddings and similarity search
Supports ChromaDB and Qdrant vector databases
"""
import asyncio
import uuid
from typing import List, Dict, Any, Optional
import chromadb
from chromadb.config import Settings as ChromaSettings
from sentence_transformers import SentenceTransformer
import numpy as np
from config import settings

class VectorService:
    """Vector service for creating and managing embeddings"""
    
    def __init__(self):
        self.db_type = settings.VECTOR_DB_TYPE
        self.embedding_model = None
        self.chroma_client = None
        self.collection_name = "content_embeddings"
        
        # Initialize embedding model
        self._init_embedding_model()
        
        # Initialize vector database
        if self.db_type == "chroma":
            self._init_chroma()
        elif self.db_type == "qdrant":
            self._init_qdrant()
    
    def _init_embedding_model(self):
        """Initialize the sentence transformer model"""
        try:
            self.embedding_model = SentenceTransformer(settings.EMBEDDING_MODEL)
        except Exception as e:
            print(f"Failed to load embedding model: {e}")
            # Fallback to a smaller model
            self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
    
    def _init_chroma(self):
        """Initialize ChromaDB client"""
        try:
            # Connect to ChromaDB server
            self.chroma_client = chromadb.HttpClient(
                host=settings.CHROMA_HOST,
                port=settings.CHROMA_PORT
            )
            
            # Get or create collection
            try:
                self.collection = self.chroma_client.get_collection(
                    name=self.collection_name
                )
            except Exception:
                # Create collection if it doesn't exist
                self.collection = self.chroma_client.create_collection(
                    name=self.collection_name,
                    metadata={"description": "Content embeddings for photos, textbooks, and audio"}
                )
                
        except Exception as e:
            print(f"Failed to initialize ChromaDB: {e}")
            # Fallback to persistent client
            self.chroma_client = chromadb.PersistentClient(path="./chroma_db")
            try:
                self.collection = self.chroma_client.get_collection(
                    name=self.collection_name
                )
            except Exception:
                self.collection = self.chroma_client.create_collection(
                    name=self.collection_name
                )
    
    def _init_qdrant(self):
        """Initialize Qdrant client (placeholder for future implementation)"""
        # TODO: Implement Qdrant support
        raise NotImplementedError("Qdrant support not yet implemented")
    
    async def create_embedding(self, text: str, metadata: Dict[str, Any]) -> str:
        """Create vector embedding for text content"""
        
        if not text or not text.strip():
            raise ValueError("Text content cannot be empty")
        
        try:
            # Generate unique ID
            vector_id = str(uuid.uuid4())
            
            # Create embedding
            loop = asyncio.get_event_loop()
            embedding = await loop.run_in_executor(
                None, 
                self.embedding_model.encode, 
                text
            )
            
            # Convert to list for storage
            embedding_list = embedding.tolist()
            
            # Store in vector database
            if self.db_type == "chroma":
                await self._store_in_chroma(vector_id, text, embedding_list, metadata)
            
            return vector_id
            
        except Exception as e:
            print(f"Failed to create embedding: {e}")
            raise
    
    async def _store_in_chroma(self, vector_id: str, text: str, embedding: List[float], metadata: Dict[str, Any]):
        """Store embedding in ChromaDB"""
        
        # Prepare metadata (ChromaDB requires string values)
        chroma_metadata = {}
        for key, value in metadata.items():
            if value is not None:
                chroma_metadata[key] = str(value)
        
        # Add the embedding
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(
            None,
            lambda: self.collection.add(
                ids=[vector_id],
                embeddings=[embedding],
                documents=[text],
                metadatas=[chroma_metadata]
            )
        )
    
    async def search_similar(self, query_text: str, limit: int = 10, filters: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """Search for similar content using vector similarity"""
        
        try:
            # Create query embedding
            loop = asyncio.get_event_loop()
            query_embedding = await loop.run_in_executor(
                None,
                self.embedding_model.encode,
                query_text
            )
            
            # Prepare filters for ChromaDB
            where_clause = None
            if filters:
                where_clause = {}
                for key, value in filters.items():
                    if value is not None:
                        where_clause[key] = str(value)
            
            # Search in vector database
            if self.db_type == "chroma":
                results = await loop.run_in_executor(
                    None,
                    lambda: self.collection.query(
                        query_embeddings=[query_embedding.tolist()],
                        n_results=limit,
                        where=where_clause,
                        include=["documents", "metadatas", "distances"]
                    )
                )
                
                # Format results
                formatted_results = []
                if results['ids'] and len(results['ids']) > 0:
                    for i in range(len(results['ids'][0])):
                        formatted_results.append({
                            "id": results['ids'][0][i],
                            "document": results['documents'][0][i],
                            "metadata": results['metadatas'][0][i],
                            "distance": results['distances'][0][i],
                            "similarity": 1 - results['distances'][0][i]  # Convert distance to similarity
                        })
                
                return formatted_results
            
        except Exception as e:
            print(f"Failed to search similar content: {e}")
            return []
    
    async def delete_embedding(self, vector_id: str) -> bool:
        """Delete an embedding from the vector database"""
        
        try:
            if self.db_type == "chroma":
                loop = asyncio.get_event_loop()
                await loop.run_in_executor(
                    None,
                    lambda: self.collection.delete(ids=[vector_id])
                )
            
            return True
            
        except Exception as e:
            print(f"Failed to delete embedding: {e}")
            return False
    
    async def update_embedding(self, vector_id: str, text: str, metadata: Dict[str, Any]) -> bool:
        """Update an existing embedding"""
        
        try:
            # Delete old embedding
            await self.delete_embedding(vector_id)
            
            # Create new embedding with same ID
            loop = asyncio.get_event_loop()
            embedding = await loop.run_in_executor(
                None,
                self.embedding_model.encode,
                text
            )
            
            # Store updated embedding
            if self.db_type == "chroma":
                await self._store_in_chroma(vector_id, text, embedding.tolist(), metadata)
            
            return True
            
        except Exception as e:
            print(f"Failed to update embedding: {e}")
            return False
    
    async def get_embedding_info(self, vector_id: str) -> Optional[Dict[str, Any]]:
        """Get information about a specific embedding"""
        
        try:
            if self.db_type == "chroma":
                loop = asyncio.get_event_loop()
                results = await loop.run_in_executor(
                    None,
                    lambda: self.collection.get(
                        ids=[vector_id],
                        include=["documents", "metadatas"]
                    )
                )
                
                if results['ids'] and len(results['ids']) > 0:
                    return {
                        "id": results['ids'][0],
                        "document": results['documents'][0],
                        "metadata": results['metadatas'][0]
                    }
            
            return None
            
        except Exception as e:
            print(f"Failed to get embedding info: {e}")
            return None
    
    def get_collection_stats(self) -> Dict[str, Any]:
        """Get statistics about the vector collection"""
        
        try:
            if self.db_type == "chroma":
                count = self.collection.count()
                return {
                    "total_embeddings": count,
                    "collection_name": self.collection_name,
                    "embedding_model": settings.EMBEDDING_MODEL
                }
            
        except Exception as e:
            print(f"Failed to get collection stats: {e}")
            return {"error": str(e)}
