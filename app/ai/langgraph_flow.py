from typing import TypedDict
from langgraph.graph import StateGraph

from app.services.task_allocator import allocate_task
from app.services.sales_analyzer import analyze_sales_performance
from app.utils.date_utils import today_date

# State definition
class SalesState(TypedDict):
    salesman_id: int
    daily_task: dict
    performance: dict

# Nodes
def allocate_daily_task(state: SalesState):
    task = allocate_task(state["salesman_id"])
    state["daily_task"] = task
    return state

def analyze_performance(state: SalesState):
    performance = analyze_sales_performance(
        db=state["db"],
        salesman_id=state["salesman_id"],
        today=today_date()
    )
    state["performance"] = performance
    return state

# Graph builder
def build_sales_graph():
    graph = StateGraph(SalesState)

    graph.add_node("allocate_task", allocate_daily_task)
    graph.add_node("analyze_performance", analyze_performance)

    graph.set_entry_point("allocate_task")
    graph.add_edge("allocate_task", "analyze_performance")

    return graph.compile()
