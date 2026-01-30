from typing import TypedDict
from langgraph.graph import StateGraph

from app.ai.chatbot_agent import detect_intent
from app.services.task_allocator import allocate_task
from app.services.sales_analyzer import analyze_sales_performance
from app.utils.date_utils import today_date

class SalesState(TypedDict):
    salesman_id: int
    db: object
    user_query: str
    intent: str | None
    daily_task: dict | None
    performance: dict | None
    response: str | None


def intent_classifier(state: SalesState):
    state["intent"] = detect_intent(state["user_query"])
    return state


def allocate_daily_task(state: SalesState):
    task = allocate_task(state["salesman_id"])
    state["daily_task"] = task
    state["response"] = "Here is your task for today."
    return state


def analyze_performance(state: SalesState):
    perf = analyze_sales_performance(
        db=state["db"],
        salesman_id=state["salesman_id"],
        today=today_date()
    )
    state["performance"] = perf
    state["response"] = "Here is your performance summary."
    return state


def fallback(state: SalesState):
    state["response"] = "Sorry, I didn't understand your request."
    return state


def build_sales_graph():
    graph = StateGraph(SalesState)

    graph.add_node("intent", intent_classifier)
    graph.add_node("task", allocate_daily_task)
    graph.add_node("performance", analyze_performance)
    graph.add_node("fallback", fallback)

    graph.set_entry_point("intent")

    graph.add_conditional_edges(
        "intent",
        lambda s: s["intent"],
        {
            "GET_DAILY_TASK": "task",
            "GET_PERFORMANCE": "performance"
        }
    )

    graph.add_edge("intent", "fallback")

    return graph.compile()
