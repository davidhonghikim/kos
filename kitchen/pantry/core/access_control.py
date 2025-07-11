"""
Access Control - Permission management and security validation.

This module provides access control functionality.
One task: permission management and security validation.
"""

import logging
from typing import List, Optional
from dataclasses import dataclass
from enum import Enum

from .pantry_manager import PantryManager, IngredientMetadata, AccessLevel

logger = logging.getLogger(__name__)


class Permission(Enum):
    """Permission types."""
    READ = "read"
    WRITE = "write"
    DELETE = "delete"
    ADMIN = "admin"


@dataclass
class AccessRequest:
    """Access request information."""
    user_id: str
    ingredient_id: str
    permission: Permission
    access_level: AccessLevel


class AccessControl:
    """
    Simple access control for pantry ingredients.
    
    Single responsibility: permission management and security validation.
    """
    
    def __init__(self, pantry_manager: PantryManager):
        """Initialize with pantry manager reference."""
        self.pantry_manager = pantry_manager
        logger.info("Access Control initialized")
    
    def can_access(self, user_id: str, ingredient_id: str, permission: Permission) -> bool:
        """
        Check if user can access ingredient with given permission.
        
        Args:
            user_id: ID of the user
            ingredient_id: ID of the ingredient
            permission: Permission to check
            
        Returns:
            True if access allowed, False otherwise
        """
        ingredient = self.pantry_manager.get_ingredient(ingredient_id)
        if not ingredient:
            return False
        
        # Public ingredients are readable by everyone
        if ingredient.access_level == AccessLevel.PUBLIC and permission == Permission.READ:
            return True
        
        # Admin users can do everything
        if self._is_admin(user_id):
            return True
        
        # Protected ingredients require authentication
        if ingredient.access_level == AccessLevel.PROTECTED:
            return self._is_authenticated(user_id)
        
        # Admin level ingredients require admin access
        if ingredient.access_level == AccessLevel.ADMIN:
            return self._is_admin(user_id)
        
        return False
    
    def validate_access(self, request: AccessRequest) -> bool:
        """
        Validate an access request.
        
        Args:
            request: Access request to validate
            
        Returns:
            True if valid, False otherwise
        """
        return self.can_access(
            request.user_id, 
            request.ingredient_id, 
            request.permission
        )
    
    def get_accessible_ingredients(self, user_id: str, permission: Permission = Permission.READ) -> List[IngredientMetadata]:
        """
        Get all ingredients accessible to a user.
        
        Args:
            user_id: ID of the user
            permission: Permission to check
            
        Returns:
            List of accessible ingredients
        """
        all_ingredients = self.pantry_manager.list_ingredients()
        accessible = []
        
        for ingredient in all_ingredients:
            if self.can_access(user_id, ingredient.id, permission):
                accessible.append(ingredient)
        
        return accessible
    
    def _is_authenticated(self, user_id: str) -> bool:
        """
        Check if user is authenticated.
        
        Args:
            user_id: ID of the user
            
        Returns:
            True if authenticated, False otherwise
        """
        # Simple authentication check - in real implementation, this would check session/token
        return bool(user_id and user_id != "anonymous")
    
    def _is_admin(self, user_id: str) -> bool:
        """
        Check if user is admin.
        
        Args:
            user_id: ID of the user
            
        Returns:
            True if admin, False otherwise
        """
        # Simple admin check - in real implementation, this would check user roles
        return user_id in ["admin", "root", "system"]
    
    def audit_access(self, user_id: str, ingredient_id: str, permission: Permission, granted: bool) -> None:
        """
        Audit access attempt.
        
        Args:
            user_id: ID of the user
            ingredient_id: ID of the ingredient
            permission: Permission requested
            granted: Whether access was granted
        """
        logger.info(f"Access audit: user={user_id}, ingredient={ingredient_id}, "
                   f"permission={permission.value}, granted={granted}") 