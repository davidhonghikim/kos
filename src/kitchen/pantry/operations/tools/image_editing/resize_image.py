"""
Image Resize Operation

Single-purpose module for resizing images.
"""

from PIL import Image
from pathlib import Path
from typing import Dict, Any
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class ImageResizer:
    """Resize image operation"""
    
    def resize(self, image_path: str, width: int, height: int, output_path: str) -> Dict[str, Any]:
        try:
            image_path = Path(image_path)
            output_path = Path(output_path)
            if not image_path.exists():
                return {
                    'success': False,
                    'error': f'Image not found: {image_path}',
                    'operation': 'resize_image'
                }
            with Image.open(image_path) as img:
                resized = img.resize((width, height))
                output_path.parent.mkdir(parents=True, exist_ok=True)
                resized.save(output_path)
            return {
                'success': True,
                'operation': 'resize_image',
                'input_path': str(image_path),
                'output_path': str(output_path),
                'new_dimensions': f"{width}x{height}",
                'timestamp': datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"Error resizing image {image_path}: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'operation': 'resize_image',
                'input_path': str(image_path),
                'output_path': str(output_path)
            } 