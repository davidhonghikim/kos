"""
Apply Filter Operation

Modular operation for applying filters to images with comprehensive error handling.
"""

import os
import logging
from pathlib import Path
from typing import Dict, Any, Union, Optional

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

try:
    from PIL import Image, ImageEnhance, ImageFilter
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False
    logger.warning("PIL (Pillow) not available. Image operations will not work.")

class ApplyFilterOperation:
    """Apply filters to images with comprehensive error handling and validation."""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """Initialize the apply filter operation.
        
        Args:
            config: Optional configuration dictionary
        """
        self.config = config or {}
        self.available_filters = {
            'blur': self._apply_blur,
            'sharpen': self._apply_sharpen,
            'emboss': self._apply_emboss,
            'edge_enhance': self._apply_edge_enhance,
            'brightness': self._apply_brightness,
            'contrast': self._apply_contrast,
            'saturation': self._apply_saturation,
            'grayscale': self._apply_grayscale,
            'sepia': self._apply_sepia
        }
        
    def apply_filter(self, input_path: Union[str, Path], filter_name: str, 
                    output_path: Optional[Union[str, Path]] = None,
                    filter_strength: float = 1.0) -> Dict[str, Any]:
        """Apply a filter to an image with comprehensive error handling.
        
        Args:
            input_path: Path to the input image
            filter_name: Name of the filter to apply
            output_path: Path for the output image (optional, auto-generated if None)
            filter_strength: Strength of the filter (0.0 to 2.0, default 1.0)
            
        Returns:
            Dictionary containing operation result
        """
        if not PIL_AVAILABLE:
            return {
                'success': False,
                'error': 'PIL (Pillow) is not available. Please install it with: pip install Pillow',
                'input_path': str(input_path),
                'operation': 'apply_filter'
            }
        
        try:
            # Convert paths to Path objects
            input_path = Path(input_path)
            
            # Validate input file
            if not input_path.exists():
                logger.error(f"Input file does not exist: {input_path}")
                return {
                    'success': False,
                    'error': f"Input file does not exist: {input_path}",
                    'input_path': str(input_path),
                    'operation': 'apply_filter'
                }
            
            if not input_path.is_file():
                logger.error(f"Input path is not a file: {input_path}")
                return {
                    'success': False,
                    'error': f"Input path is not a file: {input_path}",
                    'input_path': str(input_path),
                    'operation': 'apply_filter'
                }
            
            # Validate filter name
            if filter_name not in self.available_filters:
                logger.error(f"Unknown filter: {filter_name}")
                return {
                    'success': False,
                    'error': f"Unknown filter: {filter_name}. Available filters: {list(self.available_filters.keys())}",
                    'input_path': str(input_path),
                    'operation': 'apply_filter'
                }
            
            # Validate filter strength
            if not 0.0 <= filter_strength <= 2.0:
                logger.warning(f"Filter strength {filter_strength} is outside recommended range (0.0-2.0)")
            
            # Generate output path if not provided
            if output_path is None:
                output_path = self._generate_output_path(input_path, filter_name)
            else:
                output_path = Path(output_path)
            
            # Create output directory if it doesn't exist
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Open image
            logger.info(f"Opening image: {input_path}")
            with Image.open(input_path) as img:
                # Get original image info
                original_mode = img.mode
                original_size = img.size
                
                # Apply the filter
                logger.info(f"Applying filter '{filter_name}' with strength {filter_strength}")
                filtered_img = self.available_filters[filter_name](img, filter_strength)
                
                # Determine output format and save
                output_format = self._get_output_format(output_path)
                save_kwargs = {}
                
                if output_format.lower() in ['jpg', 'jpeg']:
                    # Convert to RGB if necessary
                    if filtered_img.mode in ('RGBA', 'LA', 'P'):
                        filtered_img = filtered_img.convert('RGB')
                    save_kwargs['quality'] = 95
                    save_kwargs['optimize'] = True
                
                # Save the filtered image
                logger.info(f"Saving filtered image: {output_path}")
                filtered_img.save(output_path, format=output_format, **save_kwargs)
                
                # Verify the output file was created
                if not output_path.exists():
                    logger.error(f"Output file was not created: {output_path}")
                    return {
                        'success': False,
                        'error': f"Output file was not created: {output_path}",
                        'input_path': str(input_path),
                        'operation': 'apply_filter'
                    }
                
                # Get output file size
                output_size = output_path.stat().st_size
                
                # Return success result
                result = {
                    'success': True,
                    'input_path': str(input_path),
                    'output_path': str(output_path),
                    'filter_name': filter_name,
                    'filter_strength': filter_strength,
                    'original_mode': original_mode,
                    'original_size': original_size,
                    'output_format': output_format,
                    'output_size': output_size,
                    'operation': 'apply_filter'
                }
                
                logger.info(f"Successfully applied filter '{filter_name}' to image: {input_path} -> {output_path}")
                return result
                
        except Exception as e:
            logger.error(f"Error applying filter '{filter_name}' to image {input_path}: {e}")
            return {
                'success': False,
                'error': f"Error applying filter: {str(e)}",
                'input_path': str(input_path),
                'filter_name': filter_name,
                'operation': 'apply_filter'
            }
    
    def _apply_blur(self, img: Image.Image, strength: float) -> Image.Image:
        """Apply blur filter."""
        radius = max(1, int(strength * 2))
        return img.filter(ImageFilter.GaussianBlur(radius=radius))
    
    def _apply_sharpen(self, img: Image.Image, strength: float) -> Image.Image:
        """Apply sharpen filter."""
        return img.filter(ImageFilter.UnsharpMask(radius=2, percent=150, threshold=3))
    
    def _apply_emboss(self, img: Image.Image, strength: float) -> Image.Image:
        """Apply emboss filter."""
        return img.filter(ImageFilter.EMBOSS)
    
    def _apply_edge_enhance(self, img: Image.Image, strength: float) -> Image.Image:
        """Apply edge enhancement filter."""
        return img.filter(ImageFilter.EDGE_ENHANCE)
    
    def _apply_brightness(self, img: Image.Image, strength: float) -> Image.Image:
        """Apply brightness adjustment."""
        enhancer = ImageEnhance.Brightness(img)
        return enhancer.enhance(strength)
    
    def _apply_contrast(self, img: Image.Image, strength: float) -> Image.Image:
        """Apply contrast adjustment."""
        enhancer = ImageEnhance.Contrast(img)
        return enhancer.enhance(strength)
    
    def _apply_saturation(self, img: Image.Image, strength: float) -> Image.Image:
        """Apply saturation adjustment."""
        enhancer = ImageEnhance.Color(img)
        return enhancer.enhance(strength)
    
    def _apply_grayscale(self, img: Image.Image, strength: float) -> Image.Image:
        """Apply grayscale conversion."""
        return img.convert('L')
    
    def _apply_sepia(self, img: Image.Image, strength: float) -> Image.Image:
        """Apply sepia filter."""
        # Convert to RGB if necessary
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        # Apply sepia transformation
        width, height = img.size
        sepia_img = Image.new('RGB', (width, height))
        
        for x in range(width):
            for y in range(height):
                r, g, b = img.getpixel((x, y))
                tr = int(0.393 * r + 0.769 * g + 0.189 * b)
                tg = int(0.349 * r + 0.686 * g + 0.168 * b)
                tb = int(0.272 * r + 0.534 * g + 0.131 * b)
                sepia_img.putpixel((x, y), (min(255, tr), min(255, tg), min(255, tb)))
        
        return sepia_img
    
    def _generate_output_path(self, input_path: Path, filter_name: str) -> Path:
        """Generate output path with filter suffix."""
        stem = input_path.stem
        suffix = input_path.suffix
        output_filename = f"{stem}_{filter_name}{suffix}"
        return input_path.parent / output_filename
    
    def _get_output_format(self, output_path: Path) -> str:
        """Get output format from file extension."""
        suffix = output_path.suffix.lower()
        format_map = {
            '.jpg': 'JPEG',
            '.jpeg': 'JPEG',
            '.png': 'PNG',
            '.gif': 'GIF',
            '.webp': 'WEBP',
            '.bmp': 'BMP',
            '.tiff': 'TIFF'
        }
        return format_map.get(suffix, 'JPEG')

def apply_filter(input_path: Union[str, Path], filter_name: str, 
                output_path: Optional[Union[str, Path]] = None,
                filter_strength: float = 1.0) -> Dict[str, Any]:
    """Convenience function for applying a filter to an image.
    
    Args:
        input_path: Path to the input image
        filter_name: Name of the filter to apply
        output_path: Path for the output image (optional)
        filter_strength: Strength of the filter (0.0 to 2.0, default 1.0)
        
    Returns:
        Dictionary containing operation result
    """
    operation = ApplyFilterOperation()
    return operation.apply_filter(input_path, filter_name, output_path, filter_strength) 