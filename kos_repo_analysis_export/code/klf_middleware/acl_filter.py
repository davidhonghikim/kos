from klf.hooks import register_hook
from klf.types import KLFEnvelope

BLOCKED = {"secret.agent.task"}

async def enforce_acl(envelope: KLFEnvelope):
    if envelope.intent in BLOCKED:
        raise Exception(f"Intent {envelope.intent} is not permitted.")

register_hook("pre_route", enforce_acl) 