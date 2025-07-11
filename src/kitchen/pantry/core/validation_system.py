"""
Validation System - Ingredient validation and testing.

This module provides ingredient validation functionality.
One task: ingredient validation and testing.
"""

import logging
from typing import List, Dict, Optional
from dataclasses import dataclass
from datetime import datetime

from .pantry_manager import PantryManager, IngredientMetadata, IngredientCategory

logger = logging.getLogger(__name__)


@dataclass
class ValidationResult:
    """Validation result information."""
    ingredient_id: str
    valid: bool
    errors: List[str]
    warnings: List[str]
    timestamp: datetime


class ValidationSystem:
    """
    Simple validation system for pantry ingredients.
    
    Single responsibility: ingredient validation and testing.
    """
    
    def __init__(self, pantry_manager: PantryManager):
        """Initialize with pantry manager reference."""
        self.pantry_manager = pantry_manager
        logger.info("Validation System initialized")
    
    def validate_ingredient(self, ingredient: IngredientMetadata) -> ValidationResult:
        """
        Validate an ingredient.
        
        Args:
            ingredient: Ingredient to validate
            
        Returns:
            Validation result
        """
        errors = []
        warnings = []
        
        # Check required fields
        if not ingredient.id:
            errors.append("Missing ingredient ID")
        elif not self._is_valid_id(ingredient.id):
            errors.append(f"Invalid ingredient ID format: {ingredient.id}")
        
        if not ingredient.name:
            errors.append("Missing ingredient name")
        
        if not ingredient.version:
            errors.append("Missing ingredient version")
        elif not self._is_valid_version(ingredient.version):
            errors.append(f"Invalid version format: {ingredient.version}")
        
        if not ingredient.description:
            warnings.append("Missing ingredient description")
        
        if not ingredient.author:
            warnings.append("Missing ingredient author")
        
        # Check category
        if not isinstance(ingredient.category, IngredientCategory):
            errors.append(f"Invalid category: {ingredient.category}")
        
        # Check dependencies
        for dep in ingredient.dependencies:
            if not self.pantry_manager.get_ingredient(dep):
                warnings.append(f"Missing dependency: {dep}")
        
        # Check tags
        if not ingredient.tags:
            warnings.append("No tags specified")
        
        valid = len(errors) == 0
        
        return ValidationResult(
            ingredient_id=ingredient.id,
            valid=valid,
            errors=errors,
            warnings=warnings,
            timestamp=datetime.utcnow()
        )
    
    def validate_ingredient_by_id(self, ingredient_id: str) -> Optional[ValidationResult]:
        """
        Validate ingredient by ID.
        
        Args:
            ingredient_id: ID of ingredient to validate
            
        Returns:
            Validation result if ingredient exists, None otherwise
        """
        ingredient = self.pantry_manager.get_ingredient(ingredient_id)
        if ingredient:
            return self.validate_ingredient(ingredient)
        return None
    
    def validate_all_ingredients(self) -> List[ValidationResult]:
        """
        Validate all ingredients in pantry.
        
        Returns:
            List of validation results
        """
        ingredients = self.pantry_manager.list_ingredients()
        results = []
        
        for ingredient in ingredients:
            result = self.validate_ingredient(ingredient)
            results.append(result)
        
        return results
    
    def get_validation_summary(self) -> Dict:
        """
        Get summary of validation results.
        
        Returns:
            Validation summary
        """
        results = self.validate_all_ingredients()
        
        total = len(results)
        valid = sum(1 for r in results if r.valid)
        invalid = total - valid
        
        total_errors = sum(len(r.errors) for r in results)
        total_warnings = sum(len(r.warnings) for r in results)
        
        return {
            "total_ingredients": total,
            "valid_ingredients": valid,
            "invalid_ingredients": invalid,
            "total_errors": total_errors,
            "total_warnings": total_warnings,
            "validation_rate": valid / total if total > 0 else 0
        }
    
    def _is_valid_id(self, ingredient_id: str) -> bool:
        """
        Check if ingredient ID follows valid format.
        
        Args:
            ingredient_id: ID to validate
            
        Returns:
            True if valid, False otherwise
        """
        # ID should be lowercase, use dots for hierarchy, no spaces
        return (ingredient_id.islower() and 
                '.' in ingredient_id and 
                ' ' not in ingredient_id and
                all(c.isalnum() or c in '._-' for c in ingredient_id))
    
    def _is_valid_version(self, version: str) -> bool:
        """
        Check if version follows semantic versioning.
        
        Args:
            version: Version to validate
            
        Returns:
            True if valid, False otherwise
        """
        # Basic semantic versioning check
        parts = version.split('.')
        return len(parts) >= 2 and all(part.isdigit() for part in parts[:2]) 