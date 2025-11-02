"""
OCR Service - Text extraction from images
Supports multiple OCR providers: Tesseract, Azure Computer Vision
"""
import os
import asyncio
from typing import Optional
from PIL import Image
import pytesseract
import requests
import base64
from config import settings

class OCRService:
    """OCR service for extracting text from images"""
    
    def __init__(self):
        self.provider = settings.OCR_PROVIDER
        
        # Configure Tesseract if using local OCR
        if self.provider == "tesseract":
            # Try to find tesseract executable
            tesseract_paths = [
                r"C:\Program Files\Tesseract-OCR\tesseract.exe",
                r"C:\Users\roger\AppData\Local\Tesseract-OCR\tesseract.exe",
                "/usr/bin/tesseract",
                "/usr/local/bin/tesseract"
            ]
            
            for path in tesseract_paths:
                if os.path.exists(path):
                    pytesseract.pytesseract.tesseract_cmd = path
                    break
    
    async def extract_text(self, image_path: str) -> str:
        """Extract text from image using configured OCR provider"""
        
        if self.provider == "tesseract":
            return await self._extract_with_tesseract(image_path)
        elif self.provider == "azure":
            return await self._extract_with_azure(image_path)
        else:
            raise ValueError(f"Unsupported OCR provider: {self.provider}")
    
    async def _extract_with_tesseract(self, image_path: str) -> str:
        """Extract text using Tesseract OCR"""
        try:
            # Run OCR in thread pool to avoid blocking
            loop = asyncio.get_event_loop()
            
            def run_ocr():
                # Open and preprocess image
                image = Image.open(image_path)
                
                # Convert to RGB if necessary
                if image.mode != 'RGB':
                    image = image.convert('RGB')
                
                # Extract text with custom config for better accuracy
                custom_config = r'--oem 3 --psm 6 -c tessedit_char_whitelist=0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz .,!?;:()[]{}"\'-+=/\\@#$%^&*'
                text = pytesseract.image_to_string(image, config=custom_config)
                
                return text.strip()
            
            text = await loop.run_in_executor(None, run_ocr)
            return text
            
        except Exception as e:
            print(f"Tesseract OCR failed: {e}")
            return ""
    
    async def _extract_with_azure(self, image_path: str) -> str:
        """Extract text using Azure Computer Vision OCR"""
        
        if not settings.AZURE_VISION_KEY or not settings.AZURE_VISION_ENDPOINT:
            raise ValueError("Azure Vision credentials not configured")
        
        try:
            # Read image file
            with open(image_path, 'rb') as image_file:
                image_data = image_file.read()
            
            # Azure Computer Vision Read API
            headers = {
                'Ocp-Apim-Subscription-Key': settings.AZURE_VISION_KEY,
                'Content-Type': 'application/octet-stream'
            }
            
            # Start read operation
            read_url = f"{settings.AZURE_VISION_ENDPOINT}/vision/v3.2/read/analyze"
            
            response = requests.post(read_url, headers=headers, data=image_data)
            response.raise_for_status()
            
            # Get operation location
            operation_location = response.headers['Operation-Location']
            
            # Poll for results
            max_attempts = 10
            for attempt in range(max_attempts):
                await asyncio.sleep(1)  # Wait 1 second between polls
                
                result_response = requests.get(
                    operation_location,
                    headers={'Ocp-Apim-Subscription-Key': settings.AZURE_VISION_KEY}
                )
                result_response.raise_for_status()
                result = result_response.json()
                
                if result['status'] == 'succeeded':
                    # Extract text from results
                    text_lines = []
                    for page in result['analyzeResult']['readResults']:
                        for line in page['lines']:
                            text_lines.append(line['text'])
                    
                    return '\n'.join(text_lines)
                
                elif result['status'] == 'failed':
                    raise Exception("Azure OCR failed")
            
            raise Exception("Azure OCR timed out")
            
        except Exception as e:
            print(f"Azure OCR failed: {e}")
            return ""
    
    def validate_image(self, image_path: str) -> bool:
        """Validate that the image file is readable"""
        try:
            with Image.open(image_path) as img:
                img.verify()
            return True
        except Exception:
            return False
    
    def get_image_info(self, image_path: str) -> dict:
        """Get basic information about the image"""
        try:
            with Image.open(image_path) as img:
                return {
                    "format": img.format,
                    "mode": img.mode,
                    "size": img.size,
                    "width": img.width,
                    "height": img.height
                }
        except Exception as e:
            return {"error": str(e)}
