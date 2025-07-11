"""
Context7 MCP Client - Kitchen Pantry Operation
==============================================

This module provides Context7 MCP server integration for the kOS kitchen system.
It enables fetching up-to-date code documentation for libraries and frameworks.

Author: kOS Kitchen System
Version: 1.0.0
Created: 2025-07-08T10:25:00Z
Updated: 2025-07-08T11:15:00Z
"""

import json
import logging
import subprocess
import asyncio
from typing import Dict, List, Optional, Any, Union
from pathlib import Path
from datetime import datetime

from .context7_rate_limiter import RateLimiter
from .context7_cache import Context7Cache
from .context7_mcp import Context7MCPExecutor

logger = logging.getLogger(__name__)


class Context7Client:
    """
    Context7 MCP client for fetching up-to-date code documentation.
    
    This client provides:
    - Library ID resolution
    - Documentation fetching
    - Caching and performance optimization
    - Error handling and retry logic
    """
    
    def __init__(self, config_path: Optional[Union[str, Path]] = None):
        """
        Initialize the Context7 client.
        
        Args:
            config_path: Path to Context7 configuration file
        """
        self.logger = self._setup_logging()
        self.logger.info("Initializing Context7 MCP Client")
        
        # Load configuration
        self.config = self._load_config(config_path)
        
        # Initialize cache and rate limiter
        cache_config = self.config.get("performance_optimization", {}).get("caching", {})
        rate_config = self.config.get("performance_optimization", {}).get("rate_limiting", {})
        
        self.cache = Context7Cache(
            cache_dir=Path(cache_config.get("cache_location", "kitchen/cache/context7")),
            enabled=cache_config.get("enabled", True),
            cache_duration=cache_config.get("cache_duration", "24_hours")
        )
        
        self.rate_limiter = RateLimiter(
            requests_per_minute=rate_config.get("requests_per_minute", 60),
            burst_limit=rate_config.get("burst_limit", 10)
        )
        
        # Initialize MCP executor
        self.mcp_executor = Context7MCPExecutor()
        
        self.logger.info("Context7 MCP Client initialized successfully")
    
    def _setup_logging(self) -> logging.Logger:
        """Setup logging for the Context7 client."""
        logger = logging.getLogger('context7_client')
        logger.setLevel(logging.INFO)
        
        if not logger.handlers:
            # Console handler
            console_handler = logging.StreamHandler()
            console_handler.setLevel(logging.INFO)
            
            # File handler
            log_dir = Path("logs")
            log_dir.mkdir(exist_ok=True)
            file_handler = logging.FileHandler(log_dir / "context7_client.log")
            file_handler.setLevel(logging.DEBUG)
            
            # Formatter
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            console_handler.setFormatter(formatter)
            file_handler.setFormatter(formatter)
            
            logger.addHandler(console_handler)
            logger.addHandler(file_handler)
        
        return logger
    
    def _load_config(self, config_path: Optional[Union[str, Path]]) -> Dict[str, Any]:
        """Load Context7 configuration."""
        if config_path is None:
            config_path = Path(__file__).parent.parent.parent.parent / "config" / "context7_integration.json"
        
        config_path = Path(config_path)
        
        if config_path.exists():
            try:
                with open(config_path, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                self.logger.info(f"Loaded Context7 configuration from {config_path}")
                return config
            except Exception as e:
                self.logger.warning(f"Failed to load Context7 config from {config_path}: {e}")
        
        # Default configuration
        default_config = {
            "context7_server": {
                "enabled": True,
                "package": "@upstash/context7-mcp",
                "transport": "stdio",
                "auto_start": True,
                "health_check": True
            },
            "performance_optimization": {
                "caching": {
                    "enabled": True,
                    "cache_duration": "24_hours",
                    "cache_location": "kitchen/cache/context7"
                },
                "rate_limiting": {
                    "enabled": True,
                    "requests_per_minute": 60,
                    "burst_limit": 10
                }
            }
        }
        
        self.logger.info("Using default Context7 configuration")
        return default_config
    
    async def resolve_library_id(self, library_name: str) -> Dict[str, Any]:
        """
        Resolve a general library name into a Context7-compatible library ID.
        
        Args:
            library_name: The name of the library to search for
            
        Returns:
            Dictionary with library ID and confidence score
        """
        try:
            # Check rate limit
            if not self.rate_limiter.can_proceed():
                raise Exception("Rate limit exceeded")
            
            # Check cache first
            cache_key = f"resolve_{library_name.lower()}"
            cached_result = self.cache.get(cache_key)
            if cached_result:
                self.logger.info(f"Returning cached library ID for {library_name}")
                return cached_result
            
            # Execute Context7 command
            command = self.mcp_executor.get_context7_command()
            args = ["-y", "@upstash/context7-mcp@latest"]
            
            # Create MCP request
            mcp_request = self.mcp_executor.create_resolve_request(library_name)
            
            # Execute command
            result = await self.mcp_executor.execute_mcp_command(command, args, mcp_request)
            
            # Cache result
            self.cache.save(cache_key, result)
            
            self.logger.info(f"Resolved library ID for {library_name}: {result}")
            return result
            
        except Exception as e:
            self.logger.error(f"Failed to resolve library ID for {library_name}: {e}")
            return {
                "error": str(e),
                "libraryId": None,
                "confidence": 0.0
            }
    
    async def get_library_docs(self, library_id: str, topic: Optional[str] = None, tokens: int = 10000) -> Dict[str, Any]:
        """
        Fetch documentation for a library using a Context7-compatible library ID.
        
        Args:
            library_id: Exact Context7-compatible library ID
            topic: Focus the docs on a specific topic
            tokens: Max number of tokens to return
            
        Returns:
            Dictionary with documentation content and metadata
        """
        try:
            # Check rate limit
            if not self.rate_limiter.can_proceed():
                raise Exception("Rate limit exceeded")
            
            # Check cache first
            cache_key = f"docs_{library_id}_{topic}_{tokens}"
            cached_result = self.cache.get(cache_key)
            if cached_result:
                self.logger.info(f"Returning cached documentation for {library_id}")
                return cached_result
            
            # Execute Context7 command
            command = self.mcp_executor.get_context7_command()
            args = ["-y", "@upstash/context7-mcp@latest"]
            
            # Create MCP request
            mcp_request = self.mcp_executor.create_docs_request(library_id, topic, tokens)
            
            # Execute command
            result = await self.mcp_executor.execute_mcp_command(command, args, mcp_request)
            
            # Cache result
            self.cache.save(cache_key, result)
            
            self.logger.info(f"Fetched documentation for {library_id}")
            return result
            
        except Exception as e:
            self.logger.error(f"Failed to fetch documentation for {library_id}: {e}")
            return {
                "error": str(e),
                "documentation": None,
                "metadata": None
            }
    

    

    
    async def health_check(self) -> Dict[str, Any]:
        """Perform health check on Context7 service."""
        try:
            # Try to resolve a simple library
            result = await self.resolve_library_id("react")
            
            if "error" in result:
                return {
                    "status": "unhealthy",
                    "error": result["error"],
                    "timestamp": datetime.utcnow().isoformat() + "Z"
                }
            
            return {
                "status": "healthy",
                "timestamp": datetime.utcnow().isoformat() + "Z",
                "response_time": "normal"
            }
            
        except Exception as e:
            return {
                "status": "unhealthy",
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat() + "Z"
            }


 