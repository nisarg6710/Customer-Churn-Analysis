from typing import TypedDict

from src.decision_engine.next_best_action import (
    RetentionDecisionEngine
)

from src.business.action_evaluator import (
    ActionEvaluator
)

from src.rag.retriever import (
    load_retriever
)

from src.llm.retention_copilot import (
    RetentionCopilot
)

from langgraph.graph import (
    StateGraph,
    START,
    END
)


# ============================================================
# STATE
# ============================================================

class RetentionState(TypedDict, total=False):

    # Customer
    customer: dict

    # Decision Engine
    decision: dict

    # Economic Evaluation
    evaluated_actions: list
    economic_decision: dict

    # Final Economic Decision
    final_action: dict

    # RAG
    retrieved_documents: list
    policy_context: str

    # LLM
    explanation: str


# ============================================================
# COMPONENTS
# ============================================================

decision_engine = RetentionDecisionEngine()

action_evaluator = ActionEvaluator()

retriever = load_retriever()

copilot = RetentionCopilot()


# ============================================================
# NODE 1: DECISION ENGINE
# ============================================================

def decision_node(state: RetentionState):

    customer = state["customer"]

    decision = decision_engine.recommend(
        customer
    )

    return {
        "decision": decision
    }


# ============================================================
# NODE 2: ECONOMIC EVALUATION
# ============================================================

def economic_evaluation_node(
    state: RetentionState
):

    customer = state["customer"]

    # Generate candidate actions directly
    candidates = decision_engine.generate_candidates(
        customer
    )

    # Evaluate every candidate economically
    evaluated_actions = action_evaluator.evaluate(
        customer,
        candidates
    )

    return {
        "evaluated_actions":
            evaluated_actions
    }


# ============================================================
# NODE 3: ECONOMIC DECISION
# ============================================================

def economic_decision_node(
    state: RetentionState
):

    evaluated_actions = state[
        "evaluated_actions"
    ]

    # Only economically attractive actions
    viable_actions = [
        action
        for action in evaluated_actions
        if action["expected_net_value"] > 0
    ]

    # If at least one economically viable action
    if viable_actions:

        best_action = max(
            viable_actions,
            key=lambda x:
                x["expected_net_value"]
        )

    else:

        # No economically attractive intervention
        best_action = {
            "action": "No intervention",
            "cost": 0,
            "score": 0.0,
            "reason":(
                "No candidate intervention has",
                "positive expected net value."
            ),
            "expected_net_value": 0.0,
            "roi": 0.0,
            "business_viability":
                "No intervention"
        }

    return {
        "economic_decision": best_action,

        "final_action": best_action
    }

# ============================================================
# NODE 4: RAG
# ============================================================

def rag_node(state: RetentionState):

    customer = state["customer"]

    decision = state["decision"]

    economic_decision = state[
        "economic_decision"
    ]

    query = f"""
Find the relevant telecom customer retention
policies, retention playbook rules, and available
retention offers supporting this economic decision.

Customer segment:
{customer.get("customer_segment")}

Risk:
{customer.get("risk_segment")}

Value:
{customer.get("value_segment")}

Strongest behavioral signal:
{decision.get("strongest_behavior_signal")}

Recommended economic action:
{economic_decision.get("action")}

Action cost:
{economic_decision.get("cost")}

Expected net value:
{economic_decision.get("expected_net_value")}

Explain which business policies and retention rules
support this recommendation.
"""

    documents = retriever.invoke(
        query
    )

    policy_context = "\n\n".join(
        document.page_content
        for document in documents
    )

    return {
        "retrieved_documents":
            documents,

        "policy_context":
            policy_context
    }


# ============================================================
# NODE 5: LLM EXPLANATION
# ============================================================

def llm_node(state: RetentionState):

    customer = state["customer"]

    decision = state["decision"]

    economic_decision = state[
        "economic_decision"
    ]

    final_decision = decision.copy()

    final_decision.update({

        "recommended_action":
            economic_decision["action"],

        "action_cost":
            economic_decision["cost"],

        "reason":
            economic_decision.get(
                "reason",
                "Economically selected intervention."
            ),

        "economic_net_value":
            economic_decision[
                "expected_net_value"
            ],

        "roi":
            economic_decision[
                "roi"
            ]

    })

    # --------------------------------------------------
    # DEMO MODE
    # --------------------------------------------------
    # Avoid consuming Gemini API quota every time
    # the Streamlit dashboard is opened.
    #
    # Set USE_GEMINI=true in .env when API access
    # is available.
    # --------------------------------------------------

    import os

    use_gemini = (
        os.getenv(
            "USE_GEMINI",
            "false"
        ).lower()
        == "true"
    )

    if use_gemini:

        response = copilot.generate_response(

            customer=customer,

            decision=final_decision,

            policy_context=
                state["policy_context"]
        )

    else:

        response = copilot.generate_fallback_response(

            customer=customer,

            decision=final_decision
        )

    return {
        "explanation":
            response
    }
# ============================================================
# BUILD GRAPH
# ============================================================

def build_retention_graph():

    graph = StateGraph(
        RetentionState
    )

    # Nodes
    graph.add_node(
        "decision",
        decision_node
    )

    graph.add_node(
        "economic_evaluation",
        economic_evaluation_node
    )

    graph.add_node(
        "economic_decision",
        economic_decision_node
    )

    graph.add_node(
        "rag",
        rag_node
    )

    graph.add_node(
        "llm",
        llm_node
    )

    # Edges
    graph.add_edge(
        START,
        "decision"
    )

    graph.add_edge(
        "decision",
        "economic_evaluation"
    )

    graph.add_edge(
        "economic_evaluation",
        "economic_decision"
    )

    graph.add_edge(
        "economic_decision",
        "rag"
    )

    graph.add_edge(
        "rag",
        "llm"
    )

    graph.add_edge(
        "llm",
        END
    )

    return graph.compile()