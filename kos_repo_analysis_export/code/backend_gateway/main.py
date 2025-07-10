from fastapi import FastAPI, Request, HTTPException
from pydantic import BaseModel
from klf.types import KLFEnvelope
from klf.router import route_message
from klf.intent_registry import register_core_handlers

app = FastAPI()

# Register handlers
register_core_handlers()

class EnvelopeIn(BaseModel):
    id: str
    intent: str
    from_: str
    to: str
    issued_at: int
    payload: dict
    meta: dict | None = None

@app.post("/api/klf")
async def handle_klf(envelope: EnvelopeIn):
    try:
        env_dict = envelope.dict()
        env_dict["from"] = env_dict.pop("from_")
        result = await route_message(KLFEnvelope(**env_dict))
        return {"status": "ok", "result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 