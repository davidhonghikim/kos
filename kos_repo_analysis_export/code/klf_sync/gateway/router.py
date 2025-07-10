from fastapi import APIRouter
from klf.router import dispatch_envelope
from klf.types import KLFEnvelope

router = APIRouter()

@router.post("/intent")
async def handle_intent(envelope: KLFEnvelope):
    result = await dispatch_envelope(envelope)
    return result 