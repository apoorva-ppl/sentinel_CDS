import logging
from datetime import datetime
from fastapi import APIRouter, HTTPException

from app.schemas.analysis_types import AnalyzeRequest, AnalyzeResponse, AgentState
from app.agents.workflow import sentinel_graph

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


router = APIRouter()

@router.post("", response_model=AnalyzeResponse)
async def analyze(request: AnalyzeRequest) -> dict:

    try:
        print("\n [DEBUG] Request received at POST /api/analyze")
        print(f"  → Isolate ID: {request.isolate_id}")
        
        # 1. Initialize strictly typed LangGraph state
        initial_state: AgentState = {
            "isolate_id": request.isolate_id,
            # Use .dict() for Pydantic V1, or .model_dump() for V2
            "patient_profile": request.patient_profile.dict(), 
            "ml_15_drug_profile": {},
            "selected_therapy": "",
            "genomic_verification": [],
            "pharmacist_review": {},
            "logistics_status": {},
            "trace": [f"Starting autonomous pipeline for {request.isolate_id}..."]
        }
        
        logger.info(f"Initializing LangGraph analysis for: {request.isolate_id}")
        print(" [DEBUG] Executing sentinel_graph.ainvoke()...")
        
        # 2. Async Invocation of the LangGraph State Machine
        # We use ainvoke() here because Node 5 (Procurement) awaits API responses.
        final_state = sentinel_graph.invoke(initial_state)
        print(" [DEBUG] LangGraph execution completed successfully")
        
        # 3. Construct explicitly validated response mapping to AnalyzeResponse
        response = AnalyzeResponse(
            isolate_id=final_state["isolate_id"],
            patient_profile=final_state["patient_profile"],
            ml_15_drug_profile=final_state["ml_15_drug_profile"],
            selected_therapy=final_state["selected_therapy"],
            genomic_verification=final_state["genomic_verification"],
            pharmacist_review=final_state["pharmacist_review"],
            logistics_status=final_state["logistics_status"],
            trace=final_state["trace"],
            timestamp=datetime.utcnow().isoformat() + "Z"
        )
        
        logger.info("Pipeline orchestration complete.")
        return response.dict()
    
    except Exception as e:
        error_msg = f"Analysis pipeline critical failure: {str(e)}"
        logger.error(error_msg)
        # Catch and bubble up a proper 500 error to the Next.js frontend
        raise HTTPException(status_code=500, detail=error_msg)