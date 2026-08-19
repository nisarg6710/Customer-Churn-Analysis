from src.business.retention_roi import (
    RetentionROISimulator
)


class ActionEvaluator:

    def __init__(self):

        self.roi_simulator = (
            RetentionROISimulator()
        )

    def evaluate(
        self,
        customer,
        candidates
    ):
        """
        Evaluate every candidate intervention
        economically using customer-level revenue.
        """

        evaluated = []

        for candidate in candidates:

            customer_for_roi = (
                customer.copy()
            )

            customer_for_roi[
                "recommended_action"
            ] = candidate["action"]

            customer_for_roi[
                "action_cost"
            ] = candidate["cost"]

            roi_result = (
                self.roi_simulator.calculate(
                    customer_for_roi
                )
            )

            evaluated_candidate = (
                candidate.copy()
            )

            evaluated_candidate.update({

                "retention_probability":
                    roi_result[
                        "retention_probability_assumption"
                    ],

                "revenue_at_risk":
                    roi_result[
                        "revenue_at_risk"
                    ],

                "expected_retained_revenue":
                    roi_result[
                        "expected_retained_revenue"
                    ],

                "expected_net_value":
                    roi_result[
                        "expected_net_value"
                    ],

                "roi":
                    roi_result[
                        "roi"
                    ],

                "business_viability":
                    roi_result[
                        "business_viability"
                    ]
            })

            evaluated.append(
                evaluated_candidate
            )

        return evaluated