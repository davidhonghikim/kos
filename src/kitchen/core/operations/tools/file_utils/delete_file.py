"""
Delete File Operation

Modular operation for deleting files with comprehensive error handling and safety checks.
"""

import os
import logging
from pathlib import Path
from typing import Dict, Any, Union, Optional

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DeleteFileOperation:
    """Delete files with comprehensive error handling and safety validation."""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """Initialize the delete file operation.
        
        Args:
            config: Optional configuration dictionary
        """
        self.config = config or {}
        
    def delete_file(self, file_path: Union[str, Path], force: bool = False, 
                   backup: bool = False, backup_dir: Optional[Union[str, Path]] = None) -> Dict[str, Any]:
        """Delete a file with comprehensive error handling and safety checks.
        
        Args:
            file_path: Path to the file to delete
            force: Whether to force deletion without additional checks
            backup: Whether to create a backup before deletion
            backup_dir: Directory to store backup (if backup=True)
            
        Returns:
            Dictionary containing operation result
        """
        try:
            # Convert to Path object for consistent handling
            path = Path(file_path)
            
            # Check if file exists
            if not path.exists():
                logger.warning(f"File does not exist: {file_path}")
                return {
                    'success': True,
                    'deleted': False,
                    'reason': 'File does not exist',
                    'file_path': str(file_path),
                    'operation': 'delete_file'
                }
            
            # Check if it's actually a file
            if not path.is_file():
                logger.error(f"Path is not a file: {file_path}")
                return {
                    'success': False,
                    'error': f"Path is not a file: {file_path}",
                    'file_path': str(file_path),
                    'operation': 'delete_file'
                }
            
            # Get file information before deletion
            try:
                stat = path.stat()
                file_size = stat.st_size
                modified_time = stat.st_mtime
            except OSError as e:
                logger.warning(f"Could not get file stats: {e}")
                file_size = None
                modified_time = None
            
            # Create backup if requested
            backup_path = None
            if backup:
                backup_path = self._create_backup(path, backup_dir)
                if not backup_path:
                    logger.error(f"Failed to create backup for: {file_path}")
                    return {
                        'success': False,
                        'error': 'Failed to create backup',
                        'file_path': str(file_path),
                        'operation': 'delete_file'
                    }
            
            # Additional safety checks (unless force=True)
            if not force:
                # Check file size (warn for large files)
                if file_size and file_size > 10 * 1024 * 1024:  # 10MB
                    logger.warning(f"Attempting to delete large file ({file_size} bytes): {file_path}")
                
                # Check if file is read-only
                if not os.access(path, os.W_OK):
                    logger.warning(f"File is read-only: {file_path}")
            
            # Attempt to delete the file
            logger.info(f"Deleting file: {file_path}")
            path.unlink()
            
            # Verify deletion
            if path.exists():
                logger.error(f"File still exists after deletion: {file_path}")
                return {
                    'success': False,
                    'error': 'File still exists after deletion',
                    'file_path': str(file_path),
                    'operation': 'delete_file'
                }
            
            # Return success result
            result = {
                'success': True,
                'deleted': True,
                'file_path': str(file_path),
                'operation': 'delete_file'
            }
            
            # Add backup information if backup was created
            if backup_path:
                result['backup_path'] = str(backup_path)
            
            # Add file information if available
            if file_size is not None:
                result['file_size'] = file_size
            if modified_time is not None:
                result['modified_time'] = modified_time
            
            logger.info(f"Successfully deleted file: {file_path}")
            return result
            
        except PermissionError as e:
            logger.error(f"Permission error deleting file {file_path}: {e}")
            return {
                'success': False,
                'error': f"Permission error: {str(e)}",
                'file_path': str(file_path),
                'operation': 'delete_file'
            }
        except OSError as e:
            logger.error(f"OS error deleting file {file_path}: {e}")
            return {
                'success': False,
                'error': f"OS error: {str(e)}",
                'file_path': str(file_path),
                'operation': 'delete_file'
            }
        except Exception as e:
            logger.error(f"Unexpected error deleting file {file_path}: {e}")
            return {
                'success': False,
                'error': f"Unexpected error: {str(e)}",
                'file_path': str(file_path),
                'operation': 'delete_file'
            }
    
    def _create_backup(self, file_path: Path, backup_dir: Optional[Union[str, Path]] = None) -> Optional[Path]:
        """Create a backup of the file before deletion.
        
        Args:
            file_path: Path to the file to backup
            backup_dir: Directory to store backup (optional)
            
        Returns:
            Path to the backup file, or None if backup failed
        """
        try:
            # Determine backup directory
            if backup_dir:
                backup_path = Path(backup_dir)
            else:
                backup_path = file_path.parent / 'backups'
            
            # Create backup directory if it doesn't exist
            backup_path.mkdir(parents=True, exist_ok=True)
            
            # Create backup filename with timestamp
            from datetime import datetime
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            backup_filename = f"{file_path.stem}_{timestamp}{file_path.suffix}"
            backup_file = backup_path / backup_filename
            
            # Copy file to backup location
            import shutil
            shutil.copy2(file_path, backup_file)
            
            logger.info(f"Created backup: {backup_file}")
            return backup_file
            
        except Exception as e:
            logger.error(f"Failed to create backup: {e}")
            return None

def delete_file(file_path: Union[str, Path], force: bool = False, 
                backup: bool = False, backup_dir: Optional[Union[str, Path]] = None) -> Dict[str, Any]:
    """Convenience function for deleting a file.
    
    Args:
        file_path: Path to the file to delete
        force: Whether to force deletion without additional checks
        backup: Whether to create a backup before deletion
        backup_dir: Directory to store backup (if backup=True)
        
    Returns:
        Dictionary containing operation result
    """
    operation = DeleteFileOperation()
    return operation.delete_file(file_path, force, backup, backup_dir) 