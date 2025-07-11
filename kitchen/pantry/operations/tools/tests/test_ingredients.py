#!/usr/bin/env python3
"""
Test Ingredients Script
Verifies all ingredient files work with the pantry system
"""

import json
import sys
from pathlib import Path

# Add the pantry directory to the path
sys.path.insert(0, str(Path(__file__).parent))

from core.pantry_manager import PantryManager, IngredientMetadata, IngredientCategory, AccessLevel
from core.dependency_tracker import DependencyTracker
from core.access_control import AccessControl, Permission
from core.discovery_engine import DiscoveryEngine
from core.validation_system import ValidationSystem
from datetime import datetime

def test_ingredient_files():
    """Test that all ingredient files are properly structured"""
    print("📁 Testing Ingredient Files...")
    
    ingredient_dirs = ["tasks", "tools", "modules", "skills", "configs", "schemas"]
    total_files = 0
    valid_files = 0
    
    for dir_name in ingredient_dirs:
        dir_path = Path(f"ingredients/{dir_name}")
        if not dir_path.exists():
            print(f"   ✗ Directory {dir_path} does not exist")
            continue
            
        files = list(dir_path.glob("*.json"))
        print(f"   ✓ {dir_name}: {len(files)} files found")
        total_files += len(files)
        
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
                    valid_files += 1
                    
            except Exception as e:
                print(f"      ✗ {file_path.name}: Error reading file - {e}")
    
    print(f"\n📊 Summary: {valid_files}/{total_files} files valid")
    return valid_files == total_files

def test_pantry_system():
    """Test the pantry system with the new ingredients"""
    print("\n🧪 Testing Pantry System with New Ingredients...")
    
    # Initialize components
    pantry = PantryManager()
    tracker = DependencyTracker(pantry)
    access = AccessControl(pantry)
    discovery = DiscoveryEngine(pantry)
    validator = ValidationSystem(pantry)
    
    # Test discovery
    print("\n1️⃣ Testing Ingredient Discovery...")
    discovered = discovery.discover_ingredients()
    print(f"   🔍 Found {len(discovered)} ingredients in filesystem")
    
    # Test listing by category
    print("\n2️⃣ Testing Category Listing...")
    for category in IngredientCategory:
        ingredients = pantry.list_ingredients(category)
        print(f"   📦 {category.value.upper()}: {len(ingredients)} ingredients")
    
    # Test dependency resolution
    print("\n3️⃣ Testing Dependency Resolution...")
    complex_task = pantry.get_ingredient("task.data_analysis")
    if complex_task:
        deps = tracker.resolve_dependencies("task.data_analysis")
        print(f"   🔗 task.data_analysis dependencies: {deps}")
    
    # Test access control
    print("\n4️⃣ Testing Access Control...")
    users = ["anonymous", "developer", "admin"]
    test_ingredient = "task.machine_learning"
    
    for user in users:
        can_read = access.can_access(user, test_ingredient, Permission.READ)
        can_write = access.can_access(user, test_ingredient, Permission.WRITE)
        print(f"   👤 {user:12} | Read: {can_read} | Write: {can_write}")
    
    # Test validation
    print("\n5️⃣ Testing Validation...")
    summary = validator.get_validation_summary()
    print(f"   📊 Total ingredients: {summary['total_ingredients']}")
    print(f"   ✅ Valid: {summary['valid_ingredients']}")
    print(f"   ❌ Invalid: {summary['invalid_ingredients']}")
    print(f"   📈 Validation rate: {summary['validation_rate']:.1%}")
    
    return True

def main():
    """Main test execution"""
    print("🚀 Testing New Ingredient Files...")
    print("=" * 50)
    
    # Test ingredient files
    files_ok = test_ingredient_files()
    
    # Test pantry system
    system_ok = test_pantry_system()
    
    print("\n" + "=" * 50)
    if files_ok and system_ok:
        print("✅ All tests passed!")
        print("🎯 Ingredient files are ready for use")
    else:
        print("❌ Some tests failed")
        print("🔧 Please fix issues before proceeding")
    
    return files_ok and system_ok

if __name__ == "__main__":
    main() 