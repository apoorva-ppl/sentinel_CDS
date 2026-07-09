import logging
from app.schemas.analysis_types import AgentState

logger = logging.getLogger(__name__)



def strategist_node(state: AgentState) -> AgentState:
    try:
        print("\n[DEBUG] Strategist Node: Formulating Patient-Adjusted Strategy...")
        ml_profile = state.get("ml_15_drug_profile", {})
        patient_profile = state.get("patient_profile", {})
        
        # 1. Extract Patient Safety Constraints
        # Assuming boolean or string representation from the UI
        penicillin_allergy = str(patient_profile.get("Penicillin_Allergy", "False")).lower() == "true"
        renal_impaired = str(patient_profile.get("Renal_Impaired", "False")).lower() == "true"
        
        viable_drugs = []
        
        # 2. Filter the 15-Drug Profile
        for drug, prediction in ml_profile.items():
            drug_upper = drug.upper().strip()
            
            # Constraint A: Is it mathematically resistant?
            if prediction.get("is_resistant", True):
                continue
                
            # Constraint B: Penicillin Allergy Check
            # (Matches common beta-lactam codes in datasets)
            if penicillin_allergy and drug_upper in ["AMX/AMP", "PEN", "TZP", "AUGMENTIN"]:
                state["trace"].append(f" Strategist: Excluded {drug} (Contraindicated: Penicillin Allergy)")
                continue
                
            # Constraint C: Renal Impairment Check (kidney issue)
            # (Nephrotoxic drugs like Aminoglycosides/Vancomycin)
            if renal_impaired and drug_upper in ["GEN", "VAN", "AMK"]:
                state["trace"].append(f" Strategist: Excluded {drug} (Contraindicated: Renal Impairment)")
                continue
            
            # remaining drugs are considered viable, which passes all above filters .
            # only drugs that passes all filters are added to viable_drugs, safe options for the patient
            viable_drugs.append({
                "drug": drug,
                "risk_score": prediction.get("confidence", 1.0) 
            })
            
        # 3. Select Optimal Therapy
        if not viable_drugs:
            # Fallback if the bacteria is resistant to everything + patient allergic to everything 
            #dont make dangerous recommendations , directly refer to human specialist.
            state["selected_therapy"] = "ESCALATE TO INFECTIOUS DISEASE SPECIALIST"
            state["trace"].append("⚠ Strategist: No safe/susceptible oral options remaining. Escalation required.")
            print("  → Result: No safe options. Escalating.")
            return state
            
        # Sort by the lowest mathematical risk of resistance
        #choose best drug with lowest risk score (confidence of resistance) among all the viable drugs
        viable_drugs.sort(key=lambda x: x["risk_score"])
        best_therapy = viable_drugs[0]["drug"]
        
        # 4. Update State info of finally selected therapy 
        state["selected_therapy"] = best_therapy
        state["trace"].append(f"✓ Strategist: Selected {best_therapy} as primary empiric therapy (Risk Score: {viable_drugs[0]['risk_score']:.2f}).")
        
        print(f"  → Result: Selected {best_therapy}")
        print(f" [DEBUG] Strategist Node: Complete")
        
        return state

    except Exception as e:
        error_msg = f"Strategist Node Error: {str(e)}"
        logger.error(error_msg)
        print(f" {error_msg}")
        
        state["trace"].append(f"✗ {error_msg}")  #adds this msg to workflow audit trace for human review
        state["selected_therapy"] = "ERROR_REQUIRES_HUMAN_REVIEW"
        return state