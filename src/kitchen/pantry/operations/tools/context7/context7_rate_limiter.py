"""
Context7 Rate Limiter - Kitchen Pantry Operation
===============================================

This module provides rate limiting functionality for Context7 MCP client operations.

Author: kOS Kitchen System
Version: 1.0.0
Created: 2025-07-08T11:15:00Z
"""

import time
from typing import List


class RateLimiter:
    """Simple rate limiter for Context7 API calls."""
    
    def __init__(self, requests_per_minute: int = 60, burst_limit: int = 10):
        """
        Initialize the rate limiter.
        
        Args:
            requests_per_minute: Maximum requests allowed per minute
            burst_limit: Maximum burst requests allowed
        """
        self.requests_per_minute = requests_per_minute
        self.burst_limit = burst_limit
        self.requests: List[float] = []
    
    def can_proceed(self) -> bool:
        """
        Check if request can proceed based on rate limits.
        
        Returns:
            True if request can proceed, False otherwise
        """
        now = time.time()
        
        # Remove old requests (older than 1 minute)
        self.requests = [req_time for req_time in self.requests if now - req_time < 60]
        
        # Check if we're within limits
        if len(self.requests) < self.burst_limit:
            self.requests.append(now)
            return True
        
        return False
    
    def get_current_usage(self) -> dict:
        """
        Get current rate limit usage statistics.
        
        Returns:
            Dictionary with usage statistics
        """
        now = time.time()
        recent_requests = [req_time for req_time in self.requests if now - req_time < 60]
        
        return {
            "current_requests": len(recent_requests),
            "burst_limit": self.burst_limit,
            "requests_per_minute": self.requests_per_minute,
            "can_proceed": len(recent_requests) < self.burst_limit
        }
    
    def reset(self) -> None:
        """Reset the rate limiter state."""
        self.requests.clear() 