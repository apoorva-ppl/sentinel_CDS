from app.core.database import db_client

def run_cypher(query: str, params: dict | None = None) -> list:
    return db_client.query(query, params or {})