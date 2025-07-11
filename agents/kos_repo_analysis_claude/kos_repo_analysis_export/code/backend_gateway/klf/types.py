from pydantic import BaseModel
from typing import Optional, Literal

class KLFEnvelope(BaseModel):
    id: str
    intent: str
    from_: str
    to: str
    issued_at: int
    payload: dict
    meta: Optional[dict] = None 