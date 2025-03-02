from PIL import Image
import requests
import io
import os
from typing import List

class ImageProcessor:
    @staticmethod
    def download_image(url: str) -> Image.Image:
        response = requests.get(url)
        return Image.open(io.BytesIO(response.content))
    
    @staticmethod
    def compress_image(image: Image.Image, quality: int = 50) -> bytes:
        # Compress image
        buffer = io.BytesIO()
        image.save(buffer, format="JPEG", optimize=True, quality=quality)
        return buffer.getvalue()
    
    @staticmethod
    def save_image(image_bytes: bytes, product_name: str, index: int) -> str:
        # Create storage directory if not exists
        storage_path = os.getenv('STORAGE_PATH', './processed_images')
        os.makedirs(storage_path, exist_ok=True)
        
        # Generate unique filename
        filename = f"{product_name}_{index}.jpg"
        full_path = os.path.join(storage_path, filename)
        
        # Save image
        with open(full_path, 'wb') as f:
            f.write(image_bytes)
        
        return full_path