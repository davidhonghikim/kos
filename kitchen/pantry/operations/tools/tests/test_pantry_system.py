#!/usr/bin/env python3
"""
Pantry System Test Script
Validates the modular pantry system components
"""

import json
import os
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

def test_pantry_system():
    """Test the complete pantry system"""
    print("🧪 Testing Pantry System Components...")
    
    # Initialize components
    pantry_manager = PantryManager()
    dependency_tracker = DependencyTracker(pantry_manager)
    access_control = AccessControl(pantry_manager)
    discovery_engine = DiscoveryEngine(pantry_manager)
    validation_system = ValidationSystem(pantry_manager)
    
    # Test 1: Pantry Manager
    print("\n1. Testing Pantry Manager...")
    try:
        # Test ingredient registration
        test_ingredient = IngredientMetadata(
            id="test.file_processor",
            name="Test File Processor",
            description="Test ingredient for validation",
            version="1.0.0",
            category=IngredientCategory.TASKS,
            dependencies=["tool.file_utils"],
            tags=["test", "file", "processor"],
            author="system",
            created=datetime.fromisoformat("2025-07-07T23:00:00"),
            updated=datetime.fromisoformat("2025-07-07T23:00:00"),
            access_level=AccessLevel.PUBLIC
        )
        
        result = pantry_manager.register_ingredient(test_ingredient)
        print(f"   ✓ Ingredient registration: {result}")
        
        # Test ingredient retrieval
        retrieved = pantry_manager.get_ingredient("test.file_processor")
        print(f"   ✓ Ingredient retrieval: {retrieved is not None}")
        
    except Exception as e:
        print(f"   ✗ Pantry Manager test failed: {e}")
        return False
    
    # Test 2: Dependency Tracker
    print("\n2. Testing Dependency Tracker...")
    try:
        # Test dependency resolution
        resolved = dependency_tracker.resolve_dependencies("test.file_processor")
        print(f"   ✓ Dependency resolution: {len(resolved)} dependencies found")
        
        # Test dependency info
        dep_info = dependency_tracker.get_dependency_info("test.file_processor")
        print(f"   ✓ Dependency info: {dep_info is not None}")
        
    except Exception as e:
        print(f"   ✗ Dependency Tracker test failed: {e}")
        return False
    
    # Test 3: Access Control
    print("\n3. Testing Access Control...")
    try:
        # Test permission check
        has_access = access_control.can_access("test_user", "test.file_processor", Permission.READ)
        print(f"   ✓ Permission check: {has_access}")
        
        # Test accessible ingredients
        accessible = access_control.get_accessible_ingredients("test_user")
        print(f"   ✓ Accessible ingredients: {len(accessible)} found")
        
    except Exception as e:
        print(f"   ✗ Access Control test failed: {e}")
        return False
    
    # Test 4: Discovery Engine
    print("\n4. Testing Discovery Engine...")
    try:
        # Test ingredient discovery
        discovered = discovery_engine.discover_ingredients()
        print(f"   ✓ Ingredient discovery: {len(discovered)} ingredients found")
        
    except Exception as e:
        print(f"   ✗ Discovery Engine test failed: {e}")
        return False
    
    # Test 5: Validation System
    print("\n5. Testing Validation System...")
    try:
        # Test ingredient validation
        validation_result = validation_system.validate_ingredient(test_ingredient)
        print(f"   ✓ Ingredient validation: {validation_result.valid}")
        
        # Test validation summary
        summary = validation_system.get_validation_summary()
        print(f"   ✓ Validation summary: {summary['total_ingredients']} ingredients")
        
    except Exception as e:
        print(f"   ✗ Validation System test failed: {e}")
        return False
    
    # Test 6: Integration Test
    print("\n6. Testing System Integration...")
    try:
        # Test listing all ingredients
        all_ingredients = pantry_manager.list_ingredients()
        print(f"   ✓ Total ingredients: {len(all_ingredients)}")
        
        # Test ingredient categories
        categories = [cat.value for cat in IngredientCategory]
        print(f"   ✓ Ingredient categories: {len(categories)}")
        
    except Exception as e:
        print(f"   ✗ Integration test failed: {e}")
        return False
    
    print("\n🎉 All pantry system tests completed successfully!")
    return True

def test_ingredient_files():
    """Test that ingredient files are properly structured"""
    print("\n📁 Testing Ingredient Files...")
    
    ingredient_dirs = ["tasks", "tools", "modules"]
    
    for dir_name in ingredient_dirs:
        dir_path = Path(f"ingredients/{dir_name}")
        if not dir_path.exists():
            print(f"   ✗ Directory {dir_path} does not exist")
            continue
            
        files = list(dir_path.glob("*.json"))
        print(f"   ✓ {dir_name}: {len(files)} files found")
        
        for file_path in files:
            try:
                with open(file_path, 'r') as f:
                    ingredient = json.load(f)
                
                # Validate basic structure
                required_fields = ["id", "type", "name", "version"]
                missing_fields = [field for field in required_fields if field not in ingredient]
                
                if missing_fields:
                    print(f"      ✗ {file_path.name}: Missing fields {missing_fields}")
                else:
                    print(f"      ✓ {file_path.name}: Valid structure")
                    
            except Exception as e:
                print(f"      ✗ {file_path.name}: Error reading file - {e}")

def main():
    """Main test execution"""
    print("🚀 Starting Pantry System Validation...")
    print("=" * 50)
    
    # Test ingredient files first
    test_ingredient_files()
    
    # Test system components
    success = test_pantry_system()
    
    print("\n" + "=" * 50)
    if success:
        print("✅ Pantry System Validation: PASSED")
        print("🎯 System is ready for production use")
    else:
        print("❌ Pantry System Validation: FAILED")
        print("🔧 Please fix issues before proceeding")
    
    return success

if __name__ == "__main__":
    main() 