#!/usr/bin/env python3
"""
kOS Environment Setup Script
Helps users set up their environment configuration files
"""

import os
import shutil
from pathlib import Path
from typing import List, Tuple


def setup_environment_files() -> None:
    """Set up environment files from examples"""
    env_dir = Path("env")
    
    if not env_dir.exists():
        print("❌ env/ directory not found. Please run this script from the kos project root.")
        return
    
    # Define the files to copy
    files_to_copy = [
        ("local.env.example", "local.env"),
        ("cloud.env.example", "cloud.env"),
        ("api-keys.env.example", "api-keys.env"),
        ("settings.env.example", "settings.env")
    ]
    
    print("🚀 Setting up kOS environment files...")
    print()
    
    copied_files = []
    skipped_files = []
    
    for example_file, target_file in files_to_copy:
        example_path = env_dir / example_file
        target_path = env_dir / target_file
        
        if not example_path.exists():
            print(f"⚠️  Warning: {example_file} not found, skipping...")
            continue
        
        if target_path.exists():
            print(f"⏭️  {target_file} already exists, skipping...")
            skipped_files.append(target_file)
        else:
            try:
                shutil.copy2(example_path, target_path)
                print(f"✅ Created {target_file}")
                copied_files.append(target_file)
            except Exception as e:
                print(f"❌ Failed to create {target_file}: {e}")
    
    print()
    print("📋 Summary:")
    print(f"   Created: {len(copied_files)} files")
    print(f"   Skipped: {len(skipped_files)} files")
    
    if copied_files:
        print()
        print("🎉 Environment setup complete!")
        print()
        print("📝 Next steps:")
        print("   1. Edit env/local.env to configure local services")
        print("   2. Edit env/cloud.env to enable cloud services")
        print("   3. Edit env/api-keys.env to add your API keys")
        print("   4. Edit env/settings.env to configure system behavior")
        print()
        print("💡 Tip: Use the toggle script to manage settings:")
        print("   python scripts/toggle_settings.py --help")
    
    if skipped_files:
        print()
        print("📝 To update existing files, manually copy from examples:")
        for file in skipped_files:
            example = file.replace('.env', '.env.example')
            print(f"   cp env/{example} env/{file}")


def validate_environment() -> None:
    """Validate that environment files are properly configured"""
    env_dir = Path("env")
    
    if not env_dir.exists():
        print("❌ env/ directory not found")
        return
    
    print("🔍 Validating environment configuration...")
    print()
    
    required_files = ["local.env", "cloud.env", "api-keys.env", "settings.env"]
    missing_files = []
    present_files = []
    
    for file in required_files:
        file_path = env_dir / file
        if file_path.exists():
            present_files.append(file)
        else:
            missing_files.append(file)
    
    if present_files:
        print("✅ Found environment files:")
        for file in present_files:
            print(f"   - {file}")
    
    if missing_files:
        print()
        print("❌ Missing environment files:")
        for file in missing_files:
            print(f"   - {file}")
        print()
        print("💡 Run this script to create them from examples")
    
    print()
    print("🔧 To start services, run:")
    print("   docker-compose up")


def main() -> None:
    """Main function"""
    print("=" * 60)
    print("kOS Environment Setup")
    print("=" * 60)
    print()
    
    # Check if we're in the right directory
    if not Path("docker-compose.yml").exists():
        print("❌ docker-compose.yml not found. Please run this script from the kos project root.")
        return
    
    # Check command line arguments
    import sys
    if len(sys.argv) > 1:
        if sys.argv[1] == "validate":
            validate_environment()
        elif sys.argv[1] == "setup":
            setup_environment_files()
        else:
            print("Usage: python scripts/setup_env.py [setup|validate]")
            print("  setup    - Create environment files from examples")
            print("  validate - Check environment configuration")
    else:
        # Default: setup
        setup_environment_files()
        print()
        validate_environment()


if __name__ == "__main__":
    main() 