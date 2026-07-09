import os
import sys
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

def build_knowledge_graph():
    from app.core.database import db_client

    script_dir = os.path.dirname(os.path.abspath(__file__))
    backend_root = os.path.abspath(os.path.join(script_dir, ".."))
    
    aro_path = os.path.join(backend_root, "data", "aro.tsv")
    index_path = os.path.join(backend_root, "data", "aro_index.tsv")
    
    print("Checking data files...")
    try:
        df_aro = pd.read_csv(aro_path, sep="\t", on_bad_lines='skip')
        desc_map = df_aro.set_index('Accession')['Description'].to_dict()

        df_idx = pd.read_csv(index_path, sep="\t", on_bad_lines='skip')
        df_idx = df_idx.dropna(subset=['ARO Name', 'Drug Class', 'Resistance Mechanism'])

        data_payload = []
        for _, row in df_idx.iterrows():
            aro_id = str(row['ARO Accession']).strip()
            data_payload.append({
                "gene_name": str(row['ARO Name']).strip(),
                "family": str(row['AMR Gene Family']).strip(),
                "mechanism": str(row['Resistance Mechanism']).strip(),
                "drug_classes": str(row['Drug Class']).strip(),
                "description": desc_map.get(aro_id, "Description unavailable."),
                "aro_id": aro_id
            })

    except Exception as e:
        print(f"Data Loading Error: {e}")
        return

    cypher_query = """
    UNWIND $data AS row
    MERGE (g:Gene {name: row.gene_name})
    SET g.family = row.family,
        g.description = row.description,
        g.aro_id = row.aro_id
    MERGE (m:Mechanism {name: row.mechanism})
    MERGE (g)-[:USES_MECHANISM]->(m)
    WITH g, row, split(row.drug_classes, ';') AS drugs
    UNWIND drugs AS drug_name
    WITH g, trim(drug_name) AS clean_drug
    WHERE clean_drug <> ""
    MERGE (d:DrugClass {name: clean_drug})
    MERGE (g)-[:CONFERS_RESISTANCE_TO]->(d)
    """

    print("Connecting to Neo4j...")
    driver = db_client.connect()
    
    if not driver:
        print("Neo4j offline - cannot ingest CARD data.")
        return

    print(f"Ingesting {len(data_payload)} nodes into Neo4j...")
    try:
        with driver.session() as session:
            session.run(cypher_query, data=data_payload)
        print("Success. Knowledge Graph built from CARD data.")
    except Exception as e:
        print(f"Ingestion Failed: {e}")

if __name__ == "__main__":
    build_knowledge_graph()