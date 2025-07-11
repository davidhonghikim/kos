from fastapi import FastAPI
from klf.vault import vault_read, vault_write
from klf.router import route_message
from klf.types import KLFEnvelope
import time, uuid

app = FastAPI()

@app.get("/admin/health")
async def health():
    return {"status": "alive"}

@app.get("/admin/vault/{key}")
async def get_vault_value(key: str):
    value = await vault_read(key)
    return {"key": key, "value": value}

@app.post("/admin/vault/{key}")
async def set_vault_value(key: str, value: str):
    await vault_write(key, value)
    return {"status": "written"}

@app.post("/admin/klf/send")
async def simulate_klf(intent: str, payload: dict):
    env = KLFEnvelope(
        id=str(uuid.uuid4()),
        intent=intent,
        from_="admin.cli",
        to="agent.local",
        issued_at=int(time.time()),
        payload=payload,
    )
    return await route_message(env) 