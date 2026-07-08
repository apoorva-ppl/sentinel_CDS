import logging
from app.schemas.analysis_types import AgentState
from app.core.database import Neo4jConnection

logger = logging.getLogger(__name__)

# The mapping converts our clinical drug abbreviations into the drug classes used in the CARD database
DRUG_CLASS_MAP = {
    "CIP": "fluoroquinolone",
    "LVX": "fluoroquinolone",
    "AMX/AMP": "beta-lactam",
    "AUGMENTIN": "beta-lactam",
    "GEN": "aminoglycoside",
    "VAN": "glycopeptide",
    "LZD": "oxazolidinone",
    "MEM": "carbapenem",
    "TZP": "beta-lactam",
    "CRO": "cephalosporin"
    
}

def verifier_node(state: AgentState) -> AgentState:
    try:
        print("\n [DEBUG] Verifier Node: Grounding ML Predictions via Neo4j CARD Graph...")
        
        ml_profile = state.get("ml_15_drug_profile", {}) #ml predictions
        isolate_id = state.get("isolate_id", "Unknown").lower() #bacterial isolate/strain
        
        # 1. Identify which drugs need biological verification
          #verifier only checks resistant drugs , hence saves database queries + efficiency increases.
        resistant_drugs = [drug for drug, data in ml_profile.items() if data.get("is_resistant", False)]
        if not resistant_drugs:
            state["genomic_verification"] = ["Organism is pan-susceptible. No specific resistance markers required."]
            state["trace"].append("✓ Verifier: No resistance flagged. Bypassing genomic graph check.")
            return state

        verification_results = []
        
        # 2. Open Neo4j Connection (Context Manager)
        with Neo4jConnection() as neo4j:
            if neo4j.driver is None: #for increasing system robustnessm if neo4j down it wont crash.
                error_msg = "Neo4j Offline - Cannot verify biological mechanisms."
                state["genomic_verification"] = [error_msg]
                state["trace"].append(f"⚠ Verifier: {error_msg}")
                return state

            # 3. query CARD for EACH resistant drug one by one
            for drug in resistant_drugs:
                drug_class = DRUG_CLASS_MAP.get(drug.upper(), drug.lower())
                
                # The Cypher query is generated dynamically using the drug class and isolate ID from the workflow state.
                cypher_query = """
                MATCH (g:Gene)-[:CONFERS_RESISTANCE_TO]->(d:DrugClass) 
                WHERE toLower(d.name) CONTAINS toLower($drug_class)
                  AND toLower(g.description) CONTAINS toLower($pathogen)
                RETURN g.name AS Gene, g.family AS Family, g.description AS Description
                ORDER BY g.name ASC
                LIMIT 1
                """
                
                results = neo4j.query(cypher_query, {"drug_class": drug_class, "pathogen": isolate_id})
                
                # Fallback: f no pathogen-specific evidence exists, we fall back to a general resistance mechanism for that drug class.
                if not results:
                    fallback_query = """
                    MATCH (g:Gene)-[:CONFERS_RESISTANCE_TO]->(d:DrugClass) 
                    WHERE toLower(d.name) CONTAINS toLower($drug_class)
                    RETURN g.name AS Gene, g.family AS Family, g.description AS Description
                    LIMIT 1
                    """
                    results = neo4j.query(fallback_query, {"drug_class": drug_class})

                if results:
                    gene_data = results[0]
                    verification_results.append(
                        f"[{drug}] Verified: {gene_data['Gene']} ({gene_data['Family']}) - {gene_data['Description'][:100]}..."
                    )
                else:
                    verification_results.append(f"[{drug}] Warning: Novel/Unmapped mechanism in CARD database.")

        # 4. Update the State
        state["genomic_verification"] = verification_results
        
        summary = f"✓ Verifier: Cross-referenced {len(resistant_drugs)} flagged drugs with CARD Genomic Graph."
        state["trace"].append(summary)
        print(f"  → Found genomic matches for {len(verification_results)} resistance vectors.")
        print(f" [DEBUG] Verifier Node: Complete")

        return state

    except Exception as e:
        error_msg = f"Verifier Node Error: {str(e)}"
        logger.error(error_msg)
        print(f" {error_msg}")
        
        state["genomic_verification"] = [f"Error during Graph-RAG verification: {str(e)}"]
        state["trace"].append(f"✗ {error_msg}")
        return state