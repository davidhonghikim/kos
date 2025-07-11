"""
Directory Lister Module

Single-purpose module for listing directory contents with actual functionality.
"""

from pathlib import Path
from typing import Dict, Any
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class DirectoryLister:
    """Real directory listing operations"""
    
    def list_directory(self, directory_path: str, include_hidden: bool = False) -> Dict[str, Any]:
        """Actually list directory contents"""
        try:
            directory = Path(directory_path)
            
            if not directory.exists():
                return {
                    'success': False,
                    'error': f'Directory not found: {directory}',
                    'operation': 'list_directory'
                }
            
            if not directory.is_dir():
                return {
                    'success': False,
                    'error': f'Path is not a directory: {directory}',
                    'operation': 'list_directory'
                }
            
            files = []
            directories = []
            
            for item in directory.iterdir():
                # Skip hidden files if not requested
                if not include_hidden and item.name.startswith('.'):
                    continue
                
                stat = item.stat()
                item_info = {
                    'name': item.name,
                    'path': str(item),
                    'size': stat.st_size,
                    'modified_time': datetime.fromtimestamp(stat.st_mtime).isoformat(),
                    'is_file': item.is_file(),
                    'is_dir': item.is_dir()
                }
                
                if item.is_file():
                    files.append(item_info)
                else:
                    directories.append(item_info)
            
            return {
                'success': True,
                'operation': 'list_directory',
                'directory_path': str(directory),
                'files': files,
                'directories': directories,
                'total_files': len(files),
                'total_directories': len(directories),
                'include_hidden': include_hidden,
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error listing directory {directory_path}: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'operation': 'list_directory',
                'directory_path': directory_path
            } 