"""
Dependency Tracker - Dependency resolution and tracking.

This module provides dependency management functionality.
One task: dependency resolution and tracking.
"""

import logging
from typing import List, Set, Dict, Optional
from dataclasses import dataclass

from .pantry_manager import PantryManager, IngredientMetadata

logger = logging.getLogger(__name__)


@dataclass
class DependencyInfo:
    """Dependency information."""
    ingredient_id: str
    dependencies: List[str]
    dependents: List[str]
    conflicts: List[str]


class DependencyTracker:
    """
    Simple dependency tracker for ingredient dependencies.
    
    Single responsibility: dependency resolution and tracking.
    """
    
    def __init__(self, pantry_manager: PantryManager):
        """Initialize with pantry manager reference."""
        self.pantry_manager = pantry_manager
        logger.info("Dependency Tracker initialized")
    
    def get_dependencies(self, ingredient_id: str) -> List[str]:
        """
        Get direct dependencies of an ingredient.
        
        Args:
            ingredient_id: ID of the ingredient
            
        Returns:
            List of dependency IDs
        """
        ingredient = self.pantry_manager.get_ingredient(ingredient_id)
        if ingredient:
            return ingredient.dependencies
        return []
    
    def get_dependents(self, ingredient_id: str) -> List[str]:
        """
        Get ingredients that depend on this ingredient.
        
        Args:
            ingredient_id: ID of the ingredient
            
        Returns:
            List of dependent ingredient IDs
        """
        all_ingredients = self.pantry_manager.list_ingredients()
        dependents = []
        
        for ingredient in all_ingredients:
            if ingredient_id in ingredient.dependencies:
                dependents.append(ingredient.id)
        
        return dependents
    
    def resolve_dependencies(self, ingredient_id: str) -> List[str]:
        """
        Resolve all dependencies (including transitive) for an ingredient.
        
        Args:
            ingredient_id: ID of the ingredient
            
        Returns:
            List of all dependency IDs in dependency order
        """
        resolved = []
        visited = set()
        
        def resolve_recursive(ing_id: str) -> None:
            if ing_id in visited:
                return
            
            visited.add(ing_id)
            
            # Resolve dependencies first
            for dep in self.get_dependencies(ing_id):
                resolve_recursive(dep)
            
            resolved.append(ing_id)
        
        resolve_recursive(ingredient_id)
        return resolved[:-1]  # Exclude the ingredient itself
    
    def check_conflicts(self, ingredient_id: str) -> List[str]:
        """
        Check for dependency conflicts for an ingredient.
        
        Args:
            ingredient_id: ID of the ingredient
            
        Returns:
            List of conflict descriptions
        """
        conflicts = []
        dependencies = self.resolve_dependencies(ingredient_id)
        
        # Check for circular dependencies
        if ingredient_id in dependencies:
            conflicts.append(f"Circular dependency detected for {ingredient_id}")
        
        # Check for missing dependencies
        for dep in self.get_dependencies(ingredient_id):
            if not self.pantry_manager.get_ingredient(dep):
                conflicts.append(f"Missing dependency: {dep}")
        
        return conflicts
    
    def get_dependency_info(self, ingredient_id: str) -> Optional[DependencyInfo]:
        """
        Get comprehensive dependency information for an ingredient.
        
        Args:
            ingredient_id: ID of the ingredient
            
        Returns:
            DependencyInfo if ingredient exists, None otherwise
        """
        ingredient = self.pantry_manager.get_ingredient(ingredient_id)
        if not ingredient:
            return None
        
        return DependencyInfo(
            ingredient_id=ingredient_id,
            dependencies=self.get_dependencies(ingredient_id),
            dependents=self.get_dependents(ingredient_id),
            conflicts=self.check_conflicts(ingredient_id)
        ) 