from klf.intent_registry import get_handler
from klf.types import KLFEnvelope
from klf.errors import InvalidEnvelopeError

async def route_message(envelope: KLFEnvelope):
    if not envelope.intent or not envelope.from_ or not envelope.to:
        raise InvalidEnvelopeError("Missing required envelope fields")

    handler = get_handler(envelope.intent)
    if not handler:
        raise Exception(f"No handler for intent {envelope.intent}")

    return await handler(envelope.payload, envelope.meta or {}) 