import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

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

# Mount routes
app.include_router(analyze_router, prefix="/api/analyze", tags=["Analysis"])
app.include_router(copilot_router, prefix="/api/copilot", tags=["Copilot"])
 
 #simple endpoint to verify if backend is running smooth or not
@app.get("/")
def health_check():
    return {"status": "Sentinel-CDS API is running"}