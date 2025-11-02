"""
PDF Processor Service - Extract and chunk text from PDF files
"""
import asyncio
from typing import List, Dict, Any
import PyPDF2
import fitz  # PyMuPDF
from io import BytesIO
from config import settings

class PDFProcessor:
    """PDF processing service for text extraction and chunking"""
    
    def __init__(self):
        self.chunk_size = settings.CHUNK_SIZE
        self.chunk_overlap = settings.CHUNK_OVERLAP
    
    def get_pdf_info(self, file_path: str) -> Dict[str, Any]:
        """Get basic information about a PDF file"""
        try:
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                
                return {
                    "page_count": len(pdf_reader.pages),
                    "title": pdf_reader.metadata.get('/Title', '') if pdf_reader.metadata else '',
                    "author": pdf_reader.metadata.get('/Author', '') if pdf_reader.metadata else '',
                    "subject": pdf_reader.metadata.get('/Subject', '') if pdf_reader.metadata else ''
                }
        except Exception as e:
            print(f"Failed to get PDF info: {e}")
            return {"page_count": 0, "error": str(e)}
    
    async def extract_text_pypdf2(self, file_path: str) -> List[Dict[str, Any]]:
        """Extract text using PyPDF2 (fallback method)"""
        
        def extract():
            pages = []
            try:
                with open(file_path, 'rb') as file:
                    pdf_reader = PyPDF2.PdfReader(file)
                    
                    for page_num, page in enumerate(pdf_reader.pages):
                        try:
                            text = page.extract_text()
                            if text.strip():
                                pages.append({
                                    "page_number": page_num + 1,
                                    "content": text.strip()
                                })
                        except Exception as e:
                            print(f"Failed to extract page {page_num + 1}: {e}")
                            continue
                            
            except Exception as e:
                print(f"Failed to read PDF with PyPDF2: {e}")
                
            return pages
        
        # Run in thread pool to avoid blocking
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, extract)
    
    async def extract_text_pymupdf(self, file_path: str) -> List[Dict[str, Any]]:
        """Extract text using PyMuPDF (preferred method)"""
        
        def extract():
            pages = []
            try:
                doc = fitz.open(file_path)
                
                for page_num in range(len(doc)):
                    try:
                        page = doc.load_page(page_num)
                        text = page.get_text()
                        
                        if text.strip():
                            pages.append({
                                "page_number": page_num + 1,
                                "content": text.strip()
                            })
                    except Exception as e:
                        print(f"Failed to extract page {page_num + 1}: {e}")
                        continue
                
                doc.close()
                
            except Exception as e:
                print(f"Failed to read PDF with PyMuPDF: {e}")
                
            return pages
        
        # Run in thread pool to avoid blocking
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, extract)
    
    async def extract_text(self, file_path: str) -> List[Dict[str, Any]]:
        """Extract text from PDF using the best available method"""
        
        # Try PyMuPDF first (better text extraction)
        try:
            pages = await self.extract_text_pymupdf(file_path)
            if pages:
                return pages
        except Exception as e:
            print(f"PyMuPDF extraction failed: {e}")
        
        # Fallback to PyPDF2
        try:
            pages = await self.extract_text_pypdf2(file_path)
            return pages
        except Exception as e:
            print(f"PyPDF2 extraction failed: {e}")
            return []
    
    def chunk_text(self, text: str, page_number: int = None) -> List[Dict[str, Any]]:
        """Split text into chunks with overlap"""
        
        if not text or not text.strip():
            return []
        
        chunks = []
        text = text.strip()
        
        # If text is shorter than chunk size, return as single chunk
        if len(text) <= self.chunk_size:
            return [{
                "content": text,
                "page_number": page_number
            }]
        
        # Split into chunks with overlap
        start = 0
        chunk_index = 0
        
        while start < len(text):
            # Calculate end position
            end = start + self.chunk_size
            
            # If this is not the last chunk, try to break at word boundary
            if end < len(text):
                # Look for the last space within the chunk
                last_space = text.rfind(' ', start, end)
                if last_space > start:
                    end = last_space
            
            # Extract chunk
            chunk_text = text[start:end].strip()
            
            if chunk_text:
                chunks.append({
                    "content": chunk_text,
                    "page_number": page_number,
                    "chunk_index": chunk_index
                })
                chunk_index += 1
            
            # Move start position with overlap
            if end >= len(text):
                break
                
            start = end - self.chunk_overlap
            
            # Ensure we don't go backwards
            if start < 0:
                start = 0
        
        return chunks
    
    async def extract_and_chunk(self, file_path: str) -> List[Dict[str, Any]]:
        """Extract text from PDF and split into chunks"""
        
        # Extract text by pages
        pages = await self.extract_text(file_path)
        
        if not pages:
            return []
        
        # Chunk each page
        all_chunks = []
        global_chunk_index = 0
        
        for page_data in pages:
            page_chunks = self.chunk_text(
                page_data["content"], 
                page_data["page_number"]
            )
            
            # Add global chunk index
            for chunk in page_chunks:
                chunk["global_chunk_index"] = global_chunk_index
                all_chunks.append(chunk)
                global_chunk_index += 1
        
        return all_chunks
    
    def validate_pdf(self, file_path: str) -> bool:
        """Validate that the file is a readable PDF"""
        try:
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                # Try to access the first page
                if len(pdf_reader.pages) > 0:
                    pdf_reader.pages[0]
                return True
        except Exception:
            return False
    
    async def extract_metadata(self, file_path: str) -> Dict[str, Any]:
        """Extract comprehensive metadata from PDF"""
        
        def extract():
            metadata = {}
            try:
                # Try PyMuPDF first for better metadata
                doc = fitz.open(file_path)
                metadata.update(doc.metadata)
                doc.close()
            except Exception:
                # Fallback to PyPDF2
                try:
                    with open(file_path, 'rb') as file:
                        pdf_reader = PyPDF2.PdfReader(file)
                        if pdf_reader.metadata:
                            for key, value in pdf_reader.metadata.items():
                                # Remove PDF metadata prefixes
                                clean_key = key.replace('/', '').lower()
                                metadata[clean_key] = value
                except Exception as e:
                    metadata["error"] = str(e)
            
            return metadata
        
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, extract)
