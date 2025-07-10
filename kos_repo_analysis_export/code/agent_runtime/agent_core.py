import importlib
import asyncio
from pathlib import Path

class AgentRuntime:
    def __init__(self):
        self.plugins = {}

    def load_plugins(self, directory="plugins"):
        plugin_dir = Path(directory)
        for file in plugin_dir.glob("*.py"):
            module_name = f"plugins.{file.stem}"
            mod = importlib.import_module(module_name)
            if hasattr(mod, "register"):
                self.plugins[file.stem] = mod.register()

    async def run_intent(self, name, payload, meta=None):
        handler = self.plugins.get(name)
        if not handler:
            raise Exception(f"Agent plugin '{name}' not found")
        return await handler(payload, meta or {}) 