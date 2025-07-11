from typing import Dict
import asyncio

vault_store: Dict[str, str] = {}
vault_lock = asyncio.Lock()

async def vault_read(key: str) -> str:
    async with vault_lock:
        return vault_store.get(key, "")

async def vault_write(key: str, value: str):
    async with vault_lock:
        vault_store[key] = value 