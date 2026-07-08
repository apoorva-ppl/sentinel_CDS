import os
import json
import logging
from app.schemas.analysis_types import AgentState

logger = logging.getLogger(__name__)

# Mock connection to local hospital ERP / Database
backend_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../"))
INVENTORY_PATH = os.path.join(backend_root, "data", "pharmacy_inventory.json")


#The Pharmacist receives the drug selected by the Strategist.
def pharmacist_node(state: AgentState) -> AgentState:
    try:
        print("\n [DEBUG] Pharmacist Node: Verifying Formulary and Interactions...")
        
        # 1. Safely extract the explicit therapy selected by Node 2 (Strategist)
        selected_therapy = state.get("selected_therapy", "").upper().strip()
        
        # Guard clause: If the Strategist escalated or error thrown , just simply skip pharmacist node .
        if not selected_therapy or "ERROR" in selected_therapy or "ESCALATE" in selected_therapy:
            state["pharmacist_review"] = {"status": "Skipped", "reason": "No viable empirical drug selected."}
            state["trace"].append(" Pharmacist: Skipped review due to escalation/error in prior node.")
            return state

        # 2.if pharmacy_inventory,json is missing , log error n skip this node again.
        if not os.path.exists(INVENTORY_PATH):
            error_msg = "Inventory DB Offline (pharmacy_inventory.json missing)."
            state["pharmacist_review"] = {"status": "Error", "reason": error_msg}
            state["trace"].append(f" Pharmacist: {error_msg}")
            return state
            
        with open(INVENTORY_PATH, "r") as f:
            db = json.load(f).get("inventory", {})
            
        drug_data = db.get(selected_therapy)
        
        # Guard clause: Drug missing from local database, node tells doctor to verify manually.
        if not drug_data:
            state["trace"].append(f" Pharmacist: '{selected_therapy}' not found in local formulary DB.")
            state["pharmacist_review"] = {
                "status": "Unlisted", 
                "formulary": "Unknown",
                "warnings": ["Drug not in local database - verify manually."],
                "cost_usd": "N/A"
            }
            return state

        # 3. Extract Formulary and DDI Constraints
        formulary = drug_data.get("formulary_status", "Tier 1 - Standard")
        status_msg = "Approved" if "Restricted" not in formulary else "Requires ID Specialist Approval"
        warnings = drug_data.get("ddi_flags", [])
        cost = drug_data.get("cost_per_vial_usd", 0.0)
        
        # 4. Populate State
        state["pharmacist_review"] = {
            "status": status_msg,
            "formulary": formulary,
            "warnings": warnings,
            "cost_usd": cost
        }
        
        state["trace"].append(f"✓ Pharmacist: Formulary checked ({status_msg}). Cost: ${cost}/vial. Warnings: {len(warnings)}")
        print(f"  → Formulary: {formulary} | Cost: ${cost}")
        print(f" [DEBUG] Pharmacist Node: Complete")
        
        return state

    except Exception as e:
        error_msg = f"Pharmacist Node Error: {str(e)}"
        logger.error(error_msg)
        print(f" {error_msg}")
        
        state["pharmacist_review"] = {"status": "Error", "reason": str(e)}
        state["trace"].append(f" {error_msg}")
        return state