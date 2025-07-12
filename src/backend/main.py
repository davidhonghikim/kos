import logging
import os
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import uvicorn

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="kOS Backend API", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class KLFEnvelope(BaseModel):
    id: str
    intent: str
    from_: str = Field(alias="from")
    to: str
    issued_at: int
    payload: dict
    meta: dict | None = None

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "kOS Backend API"}

@app.post("/api/klf")
async def handle_klf(envelope: KLFEnvelope):
    """Handle KLF messages"""
    try:
        logger.info(f"Received KLF message: {envelope.intent} from {envelope.from_} to {envelope.to}")
        # For now, just echo back the message
        return {"status": "ok", "result": envelope.payload}
    except Exception as e:
        logger.error(f"Error handling KLF message: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/kitchen/status")
async def kitchen_status():
    """Kitchen system status"""
    return {"status": "operational", "system": "kitchen"}

if __name__ == "__main__":
    host = os.getenv("KOS_BACKEND_HOST", "0.0.0.0")
    port = int(os.getenv("KOS_BACKEND_PORT", "8000"))
    
    logger.info(f"Starting kOS Backend API on {host}:{port}")
    uvicorn.run(app, host=host, port=port) 