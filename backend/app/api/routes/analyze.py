import logging
from datetime import datetime, UTC

from fastapi import APIRouter, HTTPException

from app.schemas.analysis_types import (
    AnalyzeRequest,
    AnalyzeResponse,
    AgentState,
)
from app.agents.workflow import sentinel_graph

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

router = APIRouter()


@router.post("", response_model=AnalyzeResponse)
async def analyze(request: AnalyzeRequest) -> dict:
    try:
        # Just quick visibility in the terminal to see what isolate we are treating
        print("\n[DEBUG] Request received at POST /api/analyze")
        print(f"→ Isolate ID: {request.isolate_id}")

        # Pack frontend data into the strict TypedDict contract that our 5 agents expect
        initial_state: AgentState = {
            "isolate_id": request.isolate_id,
            "patient_profile": request.patient_profile.model_dump(),
            "ml_15_drug_profile": {},
            "selected_therapy": "",
            "genomic_verification": [],
            "pharmacist_review": {},
            "logistics_status": {},
            "trace": [
                f"Starting autonomous pipeline for {request.isolate_id}..."
            ],
        }

        logger.info(
            f"Initializing LangGraph analysis for: {request.isolate_id}"
        )
        print("[DEBUG] Executing sentinel_graph.invoke()...")

        # Hand control over to LangGraph to spin through our 5-agent assembly line
        final_state = sentinel_graph.invoke(initial_state)

        print("[DEBUG] LangGraph execution completed successfully")

        # Structure the final mutated state back into a clean Pydantic schema for the frontend
        response = AnalyzeResponse(
            isolate_id=final_state["isolate_id"],
            patient_profile=final_state["patient_profile"],
            ml_15_drug_profile=final_state["ml_15_drug_profile"],
            selected_therapy=final_state["selected_therapy"],
            genomic_verification=final_state["genomic_verification"],
            pharmacist_review=final_state["pharmacist_review"],
            logistics_status=final_state["logistics_status"],
            trace=final_state["trace"],
            timestamp=datetime.now(UTC).isoformat(),
        )

        logger.info("Pipeline orchestration complete.")

        return response.model_dump()

    except Exception as e:
        # Catch anything that breaks mid-flight (ML tensor crashes, Neo4j timeouts, etc.)
        error_msg = f"Analysis pipeline critical failure: {str(e)}"
        logger.error(error_msg)
        raise HTTPException(status_code=500, detail=error_msg)