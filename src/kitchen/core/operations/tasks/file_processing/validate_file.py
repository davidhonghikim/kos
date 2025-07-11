"""
Validate File Task

Modular task for comprehensive file validation with multiple validation types.
"""

import os
import logging
import hashlib
import mimetypes
from pathlib import Path
from typing import Dict, Any, Union, Optional, List
import json

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ValidateFileTask:
    """Comprehensive file validation task with multiple validation types."""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """Initialize the file validation task.
        
        Args:
            config: Optional configuration dictionary
        """
        self.config = config or {}
        self.supported_validations = [
            'existence', 'readability', 'size', 'format', 'integrity', 'content'
        ]
        
    def validate_file(self, file_path: Union[str, Path], 
                     validations: Optional[List[str]] = None,
                     max_size_mb: Optional[float] = None,
                     allowed_formats: Optional[List[str]] = None,
                     content_schema: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Comprehensive file validation with multiple validation types.
        
        Args:
            file_path: Path to the file to validate
            validations: List of validation types to perform
            max_size_mb: Maximum file size in MB
            allowed_formats: List of allowed file formats/extensions
            content_schema: JSON schema for content validation (if applicable)
            
        Returns:
            Dictionary containing validation results
        """
        try:
            # Convert to Path object
            file_path = Path(file_path)
            
            # Set default validations if none provided
            if validations is None:
                validations = ['existence', 'readability', 'size']
            
            # Validate validation types
            invalid_validations = [v for v in validations if v not in self.supported_validations]
            if invalid_validations:
                logger.error(f"Invalid validation types: {invalid_validations}")
                return {
                    'success': False,
                    'error': f'Invalid validation types: {invalid_validations}',
                    'supported_validations': self.supported_validations,
                    'operation': 'validate_file'
                }
            
            # Initialize results
            validation_results = {
                'file_path': str(file_path),
                'validations_performed': validations,
                'overall_valid': True,
                'validation_details': {},
                'operation': 'validate_file'
            }
            
            # Perform each validation
            for validation_type in validations:
                logger.info(f"Performing {validation_type} validation on {file_path}")
                
                if validation_type == 'existence':
                    result = self._validate_existence(file_path)
                elif validation_type == 'readability':
                    result = self._validate_readability(file_path)
                elif validation_type == 'size':
                    result = self._validate_size(file_path, max_size_mb)
                elif validation_type == 'format':
                    result = self._validate_format(file_path, allowed_formats)
                elif validation_type == 'integrity':
                    result = self._validate_integrity(file_path)
                elif validation_type == 'content':
                    result = self._validate_content(file_path, content_schema)
                else:
                    result = {'valid': False, 'error': f'Unknown validation type: {validation_type}'}
                
                validation_results['validation_details'][validation_type] = result
                
                # Update overall validity
                if not result.get('valid', False):
                    validation_results['overall_valid'] = False
            
            # Add summary information
            validation_results['summary'] = self._create_validation_summary(validation_results)
            
            # Determine final success status
            validation_results['success'] = validation_results['overall_valid']
            
            logger.info(f"File validation completed for {file_path}: {'PASSED' if validation_results['overall_valid'] else 'FAILED'}")
            return validation_results
            
        except Exception as e:
            logger.error(f"Error during file validation: {e}")
            return {
                'success': False,
                'error': f'Error during file validation: {str(e)}',
                'file_path': str(file_path),
                'operation': 'validate_file'
            }
    
    def _validate_existence(self, file_path: Path) -> Dict[str, Any]:
        """Validate that the file exists."""
        exists = file_path.exists()
        return {
            'valid': exists,
            'exists': exists,
            'error': None if exists else f'File does not exist: {file_path}'
        }
    
    def _validate_readability(self, file_path: Path) -> Dict[str, Any]:
        """Validate that the file is readable."""
        try:
            if not file_path.exists():
                return {
                    'valid': False,
                    'readable': False,
                    'error': f'File does not exist: {file_path}'
                }
            
            if not file_path.is_file():
                return {
                    'valid': False,
                    'readable': False,
                    'error': f'Path is not a file: {file_path}'
                }
            
            # Test if file is readable
            with open(file_path, 'r', encoding='utf-8') as f:
                f.read(1)  # Try to read one character
            
            return {
                'valid': True,
                'readable': True,
                'error': None
            }
            
        except PermissionError as e:
            return {
                'valid': False,
                'readable': False,
                'error': f'Permission error: {str(e)}'
            }
        except UnicodeDecodeError as e:
            return {
                'valid': False,
                'readable': False,
                'error': f'Encoding error: {str(e)}'
            }
        except Exception as e:
            return {
                'valid': False,
                'readable': False,
                'error': f'Readability error: {str(e)}'
            }
    
    def _validate_size(self, file_path: Path, max_size_mb: Optional[float]) -> Dict[str, Any]:
        """Validate file size."""
        try:
            if not file_path.exists():
                return {
                    'valid': False,
                    'size_bytes': None,
                    'size_mb': None,
                    'error': f'File does not exist: {file_path}'
                }
            
            size_bytes = file_path.stat().st_size
            size_mb = size_bytes / (1024 * 1024)
            
            result = {
                'valid': True,
                'size_bytes': size_bytes,
                'size_mb': round(size_mb, 2),
                'error': None
            }
            
            # Check against maximum size if specified
            if max_size_mb is not None:
                if size_mb > max_size_mb:
                    result['valid'] = False
                    result['error'] = f'File size ({size_mb:.2f} MB) exceeds maximum ({max_size_mb} MB)'
                    result['max_size_mb'] = max_size_mb
            
            return result
            
        except Exception as e:
            return {
                'valid': False,
                'size_bytes': None,
                'size_mb': None,
                'error': f'Size validation error: {str(e)}'
            }
    
    def _validate_format(self, file_path: Path, allowed_formats: Optional[List[str]]) -> Dict[str, Any]:
        """Validate file format."""
        try:
            if not file_path.exists():
                return {
                    'valid': False,
                    'format': None,
                    'mime_type': None,
                    'error': f'File does not exist: {file_path}'
                }
            
            # Get file extension
            extension = file_path.suffix.lower()
            if extension.startswith('.'):
                extension = extension[1:]  # Remove leading dot
            
            # Get MIME type
            mime_type, _ = mimetypes.guess_type(str(file_path))
            
            result = {
                'valid': True,
                'format': extension,
                'mime_type': mime_type,
                'error': None
            }
            
            # Check against allowed formats if specified
            if allowed_formats:
                if extension not in allowed_formats:
                    result['valid'] = False
                    result['error'] = f'File format ({extension}) not in allowed formats: {allowed_formats}'
                    result['allowed_formats'] = allowed_formats
            
            return result
            
        except Exception as e:
            return {
                'valid': False,
                'format': None,
                'mime_type': None,
                'error': f'Format validation error: {str(e)}'
            }
    
    def _validate_integrity(self, file_path: Path) -> Dict[str, Any]:
        """Validate file integrity using checksums."""
        try:
            if not file_path.exists():
                return {
                    'valid': False,
                    'md5_hash': None,
                    'sha256_hash': None,
                    'error': f'File does not exist: {file_path}'
                }
            
            # Calculate MD5 hash
            md5_hash = hashlib.md5()
            sha256_hash = hashlib.sha256()
            
            with open(file_path, 'rb') as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    md5_hash.update(chunk)
                    sha256_hash.update(chunk)
            
            return {
                'valid': True,
                'md5_hash': md5_hash.hexdigest(),
                'sha256_hash': sha256_hash.hexdigest(),
                'error': None
            }
            
        except Exception as e:
            return {
                'valid': False,
                'md5_hash': None,
                'sha256_hash': None,
                'error': f'Integrity validation error: {str(e)}'
            }
    
    def _validate_content(self, file_path: Path, content_schema: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        """Validate file content against schema."""
        try:
            if not file_path.exists():
                return {
                    'valid': False,
                    'content_valid': False,
                    'error': f'File does not exist: {file_path}'
                }
            
            # Read file content
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            result = {
                'valid': True,
                'content_valid': True,
                'content_length': len(content),
                'error': None
            }
            
            # Validate against schema if provided
            if content_schema:
                try:
                    # Try to parse as JSON if schema is provided
                    json_content = json.loads(content)
                    # Basic schema validation (this could be enhanced with jsonschema library)
                    if isinstance(content_schema, dict):
                        # Simple validation - check if required fields exist
                        required_fields = content_schema.get('required', [])
                        for field in required_fields:
                            if field not in json_content:
                                result['valid'] = False
                                result['content_valid'] = False
                                result['error'] = f'Missing required field: {field}'
                                break
                except json.JSONDecodeError as e:
                    result['valid'] = False
                    result['content_valid'] = False
                    result['error'] = f'Invalid JSON content: {str(e)}'
            
            return result
            
        except Exception as e:
            return {
                'valid': False,
                'content_valid': False,
                'error': f'Content validation error: {str(e)}'
            }
    
    def _create_validation_summary(self, validation_results: Dict[str, Any]) -> Dict[str, Any]:
        """Create a summary of validation results."""
        details = validation_results.get('validation_details', {})
        
        passed_validations = []
        failed_validations = []
        
        for validation_type, result in details.items():
            if result.get('valid', False):
                passed_validations.append(validation_type)
            else:
                failed_validations.append(validation_type)
        
        return {
            'total_validations': len(details),
            'passed_validations': passed_validations,
            'failed_validations': failed_validations,
            'pass_rate': len(passed_validations) / len(details) if details else 0,
            'overall_status': 'PASSED' if validation_results.get('overall_valid', False) else 'FAILED'
        }

def validate_file(file_path: Union[str, Path], 
                 validations: Optional[List[str]] = None,
                 max_size_mb: Optional[float] = None,
                 allowed_formats: Optional[List[str]] = None,
                 content_schema: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Convenience function for comprehensive file validation.
    
    Args:
        file_path: Path to the file to validate
        validations: List of validation types to perform
        max_size_mb: Maximum file size in MB
        allowed_formats: List of allowed file formats/extensions
        content_schema: JSON schema for content validation
        
    Returns:
        Dictionary containing validation results
    """
    task = ValidateFileTask()
    return task.validate_file(file_path, validations, max_size_mb, allowed_formats, content_schema) 