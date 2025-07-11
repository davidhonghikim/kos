"""
Ingredient Registry - Simple ingredient indexing and search.

This module provides basic ingredient discovery and search functionality.
One task: ingredient indexing and search.
"""

import logging
from typing import List, Optional
from dataclasses import dataclass
from enum import Enum

from .pantry_manager import PantryManager, IngredientMetadata, IngredientCategory

logger = logging.getLogger(__name__)


@dataclass
class SearchResult:
    """Basic search result."""
    ingredient: IngredientMetadata
    relevance_score: float


class IngredientRegistry:
    """
    Simple ingredient registry for indexing and search.
    
    Single responsibility: ingredient discovery and search.
    """
    
    def __init__(self, pantry_manager: PantryManager):
        """Initialize with pantry manager reference."""
        self.pantry_manager = pantry_manager
        logger.info("Ingredient Registry initialized")
    
    def search_ingredients(self, query: str, 
                          category: Optional[IngredientCategory] = None) -> List[SearchResult]:
        """
        Search ingredients by name, description, or tags.
        
        Args:
            query: Search query string
            category: Optional category filter
            
        Returns:
            List of search results
        """
        ingredients = self.pantry_manager.list_ingredients(category=category)
        results = []
        
        query_lower = query.lower()
        
        for ingredient in ingredients:
            score = 0.0
            
            # Check name
            if query_lower in ingredient.name.lower():
                score += 10.0
            
            # Check description
            if ingredient.description and query_lower in ingredient.description.lower():
                score += 5.0
            
            # Check tags
            for tag in ingredient.tags:
                if query_lower in tag.lower():
                    score += 8.0
                    break
            
            if score > 0:
                results.append(SearchResult(ingredient=ingredient, relevance_score=score))
        
        # Sort by relevance
        results.sort(key=lambda x: x.relevance_score, reverse=True)
        return results
    
    def get_ingredients_by_category(self, category: IngredientCategory) -> List[IngredientMetadata]:
        """Get all ingredients in a category."""
        return self.pantry_manager.list_ingredients(category=category)
    
    def get_ingredients_by_tag(self, tag: str) -> List[IngredientMetadata]:
        """Get all ingredients with a specific tag."""
        all_ingredients = self.pantry_manager.list_ingredients()
        return [ing for ing in all_ingredients if tag.lower() in [t.lower() for t in ing.tags]] 