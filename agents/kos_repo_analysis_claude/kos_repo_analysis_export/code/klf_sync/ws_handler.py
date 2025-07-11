import asyncio
import websockets
import json
from klf.sync.service import bus

connected_clients = set()

async def ws_handler(websocket, path):
    topic = path.strip("/")
    q = bus.subscribe(topic)
    connected_clients.add(websocket)
    try:
        while True:
            msg = await q.get()
            await websocket.send(json.dumps(msg))
    except:
        pass
    finally:
        bus.unsubscribe(topic, q)
        connected_clients.remove(websocket) 