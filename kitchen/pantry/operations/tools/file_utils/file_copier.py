"""
File Copier Module

Single-purpose module for copying files with actual functionality.
"""

import shutil
from pathlib import Path
from typing import Dict, Any
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class FileCopier:
    """Real file copying operations"""
    
    def copy_file(self, source_path: str, dest_path: str, overwrite: bool = True) -> Dict[str, Any]:
        """Actually copy a file"""
        try:
            source = Path(source_path)
            dest = Path(dest_path)
            
            if not source.exists():
                return {
                    'success': False,
                    'error': f'Source file not found: {source}',
                    'operation': 'copy_file'
                }
            
            if dest.exists() and not overwrite:
                return {
                    'success': False,
                    'error': f'Destination file exists and overwrite=False: {dest}',
                    'operation': 'copy_file'
                }
            
            # Create destination directory if it doesn't exist
            dest.parent.mkdir(parents=True, exist_ok=True)
            
            # Copy the file
            shutil.copy2(source, dest)
            
            # Verify copy was successful
            if dest.exists():
                source_size = source.stat().st_size
                dest_size = dest.stat().st_size
                
                return {
                    'success': True,
                    'operation': 'copy_file',
                    'source_path': str(source),
                    'dest_path': str(dest),
                    'source_size': source_size,
                    'dest_size': dest_size,
                    'copy_successful': source_size == dest_size,
                    'timestamp': datetime.now().isoformat()
                }
            else:
                return {
                    'success': False,
                    'error': 'File copy failed - destination file not created',
                    'operation': 'copy_file',
                    'source_path': str(source),
                    'dest_path': str(dest)
                }
                
        except Exception as e:
            logger.error(f"Error copying file {source_path} to {dest_path}: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'operation': 'copy_file',
                'source_path': source_path,
                'dest_path': dest_path
            } 