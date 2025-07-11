"""
File Deleter Module

Single-purpose module for deleting files with actual functionality.
"""

from pathlib import Path
from typing import Dict, Any
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class FileDeleter:
    """Real file deletion operations"""
    
    def delete_file(self, file_path: str, force: bool = False) -> Dict[str, Any]:
        """Actually delete a file"""
        try:
            path = Path(file_path)
            
            if not path.exists():
                if force:
                    return {
                        'success': True,
                        'operation': 'delete_file',
                        'file_path': str(path),
                        'message': 'File does not exist (force=True)',
                        'timestamp': datetime.now().isoformat()
                    }
                else:
                    return {
                        'success': False,
                        'error': f'File not found: {path}',
                        'operation': 'delete_file'
                    }
            
            # Get file info before deletion
            file_size = path.stat().st_size
            
            # Delete the file
            path.unlink()
            
            return {
                'success': True,
                'operation': 'delete_file',
                'file_path': str(path),
                'deleted_size': file_size,
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error deleting file {file_path}: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'operation': 'delete_file',
                'file_path': file_path
            } 