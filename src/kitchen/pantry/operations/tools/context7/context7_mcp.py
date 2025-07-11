"""
Context7 MCP Command Executor - Kitchen Pantry Operation
=====================================================

This module provides MCP command execution functionality for Context7 operations.

Author: kOS Kitchen System
Version: 1.0.0
Created: 2025-07-08T11:20:00Z
"""

import json
import logging
import subprocess
import asyncio
from typing import Dict, List, Any


class Context7MCPExecutor:
    """MCP command executor for Context7 operations."""
    
    def __init__(self):
        """Initialize the MCP executor."""
        self.logger = logging.getLogger('context7_mcp')
    
    def get_context7_command(self) -> str:
        """
        Get the appropriate Context7 command based on available package managers.
        
        Returns:
            Available package manager command
        """
        # Try different package managers in order of preference
        package_managers = ["bunx", "npx", "yarn", "pnpm"]
        
        for pm in package_managers:
            try:
                # Check if package manager is available
                result = subprocess.run([pm, "--version"], capture_output=True, text=True, timeout=5)
                if result.returncode == 0:
                    self.logger.info(f"Using package manager: {pm}")
                    return pm
            except (subprocess.TimeoutExpired, FileNotFoundError):
                continue
        
        # Default to npx
        self.logger.warning("No package manager found, defaulting to npx")
        return "npx"
    
    async def execute_mcp_command(self, command: str, args: List[str], mcp_request: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute MCP command and return result.
        
        Args:
            command: Package manager command
            args: Command arguments
            mcp_request: MCP request dictionary
            
        Returns:
            MCP response result
            
        Raises:
            Exception: If command execution fails
        """
        try:
            # Prepare the full command
            full_command = [command] + args
            
            # Create process
            process = await asyncio.create_subprocess_exec(
                *full_command,
                stdin=asyncio.subprocess.PIPE,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            # Send MCP request
            request_json = json.dumps(mcp_request) + "\n"
            stdout, stderr = await process.communicate(input=request_json.encode())
            
            if process.returncode != 0:
                raise Exception(f"Context7 command failed: {stderr.decode()}")
            
            # Parse response
            response_lines = stdout.decode().strip().split('\n')
            for line in response_lines:
                if line.strip():
                    try:
                        response = json.loads(line)
                        if "result" in response:
                            return response["result"]
                        elif "error" in response:
                            raise Exception(f"Context7 error: {response['error']}")
                    except json.JSONDecodeError:
                        continue
            
            raise Exception("No valid response from Context7")
            
        except Exception as e:
            self.logger.error(f"Failed to execute MCP command: {e}")
            raise
    
    def create_resolve_request(self, library_name: str) -> Dict[str, Any]:
        """
        Create MCP request for library ID resolution.
        
        Args:
            library_name: Name of the library to resolve
            
        Returns:
            MCP request dictionary
        """
        return {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "tools/call",
            "params": {
                "name": "resolve-library-id",
                "arguments": {
                    "libraryName": library_name
                }
            }
        }
    
    def create_docs_request(self, library_id: str, topic: str | None = None, tokens: int = 10000) -> Dict[str, Any]:
        """
        Create MCP request for library documentation.
        
        Args:
            library_id: Context7-compatible library ID
            topic: Optional topic focus
            tokens: Maximum tokens to return
            
        Returns:
            MCP request dictionary
        """
        request = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "tools/call",
            "params": {
                "name": "get-library-docs",
                "arguments": {
                    "context7CompatibleLibraryID": library_id,
                    "tokens": tokens
                }
            }
        }
        
        if topic:
            request["params"]["arguments"]["topic"] = topic
        
        return request 