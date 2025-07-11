from klf.vault import get_secret
from klf.types import KLFEnvelope

async def handle_vault_read(envelope: KLFEnvelope):
    key = envelope.payload.get("key")
    value = get_secret(key)
    return {"status": "ok", "value": value} 