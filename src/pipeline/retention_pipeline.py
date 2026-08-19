from src.decision_engine.next_best_action import (
    RetentionDecisionEngine
)

from src.business.action_evaluator import (
    ActionEvaluator
)

from src.business.budget_optimizer import (
    RetentionBudgetOptimizer
)

from src.graph.retention_graph import (
    build_retention_graph
)


class RetentionPipeline:

    def __init__(
        self,
        budget=50
    ):

        self.decision_engine = (
            RetentionDecisionEngine()
        )

        self.action_evaluator = ActionEvaluator()

        self.budget_optimizer = (
            RetentionBudgetOptimizer(
                budget=budget
            )
        )

        # LangGraph
        self.retention_graph = (
            build_retention_graph()
        )

    # ========================================================
    # PROCESS ONE CUSTOMER
    # ========================================================

    def process_customer(self, customer):

        # --------------------------------------------------
        # 1. ML / BUSINESS DECISION ENGINE
        # --------------------------------------------------

        decision = self.decision_engine.recommend(
            customer
        )

        # --------------------------------------------------
        # 2. GENERATE ALL POSSIBLE ACTIONS
        # --------------------------------------------------

        candidates = self.decision_engine.generate_candidates(
            customer
        )

        # --------------------------------------------------
        # 3. ECONOMICALLY EVALUATE EVERY ACTION
        # --------------------------------------------------

        evaluated_actions = self.action_evaluator.evaluate(
            customer,
            candidates
        )

        # --------------------------------------------------
        # 4. SELECT BEST ECONOMIC ACTION
        # --------------------------------------------------

        viable_actions = [
            action
            for action in evaluated_actions
            if action["expected_net_value"] > 0
        ]

        if viable_actions:

            economic_decision = max(
                viable_actions,
                key=lambda x:
                    x["expected_net_value"]
            )

        else:

            economic_decision = {
                "action": "No intervention",
                "cost": 0,
                "score": 0.0,
                "reason":
                    "No candidate intervention has "
                    "positive expected net value.",
                "expected_net_value": 0.0,
                "roi": 0.0,
                "business_viability":
                    "Economically unattractive"
            }

        return {

            "customer": customer,

            "decision": decision,

            "candidates": candidates,

            "evaluated_actions":
                evaluated_actions,

            "economic_decision":
                economic_decision
        }
    # ========================================================
    # RUN LANGGRAPH FOR ONE CUSTOMER
    # ========================================================

    def explain_customer(self, customer):

        result = self.retention_graph.invoke({
            "customer": customer
        })

        return result

    # ========================================================
    # OPTIMIZE PORTFOLIO
    # ========================================================

    def optimize_portfolio(self, customers):

        customer_results = []

        customer_evaluations = []

        # ----------------------------------------------------
        # PROCESS EVERY CUSTOMER
        # ----------------------------------------------------

        for customer in customers:

            result = self.process_customer(
                customer
            )

            customer_results.append(
                result
            )

            customer_evaluations.append({

                "customer_id":
                    customer["mobile_number"],

                "evaluated_actions":
                    result[
                        "evaluated_actions"
                    ]
            })

        # ----------------------------------------------------
        # BUDGET OPTIMIZATION
        # ----------------------------------------------------

        portfolio = (
            self.budget_optimizer.optimize(
                customer_evaluations
            )
        )

        # ----------------------------------------------------
        # LANGGRAPH EXPLANATIONS
        # ONLY FOR SELECTED CUSTOMERS
        # ----------------------------------------------------

        explanations = []

        selected_ids = {
            item["customer_id"]
            for item in
            portfolio["selected_customers"]
        }

        for customer in customers:

            customer_id = (
                customer["mobile_number"]
            )

            if customer_id not in selected_ids:
                continue

            graph_result = (
                self.explain_customer(
                    customer
                )
            )

            economic_decision = (
                graph_result[
                    "economic_decision"
                ]
            )

            explanations.append({

                "customer_id":
                    customer_id,

                "recommended_action":
                    economic_decision[
                        "action"
                    ],

                "action_cost":
                    economic_decision[
                        "cost"
                    ],

                "expected_net_value":
                    economic_decision[
                        "expected_net_value"
                    ],

                "roi":
                    economic_decision[
                        "roi"
                    ],

                "business_viability":
                    economic_decision[
                        "business_viability"
                    ],

                "explanation":
                    graph_result[
                        "explanation"
                    ],

                "policy_context":
                    graph_result.get(
                        "policy_context",
                        ""
                    )
            })

        # ----------------------------------------------------
        # FINAL RESULT
        # ----------------------------------------------------

        return {

            "customer_results":
                customer_results,

            "portfolio":
                portfolio,

            "explanations":
                explanations
        }