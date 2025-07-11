"""
Pantry Manager - Basic ingredient registration and retrieval.

This module provides core ingredient management functionality.
One task: ingredient registration and retrieval.
"""

import json
import logging
from typing import Dict, List, Optional
from datetime import datetime
from pathlib import Path
from dataclasses import dataclass
from enum import Enum
import sqlite3
from contextlib import contextmanager

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class IngredientCategory(Enum):
    """Ingredient categories."""
    TASKS = "tasks"
    TOOLS = "tools"
    MODULES = "modules"
    SKILLS = "skills"
    CONFIGS = "configs"
    SCHEMAS = "schemas"


class AccessLevel(Enum):
    """Access levels."""
    PUBLIC = "public"
    PROTECTED = "protected"
    ADMIN = "admin"


@dataclass
class IngredientMetadata:
    """Basic ingredient metadata."""
    id: str
    name: str
    description: str
    version: str
    category: IngredientCategory
    dependencies: List[str]
    tags: List[str]
    author: str
    created: datetime
    updated: datetime
    access_level: AccessLevel = AccessLevel.PUBLIC


class PantryManager:
    """
    Simple pantry manager for ingredient registration and retrieval.
    
    Single responsibility: ingredient registration and retrieval.
    """
    
    def __init__(self, pantry_root: str = "recipes/pantry"):
        """Initialize pantry manager."""
        self.pantry_root = Path(pantry_root)
        self.db_path = self.pantry_root / "pantry.db"
        
        # Ensure directory exists
        self.pantry_root.mkdir(parents=True, exist_ok=True)
        
        # Initialize database
        self._init_database()
        
        logger.info(f"Pantry Manager initialized at {self.pantry_root}")
    
    def _init_database(self) -> None:
        """Initialize SQLite database."""
        with self._get_db_connection() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS ingredients (
                    id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    description TEXT,
                    version TEXT NOT NULL,
                    category TEXT NOT NULL,
                    dependencies TEXT,
                    tags TEXT,
                    author TEXT,
                    created TEXT NOT NULL,
                    updated TEXT NOT NULL,
                    access_level TEXT DEFAULT 'public'
                )
            """)
            conn.commit()
    
    @contextmanager
    def _get_db_connection(self):
        """Database connection context manager."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
        finally:
            conn.close()
    
    def register_ingredient(self, ingredient: IngredientMetadata) -> bool:
        """
        Register a new ingredient.
        
        Args:
            ingredient: Ingredient to register
            
        Returns:
            True if successful, False otherwise
        """
        try:
            with self._get_db_connection() as conn:
                conn.execute("""
                    INSERT INTO ingredients 
                    (id, name, description, version, category, dependencies, tags, 
                     author, created, updated, access_level)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    ingredient.id, ingredient.name, ingredient.description, ingredient.version,
                    ingredient.category.value, json.dumps(ingredient.dependencies), json.dumps(ingredient.tags),
                    ingredient.author, ingredient.created.isoformat(), ingredient.updated.isoformat(),
                    ingredient.access_level.value
                ))
                conn.commit()
            
            logger.info(f"Ingredient {ingredient.id} registered")
            return True
            
        except Exception as e:
            logger.error(f"Failed to register ingredient {ingredient.id}: {e}")
            return False
    
    def get_ingredient(self, ingredient_id: str) -> Optional[IngredientMetadata]:
        """
        Get ingredient by ID.
        
        Args:
            ingredient_id: ID of ingredient to retrieve
            
        Returns:
            IngredientMetadata if found, None otherwise
        """
        with self._get_db_connection() as conn:
            row = conn.execute("""
                SELECT * FROM ingredients WHERE id = ?
            """, (ingredient_id,)).fetchone()
            
            if row:
                return self._row_to_ingredient(row)
        
        return None
    
    def list_ingredients(self, category: Optional[IngredientCategory] = None) -> List[IngredientMetadata]:
        """
        List ingredients with optional category filter.
        
        Args:
            category: Optional category filter
            
        Returns:
            List of ingredients
        """
        query = "SELECT * FROM ingredients"
        params = []
        
        if category:
            query += " WHERE category = ?"
            params.append(category.value)
        
        with self._get_db_connection() as conn:
            rows = conn.execute(query, params).fetchall()
            return [self._row_to_ingredient(row) for row in rows]
    
    def _row_to_ingredient(self, row) -> IngredientMetadata:
        """Convert database row to IngredientMetadata."""
        return IngredientMetadata(
            id=row['id'],
            name=row['name'],
            description=row['description'],
            version=row['version'],
            category=IngredientCategory(row['category']),
            dependencies=json.loads(row['dependencies']) if row['dependencies'] else [],
            tags=json.loads(row['tags']) if row['tags'] else [],
            author=row['author'],
            created=datetime.fromisoformat(row['created']),
            updated=datetime.fromisoformat(row['updated']),
            access_level=AccessLevel(row['access_level'])
        ) 