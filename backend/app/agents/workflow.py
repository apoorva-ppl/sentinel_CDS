from langgraph.graph import StateGraph, END

from app.schemas.analysis_types import AgentState
from app.agents.nodes.predictor import predictor_node
from app.agents.nodes.strategist import strategist_node
from app.agents.nodes.verifier import verifier_node
from app.agents.nodes.pharmacist import pharmacist_node
from app.agents.nodes.procurement import procurement_node




#This function creates the complete LangGraph workflow
def build_sentinel_graph():
    graph = StateGraph(AgentState)
    
    # 1. Register all 5 nodes 
    graph.add_node("predictor", predictor_node)
    graph.add_node("strategist", strategist_node)
    graph.add_node("verifier", verifier_node)
    graph.add_node("pharmacist", pharmacist_node)
    graph.add_node("procurement", procurement_node)
    
    # 2.wire the edges to define the flow of execution.
    graph.set_entry_point("predictor")
    graph.add_edge("predictor", "strategist")
    graph.add_edge("strategist", "verifier")
    graph.add_edge("verifier", "pharmacist")
    graph.add_edge("pharmacist", "procurement")
    graph.add_edge("procurement", END)
    
    # 3. Compile the graph n run 
    # this converts the graph into an executable workflow.
    return graph.compile()



# Single graph instance reused across all API calls (extensible + deterministic assembly flow + thread safe)
# This prevents FastAPI from rebuilding the graph on every single HTTP request.
sentinel_graph = build_sentinel_graph()