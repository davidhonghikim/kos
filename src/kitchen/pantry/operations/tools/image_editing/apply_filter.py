"""
Image Filter Operation

Single-purpose module for applying a filter to an image.
"""

from PIL import Image, ImageFilter
from pathlib import Path
from typing import Dict, Any
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class ImageFilterer:
    """Apply filter to image operation"""
    
    def apply_filter(self, image_path: str, filter_name: str, output_path: str) -> Dict[str, Any]:
        try:
            image_path = Path(image_path)
            output_path = Path(output_path)
            if not image_path.exists():
                return {
                    'success': False,
                    'error': f'Image not found: {image_path}',
                    'operation': 'apply_filter'
                }
            with Image.open(image_path) as img:
                filter_map = {
                    'BLUR': ImageFilter.BLUR,
                    'CONTOUR': ImageFilter.CONTOUR,
                    'DETAIL': ImageFilter.DETAIL,
                    'EDGE_ENHANCE': ImageFilter.EDGE_ENHANCE,
                    'SHARPEN': ImageFilter.SHARPEN
                }
                if filter_name not in filter_map:
                    return {
                        'success': False,
                        'error': f'Unsupported filter: {filter_name}',
                        'operation': 'apply_filter'
                    }
                filtered = img.filter(filter_map[filter_name])
                output_path.parent.mkdir(parents=True, exist_ok=True)
                filtered.save(output_path)
            return {
                'success': True,
                'operation': 'apply_filter',
                'input_path': str(image_path),
                'output_path': str(output_path),
                'filter': filter_name,
                'timestamp': datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"Error applying filter to image {image_path}: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'operation': 'apply_filter',
                'input_path': str(image_path),
                'output_path': str(output_path)
            } 