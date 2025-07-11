"""
Pantry Operations Package

This package contains all operational components for the pantry system:
- Tools: Utility operations for file, data, and system management
- Modules: Reusable code components
- Tasks: Atomic operations and workflows
- Skills: Specialized capabilities
"""

__version__ = "1.0.0"
__author__ = "kOS Kitchen System"
__description__ = "Pantry operations for kOS kitchen system"

# Import main components
from .registry import OperationRegistry
from .context_manager import ContextManager

__all__ = [
    "OperationRegistry",
    "ContextManager"
] 