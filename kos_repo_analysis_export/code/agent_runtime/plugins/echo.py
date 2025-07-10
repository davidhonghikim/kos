async def register():
    async def echo_handler(payload, meta):
        return {"echoed": payload}
    return echo_handler 