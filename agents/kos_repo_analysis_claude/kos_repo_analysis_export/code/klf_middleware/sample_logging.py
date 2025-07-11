from klf.hooks import register_hook
from klf.logger import log

async def log_before_send(envelope):
    log("HOOK: PRE_SEND", envelope.intent, envelope.id)

register_hook("pre_send", log_before_send) 