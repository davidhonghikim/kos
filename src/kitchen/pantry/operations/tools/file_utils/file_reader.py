"""
File Reader Module

Single-purpose module for reading files with actual functionality.
Handles both text and binary file reading operations.
"""

import hashlib
from pathlib import Path
from typing import Dict, Any
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class FileReader:
    """Real file reading operations"""
    
    def __init__(self):
        self.supported_text_formats = ['.txt', '.json', '.yaml', '.yml', '.md', '.csv', '.xml', '.html']
        self.supported_binary_formats = ['.jpg', '.jpeg', '.png', '.gif', '.pdf', '.zip', '.exe', '.dll']
    
    def read_file(self, file_path: str, encoding: str = 'utf-8') -> Dict[str, Any]:
        """Actually read a file and return its contents"""
        try:
            file_path = Path(file_path)
            if not file_path.exists():
                return {
                    'success': False,
                    'error': f'File not found: {file_path}',
                    'operation': 'read_file'
                }
            
            # Determine if file is binary or text
            is_binary = file_path.suffix.lower() in self.supported_binary_formats
            
            if is_binary:
                with open(file_path, 'rb') as f:
                    content = f.read()
                file_hash = hashlib.md5(content).hexdigest()
                return {
                    'success': True,
                    'operation': 'read_file',
                    'file_path': str(file_path),
                    'content_type': 'binary',
                    'file_size': len(content),
                    'file_hash': file_hash,
                    'timestamp': datetime.now().isoformat()
                }
            else:
                with open(file_path, 'r', encoding=encoding) as f:
                    content = f.read()
                return {
                    'success': True,
                    'operation': 'read_file',
                    'file_path': str(file_path),
                    'content': content,
                    'content_type': 'text',
                    'file_size': len(content),
                    'encoding': encoding,
                    'timestamp': datetime.now().isoformat()
                }
                
        except Exception as e:
            logger.error(f"Error reading file {file_path}: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'operation': 'read_file',
                'file_path': file_path
            } 