#!/usr/bin/env python3
"""
Show Pantry Inventory
Displays all ingredients in the pantry system
"""

import sys
from pathlib import Path

# Add the pantry directory to the path
sys.path.insert(0, str(Path(__file__).parent))

from core.pantry_manager import PantryManager, IngredientCategory

def show_inventory():
    """Show complete pantry inventory"""
    print("🏪 PANTRY INVENTORY")
    print("=" * 50)
    
    pantry = PantryManager()
    
    # Show by category
    for category in IngredientCategory:
        ingredients = pantry.list_ingredients(category)
        print(f"\n📦 {category.value.upper()} ({len(ingredients)} ingredients)")
        print("-" * 30)
        
        if ingredients:
            for ingredient in ingredients:
                print(f"  • {ingredient.id}")
                print(f"    Name: {ingredient.name}")
                print(f"    Version: {ingredient.version}")
                print(f"    Access: {ingredient.access_level.value}")
                print(f"    Dependencies: {ingredient.dependencies}")
                print(f"    Tags: {ingredient.tags}")
                print()
        else:
            print("  (No ingredients)")
    
    # Show summary
    all_ingredients = pantry.list_ingredients()
    print(f"\n📊 SUMMARY")
    print("-" * 30)
    print(f"Total ingredients: {len(all_ingredients)}")
    
    # Count by access level
    public = [i for i in all_ingredients if i.access_level.value == "public"]
    protected = [i for i in all_ingredients if i.access_level.value == "protected"]
    admin = [i for i in all_ingredients if i.access_level.value == "admin"]
    
    print(f"Public: {len(public)}")
    print(f"Protected: {len(protected)}")
    print(f"Admin: {len(admin)}")

if __name__ == "__main__":
    show_inventory() 