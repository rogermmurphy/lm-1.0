"""
Content Loader - Load educational content into ChromaDB
Supports: PDFs, text files, markdown, and plain text
"""

import chromadb
from chromadb.config import Settings
import os
import sys
from typing import List, Dict
import uuid

class ContentLoader:
    def __init__(self, chroma_host="localhost", chroma_port=8000):
        """Initialize connection to ChromaDB"""
        self.client = chromadb.HttpClient(
            host=chroma_host,
            port=chroma_port,
            settings=Settings(allow_reset=True)
        )
        print(f"[OK] Connected to ChromaDB at {chroma_host}:{chroma_port}")
    
    def create_collection(self, collection_name="education"):
        """Create or get a collection for educational content"""
        try:
            collection = self.client.get_or_create_collection(
                name=collection_name,
                metadata={"description": "Educational content for study assistance"}
            )
            print(f"[OK] Collection '{collection_name}' ready")
            return collection
        except Exception as e:
            print(f"[ERROR] Error creating collection: {e}")
            raise
    
    def chunk_text(self, text: str, chunk_size: int = 1000, overlap: int = 200) -> List[str]:
        """Split text into overlapping chunks"""
        chunks = []
        start = 0
        text_length = len(text)
        
        while start < text_length:
            end = start + chunk_size
            chunk = text[start:end]
            chunks.append(chunk)
            start += (chunk_size - overlap)
        
        return chunks
    
    def load_text_file(self, file_path: str, collection_name="education", metadata: Dict = None):
        """Load a text file into ChromaDB"""
        try:
            # Read file
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Get collection
            collection = self.create_collection(collection_name)
            
            # Chunk the content
            chunks = self.chunk_text(content)
            
            # Prepare metadata
            if metadata is None:
                metadata = {}
            metadata['source'] = os.path.basename(file_path)
            metadata['file_path'] = file_path
            metadata['file_type'] = 'text'
            
            # Add chunks to collection
            ids = []
            documents = []
            metadatas = []
            
            for i, chunk in enumerate(chunks):
                chunk_id = f"{os.path.basename(file_path)}_{i}_{uuid.uuid4().hex[:8]}"
                ids.append(chunk_id)
                documents.append(chunk)
                chunk_metadata = metadata.copy()
                chunk_metadata['chunk_index'] = i
                metadatas.append(chunk_metadata)
            
            collection.add(
                ids=ids,
                documents=documents,
                metadatas=metadatas
            )
            
            print(f"[OK] Loaded {len(chunks)} chunks from {file_path}")
            return len(chunks)
            
        except Exception as e:
            print(f"[ERROR] Error loading file {file_path}: {e}")
            raise
    
    def load_text_content(self, content: str, source_name: str, collection_name="education", metadata: Dict = None):
        """Load raw text content into ChromaDB"""
        try:
            # Get collection
            collection = self.create_collection(collection_name)
            
            # Chunk the content
            chunks = self.chunk_text(content)
            
            # Prepare metadata
            if metadata is None:
                metadata = {}
            metadata['source'] = source_name
            metadata['file_type'] = 'text'
            
            # Add chunks to collection
            ids = []
            documents = []
            metadatas = []
            
            for i, chunk in enumerate(chunks):
                chunk_id = f"{source_name}_{i}_{uuid.uuid4().hex[:8]}"
                ids.append(chunk_id)
                documents.append(chunk)
                chunk_metadata = metadata.copy()
                chunk_metadata['chunk_index'] = i
                metadatas.append(chunk_metadata)
            
            collection.add(
                ids=ids,
                documents=documents,
                metadatas=metadatas
            )
            
            print(f"[OK] Loaded {len(chunks)} chunks from {source_name}")
            return len(chunks)
            
        except Exception as e:
            print(f"[ERROR] Error loading content: {e}")
            raise
    
    def list_collections(self):
        """List all collections in ChromaDB"""
        try:
            collections = self.client.list_collections()
            print(f"\nCollections in ChromaDB:")
            for col in collections:
                count = col.count()
                print(f"  - {col.name}: {count} documents")
            return collections
        except Exception as e:
            print(f"[ERROR] Error listing collections: {e}")
            raise
    
    def get_collection_info(self, collection_name="education"):
        """Get information about a collection"""
        try:
            collection = self.client.get_collection(collection_name)
            count = collection.count()
            print(f"\nCollection '{collection_name}':")
            print(f"  - Document count: {count}")
            
            # Get a sample document
            if count > 0:
                results = collection.peek(limit=1)
                print(f"  - Sample document: {results['documents'][0][:100]}...")
            
            return collection
        except Exception as e:
            print(f"[ERROR] Error getting collection info: {e}")
            raise

def main():
    """Test the content loader"""
    if len(sys.argv) < 2:
        print("Usage: python content_loader.py <file_path>")
        print("Example: python content_loader.py test_content/biology.txt")
        sys.exit(1)
    
    file_path = sys.argv[1]
    
    if not os.path.exists(file_path):
        print(f"[ERROR] File not found: {file_path}")
        sys.exit(1)
    
    # Load content
    loader = ContentLoader()
    loader.load_text_file(file_path)
    
    # Show collections
    loader.list_collections()
    loader.get_collection_info()

if __name__ == "__main__":
    main()
