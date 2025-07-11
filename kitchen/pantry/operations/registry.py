"""
Pantry Operations Registry

Dynamic registry system for discovering and loading operations automatically.
This allows for scalable operation management without hardcoding imports.
"""

import os
import json
import importlib
import inspect
from pathlib import Path
from typing import Dict, List, Any, Optional, Type, Union
from datetime import datetime

class OperationRegistry:
    """Dynamic registry for discovering and managing operations"""
    
    def __init__(self, operations_root: Optional[str] = None):
        self.operations_root = Path(operations_root) if operations_root else Path(__file__).parent
        self.operations_cache = {}
        self.operation_metadata = {}
        self.discovery_cache = {}
        
    def discover_operations(self, force_refresh: bool = False) -> Dict[str, Any]:
        """Discover all available operations in the operations directory"""
        if not force_refresh and self.discovery_cache:
            return self.discovery_cache
            
        operations = {
            'tools': {},
            'modules': {},
            'tasks': {},
            'skills': {}
        }
        
        # Scan operations directory structure
        for category in operations.keys():
            category_path = self.operations_root / category
            if category_path.exists():
                operations[category] = self._scan_category(category_path, category)
                
        self.discovery_cache = operations
        return operations
    
    def _scan_category(self, category_path: Path, category: str) -> Dict[str, Any]:
        """Scan a category directory for operations"""
        category_ops = {}
        
        # Look for Python files in the category
        for py_file in category_path.rglob("*.py"):
            if py_file.name.startswith("__"):
                continue
                
            module_name = self._path_to_module_name(py_file)
            try:
                # Import the module
                module = importlib.import_module(module_name)
                
                # Find operation classes in the module
                for name, obj in inspect.getmembers(module):
                    if (inspect.isclass(obj) and 
                        name.endswith('Operations') and 
                        hasattr(obj, '__init__')):
                        
                        operation_id = f"{category}.{name.lower()}"
                        category_ops[operation_id] = {
                            'module': module_name,
                            'class': name,
                            'class_obj': obj,
                            'file_path': str(py_file),
                            'discovered_at': datetime.now().isoformat()
                        }
                        
            except Exception as e:
                print(f"Warning: Could not load operations from {py_file}: {e}")
                
        return category_ops
    
    def _path_to_module_name(self, file_path: Path) -> str:
        """Convert file path to module name"""
        relative_path = file_path.relative_to(self.operations_root.parent)
        return str(relative_path).replace(os.sep, '.').replace('.py', '')
    
    def get_operation(self, operation_id: str) -> Optional[Any]:
        """Get an operation instance by ID"""
        if operation_id in self.operations_cache:
            return self.operations_cache[operation_id]
            
        # Parse operation ID (e.g., "tools.image_editor_operations")
        parts = operation_id.split('.')
        if len(parts) != 2:
            raise ValueError(f"Invalid operation ID format: {operation_id}")
            
        category, operation_name = parts
        
        # Discover operations if not cached
        if not self.discovery_cache:
            self.discover_operations()
            
        # Find the operation
        if category not in self.discovery_cache:
            raise ValueError(f"Unknown category: {category}")
            
        if operation_id not in self.discovery_cache[category]:
            raise ValueError(f"Unknown operation: {operation_id}")
            
        # Load the operation
        op_info = self.discovery_cache[category][operation_id]
        module = importlib.import_module(op_info['module'])
        operation_class = getattr(module, op_info['class'])
        
        # Create instance and cache it
        instance = operation_class({})  # Default config
        self.operations_cache[operation_id] = instance
        
        return instance
    
    def list_operations(self, category: Optional[str] = None) -> List[str]:
        """List all available operations or operations in a category"""
        if not self.discovery_cache:
            self.discover_operations()
            
        if category is not None:
            if category not in self.discovery_cache:
                return []
            return list(self.discovery_cache[category].keys())
        else:
            all_ops = []
            for cat_ops in self.discovery_cache.values():
                all_ops.extend(cat_ops.keys())
            return all_ops
    
    def get_operation_metadata(self, operation_id: str) -> Dict[str, Any]:
        """Get metadata about an operation"""
        if not self.discovery_cache:
            self.discover_operations()
            
        for category, ops in self.discovery_cache.items():
            if operation_id in ops:
                return ops[operation_id]
        return {}
    
    def reload_operations(self) -> None:
        """Reload all operations (useful for development)"""
        self.operations_cache.clear()
        self.discovery_cache.clear()
        self.discover_operations(force_refresh=True)

# Global registry instance
registry = OperationRegistry()

# Convenience functions
def get_operation(operation_id: str) -> Any:
    """Get an operation by ID"""
    return registry.get_operation(operation_id)

def list_operations(category: Optional[str] = None) -> List[str]:
    """List available operations"""
    return registry.list_operations(category)

def discover_operations() -> Dict[str, Any]:
    """Discover all operations"""
    return registry.discover_operations() 