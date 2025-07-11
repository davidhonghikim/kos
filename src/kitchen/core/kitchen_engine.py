"""
kOS Kitchen Engine - Main Orchestration System
==============================================

The Kitchen Engine is the central orchestrator for the kOS kitchen system.
It manages recipe execution, pantry access, and coordinates all kitchen components.

Author: kOS Kitchen System
Version: 1.0.0
Created: 2025-07-08T02:00:00Z
"""

import os
import sys
import json
import logging
from pathlib import Path
from typing import Dict, List, Optional, Any, Union
from datetime import datetime
import traceback

# Add kitchen core to path
sys.path.insert(0, str(Path(__file__).parent))

# Import from pantry operations
pantry_ops_path = Path(__file__).parent.parent / "pantry" / "operations"
sys.path.insert(0, str(pantry_ops_path))

from registry import OperationRegistry
from context_manager import ContextManager

class KitchenEngine:
    """
    Main kitchen engine that orchestrates the entire kOS kitchen system.
    
    The Kitchen Engine provides:
    - Recipe execution and management
    - Pantry ingredient access and loading
    - Context management and optimization
    - Error handling and recovery
    - System monitoring and logging
    """
    
    def __init__(self, config_path: Optional[Union[str, Path]] = None):
        """
        Initialize the Kitchen Engine.
        
        Args:
            config_path: Path to kitchen configuration file
        """
        self.logger = self._setup_logging()
        self.logger.info("Initializing kOS Kitchen Engine")
        
        # Load configuration
        self.config = self._load_config(config_path)
        
        # Initialize core components
        self.registry = OperationRegistry()
        self.context_manager = ContextManager()
        
        # System state
        self.is_running = False
        self.active_recipes = {}
        self.execution_history = []
        
        self.logger.info("Kitchen Engine initialized successfully")
    
    def _setup_logging(self) -> logging.Logger:
        """Setup logging for the kitchen engine."""
        logger = logging.getLogger('kitchen_engine')
        logger.setLevel(logging.INFO)
        
        # Create handlers
        if not logger.handlers:
            # Console handler
            console_handler = logging.StreamHandler()
            console_handler.setLevel(logging.INFO)
            
            # File handler
            log_dir = Path("logs")
            log_dir.mkdir(exist_ok=True)
            file_handler = logging.FileHandler(log_dir / "kitchen_engine.log")
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
        """Load kitchen configuration."""
        if config_path is None:
            config_path = Path(__file__).parent.parent / "config" / "kitchen_config.json"
        
        config_path = Path(config_path)
        
        if config_path.exists():
            try:
                with open(config_path, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                self.logger.info(f"Loaded configuration from {config_path}")
                return config
            except Exception as e:
                self.logger.warning(f"Failed to load config from {config_path}: {e}")
        
        # Default configuration
        default_config = {
            "kitchen": {
                "name": "kOS Kitchen",
                "version": "1.0.0",
                "max_concurrent_recipes": 5,
                "context_window_size": 28000,
                "timeout_seconds": 300
            },
            "pantry": {
                "path": "pantry",
                "auto_discover": True,
                "validate_ingredients": True
            },
            "recipes": {
                "path": "recipes",
                "auto_discover": True,
                "validate_recipes": True
            },
            "logging": {
                "level": "INFO",
                "file": "logs/kitchen_engine.log",
                "max_size_mb": 10,
                "backup_count": 5
            }
        }
        
        self.logger.info("Using default configuration")
        return default_config
    
    def start(self) -> Dict[str, Any]:
        """
        Start the kitchen engine.
        
        Returns:
            Dictionary with startup status and information
        """
        try:
            self.logger.info("Starting kOS Kitchen Engine")
            
            # Initialize registry
            self.registry.discover_operations()
            self.logger.info(f"Discovered {len(self.registry.get_all_operations())} operations")
            
            # Initialize context manager
            self.context_manager.initialize()
            
            # Mark as running
            self.is_running = True
            
            result = {
                "status": "success",
                "message": "Kitchen Engine started successfully",
                "timestamp": datetime.utcnow().isoformat() + "Z",
                "operations_count": len(self.registry.get_all_operations()),
                "config": self.config
            }
            
            self.logger.info("Kitchen Engine started successfully")
            return result
            
        except Exception as e:
            self.logger.error(f"Failed to start Kitchen Engine: {e}")
            self.logger.error(traceback.format_exc())
            
            return {
                "status": "error",
                "message": f"Failed to start Kitchen Engine: {str(e)}",
                "timestamp": datetime.utcnow().isoformat() + "Z",
                "error": str(e)
            }
    
    def stop(self) -> Dict[str, Any]:
        """
        Stop the kitchen engine.
        
        Returns:
            Dictionary with shutdown status
        """
        try:
            self.logger.info("Stopping kOS Kitchen Engine")
            
            # Stop all active recipes
            for recipe_id in list(self.active_recipes.keys()):
                self.stop_recipe(recipe_id)
            
            # Mark as stopped
            self.is_running = False
            
            result = {
                "status": "success",
                "message": "Kitchen Engine stopped successfully",
                "timestamp": datetime.utcnow().isoformat() + "Z"
            }
            
            self.logger.info("Kitchen Engine stopped successfully")
            return result
            
        except Exception as e:
            self.logger.error(f"Failed to stop Kitchen Engine: {e}")
            
            return {
                "status": "error",
                "message": f"Failed to stop Kitchen Engine: {str(e)}",
                "timestamp": datetime.utcnow().isoformat() + "Z",
                "error": str(e)
            }
    
    def execute_recipe(self, recipe_id: str, parameters: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Execute a recipe with the given parameters.
        
        Args:
            recipe_id: ID of the recipe to execute
            parameters: Optional parameters for the recipe
            
        Returns:
            Dictionary with execution results
        """
        if not self.is_running:
            return {
                "status": "error",
                "message": "Kitchen Engine is not running",
                "timestamp": datetime.utcnow().isoformat() + "Z"
            }
        
        try:
            self.logger.info(f"Executing recipe: {recipe_id}")
            
            # Load recipe
            recipe = self._load_recipe(recipe_id)
            if not recipe:
                return {
                    "status": "error",
                    "message": f"Recipe not found: {recipe_id}",
                    "timestamp": datetime.utcnow().isoformat() + "Z"
                }
            
            # Validate recipe
            validation_result = self._validate_recipe(recipe)
            if not validation_result["valid"]:
                return {
                    "status": "error",
                    "message": f"Recipe validation failed: {validation_result['errors']}",
                    "timestamp": datetime.utcnow().isoformat() + "Z",
                    "validation_errors": validation_result["errors"]
                }
            
            # Build execution context
            context = self.context_manager.build_context(recipe, parameters or {})
            
            # Execute recipe
            execution_id = f"{recipe_id}_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}"
            self.active_recipes[execution_id] = {
                "recipe_id": recipe_id,
                "start_time": datetime.utcnow(),
                "status": "running",
                "context": context
            }
            
            # Execute steps
            results = []
            for step in recipe.get("steps", []):
                step_result = self._execute_step(step, context)
                results.append(step_result)
                
                if step_result["status"] == "error":
                    break
            
            # Update execution status
            final_status = "completed" if all(r["status"] == "success" for r in results) else "failed"
            self.active_recipes[execution_id]["status"] = final_status
            self.active_recipes[execution_id]["end_time"] = datetime.utcnow()
            self.active_recipes[execution_id]["results"] = results
            
            # Add to history
            self.execution_history.append({
                "execution_id": execution_id,
                "recipe_id": recipe_id,
                "start_time": self.active_recipes[execution_id]["start_time"],
                "end_time": self.active_recipes[execution_id]["end_time"],
                "status": final_status,
                "results": results
            })
            
            result = {
                "status": "success",
                "execution_id": execution_id,
                "recipe_id": recipe_id,
                "final_status": final_status,
                "results": results,
                "timestamp": datetime.utcnow().isoformat() + "Z"
            }
            
            self.logger.info(f"Recipe execution completed: {recipe_id} - {final_status}")
            return result
            
        except Exception as e:
            self.logger.error(f"Recipe execution failed: {recipe_id} - {e}")
            self.logger.error(traceback.format_exc())
            
            return {
                "status": "error",
                "message": f"Recipe execution failed: {str(e)}",
                "recipe_id": recipe_id,
                "timestamp": datetime.utcnow().isoformat() + "Z",
                "error": str(e)
            }
    
    def _load_recipe(self, recipe_id: str) -> Optional[Dict[str, Any]]:
        """Load a recipe from the recipes directory."""
        recipes_path = Path(__file__).parent.parent / "recipes"
        
        # Try to find recipe file
        recipe_file = recipes_path / f"{recipe_id}.json"
        if recipe_file.exists():
            try:
                with open(recipe_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                self.logger.error(f"Failed to load recipe {recipe_id}: {e}")
                return None
        
        # Try subdirectories
        for subdir in recipes_path.iterdir():
            if subdir.is_dir():
                recipe_file = subdir / f"{recipe_id}.json"
                if recipe_file.exists():
                    try:
                        with open(recipe_file, 'r', encoding='utf-8') as f:
                            return json.load(f)
                    except Exception as e:
                        self.logger.error(f"Failed to load recipe {recipe_id}: {e}")
                        continue
        
        return None
    
    def _validate_recipe(self, recipe: Dict[str, Any]) -> Dict[str, Any]:
        """Validate a recipe structure."""
        errors = []
        
        # Check required fields
        required_fields = ["id", "name", "description", "steps"]
        for field in required_fields:
            if field not in recipe:
                errors.append(f"Missing required field: {field}")
        
        # Validate steps
        if "steps" in recipe:
            for i, step in enumerate(recipe["steps"]):
                if not isinstance(step, dict):
                    errors.append(f"Step {i} must be a dictionary")
                    continue
                
                if "operation" not in step:
                    errors.append(f"Step {i} missing 'operation' field")
        
        return {
            "valid": len(errors) == 0,
            "errors": errors
        }
    
    def _execute_step(self, step: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a single recipe step."""
        try:
            operation_name = step.get("operation")
            parameters = step.get("parameters", {})
            
            # Get operation from registry
            operation = self.registry.get_operation(operation_name)
            if not operation:
                return {
                    "status": "error",
                    "message": f"Operation not found: {operation_name}",
                    "step": step
                }
            
            # Execute operation
            result = operation.execute(parameters, context)
            
            return {
                "status": "success",
                "operation": operation_name,
                "result": result,
                "step": step
            }
            
        except Exception as e:
            self.logger.error(f"Step execution failed: {e}")
            return {
                "status": "error",
                "message": f"Step execution failed: {str(e)}",
                "step": step,
                "error": str(e)
            }
    
    def stop_recipe(self, execution_id: str) -> Dict[str, Any]:
        """Stop a running recipe execution."""
        if execution_id not in self.active_recipes:
            return {
                "status": "error",
                "message": f"Execution not found: {execution_id}"
            }
        
        try:
            self.active_recipes[execution_id]["status"] = "stopped"
            self.active_recipes[execution_id]["end_time"] = datetime.utcnow()
            
            return {
                "status": "success",
                "message": f"Recipe execution stopped: {execution_id}"
            }
            
        except Exception as e:
            return {
                "status": "error",
                "message": f"Failed to stop recipe: {str(e)}"
            }
    
    def get_status(self) -> Dict[str, Any]:
        """Get the current status of the kitchen engine."""
        return {
            "status": "running" if self.is_running else "stopped",
            "active_recipes": len(self.active_recipes),
            "total_operations": len(self.registry.get_all_operations()),
            "execution_history_count": len(self.execution_history),
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "config": self.config
        }
    
    def get_available_recipes(self) -> List[Dict[str, Any]]:
        """Get list of available recipes."""
        recipes_path = Path(__file__).parent.parent / "recipes"
        recipes = []
        
        if recipes_path.exists():
            for recipe_file in recipes_path.rglob("*.json"):
                try:
                    with open(recipe_file, 'r', encoding='utf-8') as f:
                        recipe = json.load(f)
                        if "id" in recipe and "name" in recipe:
                            recipes.append({
                                "id": recipe["id"],
                                "name": recipe["name"],
                                "description": recipe.get("description", ""),
                                "path": str(recipe_file.relative_to(recipes_path))
                            })
                except Exception as e:
                    self.logger.warning(f"Failed to load recipe {recipe_file}: {e}")
        
        return recipes


def main():
    """Main function for testing the kitchen engine."""
    engine = KitchenEngine()
    
    # Start the engine
    start_result = engine.start()
    print("Start result:", json.dumps(start_result, indent=2))
    
    if start_result["status"] == "success":
        # Get status
        status = engine.get_status()
        print("Status:", json.dumps(status, indent=2))
        
        # Get available recipes
        recipes = engine.get_available_recipes()
        print(f"Available recipes: {len(recipes)}")
        for recipe in recipes[:5]:  # Show first 5
            print(f"  - {recipe['id']}: {recipe['name']}")
        
        # Stop the engine
        stop_result = engine.stop()
        print("Stop result:", json.dumps(stop_result, indent=2))


if __name__ == "__main__":
    main() 