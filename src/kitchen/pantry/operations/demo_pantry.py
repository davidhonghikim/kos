#!/usr/bin/env python3
"""
Pantry System Demonstration
Shows practical examples of what the pantry system can do
"""

import sys
from pathlib import Path
from datetime import datetime

# Add the pantry directory to the path
sys.path.insert(0, str(Path(__file__).parent))

from core.pantry_manager import PantryManager, IngredientMetadata, IngredientCategory, AccessLevel
from core.dependency_tracker import DependencyTracker
from core.access_control import AccessControl, Permission
from core.discovery_engine import DiscoveryEngine
from core.validation_system import ValidationSystem

def demo_pantry_system():
    """Demonstrate pantry system capabilities"""
    print("🏪 PANTRY SYSTEM DEMONSTRATION")
    print("=" * 50)
    
    # Initialize pantry system
    pantry = PantryManager()
    tracker = DependencyTracker(pantry)
    access = AccessControl(pantry)
    discovery = DiscoveryEngine(pantry)
    validator = ValidationSystem(pantry)
    
    # Example 1: Register a new ingredient
    print("\n1️⃣ REGISTERING A NEW INGREDIENT")
    print("-" * 30)
    
    new_task = IngredientMetadata(
        id='task.data_analyzer',
        name='Data Analysis Task',
        description='Performs statistical analysis on datasets',
        version='2.1.0',
        category=IngredientCategory.TASKS,
        dependencies=['tool.pandas', 'module.statistics'],
        tags=['data', 'analysis', 'statistics', 'pandas'],
        author='data_team',
        created=datetime.now(),
        updated=datetime.now(),
        access_level=AccessLevel.PROTECTED
    )
    
    success = pantry.register_ingredient(new_task)
    print(f"✅ Registered: {success}")
    print(f"📝 Task ID: {new_task.id}")
    print(f"🏷️  Tags: {new_task.tags}")
    print(f"🔗 Dependencies: {new_task.dependencies}")
    
    # Example 2: Dependency tracking
    print("\n2️⃣ DEPENDENCY TRACKING")
    print("-" * 30)
    
    deps = tracker.get_dependencies('task.data_analyzer')
    print(f"📋 Direct dependencies: {deps}")
    
    resolved = tracker.resolve_dependencies('task.data_analyzer')
    print(f"🔍 All dependencies (including transitive): {resolved}")
    
    info = tracker.get_dependency_info('task.data_analyzer')
    if info:
        print(f"⚠️  Conflicts: {info.conflicts}")
        print(f"📊 Dependents: {info.dependents}")
    
    # Example 3: Access control
    print("\n3️⃣ ACCESS CONTROL")
    print("-" * 30)
    
    # Test different user access levels
    users = ['anonymous', 'developer', 'admin']
    for user in users:
        can_read = access.can_access(user, 'task.data_analyzer', Permission.READ)
        can_write = access.can_access(user, 'task.data_analyzer', Permission.WRITE)
        print(f"👤 {user:12} | Read: {can_read} | Write: {can_write}")
    
    # Example 4: Discovery
    print("\n4️⃣ INGREDIENT DISCOVERY")
    print("-" * 30)
    
    discovered = discovery.discover_ingredients()
    print(f"🔍 Found {len(discovered)} ingredients in filesystem")
    
    # Example 5: Validation
    print("\n5️⃣ VALIDATION & QUALITY CONTROL")
    print("-" * 30)
    
    validation = validator.validate_ingredient(new_task)
    print(f"✅ Valid: {validation.valid}")
    if validation.errors:
        print(f"❌ Errors: {validation.errors}")
    if validation.warnings:
        print(f"⚠️  Warnings: {validation.warnings}")
    
    # Example 6: Listing and searching
    print("\n6️⃣ INGREDIENT BROWSING")
    print("-" * 30)
    
    all_ingredients = pantry.list_ingredients()
    print(f"📦 Total ingredients: {len(all_ingredients)}")
    
    tasks = pantry.list_ingredients(IngredientCategory.TASKS)
    print(f"📋 Tasks: {len(tasks)}")
    
    for task in tasks:
        print(f"  • {task.id} (v{task.version}) - {task.name}")
    
    print("\n🎉 Pantry system demonstration complete!")

