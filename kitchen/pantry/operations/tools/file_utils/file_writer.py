"""
File Writer Module

Single-purpose module for writing files with actual functionality.
Handles both text and binary file writing operations.
"""

from pathlib import Path
from typing import Dict, Any, Union
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class FileWriter:
    """Real file writing operations"""
    
    def write_file(self, file_path: str, content: Union[str, bytes], 
                   encoding: str = 'utf-8', overwrite: bool = True) -> Dict[str, Any]:
        """Actually write content to a file"""
        try:
            file_path = Path(file_path)
            
            # Check if file exists and overwrite setting
            if file_path.exists() and not overwrite:
                return {
                    'success': False,
                    'error': f'File already exists and overwrite=False: {file_path}',
                    'operation': 'write_file'
                }
            
            # Create directory if it doesn't exist
            file_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Determine if content is binary or text
            if isinstance(content, bytes):
                with open(file_path, 'wb') as f:
                    f.write(content)
                content_type = 'binary'
            else:
                with open(file_path, 'w', encoding=encoding) as f:
                    f.write(content)
                content_type = 'text'
            
            # Verify file was written
            if file_path.exists():
                file_size = file_path.stat().st_size
                return {
                    'success': True,
                    'operation': 'write_file',
                    'file_path': str(file_path),
                    'content_type': content_type,
                    'file_size': file_size,
                    'encoding': encoding if content_type == 'text' else None,
                    'timestamp': datetime.now().isoformat()
                }
            else:
                return {
                    'success': False,
                    'error': 'File was not created successfully',
                    'operation': 'write_file',
                    'file_path': str(file_path)
                }
                
        except Exception as e:
            logger.error(f"Error writing file {file_path}: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'operation': 'write_file',
                'file_path': file_path
            } 