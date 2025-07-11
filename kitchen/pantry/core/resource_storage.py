"""
Resource Storage - File system management for pantry resources.

This module provides basic file system operations for pantry resources.
One task: file system management.
"""

import os
import shutil
import logging
from pathlib import Path
from typing import Optional, List

logger = logging.getLogger(__name__)


class ResourceStorage:
    """
    Simple resource storage for file system management.
    
    Single responsibility: file system operations.
    """
    
    def __init__(self, storage_root: str = "recipes/pantry/storage"):
        """Initialize storage with root directory."""
        self.storage_root = Path(storage_root)
        self.storage_root.mkdir(parents=True, exist_ok=True)
        logger.info(f"Resource Storage initialized at {self.storage_root}")
    
    def store_file(self, file_path: str, destination: str) -> bool:
        """
        Store a file in the pantry storage.
        
        Args:
            file_path: Source file path
            destination: Destination path within storage
            
        Returns:
            True if successful, False otherwise
        """
        try:
            source = Path(file_path)
            dest = self.storage_root / destination
            
            # Create destination directory
            dest.parent.mkdir(parents=True, exist_ok=True)
            
            # Copy file
            shutil.copy2(source, dest)
            
            logger.info(f"File stored: {file_path} -> {dest}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to store file {file_path}: {e}")
            return False
    
    def get_file(self, storage_path: str) -> Optional[str]:
        """
        Get file path from storage.
        
        Args:
            storage_path: Path within storage
            
        Returns:
            Full file path if exists, None otherwise
        """
        file_path = self.storage_root / storage_path
        
        if file_path.exists():
            return str(file_path)
        
        return None
    
    def list_files(self, directory: str = "") -> List[str]:
        """
        List files in storage directory.
        
        Args:
            directory: Subdirectory to list
            
        Returns:
            List of file paths
        """
        dir_path = self.storage_root / directory
        
        if not dir_path.exists():
            return []
        
        files = []
        for file_path in dir_path.rglob("*"):
            if file_path.is_file():
                files.append(str(file_path.relative_to(self.storage_root)))
        
        return files
    
    def delete_file(self, storage_path: str) -> bool:
        """
        Delete file from storage.
        
        Args:
            storage_path: Path within storage
            
        Returns:
            True if successful, False otherwise
        """
        try:
            file_path = self.storage_root / storage_path
            
            if file_path.exists():
                file_path.unlink()
                logger.info(f"File deleted: {storage_path}")
                return True
            
            return False
            
        except Exception as e:
            logger.error(f"Failed to delete file {storage_path}: {e}")
            return False
    
    def file_exists(self, storage_path: str) -> bool:
        """Check if file exists in storage."""
        return (self.storage_root / storage_path).exists() 