from src.business.action_effectiveness import (
    get_retention_probability
)


class RetentionROISimulator:

    def __init__(self):
        """
        ROI simulator.

        Customer-level revenue must be provided by the
        customer's business profile.
        """

        pass

    def calculate(self, customer):
        """
        Calculate expected business value for the
        customer's recommended intervention.

        Customer revenue is taken directly from
        customer["avg_revenue"].

        IMPORTANT:
        Intervention effectiveness values are scenario
        assumptions and are NOT causal estimates.
        """

        # --------------------------------------------------
        # CUSTOMER BUSINESS PROFILE
        # --------------------------------------------------

        if "avg_revenue" not in customer:

            raise ValueError(
                "Customer is missing 'avg_revenue'. "
                "ROI calculation requires customer-level "
                "revenue information."
            )

        churn_probability = float(
            customer.get(
                "churn_probability",
                0
            )
        )

        avg_revenue = float(
            customer["avg_revenue"]
        )

        # --------------------------------------------------
        # RETENTION ACTION
        # --------------------------------------------------

        action = customer.get(
            "recommended_action",
            "No intervention"
        )

        action_cost = float(
            customer.get(
                "action_cost",
                0
            )
        )

        # --------------------------------------------------
        # SCENARIO-BASED EFFECTIVENESS
        # --------------------------------------------------

        retention_probability = (
            get_retention_probability(action)
        )

        # --------------------------------------------------
        # REVENUE AT RISK
        # --------------------------------------------------

        revenue_at_risk = (
            churn_probability *
            avg_revenue
        )

        # --------------------------------------------------
        # EXPECTED RETAINED REVENUE
        # --------------------------------------------------

        expected_retained_revenue = (
            revenue_at_risk *
            retention_probability
        )

        # --------------------------------------------------
        # EXPECTED NET BUSINESS VALUE
        # --------------------------------------------------

        expected_net_value = (
            expected_retained_revenue -
            action_cost
        )

        # --------------------------------------------------
        # ROI
        # --------------------------------------------------

        if action_cost > 0:

            roi = (
                expected_net_value /
                action_cost
            )

        else:

            roi = 0.0

        # --------------------------------------------------
        # BUSINESS VIABILITY
        # --------------------------------------------------

        if action == "No intervention":

            business_viability = (
                "No intervention"
            )

        elif expected_net_value > 0:

            business_viability = (
                "Economically attractive"
            )

        else:

            business_viability = (
                "Economically unattractive"
            )

        # --------------------------------------------------
        # RESULT
        # --------------------------------------------------

        return {

            "action":
                action,

            "retention_probability_assumption":
                retention_probability,

            "revenue_at_risk":
                round(
                    revenue_at_risk,
                    2
                ),

            "expected_retained_revenue":
                round(
                    expected_retained_revenue,
                    2
                ),

            "intervention_cost":
                round(
                    action_cost,
                    2
                ),

            "expected_net_value":
                round(
                    expected_net_value,
                    2
                ),

            "roi":
                round(
                    roi,
                    2
                ),

            "business_viability":
                business_viability
        }