from typing import TypedDict

from langgraph.graph import StateGraph, END

from src.tools.customer_tool import get_customer
from src.tools.decision_tool import get_next_best_action


class RetentionState(TypedDict, total=False):

    customer_id: str

    customer: dict

    decision: dict

    policy_context: str

    final_answer: str


def fetch_customer(state):

    customer = get_customer(
        state["customer_id"]
    )

    return {
        "customer": customer
    }


def generate_decision(state):

    decision = get_next_best_action(
        state["customer"]
    )

    return {
        "decision": decision
    }


def build_graph():

    graph = StateGraph(RetentionState)

    graph.add_node(
        "fetch_customer",
        fetch_customer
    )

    graph.add_node(
        "generate_decision",
        generate_decision
    )

    graph.set_entry_point(
        "fetch_customer"
    )

    graph.add_edge(
        "fetch_customer",
        "generate_decision"
    )

    graph.add_edge(
        "generate_decision",
        END
    )

    return graph.compile()