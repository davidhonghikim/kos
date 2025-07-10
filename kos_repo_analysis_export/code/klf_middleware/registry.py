from importlib import import_module
from pathlib import Path

def load_all_hooks():
    for path in Path("klf/middleware").glob("*.py"):
        if path.name.startswith("__"):
            continue
        modname = f"klf.middleware.{path.stem}"
        import_module(modname) 