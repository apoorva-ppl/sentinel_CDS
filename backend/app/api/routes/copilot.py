from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict
from app.rag.copilot import get_copilot_response

router = APIRouter()

# Schema for incoming user chat request
#request schema.
class ChatRequest(BaseModel):
    message: str
    patient_context: Dict
#response schema.
class ChatResponse(BaseModel):
    response: str

#endpoint to handle chat req to copilot engine
@router.post("", response_model=ChatResponse)

#main function
def chat_with_copilot(request: ChatRequest):
    try: 
        #response in JSON  format so that frontend can parse easily.
        reply = get_copilot_response(
            message=request.message, 
            patient_context=request.patient_context
        )
        return ChatResponse(response=reply)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Copilot engine failure: {str(e)}")