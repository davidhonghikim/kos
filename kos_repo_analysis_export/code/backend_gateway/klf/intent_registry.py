registry = {}

def register_intent(intent: str, fn):
    if intent in registry:
        raise Exception(f"Intent {intent} already registered")
    registry[intent] = fn

def get_handler(intent: str):
    return registry.get(intent)

def register_core_handlers():
    register_intent("agent.ping", lambda p, m: {"pong": True})
    register_intent("agent.echo", lambda p, m: {"echo": p}) 