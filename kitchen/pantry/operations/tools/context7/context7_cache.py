"""
Context7 Cache Manager - Kitchen Pantry Operation
===============================================

This module provides caching functionality for Context7 MCP client operations.

Author: kOS Kitchen System
Version: 1.0.0
Created: 2025-07-08T11:15:00Z
"""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional


class Context7Cache:
    """Cache manager for Context7 API responses."""
    
    def __init__(self, cache_dir: Path, enabled: bool = True, cache_duration: str = "24_hours"):
        """
        Initialize the cache manager.
        
        Args:
            cache_dir: Directory to store cache files
            enabled: Whether caching is enabled
            cache_duration: Cache duration (e.g., "24_hours")
        """
        self.cache_dir = cache_dir
        self.enabled = enabled
        self.cache_duration = cache_duration
        self.logger = logging.getLogger('context7_cache')
        
        # Create cache directory if it doesn't exist
        if self.enabled:
            self.cache_dir.mkdir(parents=True, exist_ok=True)
    
    def get(self, cache_key: str) -> Optional[Dict[str, Any]]:
        """
        Get result from cache.
        
        Args:
            cache_key: Unique key for the cached data
            
        Returns:
            Cached data if valid, None otherwise
        """
        if not self.enabled:
            return None
        
        cache_file = self.cache_dir / f"{cache_key}.json"
        if cache_file.exists():
            try:
                with open(cache_file, 'r', encoding='utf-8') as f:
                    cached_data = json.load(f)
                
                # Check if cache is still valid
                if self._is_cache_valid(cached_data):
                    return cached_data.get("data")
                else:
                    # Remove expired cache
                    cache_file.unlink()
                    self.logger.info(f"Removed expired cache: {cache_key}")
            except Exception as e:
                self.logger.warning(f"Failed to read cache {cache_key}: {e}")
        
        return None
    
    def save(self, cache_key: str, data: Dict[str, Any]) -> None:
        """
        Save result to cache.
        
        Args:
            cache_key: Unique key for the cached data
            data: Data to cache
        """
        if not self.enabled:
            return
        
        try:
            cache_file = self.cache_dir / f"{cache_key}.json"
            cache_data = {
                "data": data,
                "cached_at": datetime.utcnow().isoformat() + "Z",
                "cache_duration": self.cache_duration
            }
            
            with open(cache_file, 'w', encoding='utf-8') as f:
                json.dump(cache_data, f, indent=2)
            
            self.logger.info(f"Cached data for key: {cache_key}")
                
        except Exception as e:
            self.logger.warning(f"Failed to save cache {cache_key}: {e}")
    
    def _is_cache_valid(self, cached_data: Dict[str, Any]) -> bool:
        """
        Check if cache is still valid.
        
        Args:
            cached_data: Cached data dictionary
            
        Returns:
            True if cache is valid, False otherwise
        """
        try:
            cached_at = datetime.fromisoformat(cached_data.get("cached_at", "").replace("Z", "+00:00"))
            now = datetime.utcnow()
            
            # Parse cache duration
            if self.cache_duration == "24_hours":
                duration_hours = 24
            elif self.cache_duration == "1_hour":
                duration_hours = 1
            elif self.cache_duration == "12_hours":
                duration_hours = 12
            else:
                # Default to 24 hours
                duration_hours = 24
            
            # Check if cache is expired
            time_diff = now - cached_at.replace(tzinfo=None)
            return time_diff.total_seconds() < (duration_hours * 3600)
            
        except Exception as e:
            self.logger.warning(f"Failed to validate cache: {e}")
            return False
    
    def clear(self) -> None:
        """Clear all cached data."""
        if not self.enabled:
            return
        
        try:
            for cache_file in self.cache_dir.glob("*.json"):
                cache_file.unlink()
            self.logger.info("Cleared all cached data")
        except Exception as e:
            self.logger.warning(f"Failed to clear cache: {e}")
    
    def get_cache_stats(self) -> Dict[str, Any]:
        """
        Get cache statistics.
        
        Returns:
            Dictionary with cache statistics
        """
        if not self.enabled:
            return {"enabled": False}
        
        try:
            cache_files = list(self.cache_dir.glob("*.json"))
            total_size = sum(f.stat().st_size for f in cache_files)
            
            return {
                "enabled": True,
                "cache_directory": str(self.cache_dir),
                "cache_duration": self.cache_duration,
                "total_files": len(cache_files),
                "total_size_bytes": total_size,
                "total_size_mb": round(total_size / (1024 * 1024), 2)
            }
        except Exception as e:
            self.logger.warning(f"Failed to get cache stats: {e}")
            return {"enabled": True, "error": str(e)} 