"""
File Exists Operation

Modular operation for checking if files exist with comprehensive validation.
"""

import os
import logging
from pathlib import Path
from typing import Dict, Any, Union, Optional

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class FileExistsOperation:
    """Check if files exist with comprehensive validation and error handling."""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """Initialize the file exists operation.
        
        Args:
            config: Optional configuration dictionary
        """
        self.config = config or {}
        
    def file_exists(self, file_path: Union[str, Path], check_type: str = 'file') -> Dict[str, Any]:
        """Check if a file or directory exists with comprehensive validation.
        
        Args:
            file_path: Path to check
            check_type: Type of check ('file', 'directory', 'any')
            
        Returns:
            Dictionary containing operation result with existence information
        """
        try:
            # Convert to Path object for consistent handling
            path = Path(file_path)
            
            # Validate check_type parameter
            valid_types = ['file', 'directory', 'any']
            if check_type not in valid_types:
                logger.warning(f"Invalid check_type '{check_type}', using 'any'")
                check_type = 'any'
            
            # Check if path exists
            exists = path.exists()
            
            if not exists:
                logger.info(f"Path does not exist: {file_path}")
                return {
                    'success': True,
                    'exists': False,
                    'file_path': str(file_path),
                    'check_type': check_type,
                    'operation': 'file_exists'
                }
            
            # Perform type-specific checks
            if check_type == 'file':
                is_file = path.is_file()
                result = {
                    'success': True,
                    'exists': exists,
                    'is_file': is_file,
                    'file_path': str(file_path),
                    'check_type': check_type,
                    'operation': 'file_exists'
                }
                
                if not is_file:
                    logger.warning(f"Path exists but is not a file: {file_path}")
                    result['warning'] = "Path exists but is not a file"
                
                return result
                
            elif check_type == 'directory':
                is_dir = path.is_dir()
                result = {
                    'success': True,
                    'exists': exists,
                    'is_directory': is_dir,
                    'file_path': str(file_path),
                    'check_type': check_type,
                    'operation': 'file_exists'
                }
                
                if not is_dir:
                    logger.warning(f"Path exists but is not a directory: {file_path}")
                    result['warning'] = "Path exists but is not a directory"
                
                return result
                
            else:  # check_type == 'any'
                is_file = path.is_file()
                is_dir = path.is_dir()
                
                result = {
                    'success': True,
                    'exists': exists,
                    'is_file': is_file,
                    'is_directory': is_dir,
                    'file_path': str(file_path),
                    'check_type': check_type,
                    'operation': 'file_exists'
                }
                
                # Add file information if it's a file
                if is_file:
                    try:
                        stat = path.stat()
                        result.update({
                            'file_size': stat.st_size,
                            'modified_time': stat.st_mtime,
                            'created_time': stat.st_ctime
                        })
                    except OSError as e:
                        logger.warning(f"Could not get file stats: {e}")
                
                return result
                
        except Exception as e:
            logger.error(f"Error checking file existence {file_path}: {e}")
            return {
                'success': False,
                'error': f"Error checking file existence: {str(e)}",
                'file_path': str(file_path),
                'check_type': check_type,
                'operation': 'file_exists'
            }

def file_exists(file_path: Union[str, Path], check_type: str = 'file') -> Dict[str, Any]:
    """Convenience function for checking if a file exists.
    
    Args:
        file_path: Path to check
        check_type: Type of check ('file', 'directory', 'any')
        
    Returns:
        Dictionary containing operation result
    """
    operation = FileExistsOperation()
    return operation.file_exists(file_path, check_type) 