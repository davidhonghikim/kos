#!/usr/bin/env python3
"""
Test Pantry Operations

Demonstrates how ingredients (metadata) and operations (functionality) work together.
"""

import json
import sys
from pathlib import Path

# Add the operations package to the path
sys.path.append(str(Path(__file__).parent))

from operations.tools import (
    image_editor_operations,
    video_editor_operations,
    social_media_operations,
    ai_content_operations,
    calendar_operations
)

def load_ingredient(ingredient_path: str) -> dict:
    """Load an ingredient from JSON file"""
    try:
        with open(ingredient_path, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading ingredient {ingredient_path}: {e}")
        return {}

def test_ingredient_operation_connection():
    """Test how ingredients and operations work together"""
    
    print("🧪 Testing Ingredient + Operation Connection")
    print("=" * 50)
    
    # Test 1: Image Editor
    print("\n1. Testing Image Editor:")
    ingredient = load_ingredient("ingredients/tools/image_editor_tool.json")
    print(f"   Ingredient: {ingredient.get('name', 'Unknown')}")
    print(f"   Description: {ingredient.get('description', 'No description')}")
    
    # Use the actual operation
    result = image_editor_operations.resize_image(
        "test_image.jpg", 800, 600, "resized_image.jpg"
    )
    print(f"   Operation Result: {result['operation']} - {result['new_dimensions']}")
    
    # Test 2: AI Content Generator
    print("\n2. Testing AI Content Generator:")
    ingredient = load_ingredient("ingredients/tools/ai_content_generator_tool.json")
    print(f"   Ingredient: {ingredient.get('name', 'Unknown')}")
    print(f"   Capabilities: {ingredient.get('capabilities', [])}")
    
    # Use the actual operation
    result = ai_content_operations.generate_content(
        "blog_post", "Create a post about AI trends", "medium"
    )
    print(f"   Operation Result: {result['operation']} - {result['generated_content'][:50]}...")
    
    # Test 3: Social Media Tool
    print("\n3. Testing Social Media Tool:")
    ingredient = load_ingredient("ingredients/tools/social_media_tool.json")
    print(f"   Ingredient: {ingredient.get('name', 'Unknown')}")
    print(f"   Platforms: {ingredient.get('platforms', [])}")
    
    # Use the actual operation
    result = social_media_operations.schedule_post(
        "twitter", "Check out our new AI features!", "2025-07-08T10:00:00Z"
    )
    print(f"   Operation Result: {result['operation']} - {result['platform']}")
    
    print("\n✅ All tests completed successfully!")
    print("\n📝 Key Points:")
    print("   • Ingredients = Metadata (what something is)")
    print("   • Operations = Functionality (what something does)")
    print("   • They work together but are separate")
    print("   • Ingredients describe capabilities")
    print("   • Operations provide actual implementation")

if __name__ == "__main__":
    test_ingredient_operation_connection() 