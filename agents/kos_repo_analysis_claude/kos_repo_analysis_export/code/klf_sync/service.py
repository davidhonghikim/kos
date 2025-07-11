import asyncio
from collections import defaultdict

class EventBus:
    def __init__(self):
        self.subscribers = defaultdict(set)

    async def publish(self, topic, message):
        for q in self.subscribers[topic]:
            await q.put(message)

    def subscribe(self, topic):
        q = asyncio.Queue()
        self.subscribers[topic].add(q)
        return q

    def unsubscribe(self, topic, q):
        self.subscribers[topic].discard(q)

bus = EventBus() 