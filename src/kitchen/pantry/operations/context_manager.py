"""
Context Manager - Minimal Recipe Runner & Context Pruning

Demonstrates strict, dependency-driven context management with pruning.
"""

import json
import sys
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime

# Add operations to path
sys.path.append(str(Path(__file__).parent))

from registry import get_operation, list_operations

class ContextManager:
    """Manages minimal, pruned execution context for recipes and tasks"""
    
    def __init__(self, max_context_size: int = 1000):
        self.max_context_size = max_context_size
        self.context_history = []
        
    def create_context(self, dependencies: Dict[str, List[str]]) -> Dict[str, Any]:
        """Create minimal context with only required dependencies"""
        context = {
            'timestamp': datetime.now().isoformat(),
            'operations': {},
            'skills': {},
            'modules': {},
            'data': dependencies.get('input_data', {})
        }
        
        # Load only required tools/operations
        for op_id in dependencies.get('required_tools', []):
            try:
                context['operations'][op_id] = get_operation(op_id)
            except Exception as e:
                print(f"Warning: Could not load operation {op_id}: {e}")
                
        # Load only required skills
        for skill_id in dependencies.get('required_skills', []):
            try:
                context['skills'][skill_id] = get_operation(skill_id)
            except Exception as e:
                print(f"Warning: Could not load skill {skill_id}: {e}")
                
        # Load only required modules
        for module_id in dependencies.get('required_modules', []):
            try:
                context['modules'][module_id] = get_operation(module_id)
            except Exception as e:
                print(f"Warning: Could not load module {module_id}: {e}")
                
        return context
    
    def build_context(self, recipe: Dict[str, Any]) -> Dict[str, Any]:
        """Build minimal context with only required dependencies"""
        context = {
            'recipe_id': recipe.get('id', 'unknown'),
            'timestamp': datetime.now().isoformat(),
            'operations': {},
            'skills': {},
            'modules': {},
            'data': recipe.get('input_data', {})
        }
        
        # Load only required tools/operations
        for op_id in recipe.get('required_tools', []):
            try:
                context['operations'][op_id] = get_operation(op_id)
            except Exception as e:
                print(f"Warning: Could not load operation {op_id}: {e}")
                
        # Load only required skills
        for skill_id in recipe.get('required_skills', []):
            try:
                context['skills'][skill_id] = get_operation(skill_id)
            except Exception as e:
                print(f"Warning: Could not load skill {skill_id}: {e}")
                
        # Load only required modules
        for module_id in recipe.get('required_modules', []):
            try:
                context['modules'][module_id] = get_operation(module_id)
            except Exception as e:
                print(f"Warning: Could not load module {module_id}: {e}")
                
        return context
    
    def prune_context(self, context: Dict[str, Any], keep_keys: List[str]) -> Dict[str, Any]:
        """Prune context to keep only essential data"""
        pruned = {}
        for key in keep_keys:
            if key in context:
                pruned[key] = context[key]
        return pruned
    
    def validate_context_size(self, context: Dict[str, Any]) -> bool:
        """Validate context size and warn if too large"""
        context_str = json.dumps(context, default=str)
        size = len(context_str)
        
        if size > self.max_context_size:
            print(f"Warning: Context size ({size}) exceeds limit ({self.max_context_size})")
            return False
        return True
    
    def execute_recipe(self, recipe_path: str) -> Dict[str, Any]:
        """Execute a recipe with minimal context management"""
        try:
            # Load recipe
            with open(recipe_path, 'r') as f:
                recipe = json.load(f)
                
            print(f"Executing recipe: {recipe.get('id', 'unknown')}")
            
            # Build minimal context
            context = self.build_context(recipe)
            
            # Validate context size
            if not self.validate_context_size(context):
                print("Context too large - pruning...")
                context = self.prune_context(context, ['recipe_id', 'timestamp', 'data'])
            
            # Execute recipe steps
            results = []
            for step in recipe.get('steps', []):
                step_result = self.execute_step(step, context)
                results.append(step_result)
                
                # Prune context after each step
                context = self.prune_context(context, ['recipe_id', 'timestamp', 'data'])
                
            return {
                'success': True,
                'recipe_id': recipe.get('id'),
                'results': results,
                'context_size': len(json.dumps(context, default=str))
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'recipe_id': recipe.get('id', 'unknown')
            }
    
    def execute_step(self, step: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a single step with minimal context"""
        step_id = step.get('step_id', 'unknown')
        print(f"  Executing step: {step_id}")
        
        # Add step-specific context
        step_context = context.copy()
        step_context['step'] = step
        
        # Execute step (simplified - would call actual operation)
        result = {
            'step_id': step_id,
            'status': 'completed',
            'timestamp': datetime.now().isoformat(),
            'context_size': len(json.dumps(step_context, default=str))
        }
        
        return result

def demo_minimal_context():
    """Demonstrate minimal context management"""
    print("🧪 Demo: Minimal Context Management")
    print("=" * 50)
    
    # Sample recipe with explicit dependencies
    sample_recipe = {
        "id": "kos.recipe.demo.content_creation",
        "required_tools": ["tools.image_editing.image_editor_operations"],
        "required_skills": ["skills.content_creator_skill"],
        "required_modules": ["modules.content_creation_module"],
        "input_data": {"topic": "AI trends", "platform": "twitter"},
        "steps": [
            {"step_id": "STEP-01", "description": "Generate content"},
            {"step_id": "STEP-02", "description": "Optimize for platform"}
        ]
    }
    
    # Create context manager
    manager = ContextManager(max_context_size=5000)
    
    # Build context
    context = manager.build_context(sample_recipe)
    print(f"Initial context size: {len(json.dumps(context, default=str))}")
    print(f"Loaded operations: {list(context['operations'].keys())}")
    print(f"Loaded skills: {list(context['skills'].keys())}")
    print(f"Loaded modules: {list(context['modules'].keys())}")
    
    # Prune context
    pruned = manager.prune_context(context, ['recipe_id', 'timestamp'])
    print(f"Pruned context size: {len(json.dumps(pruned, default=str))}")
    
    print("\n✅ Demo completed successfully!")
    print("\n📝 Key Points:")
    print("   • Only required dependencies are loaded")
    print("   • Context is pruned after each step")
    print("   • Context size is validated and controlled")
    print("   • No global state or unnecessary data")

if __name__ == "__main__":
    demo_minimal_context() 