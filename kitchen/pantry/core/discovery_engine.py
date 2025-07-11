"""
Discovery Engine - Dynamic ingredient discovery.

This module provides ingredient discovery functionality.
One task: dynamic ingredient discovery.
"""

import logging
import os
from typing import List, Dict, Optional
from pathlib import Path
from dataclasses import dataclass

from .pantry_manager import PantryManager, IngredientMetadata, IngredientCategory

logger = logging.getLogger(__name__)


@dataclass
class DiscoveryResult:
    """Discovery result information."""
    ingredient_id: str
    file_path: str
    category: IngredientCategory
    auto_registered: bool


class DiscoveryEngine:
    """
    Simple discovery engine for finding ingredients.
    
    Single responsibility: dynamic ingredient discovery.
    """
    
    def __init__(self, pantry_manager: PantryManager, discovery_paths: Optional[List[str]] = None):
        """
        Initialize discovery engine.
        
        Args:
            pantry_manager: Reference to pantry manager
            discovery_paths: Paths to search for ingredients
        """
        self.pantry_manager = pantry_manager
        self.discovery_paths = discovery_paths if discovery_paths is not None else ["recipes/pantry/ingredients"]
        logger.info("Discovery Engine initialized")
    
    def discover_ingredients(self) -> List[DiscoveryResult]:
        """
        Discover ingredients in configured paths.
        
        Returns:
            List of discovery results
        """
        results = []
        
        for path in self.discovery_paths:
            path_obj = Path(path)
            if path_obj.exists():
                results.extend(self._scan_directory(path_obj))
        
        return results
    
    def _scan_directory(self, directory: Path) -> List[DiscoveryResult]:
        """
        Scan directory for ingredients.
        
        Args:
            directory: Directory to scan
            
        Returns:
            List of discovery results
        """
        results = []
        
        for file_path in directory.rglob("*.json"):
            try:
                result = self._analyze_file(file_path)
                if result:
                    results.append(result)
            except Exception as e:
                logger.error(f"Error analyzing file {file_path}: {e}")
        
        return results
    
    def _analyze_file(self, file_path: Path) -> Optional[DiscoveryResult]:
        """
        Analyze a file to determine if it's an ingredient.
        
        Args:
            file_path: File to analyze
            
        Returns:
            DiscoveryResult if ingredient found, None otherwise
        """
        try:
            import json
            with open(file_path, 'r') as f:
                data = json.load(f)
            
            # Check if file has ingredient metadata
            if self._is_ingredient_file(data):
                ingredient_id = self._extract_ingredient_id(data, file_path)
                category = self._extract_category(data, file_path)
                
                return DiscoveryResult(
                    ingredient_id=ingredient_id,
                    file_path=str(file_path),
                    category=category,
                    auto_registered=False
                )
        
        except Exception as e:
            logger.debug(f"File {file_path} is not a valid ingredient: {e}")
        
        return None
    
    def _is_ingredient_file(self, data: Dict) -> bool:
        """
        Check if data represents an ingredient file.
        
        Args:
            data: JSON data from file
            
        Returns:
            True if ingredient file, False otherwise
        """
        required_fields = ['id', 'name', 'version', 'category']
        return all(field in data for field in required_fields)
    
    def _extract_ingredient_id(self, data: Dict, file_path: Path) -> str:
        """
        Extract ingredient ID from data or file path.
        
        Args:
            data: JSON data from file
            file_path: Path to file
            
        Returns:
            Ingredient ID
        """
        if 'id' in data:
            return data['id']
        
        # Fallback to filename-based ID
        return f"ingredient.{file_path.stem}"
    
    def _extract_category(self, data: Dict, file_path: Path) -> IngredientCategory:
        """
        Extract category from data or file path.
        
        Args:
            data: JSON data from file
            file_path: Path to file
            
        Returns:
            Ingredient category
        """
        if 'category' in data:
            try:
                return IngredientCategory(data['category'])
            except ValueError:
                pass
        
        # Fallback to directory-based category
        parent_dir = file_path.parent.name
        try:
            return IngredientCategory(parent_dir)
        except ValueError:
            return IngredientCategory.TASKS  # Default category 