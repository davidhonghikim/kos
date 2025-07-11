"""
File Checker Module

Single-purpose module for checking file existence and getting file information.
"""

from pathlib import Path
from typing import Dict, Any
from datetime import datetime
import hashlib
import logging

logger = logging.getLogger(__name__)

class FileChecker:
    """Real file checking operations"""
    
    def file_exists(self, file_path: str) -> Dict[str, Any]:
        """Actually check if a file exists"""
        try:
            path = Path(file_path)
            exists = path.exists()
            
            if exists:
                stat = path.stat()
                return {
                    'success': True,
                    'operation': 'file_exists',
                    'file_path': str(path),
                    'exists': True,
                    'file_size': stat.st_size,
                    'modified_time': datetime.fromtimestamp(stat.st_mtime).isoformat(),
                    'timestamp': datetime.now().isoformat()
                }
            else:
                return {
                    'success': True,
                    'operation': 'file_exists',
                    'file_path': str(path),
                    'exists': False,
                    'timestamp': datetime.now().isoformat()
                }
                
        except Exception as e:
            logger.error(f"Error checking file existence {file_path}: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'operation': 'file_exists',
                'file_path': file_path
            }
    
    def get_file_info(self, file_path: str) -> Dict[str, Any]:
        """Actually get detailed file information"""
        try:
            path = Path(file_path)
            
            if not path.exists():
                return {
                    'success': False,
                    'error': f'File not found: {path}',
                    'operation': 'get_file_info'
                }
            
            stat = path.stat()
            
            # Calculate file hash for verification
            try:
                with open(path, 'rb') as f:
                    file_hash = hashlib.md5(f.read()).hexdigest()
            except Exception:
                file_hash = None
            
            return {
                'success': True,
                'operation': 'get_file_info',
                'file_path': str(path),
                'file_name': path.name,
                'file_extension': path.suffix,
                'file_size': stat.st_size,
                'file_hash': file_hash,
                'created_time': datetime.fromtimestamp(stat.st_ctime).isoformat(),
                'modified_time': datetime.fromtimestamp(stat.st_mtime).isoformat(),
                'accessed_time': datetime.fromtimestamp(stat.st_atime).isoformat(),
                'is_file': path.is_file(),
                'is_dir': path.is_dir(),
                'is_symlink': path.is_symlink(),
                'permissions': oct(stat.st_mode)[-3:],
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error getting file info {file_path}: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'operation': 'get_file_info',
                'file_path': file_path
            } 