def show_ingredient_examples():
    """Show examples of different ingredient types"""
    print("\n📚 INGREDIENT TYPE EXAMPLES")
    print("=" * 50)
    
    # Task example
    print("\n🔧 TASK INGREDIENT")
    print("-" * 20)
    task_example = {
        "id": "task.file_processor",
        "type": "task",
        "name": "File Processor",
        "description": "Process files with various operations",
        "version": "1.0.0",
        "category": "tasks",
        "dependencies": ["tool.file_utils"],
        "tags": ["file", "processing", "io"],
        "author": "system",
        "access_level": "public"
    }
    print(f"📝 Purpose: {task_example['description']}")
    print(f"🔗 Dependencies: {task_example['dependencies']}")
    print(f"🏷️  Tags: {task_example['tags']}")
    
    # Tool example
    print("\n🛠️  TOOL INGREDIENT")
    print("-" * 20)
    tool_example = {
        "id": "tool.file_utils",
        "type": "tool",
        "name": "File Utilities",
        "description": "Basic file utility functions",
        "version": "1.0.0",
        "category": "tools",
        "dependencies": [],
        "tags": ["file", "utility", "io"],
        "author": "system",
        "access_level": "public"
    }
    print(f"📝 Purpose: {tool_example['description']}")
    print(f"🔗 Dependencies: {tool_example['dependencies']}")
    print(f"🏷️  Tags: {tool_example['tags']}")
    
    # Module example
    print("\n📦 MODULE INGREDIENT")
    print("-" * 20)
    module_example = {
        "id": "module.json_processor",
        "type": "module",
        "name": "JSON Processor",
        "description": "Module for processing JSON data",
        "version": "1.0.0",
        "category": "modules",
        "dependencies": ["tool.file_utils"],
        "tags": ["json", "data", "processing"],
        "author": "system",
        "access_level": "public"
    }
    print(f"📝 Purpose: {module_example['description']}")
    print(f"🔗 Dependencies: {module_example['dependencies']}")
    print(f"🏷️  Tags: {module_example['tags']}")

def show_use_cases():
    """Show practical use cases for the pantry system"""
    print("\n💡 PRACTICAL USE CASES")
    print("=" * 50)
    
    use_cases = [
        {
            "title": "Recipe Development",
            "description": "Store reusable components for recipe creation",
            "example": "Save common data processing tasks as ingredients"
        },
        {
            "title": "Dependency Management",
            "description": "Track and resolve complex dependency chains",
            "example": "Ensure all required tools are available before execution"
        },
        {
            "title": "Access Control",
            "description": "Control who can access sensitive ingredients",
            "example": "Restrict admin tools to authorized users only"
        },
        {
            "title": "Quality Assurance",
            "description": "Validate ingredient structure and metadata",
            "example": "Ensure all ingredients follow proper standards"
        },
        {
            "title": "Discovery & Search",
            "description": "Find ingredients by type, tags, or content",
            "example": "Search for all data processing related ingredients"
        },
        {
            "title": "Version Control",
            "description": "Track ingredient versions and updates",
            "example": "Maintain multiple versions of the same tool"
        }
    ]
    
    for i, use_case in enumerate(use_cases, 1):
        print(f"\n{i}. {use_case['title']}")
        print(f"   📝 {use_case['description']}")
        print(f"   💡 Example: {use_case['example']}")

def main():
    """Main demonstration"""
    print("🚀 Starting Pantry System Examples...")
    
    # Show ingredient examples
    show_ingredient_examples()
    
    # Show use cases
    show_use_cases()
    
    # Run live demonstration
    demo_pantry_system()
    
    print("\n" + "=" * 50)
    print("✅ Pantry System Examples Complete!")
    print("🎯 The pantry system provides:")
    print("   • Centralized ingredient storage")
    print("   • Dependency tracking and resolution")
    print("   • Access control and security")
    print("   • Quality validation and testing")
    print("   • Discovery and search capabilities")
    print("   • Version control and management")

if __name__ == "__main__":
    main() 