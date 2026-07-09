from typing import TypedDict, Dict, List
from pydantic import BaseModel, Field


# Pydantic Request Models 
class PatientProfile(BaseModel):
    Age: int = Field(ge=0, le=120)
    Gender: str
    Diabetes: bool
    Hospital_before: bool
    Hypertension: bool
    Infection_Freq: int = Field(ge=0, le=10)
    Penicillin_Allergy: bool = False
    Renal_Impaired: bool = False

class AnalyzeRequest(BaseModel):
    isolate_id: str = Field(min_length=1, max_length=100)
    patient_profile: PatientProfile


# Pydantic Response Model 
class AnalyzeResponse(BaseModel):
    isolate_id: str
    patient_profile: Dict
    ml_15_drug_profile: Dict
    selected_therapy: str
    genomic_verification: List
    pharmacist_review: Dict
    logistics_status: Dict
    trace: List[str]
    timestamp: str


# LangGraph Shared State
class AgentState(TypedDict):
    isolate_id: str
    patient_profile: Dict
    ml_15_drug_profile: Dict      # Node 1 output
    selected_therapy: str          # Node 2 output
    genomic_verification: List     # Node 3 output
    pharmacist_review: Dict        # Node 4 output
    logistics_status: Dict         # Node 5 output
    trace: List[str]