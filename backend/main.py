import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from app.rag.copilot import get_copilot_response
from pydantic import BaseModel
from typing import Optional, List, Dict

from app.api.routes.analyze import router as analyze_router
from app.api.routes.copilot import router as copilot_router

load_dotenv() #load all env variables  frm .env file
#create fastapi app .
app = FastAPI(title="Sentinel-CDS API")

# CORS — allows Next.js frontend to talk to FastAPI
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
class ChatRequest(BaseModel):
    message: str
    context: Optional[Dict] = None
    history: Optional[List[Dict]] = []

@app.post("/api/chat")
def chat(request: ChatRequest):
    try:
        reply = get_copilot_response(
            message=request.message,
            patient_context=request.context or {}
        )
        return {"reply": reply}
    except Exception as e:
        return {"reply": f"Error: {str(e)}"}
# Mount routes
app.include_router(analyze_router, prefix="/api/analyze", tags=["Analysis"])
app.include_router(copilot_router, prefix="/api/copilot", tags=["Copilot"])
 
 
 #simple endpoint to verify if backend is running smooth or not
@app.get("/")
def health_check():
    return {"status": "Sentinel-CDS API is running"}