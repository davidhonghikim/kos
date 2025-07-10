from contextvars import ContextVar
from uuid import uuid4
from klf.logger import log

current_trace_id: ContextVar[str] = ContextVar("trace_id", default=None)

def start_trace(intent: str) -> str:
    trace_id = str(uuid4())
    current_trace_id.set(trace_id)
    log("debug", f"[TRACE START] {trace_id} :: {intent}")
    return trace_id

def trace_event(stage: str, data: dict):
    trace_id = current_trace_id.get()
    if trace_id:
        log("debug", f"[TRACE] {trace_id} :: {stage} :: {data}")

def end_trace():
    trace_id = current_trace_id.get()
    if trace_id:
        log("debug", f"[TRACE END] {trace_id}") 