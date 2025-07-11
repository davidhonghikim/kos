"""
Read File Operation

Modular operation for reading file contents with comprehensive error handling.
"""

import os
import logging
from pathlib import Path
from typing import Dict, Any, Union, Optional

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ReadFileOperation:
    """Read file contents with comprehensive error handling and validation."""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """Initialize the read file operation.
        
        Args:
            config: Optional configuration dictionary
        """
        self.config = config or {}
        self.supported_encodings = ['utf-8', 'ascii', 'latin-1', 'cp1252']
        
    def read_file(self, file_path: Union[str, Path], encoding: str = 'utf-8') -> Dict[str, Any]:
        """Read file contents with comprehensive error handling.
        
        Args:
            file_path: Path to the file to read
            encoding: File encoding (default: utf-8)
            
        Returns:
            Dictionary containing operation result with file contents or error information
        """
        try:
            # Convert to Path object for consistent handling
            path = Path(file_path)
            
            # Validate file path
            if not path.exists():
                logger.error(f"File does not exist: {file_path}")
                return {
                    'success': False,
                    'error': f"File does not exist: {file_path}",
                    'file_path': str(file_path),
                    'operation': 'read_file'
                }
            
            if not path.is_file():
                logger.error(f"Path is not a file: {file_path}")
                return {
                    'success': False,
                    'error': f"Path is not a file: {file_path}",
                    'file_path': str(file_path),
                    'operation': 'read_file'
                }
            
            # Check file size to prevent memory issues
            file_size = path.stat().st_size
            if file_size > 100 * 1024 * 1024:  # 100MB limit
                logger.warning(f"File is very large ({file_size} bytes): {file_path}")
                return {
                    'success': False,
                    'error': f"File too large ({file_size} bytes): {file_path}",
                    'file_path': str(file_path),
                    'file_size': file_size,
                    'operation': 'read_file'
                }
            
            # Validate encoding
            if encoding not in self.supported_encodings:
                logger.warning(f"Unsupported encoding '{encoding}', using utf-8")
                encoding = 'utf-8'
            
            # Read file contents
            logger.info(f"Reading file: {file_path} with encoding: {encoding}")
            with open(path, 'r', encoding=encoding) as file:
                content = file.read()
            
            # Return success result
            result = {
                'success': True,
                'content': content,
                'file_path': str(file_path),
                'file_size': len(content),
                'encoding': encoding,
                'operation': 'read_file'
            }
            
            logger.info(f"Successfully read file: {file_path} ({len(content)} characters)")
            return result
            
        except UnicodeDecodeError as e:
            logger.error(f"Encoding error reading file {file_path}: {e}")
            return {
                'success': False,
                'error': f"Encoding error: {str(e)}",
                'file_path': str(file_path),
                'encoding': encoding,
                'operation': 'read_file'
            }
        except PermissionError as e:
            logger.error(f"Permission error reading file {file_path}: {e}")
            return {
                'success': False,
                'error': f"Permission error: {str(e)}",
                'file_path': str(file_path),
                'operation': 'read_file'
            }
        except Exception as e:
            logger.error(f"Unexpected error reading file {file_path}: {e}")
            return {
                'success': False,
                'error': f"Unexpected error: {str(e)}",
                'file_path': str(file_path),
                'operation': 'read_file'
            }

def read_file(file_path: Union[str, Path], encoding: str = 'utf-8') -> Dict[str, Any]:
    """Convenience function for reading file contents.
    
    Args:
        file_path: Path to the file to read
        encoding: File encoding (default: utf-8)
        
    Returns:
        Dictionary containing operation result
    """
    operation = ReadFileOperation()
    return operation.read_file(file_path, encoding) 