from typing import TypedDict, Dict, List

class AgentState(TypedDict):
    # Input
    isolate_id: str
    patient_profile: Dict

    # Node 1 - Predictor
    ml_15_drug_profile: Dict     # {drug: {is_resistant, confidence}} x15

    # Node 2 - Strategist
    selected_therapy: str        # best safe drug after filtering

    # Node 3 - Verifier
    genomic_verification: List   # CARD genes explaining resistance

    # Node 4 - Pharmacist
    pharmacist_review: Dict      # formulary status, DDIs, cost

    # Node 5 - Procurement
    logistics_status: Dict       # stock level or PO payload

    # Audit
    trace: List[str]