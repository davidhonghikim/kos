"""
Pantry System - Main orchestrator for pantry components.

This module coordinates all pantry system components.
One task: system orchestration.
"""

import logging
from typing import List, Optional

from .core.pantry_manager import PantryManager, IngredientMetadata, IngredientCategory
from .core.ingredient_registry import IngredientRegistry
from .core.resource_storage import ResourceStorage
from .core.dependency_tracker import DependencyTracker
from .core.access_control import AccessControl
from .core.discovery_engine import DiscoveryEngine
from .core.validation_system import ValidationSystem

logger = logging.getLogger(__name__)


class PantrySystem:
    """
    Main pantry system orchestrator.
    
    Coordinates all pantry components for complete functionality.
    """
    
    def __init__(self, pantry_root: str = "recipes/pantry"):
        """
        Initialize pantry system with all components.
        
        Args:
            pantry_root: Root directory for pantry system
        """
        # Initialize core components
        self.pantry_manager = PantryManager(pantry_root)
        self.ingredient_registry = IngredientRegistry(self.pantry_manager)
        self.resource_storage = ResourceStorage(f"{pantry_root}/storage")
        self.dependency_tracker = DependencyTracker(self.pantry_manager)
        self.access_control = AccessControl(self.pantry_manager)
        self.discovery_engine = DiscoveryEngine(self.pantry_manager)
        self.validation_system = ValidationSystem(self.pantry_manager)
        
        logger.info("Pantry System initialized with all components")
    
    def register_ingredient(self, ingredient: IngredientMetadata) -> bool:
        """
        Register a new ingredient with validation.
        
        Args:
            ingredient: Ingredient to register
            
        Returns:
            True if successful, False otherwise
        """
        # Validate ingredient first
        validation = self.validation_system.validate_ingredient(ingredient)
        if not validation.valid:
            logger.error(f"Ingredient validation failed: {validation.errors}")
            return False
        
        # Register with pantry manager
        success = self.pantry_manager.register_ingredient(ingredient)
        if success:
            # Update registry index
            self.ingredient_registry.update_index(ingredient)
            logger.info(f"Ingredient {ingredient.id} registered successfully")
        
        return success
    
    def search_ingredients(self, query: str, category: Optional[IngredientCategory] = None) -> List:
        """
        Search ingredients using registry.
        
        Args:
            query: Search query
            category: Optional category filter
            
        Returns:
            List of search results
        """
        return self.ingredient_registry.search_ingredients(query, category)
    
    def get_ingredient(self, ingredient_id: str) -> Optional[IngredientMetadata]:
        """
        Get ingredient by ID.
        
        Args:
            ingredient_id: ID of ingredient to retrieve
            
        Returns:
            Ingredient if found, None otherwise
        """
        return self.pantry_manager.get_ingredient(ingredient_id)
    
    def list_ingredients(self, category: Optional[IngredientCategory] = None) -> List[IngredientMetadata]:
        """
        List ingredients with optional category filter.
        
        Args:
            category: Optional category filter
            
        Returns:
            List of ingredients
        """
        return self.pantry_manager.list_ingredients(category)
    
    def discover_new_ingredients(self) -> List:
        """
        Discover new ingredients using discovery engine.
        
        Returns:
            List of discovery results
        """
        return self.discovery_engine.discover_ingredients()
    
    def validate_ingredient(self, ingredient_id: str) -> Optional:
        """
        Validate an ingredient.
        
        Args:
            ingredient_id: ID of ingredient to validate
            
        Returns:
            Validation result if ingredient exists, None otherwise
        """
        return self.validation_system.validate_ingredient_by_id(ingredient_id)
    
    def get_dependencies(self, ingredient_id: str) -> List[str]:
        """
        Get dependencies for an ingredient.
        
        Args:
            ingredient_id: ID of ingredient
            
        Returns:
            List of dependency IDs
        """
        return self.dependency_tracker.get_dependencies(ingredient_id)
    
    def check_access(self, user_id: str, ingredient_id: str, permission) -> bool:
        """
        Check access permission for user and ingredient.
        
        Args:
            user_id: ID of user
            ingredient_id: ID of ingredient
            permission: Permission to check
            
        Returns:
            True if access allowed, False otherwise
        """
        return self.access_control.can_access(user_id, ingredient_id, permission)
    
    def store_resource(self, file_path: str, destination: str) -> bool:
        """
        Store a resource file.
        
        Args:
            file_path: Source file path
            destination: Destination path within storage
            
        Returns:
            True if successful, False otherwise
        """
        return self.resource_storage.store_file(file_path, destination)
    
    def get_system_status(self) -> dict:
        """
        Get overall system status.
        
        Returns:
            System status information
        """
        validation_summary = self.validation_system.get_validation_summary()
        pantry_stats = self.pantry_manager.get_statistics()
        
        return {
            "validation": validation_summary,
            "pantry_stats": pantry_stats,
            "components": {
                "pantry_manager": "active",
                "ingredient_registry": "active",
                "resource_storage": "active",
                "dependency_tracker": "active",
                "access_control": "active",
                "discovery_engine": "active",
                "validation_system": "active"
            }
        } 