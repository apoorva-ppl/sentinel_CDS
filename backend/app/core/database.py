import os
import logging
from typing import Dict, List, Any, Optional
from neo4j import GraphDatabase, Driver
from neo4j.exceptions import ServiceUnavailable, AuthError
from dotenv import load_dotenv

load_dotenv()

# Setup structured logger
logger = logging.getLogger("app.database.neo4j")
logger.setLevel(logging.INFO)

class Neo4jManager:
 
    _instance: Optional['Neo4jManager'] = None
    _driver: Optional[Driver] = None

    def __new__(cls):
        """Implement Singleton pattern to prevent multiple driver pools."""
        if cls._instance is None:
            cls._instance = super(Neo4jManager, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, "initialized"):
            self.uri = os.getenv("NEO4J_URI", "bolt://localhost:7687")
            self.user = os.getenv("NEO4J_USERNAME", "neo4j")
            self.password = os.getenv("NEO4J_PASSWORD", "password")
            self.initialized = True

    def connect(self) -> Optional[Driver]:
        if self._driver is not None:
            return self._driver

        try:
            # Handle secure/encrypted cloud routing vs local routing strings automatically
            is_secure = "+s" in self.uri or "neo4j+s" in self.uri
            
            self._driver = GraphDatabase.driver(
                self.uri,
                auth=(self.user, self.password),
                connection_timeout=5.0,
                max_connection_lifetime=3600, # 1 hour max pool connection age
                max_connection_pool_size=50    # Capacity for concurrent agent tasks
            )
            
            # Verify the pool is active and ready
            self._driver.verify_connectivity()
            logger.info(f" Neo4j Connection Pool Initialized: {self.uri}")
            return self._driver

        except (ServiceUnavailable, AuthError) as e:
            logger.critical(f" Neo4j Connection Pool Initialization Failed: {str(e)}")
            self._driver = None
            return None

    def close(self):
        """Gracefully tears down the connection pool during backend shutdown."""
        if self._driver:
            logger.info("Closing Neo4j connection pool...")
            self._driver.close()
            self._driver = None

    def query(self, cypher: str, parameters: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
       
        # Auto-connect if driver wasn't explicitly initialized
        driver = self.connect()
        
        if not driver:
            logger.warning("Graph database engine offline. Skipping execution and returning empty results.")
            return []

        try:
            # Using implicit or explicit read transactions is standard best practice for Neo4j 5.x+
            with driver.session() as session:
                def _execute_tx(tx):
                    result = tx.run(cypher, parameters or {})
                    return [dict(record) for record in result]
                
                return session.execute_read(_execute_tx)
                
        except Exception as e:
            logger.error(f"Cypher execution anomaly detected: {str(e)}")
            logger.debug(f"Failed Cypher statement: {cypher} with parameters: {parameters}")
            return []

# Expose a clean, reusable singleton instance for your nodes and routers
db_client = Neo4jManager()
# Alias for backward compatibility with verifier.py
Neo4jConnection = Neo4jManager