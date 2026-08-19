class RetentionBudgetOptimizer:

    def __init__(self, budget):
        self.budget = float(budget)

    def optimize(self, customer_evaluations):
        """
        Allocate a limited retention budget across customers.

        Only economically viable interventions
        (expected_net_value > 0) are eligible for selection.
        """

        opportunities = []
        rejected = []

        # --------------------------------------------------
        # Evaluate every customer
        # --------------------------------------------------

        for customer in customer_evaluations:

            customer_id = customer["customer_id"]

            actions = customer["evaluated_actions"]

            # Find economically viable actions
            viable_actions = [
                action
                for action in actions
                if action["expected_net_value"] > 0
                and action["cost"] > 0
            ]

            # --------------------------------------------------
            # No economically viable intervention
            # --------------------------------------------------

            if not viable_actions:

                if actions:

                    best_action = max(
                        actions,
                        key=lambda x: x["expected_net_value"]
                    )

                    rejected_action = best_action.copy()

                    rejected_action["customer_id"] = customer_id

                    rejected_action["rejection_reason"] = (
                        "No economically viable intervention."
                    )

                    rejected.append(rejected_action)

                continue

            # --------------------------------------------------
            # Best economically viable action
            # --------------------------------------------------

            best_action = max(
                viable_actions,
                key=lambda x: x["expected_net_value"]
            )

            opportunity = best_action.copy()

            opportunity["customer_id"] = customer_id

            opportunities.append(opportunity)

        # --------------------------------------------------
        # Rank viable opportunities
        # --------------------------------------------------

        opportunities.sort(
            key=lambda x: x["expected_net_value"],
            reverse=True
        )

        selected = []

        total_cost = 0.0
        total_net_value = 0.0

        # --------------------------------------------------
        # Allocate budget
        # --------------------------------------------------

        for opportunity in opportunities:

            cost = opportunity["cost"]

            if total_cost + cost <= self.budget:

                selected.append(opportunity)

                total_cost += cost

                total_net_value += (
                    opportunity["expected_net_value"]
                )

            else:

                rejected_action = opportunity.copy()

                rejected_action["rejection_reason"] = (
                    "Economically viable but budget was insufficient."
                )

                rejected.append(rejected_action)

        # --------------------------------------------------
        # Mark selected customers
        # --------------------------------------------------

        selected_ids = {
            item["customer_id"]
            for item in selected
        }

        # --------------------------------------------------
        # Final result
        # --------------------------------------------------

        return {
            "budget": self.budget,

            "recommended_spend": total_cost,

            "remaining_budget":
                self.budget - total_cost,

            "customers_targeted":
                len(selected),

            "customers_considered":
                len(customer_evaluations),

            "economically_viable_customers":
                len(opportunities),

            "customers_rejected":
                len(customer_evaluations) - len(selected),

            "expected_net_value":
                total_net_value,

            "selected_customers":
                selected,

            "rejected_customers":
                rejected
        }