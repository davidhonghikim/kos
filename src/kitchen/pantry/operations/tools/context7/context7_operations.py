"""
Context7 Operations - Kitchen Pantry Operation
============================================

This module provides kitchen operation interface functions for Context7 MCP client.

Author: kOS Kitchen System
Version: 1.0.0
Created: 2025-07-08T11:15:00Z
"""

from typing import Dict, Any, Optional
from .context7_client import Context7Client


async def resolve_library_id_operation(library_name: str) -> Dict[str, Any]:
    """
    Kitchen operation for resolving library ID.
    
    Args:
        library_name: The name of the library to search for
        
    Returns:
        Dictionary with library ID and confidence score
    """
    client = Context7Client()
    return await client.resolve_library_id(library_name)


async def get_library_docs_operation(library_id: str, topic: Optional[str] = None, tokens: int = 10000) -> Dict[str, Any]:
    """
    Kitchen operation for getting library documentation.
    
    Args:
        library_id: Exact Context7-compatible library ID
        topic: Focus the docs on a specific topic
        tokens: Max number of tokens to return
        
    Returns:
        Dictionary with documentation content and metadata
    """
    client = Context7Client()
    return await client.get_library_docs(library_id, topic, tokens)


async def context7_health_check_operation() -> Dict[str, Any]:
    """
    Kitchen operation for Context7 health check.
    
    Returns:
        Dictionary with health status information
    """
    client = Context7Client()
    return await client.health_check()


async def context7_cache_stats_operation() -> Dict[str, Any]:
    """
    Kitchen operation for getting Context7 cache statistics.
    
    Returns:
        Dictionary with cache statistics
    """
    client = Context7Client()
    return client.cache.get_cache_stats()


async def context7_rate_limit_stats_operation() -> Dict[str, Any]:
    """
    Kitchen operation for getting Context7 rate limit statistics.
    
    Returns:
        Dictionary with rate limit usage statistics
    """
    client = Context7Client()
    return client.rate_limiter.get_current_usage()


async def clear_context7_cache_operation() -> Dict[str, Any]:
    """
    Kitchen operation for clearing Context7 cache.
    
    Returns:
        Dictionary with operation result
    """
    client = Context7Client()
    client.cache.clear()
    return {
        "status": "success",
        "message": "Context7 cache cleared successfully",
        "timestamp": client.cache.cache_dir.stat().st_mtime if client.cache.cache_dir.exists() else None
    }


async def reset_context7_rate_limiter_operation() -> Dict[str, Any]:
    """
    Kitchen operation for resetting Context7 rate limiter.
    
    Returns:
        Dictionary with operation result
    """
    client = Context7Client()
    client.rate_limiter.reset()
    return {
        "status": "success",
        "message": "Context7 rate limiter reset successfully",
        "timestamp": client.rate_limiter.requests[-1] if client.rate_limiter.requests else None
    } 