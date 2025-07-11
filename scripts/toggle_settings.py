#!/usr/bin/env python3
"""
kOS Settings Toggle Script
Easy way to enable/disable features without manually editing files
"""

import os
import sys
from pathlib import Path
from typing import Dict, List, Optional

class SettingsManager:
    def __init__(self, settings_file: str = "settings.env"):
        self.settings_file = Path(settings_file)
        self.settings: Dict[str, str] = {}
        self.load_settings()
    
    def load_settings(self) -> None:
        """Load current settings from file"""
        if self.settings_file.exists():
            with open(self.settings_file, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#') and '=' in line:
                        key, value = line.split('=', 1)
                        self.settings[key.strip()] = value.strip()
    
    def save_settings(self) -> None:
        """Save settings back to file"""
        # Read the original file to preserve comments and structure
        lines = []
        if self.settings_file.exists():
            with open(self.settings_file, 'r') as f:
                lines = f.readlines()
        
        # Update values while preserving structure
        updated_lines = []
        for line in lines:
            if line.strip() and not line.strip().startswith('#') and '=' in line:
                key = line.split('=', 1)[0].strip()
                if key in self.settings:
                    updated_lines.append(f"{key}={self.settings[key]}\n")
                else:
                    updated_lines.append(line)
            else:
                updated_lines.append(line)
        
        # Write back to file
        with open(self.settings_file, 'w') as f:
            f.writelines(updated_lines)
    
    def toggle_setting(self, setting_name: str, value: Optional[str] = None) -> None:
        """Toggle a setting on/off or set to specific value"""
        if value is None:
            # Toggle between true/false
            current = self.settings.get(setting_name, 'false').lower()
            new_value = 'false' if current == 'true' else 'true'
        else:
            new_value = value
        
        self.settings[setting_name] = new_value
        print(f"✅ {setting_name} = {new_value}")
    
    def enable_setting(self, setting_name: str) -> None:
        """Enable a setting"""
        self.toggle_setting(setting_name, 'true')
    
    def disable_setting(self, setting_name: str) -> None:
        """Disable a setting"""
        self.toggle_setting(setting_name, 'false')
    
    def show_setting(self, setting_name: str) -> None:
        """Show current value of a setting"""
        value = self.settings.get(setting_name, 'not set')
        print(f"{setting_name} = {value}")
    
    def list_settings(self, category: Optional[str] = None) -> None:
        """List all settings or settings in a category"""
        if category:
            filtered = {k: v for k, v in self.settings.items() if category.lower() in k.lower()}
            print(f"\n📋 Settings containing '{category}':")
        else:
            filtered = self.settings
            print(f"\n📋 All Settings ({len(filtered)} total):")
        
        for key, value in sorted(filtered.items()):
            status = "🟢" if value.lower() == 'true' else "🔴"
            print(f"  {status} {key} = {value}")
    
    def batch_toggle(self, settings: List[str], value: str) -> None:
        """Toggle multiple settings at once"""
        for setting in settings:
            self.toggle_setting(setting, value)
    
    def enable_dev_mode(self) -> None:
        """Enable common development settings"""
        dev_settings = [
            'KOS_DEBUG',
            'KOS_ENABLE_DEBUG_LOGGING',
            'KOS_ENABLE_DEV_TOOLS',
            'KOS_ENABLE_API_DOCS',
            'KOS_ENABLE_HOT_RELOAD'
        ]
        self.batch_toggle(dev_settings, 'true')
        print("🚀 Development mode enabled!")
    
    def enable_prod_mode(self) -> None:
        """Enable production settings"""
        prod_settings = [
            'KOS_ENABLE_SECURITY_HEADERS',
            'KOS_ENABLE_HTTPS_REDIRECT',
            'KOS_ENABLE_RATE_LIMITING',
            'KOS_ENABLE_HEALTH_CHECKS',
            'KOS_ENABLE_METRICS'
        ]
        self.batch_toggle(prod_settings, 'true')
        print("🏭 Production mode enabled!")

def main():
    if len(sys.argv) < 2:
        print("""
🔧 kOS Settings Manager

Usage:
  python toggle_settings.py <command> [options]

Commands:
  toggle <setting>           - Toggle a setting on/off
  enable <setting>           - Enable a setting
  disable <setting>          - Disable a setting
  show <setting>             - Show current value
  list [category]            - List all settings or by category
  dev                        - Enable development mode
  prod                       - Enable production mode
  save                       - Save changes to file

Examples:
  python toggle_settings.py toggle KOS_ENABLE_ELASTICSEARCH
  python toggle_settings.py enable KOS_DEBUG
  python toggle_settings.py list monitoring
  python toggle_settings.py dev
  python toggle_settings.py save

Categories: core, optional, llm, storage, monitoring, auth, security, dev
        """)
        return
    
    manager = SettingsManager()
    command = sys.argv[1].lower()
    
    try:
        if command == 'toggle' and len(sys.argv) >= 3:
            manager.toggle_setting(sys.argv[2])
        elif command == 'enable' and len(sys.argv) >= 3:
            manager.enable_setting(sys.argv[2])
        elif command == 'disable' and len(sys.argv) >= 3:
            manager.disable_setting(sys.argv[2])
        elif command == 'show' and len(sys.argv) >= 3:
            manager.show_setting(sys.argv[2])
        elif command == 'list':
            category = sys.argv[2] if len(sys.argv) >= 3 else None
            manager.list_settings(category)
        elif command == 'dev':
            manager.enable_dev_mode()
        elif command == 'prod':
            manager.enable_prod_mode()
        elif command == 'save':
            manager.save_settings()
            print("💾 Settings saved!")
        else:
            print("❌ Invalid command. Use 'python toggle_settings.py' for help.")
            return
        
        # Auto-save for most commands
        if command not in ['list', 'show', 'save']:
            manager.save_settings()
            print("💾 Changes saved automatically!")
    
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main() 