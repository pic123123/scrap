from langgraph.graph import StateGraph, END
from app.nodes import GraphState, fetch_page, parse_html, extract_with_llm

def create_workflow():
    workflow = StateGraph(GraphState)
    
    workflow.add_node("fetch", fetch_page)
    workflow.add_node("parse", parse_html)
    workflow.add_node("extract", extract_with_llm)
    
    # Define edges
    workflow.set_entry_point("fetch")
    
    # Conditional edge or direct? 
    # For now linear: fetch -> parse -> extract
    workflow.add_edge("fetch", "parse")
    workflow.add_edge("parse", "extract")
    workflow.add_edge("extract", END)
    
    return workflow.compile()

app_workflow = create_workflow()
