from langgraph.graph import StateGraph, END
from pdf_agent import pdf_research
from web_agent import web_research
from synthesis_agent import synthesis_node
from state import ResearchState
from supervisor import supervisor_node

def where_to(state: ResearchState):
    if state["next_node"] == "pdf_research":
        return "pdf_research"
    elif state["next_node"] == "web_research":
        return "web_research"
    elif state["next_node"] == "FINISH":
        return "synthesis_node"

graph = StateGraph(ResearchState)

graph.add_node("supervisor_node", supervisor_node)
graph.add_node("pdf_research", pdf_research)
graph.add_node("web_research", web_research)
graph.add_node("synthesis_node", synthesis_node)

graph.set_entry_point("supervisor_node")

graph.add_conditional_edges("supervisor_node", where_to)
graph.add_edge("pdf_research", "supervisor_node")
graph.add_edge("web_research", "supervisor_node")
graph.add_edge("synthesis_node", END)

final_app = graph.compile()