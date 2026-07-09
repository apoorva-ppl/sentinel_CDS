import os
import json
import uuid
import asyncio
import logging
from datetime import datetime
from app.schemas.analysis_types import AgentState

logger = logging.getLogger(__name__)

backend_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../"))
INVENTORY_PATH = os.path.join(backend_root, "data", "pharmacy_inventory.json")


#helper function to simulate async http POST req to supplier api.
async def execute_external_order(drug_name: str, quantity: int, total_cost: float) -> dict:
    """
    Simulates sending an async HTTP POST request to a Supplier API.
    Uses asyncio.sleep to prevent blocking the main FastAPI event loop.
    """
    print(f"\n[NETWORK] Connecting to Supplier API (B2B Pharma Gateway)...")
    await asyncio.sleep(1.2) # Simulate network latency
    
    # json payload that would be sent to the supplier's api.
    api_payload = {
        "hospital_id": "HOSP-9942-A",
        "billing_ref": "FIN-DEPT-Q3",
        "shipping_address": "Loading Dock B, Main Hospital Campus",
        "items": [
            {
                "ndc_code": f"NDC-{uuid.uuid4().hex[:6].upper()}",
                "medication": drug_name,
                "quantity_vials": quantity,
                "authorized_price_usd": total_cost
            }
        ],
        "priority": "URGENT_MEDICAL",
        "timestamp": datetime.now().isoformat()
    }
    
    print(f"  → [POST] Payload Transmitted to Supplier...")
    await asyncio.sleep(0.8) # Simulate server processing
    
    confirmation_code = f"SUPPLIER-ACK-{str(uuid.uuid4())[:8].upper()}"
    return {
        "status": "success",
        "supplier_ref": confirmation_code,
        "eta": "24-48 Hours",
        "payload": api_payload
    }


#main function (procurement_node)
async def procurement_node(state: AgentState) -> AgentState:
    try:
        print("\n [DEBUG] Procurement Node: Checking Supply Chain Logistics...")
        
        # 1. read the selected drug from strategist node
        selected_therapy = state.get("selected_therapy", "").upper().strip()
        
        #guard claude :- if error or escalate, skip procurement.
        if not selected_therapy or "ERROR" in selected_therapy or "ESCALATE" in selected_therapy:
            state["logistics_status"] = {"status": "Skipped", "reason": "No drug requires procurement."}
            return state

        # 2. check whether the inventory database exists, if missing record error n stop.
        if not os.path.exists(INVENTORY_PATH):
            state["logistics_status"] = {"status": "Error", "reason": "Inventory DB Offline"}
            state["trace"].append("✗ Procurement: Inventory DB missing.")
            return state
        #if exists , read the inventory (pharmacy_inventory.json)
        with open(INVENTORY_PATH, "r") as f:
            full_db = json.load(f)
            inventory = full_db.get("inventory", {})
            
        drug_data = inventory.get(selected_therapy)
        if not drug_data:
            state["logistics_status"] = {"status": "NOT_IN_FORMULARY", "drug": selected_therapy}
            state["trace"].append(f" Procurement: {selected_therapy} not tracked in local inventory.")
            return state
        #retrive stock , threshold n cost from the inventory data.
        stock = drug_data.get("stock_vials", 0)
        threshold = drug_data.get("critical_threshold", 10)
        
        # 3. Decision Logic(2 possibilities).
         #case-1(critical stock) helper function called to execute order.
        if stock <= threshold:
            order_qty = 50 
            total_cost = order_qty * drug_data.get("cost_per_vial_usd", 0.0)
            
            # Execute that helper function .
            api_response = await execute_external_order(selected_therapy, order_qty, total_cost)
            
            # Update state with the Purchase Order payload (Frontend renders this)
            state["logistics_status"] = {
                "status": "ORDER_GENERATED",
                "po_number": api_response["supplier_ref"],
                "drug": selected_therapy,
                "quantity_ordered": order_qty,
                "total_cost_usd": total_cost,
                "alert": f"CRITICAL STOCK ({stock} vials). Auto-replenishment triggered."
            }
            state["trace"].append(f"✓ Procurement: Stock critical ({stock}). Auto-ordered 50 vials via B2B API.")
            print(f"  → Order Confirmed. Ref: {api_response['supplier_ref']}")
             
             #case-2(stock sufficient) no order needed .
        else:
            state["logistics_status"] = {
                "status": "STOCK_SUFFICIENT",
                "current_stock": stock,
                "drug": selected_therapy
            }
            state["trace"].append(f"✓ Procurement: Stock levels healthy ({stock} vials available).")
            print(f"  → Stock healthy: {stock} vials available.")
            
        print(f" [DEBUG] Procurement Node: Complete")
        return state

    except Exception as e:
        error_msg = f"Procurement Node Error: {str(e)}"
        logger.error(error_msg)
        print(f" {error_msg}")
        
        state["logistics_status"] = {"status": "Error", "reason": str(e)}
        state["trace"].append(f"✗ {error_msg}")
        return state