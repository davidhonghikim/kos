#!/usr/bin/env python3
"""
Advanced Pantry System Examples
Shows sophisticated capabilities and real-world scenarios
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

def create_complex_ingredients():
    """Create a complex set of ingredients with dependencies"""
    print("🔧 CREATING COMPLEX INGREDIENT ECOSYSTEM")
    print("=" * 50)
    
    pantry = PantryManager()
    
    # Create base tools
    base_tools = [
        IngredientMetadata(
            id='tool.pandas',
            name='Pandas Data Tool',
            description='Data manipulation and analysis tool',
            version='1.5.0',
            category=IngredientCategory.TOOLS,
            dependencies=[],
            tags=['data', 'pandas', 'analysis'],
            author='data_team',
            created=datetime.now(),
            updated=datetime.now(),
            access_level=AccessLevel.PUBLIC
        ),
        IngredientMetadata(
            id='tool.numpy',
            name='NumPy Array Tool',
            description='Numerical computing tool',
            version='1.21.0',
            category=IngredientCategory.TOOLS,
            dependencies=[],
            tags=['data', 'numpy', 'numerical'],
            author='data_team',
            created=datetime.now(),
            updated=datetime.now(),
            access_level=AccessLevel.PUBLIC
        ),
        IngredientMetadata(
            id='tool.matplotlib',
            name='Matplotlib Visualization Tool',
            description='Data visualization tool',
            version='3.5.0',
            category=IngredientCategory.TOOLS,
            dependencies=['tool.numpy'],
            tags=['data', 'visualization', 'plotting'],
            author='data_team',
            created=datetime.now(),
            updated=datetime.now(),
            access_level=AccessLevel.PUBLIC
        )
    ]
    
    # Create modules that depend on tools
    modules = [
        IngredientMetadata(
            id='module.statistics',
            name='Statistics Module',
            description='Statistical analysis module',
            version='2.0.0',
            category=IngredientCategory.MODULES,
            dependencies=['tool.pandas', 'tool.numpy'],
            tags=['statistics', 'analysis', 'math'],
            author='data_team',
            created=datetime.now(),
            updated=datetime.now(),
            access_level=AccessLevel.PROTECTED
        ),
        IngredientMetadata(
            id='module.visualization',
            name='Visualization Module',
            description='Data visualization module',
            version='1.8.0',
            category=IngredientCategory.MODULES,
            dependencies=['tool.matplotlib', 'tool.pandas'],
            tags=['visualization', 'plotting', 'charts'],
            author='data_team',
            created=datetime.now(),
            updated=datetime.now(),
            access_level=AccessLevel.PROTECTED
        )
    ]
    
    # Create complex tasks
    tasks = [
        IngredientMetadata(
            id='task.data_analysis',
            name='Complete Data Analysis',
            description='Full data analysis pipeline',
            version='3.0.0',
            category=IngredientCategory.TASKS,
            dependencies=['module.statistics', 'module.visualization'],
            tags=['analysis', 'pipeline', 'complete'],
            author='data_team',
            created=datetime.now(),
            updated=datetime.now(),
            access_level=AccessLevel.PROTECTED
        ),
        IngredientMetadata(
            id='task.machine_learning',
            name='Machine Learning Pipeline',
            description='ML model training and evaluation',
            version='2.5.0',
            category=IngredientCategory.TASKS,
            dependencies=['module.statistics', 'tool.pandas'],
            tags=['ml', 'training', 'evaluation'],
            author='ml_team',
            created=datetime.now(),
            updated=datetime.now(),
            access_level=AccessLevel.ADMIN
        )
    ]
    
    # Register all ingredients
    all_ingredients = base_tools + modules + tasks
    for ingredient in all_ingredients:
        success = pantry.register_ingredient(ingredient)
        print(f"✅ Registered {ingredient.id}: {success}")
    
    return pantry

def demonstrate_dependency_resolution():
    """Show complex dependency resolution"""
    print("\n🔗 COMPLEX DEPENDENCY RESOLUTION")
    print("=" * 50)
    
    pantry = PantryManager()
    tracker = DependencyTracker(pantry)
    
    # Get all tasks
    tasks = pantry.list_ingredients(IngredientCategory.TASKS)
    
    for task in tasks:
        print(f"\n📋 Task: {task.name}")
        print(f"   ID: {task.id}")
        
        # Direct dependencies
        direct_deps = tracker.get_dependencies(task.id)
        print(f"   🔗 Direct dependencies: {direct_deps}")
        
        # All dependencies (including transitive)
        all_deps = tracker.resolve_dependencies(task.id)
        print(f"   🔍 All dependencies: {all_deps}")
        
        # Dependency info
        info = tracker.get_dependency_info(task.id)
        if info:
            print(f"   📊 Dependents: {info.dependents}")
            if info.conflicts:
                print(f"   ⚠️  Conflicts: {info.conflicts}")

def demonstrate_access_control_scenarios():
    """Show different access control scenarios"""
    print("\n🔐 ACCESS CONTROL SCENARIOS")
    print("=" * 50)
    
    pantry = PantryManager()
    access = AccessControl(pantry)
    
    # Test different scenarios
    scenarios = [
        {
            "user": "anonymous",
            "ingredient": "tool.pandas",
            "permission": Permission.READ,
            "expected": True,
            "reason": "Public tool - readable by everyone"
        },
        {
            "user": "anonymous",
            "ingredient": "task.machine_learning",
            "permission": Permission.READ,
            "expected": False,
            "reason": "Admin task - not accessible to anonymous"
        },
        {
            "user": "developer",
            "ingredient": "module.statistics",
            "permission": Permission.READ,
            "expected": True,
            "reason": "Protected module - accessible to authenticated users"
        },
        {
            "user": "admin",
            "ingredient": "task.machine_learning",
            "permission": Permission.WRITE,
            "expected": True,
            "reason": "Admin user - full access to all ingredients"
        }
    ]
    
    for scenario in scenarios:
        result = access.can_access(
            scenario["user"], 
            scenario["ingredient"], 
            scenario["permission"]
        )
        status = "✅ PASS" if result == scenario["expected"] else "❌ FAIL"
        print(f"{status} {scenario['user']} -> {scenario['ingredient']} ({scenario['permission'].value})")
        print(f"   Expected: {scenario['expected']}, Got: {result}")
        print(f"   Reason: {scenario['reason']}")

def demonstrate_validation_workflow():
    """Show comprehensive validation workflow"""
    print("\n✅ COMPREHENSIVE VALIDATION WORKFLOW")
    print("=" * 50)
    
    pantry = PantryManager()
    validator = ValidationSystem(pantry)
    
    # Validate all ingredients
    print("🔍 Validating all ingredients...")
    validation_results = validator.validate_all_ingredients()
    
    # Group by validation status
    valid_ingredients = [r for r in validation_results if r.valid]
    invalid_ingredients = [r for r in validation_results if not r.valid]
    
    print(f"✅ Valid ingredients: {len(valid_ingredients)}")
    print(f"❌ Invalid ingredients: {len(invalid_ingredients)}")
    
    # Show validation summary
    summary = validator.get_validation_summary()
    print(f"\n📊 Validation Summary:")
    print(f"   Total ingredients: {summary['total_ingredients']}")
    print(f"   Valid: {summary['valid_ingredients']}")
    print(f"   Invalid: {summary['invalid_ingredients']}")
    print(f"   Total errors: {summary['total_errors']}")
    print(f"   Total warnings: {summary['total_warnings']}")
    print(f"   Validation rate: {summary['validation_rate']:.1%}")
    
    # Show details for invalid ingredients
    if invalid_ingredients:
        print(f"\n❌ Invalid Ingredients Details:")
        for result in invalid_ingredients:
            print(f"   • {result.ingredient_id}:")
            for error in result.errors:
                print(f"     - {error}")

def demonstrate_ingredient_discovery():
    """Show ingredient discovery capabilities"""
    print("\n🔍 INGREDIENT DISCOVERY CAPABILITIES")
    print("=" * 50)
    
    pantry = PantryManager()
    discovery = DiscoveryEngine(pantry)
    
    # Discover ingredients in filesystem
    discovered = discovery.discover_ingredients()
    print(f"🔍 Found {len(discovered)} ingredients in filesystem")
    
    # Show discovery results
    for result in discovered:
        print(f"   • {result.ingredient_id} ({result.category.value})")
        print(f"     File: {result.file_path}")
        print(f"     Auto-registered: {result.auto_registered}")
    
    # List all ingredients by category
    print(f"\n📦 Current Pantry Inventory:")
    for category in IngredientCategory:
        ingredients = pantry.list_ingredients(category)
        print(f"   {category.value.upper()}: {len(ingredients)} ingredients")
        for ingredient in ingredients:
            print(f"     • {ingredient.id} (v{ingredient.version})")

def demonstrate_real_world_scenario():
    """Show a real-world scenario using the pantry"""
    print("\n🌍 REAL-WORLD SCENARIO: DATA SCIENCE PROJECT")
    print("=" * 50)
    
    print("Scenario: A data scientist wants to create a new analysis task")
    print("that depends on existing tools and modules in the pantry.")
    
    pantry = PantryManager()
    tracker = DependencyTracker(pantry)
    validator = ValidationSystem(pantry)
    
    # Step 1: Check what's available
    print("\n1️⃣ CHECKING AVAILABLE INGREDIENTS")
    available_tools = pantry.list_ingredients(IngredientCategory.TOOLS)
    available_modules = pantry.list_ingredients(IngredientCategory.MODULES)
    
    print(f"   Available tools: {len(available_tools)}")
    for tool in available_tools:
        print(f"     • {tool.id}: {tool.name}")
    
    print(f"   Available modules: {len(available_modules)}")
    for module in available_modules:
        print(f"     • {module.id}: {module.name}")
    
    # Step 2: Create new task
    print("\n2️⃣ CREATING NEW ANALYSIS TASK")
    new_analysis = IngredientMetadata(
        id='task.custom_analysis',
        name='Custom Data Analysis',
        description='Custom analysis combining statistics and visualization',
        version='1.0.0',
        category=IngredientCategory.TASKS,
        dependencies=['module.statistics', 'module.visualization'],
        tags=['custom', 'analysis', 'combined'],
        author='data_scientist',
        created=datetime.now(),
        updated=datetime.now(),
        access_level=AccessLevel.PROTECTED
    )
    
    # Step 3: Validate before registration
    print("\n3️⃣ VALIDATING NEW TASK")
    validation = validator.validate_ingredient(new_analysis)
    print(f"   Valid: {validation.valid}")
    if validation.errors:
        print(f"   Errors: {validation.errors}")
    if validation.warnings:
        print(f"   Warnings: {validation.warnings}")
    
    # Step 4: Register if valid
    if validation.valid:
        print("\n4️⃣ REGISTERING NEW TASK")
        success = pantry.register_ingredient(new_analysis)
        print(f"   Registration: {success}")
        
        # Step 5: Check dependencies
        print("\n5️⃣ VERIFYING DEPENDENCIES")
        deps = tracker.get_dependencies(new_analysis.id)
        print(f"   Dependencies: {deps}")
        
        resolved = tracker.resolve_dependencies(new_analysis.id)
        print(f"   All dependencies: {resolved}")
        
        print("\n✅ Task successfully created and registered!")
    else:
        print("\n❌ Task validation failed - cannot register")

def main():
    """Main demonstration"""
    print("🚀 Advanced Pantry System Examples")
    print("=" * 60)
    
    # Create complex ingredient ecosystem
    create_complex_ingredients()
    
    # Demonstrate various capabilities
    demonstrate_dependency_resolution()
    demonstrate_access_control_scenarios()
    demonstrate_validation_workflow()
    demonstrate_ingredient_discovery()
    demonstrate_real_world_scenario()
    
    print("\n" + "=" * 60)
    print("🎉 Advanced Examples Complete!")
    print("🎯 The pantry system provides a complete ecosystem for:")
    print("   • Managing complex ingredient dependencies")
    print("   • Enforcing access control policies")
    print("   • Ensuring quality through validation")
    print("   • Discovering and organizing ingredients")
    print("   • Supporting real-world development workflows")

if __name__ == "__main__":
    main() 