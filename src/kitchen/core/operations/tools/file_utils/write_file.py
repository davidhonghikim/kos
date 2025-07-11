"""
Write File Operation

Modular operation for writing file contents with comprehensive error handling.
"""

import os
import logging
from pathlib import Path
from typing import Dict, Any, Union, Optional

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class WriteFileOperation:
    """Write file contents with comprehensive error handling and validation."""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """Initialize the write file operation.
        
        Args:
            config: Optional configuration dictionary
        """
        self.config = config or {}
        self.supported_encodings = ['utf-8', 'ascii', 'latin-1', 'cp1252']
        
    def write_file(self, file_path: Union[str, Path], content: str, encoding: str = 'utf-8', 
                   create_dirs: bool = True, overwrite: bool = True) -> Dict[str, Any]:
        """Write content to file with comprehensive error handling.
        
        Args:
            file_path: Path to the file to write
            content: Content to write to the file
            encoding: File encoding (default: utf-8)
            create_dirs: Whether to create parent directories if they don't exist
            overwrite: Whether to overwrite existing files
            
        Returns:
            Dictionary containing operation result
        """
        try:
            # Convert to Path object for consistent handling
            path = Path(file_path)
            
            # Validate content
            if not isinstance(content, str):
                logger.error(f"Content must be a string, got {type(content)}")
                return {
                    'success': False,
                    'error': f"Content must be a string, got {type(content)}",
                    'file_path': str(file_path),
                    'operation': 'write_file'
                }
            
            # Check if file exists and handle overwrite
            if path.exists() and not overwrite:
                logger.error(f"File already exists and overwrite=False: {file_path}")
                return {
                    'success': False,
                    'error': f"File already exists: {file_path}",
                    'file_path': str(file_path),
                    'operation': 'write_file'
                }
            
            # Create parent directories if needed
            if create_dirs:
                parent_dir = path.parent
                if not parent_dir.exists():
                    logger.info(f"Creating parent directory: {parent_dir}")
                    parent_dir.mkdir(parents=True, exist_ok=True)
            
            # Validate encoding
            if encoding not in self.supported_encodings:
                logger.warning(f"Unsupported encoding '{encoding}', using utf-8")
                encoding = 'utf-8'
            
            # Write file contents
            logger.info(f"Writing file: {file_path} with encoding: {encoding}")
            with open(path, 'w', encoding=encoding) as file:
                file.write(content)
            
            # Verify file was written
            if not path.exists():
                logger.error(f"File was not created: {file_path}")
                return {
                    'success': False,
                    'error': f"File was not created: {file_path}",
                    'file_path': str(file_path),
                    'operation': 'write_file'
                }
            
            # Get file stats
            file_size = path.stat().st_size
            
            # Return success result
            result = {
                'success': True,
                'file_path': str(file_path),
                'content_length': len(content),
                'file_size': file_size,
                'encoding': encoding,
                'created': not path.exists() or overwrite,
                'operation': 'write_file'
            }
            
            logger.info(f"Successfully wrote file: {file_path} ({len(content)} characters)")
            return result
            
        except PermissionError as e:
            logger.error(f"Permission error writing file {file_path}: {e}")
            return {
                'success': False,
                'error': f"Permission error: {str(e)}",
                'file_path': str(file_path),
                'operation': 'write_file'
            }
        except OSError as e:
            logger.error(f"OS error writing file {file_path}: {e}")
            return {
                'success': False,
                'error': f"OS error: {str(e)}",
                'file_path': str(file_path),
                'operation': 'write_file'
            }
        except Exception as e:
            logger.error(f"Unexpected error writing file {file_path}: {e}")
            return {
                'success': False,
                'error': f"Unexpected error: {str(e)}",
                'file_path': str(file_path),
                'operation': 'write_file'
            }

def write_file(file_path: Union[str, Path], content: str, encoding: str = 'utf-8', 
               create_dirs: bool = True, overwrite: bool = True) -> Dict[str, Any]:
    """Convenience function for writing file contents.
    
    Args:
        file_path: Path to the file to write
        content: Content to write to the file
        encoding: File encoding (default: utf-8)
        create_dirs: Whether to create parent directories if they don't exist
        overwrite: Whether to overwrite existing files
        
    Returns:
        Dictionary containing operation result
    """
    operation = WriteFileOperation()
    return operation.write_file(file_path, content, encoding, create_dirs, overwrite) 