"""
Resize Image Operation

Modular operation for resizing images with comprehensive error handling and validation.
"""

import os
import logging
from pathlib import Path
from typing import Dict, Any, Union, Optional, Tuple

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

try:
    from PIL import Image, ImageOps
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False
    logger.warning("PIL (Pillow) not available. Image operations will not work.")

class ResizeImageOperation:
    """Resize images with comprehensive error handling and validation."""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """Initialize the resize image operation.
        
        Args:
            config: Optional configuration dictionary
        """
        self.config = config or {}
        self.supported_formats = ['jpg', 'jpeg', 'png', 'gif', 'webp', 'bmp', 'tiff']
        
    def resize_image(self, input_path: Union[str, Path], width: int, height: int, 
                    output_path: Optional[Union[str, Path]] = None, 
                    maintain_aspect: bool = True, quality: int = 95) -> Dict[str, Any]:
        """Resize an image with comprehensive error handling.
        
        Args:
            input_path: Path to the input image
            width: Target width in pixels
            height: Target height in pixels
            output_path: Path for the output image (optional, auto-generated if None)
            maintain_aspect: Whether to maintain aspect ratio
            quality: JPEG quality (1-100, only for JPEG output)
            
        Returns:
            Dictionary containing operation result
        """
        if not PIL_AVAILABLE:
            return {
                'success': False,
                'error': 'PIL (Pillow) is not available. Please install it with: pip install Pillow',
                'input_path': str(input_path),
                'operation': 'resize_image'
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
                    'operation': 'resize_image'
                }
            
            if not input_path.is_file():
                logger.error(f"Input path is not a file: {input_path}")
                return {
                    'success': False,
                    'error': f"Input path is not a file: {input_path}",
                    'input_path': str(input_path),
                    'operation': 'resize_image'
                }
            
            # Validate dimensions
            if width <= 0 or height <= 0:
                logger.error(f"Invalid dimensions: width={width}, height={height}")
                return {
                    'success': False,
                    'error': f"Invalid dimensions: width={width}, height={height}",
                    'input_path': str(input_path),
                    'operation': 'resize_image'
                }
            
            # Generate output path if not provided
            if output_path is None:
                output_path = self._generate_output_path(input_path, width, height)
            else:
                output_path = Path(output_path)
            
            # Create output directory if it doesn't exist
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Open and validate image
            logger.info(f"Opening image: {input_path}")
            with Image.open(input_path) as img:
                # Get original dimensions
                original_width, original_height = img.size
                
                # Calculate new dimensions
                if maintain_aspect:
                    new_width, new_height = self._calculate_aspect_ratio(
                        original_width, original_height, width, height
                    )
                else:
                    new_width, new_height = width, height
                
                # Resize the image
                logger.info(f"Resizing image from {original_width}x{original_height} to {new_width}x{new_height}")
                resized_img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
                
                # Determine output format and save
                output_format = self._get_output_format(output_path)
                save_kwargs = {}
                
                if output_format.lower() in ['jpg', 'jpeg']:
                    # Convert to RGB if necessary
                    if resized_img.mode in ('RGBA', 'LA', 'P'):
                        resized_img = resized_img.convert('RGB')
                    save_kwargs['quality'] = max(1, min(100, quality))
                    save_kwargs['optimize'] = True
                
                # Save the resized image
                logger.info(f"Saving resized image: {output_path}")
                resized_img.save(output_path, format=output_format, **save_kwargs)
                
                # Verify the output file was created
                if not output_path.exists():
                    logger.error(f"Output file was not created: {output_path}")
                    return {
                        'success': False,
                        'error': f"Output file was not created: {output_path}",
                        'input_path': str(input_path),
                        'operation': 'resize_image'
                    }
                
                # Get output file size
                output_size = output_path.stat().st_size
                
                # Return success result
                result = {
                    'success': True,
                    'input_path': str(input_path),
                    'output_path': str(output_path),
                    'original_dimensions': f"{original_width}x{original_height}",
                    'new_dimensions': f"{new_width}x{new_height}",
                    'maintain_aspect': maintain_aspect,
                    'output_format': output_format,
                    'output_size': output_size,
                    'operation': 'resize_image'
                }
                
                logger.info(f"Successfully resized image: {input_path} -> {output_path}")
                return result
                
        except Exception as e:
            logger.error(f"Error resizing image {input_path}: {e}")
            return {
                'success': False,
                'error': f"Error resizing image: {str(e)}",
                'input_path': str(input_path),
                'operation': 'resize_image'
            }
    
    def _calculate_aspect_ratio(self, orig_width: int, orig_height: int, 
                               target_width: int, target_height: int) -> Tuple[int, int]:
        """Calculate new dimensions maintaining aspect ratio."""
        orig_ratio = orig_width / orig_height
        target_ratio = target_width / target_height
        
        if orig_ratio > target_ratio:
            # Original is wider, fit to width
            new_width = target_width
            new_height = int(target_width / orig_ratio)
        else:
            # Original is taller, fit to height
            new_height = target_height
            new_width = int(target_height * orig_ratio)
        
        return new_width, new_height
    
    def _generate_output_path(self, input_path: Path, width: int, height: int) -> Path:
        """Generate output path with size suffix."""
        stem = input_path.stem
        suffix = input_path.suffix
        output_filename = f"{stem}_{width}x{height}{suffix}"
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

def resize_image(input_path: Union[str, Path], width: int, height: int, 
                output_path: Optional[Union[str, Path]] = None, 
                maintain_aspect: bool = True, quality: int = 95) -> Dict[str, Any]:
    """Convenience function for resizing an image.
    
    Args:
        input_path: Path to the input image
        width: Target width in pixels
        height: Target height in pixels
        output_path: Path for the output image (optional)
        maintain_aspect: Whether to maintain aspect ratio
        quality: JPEG quality (1-100, only for JPEG output)
        
    Returns:
        Dictionary containing operation result
    """
    operation = ResizeImageOperation()
    return operation.resize_image(input_path, width, height, output_path, maintain_aspect, quality) 