import pandas as pd


class RetentionDecisionEngine:

    def _to_float(self, value):
        try:
            return float(value)
        except (TypeError, ValueError):
            return 0.0

    def _behavior_signals(self, row):
        """
        Detect the strongest behavioral deterioration.
        Negative values represent declining behavior in the
        existing feature-engineering pipeline.
        """

        signals = {
            "recharge": self._to_float(row.get("rech_freq_drop", 0)),
            "data": self._to_float(row.get("data_usage_drop", 0)),
            "outgoing": self._to_float(row.get("og_usage_drop", 0)),
        }

        # Most negative = strongest deterioration
        strongest = min(signals, key=signals.get)

        return signals, strongest

    def generate_candidates(self, row):

        risk = row["risk_segment"]
        value = row["value_segment"]

        signals, strongest = self._behavior_signals(row)

        candidates = []

        # --------------------------------------------------
        # LOW RISK
        # --------------------------------------------------

        if risk == "Low Risk":
            candidates.append({
                "action": "No intervention",
                "cost": 0,
                "score": 1.0,
                "reason": "Customer currently has low predicted churn risk."
            })

            return candidates

        # --------------------------------------------------
        # MEDIUM RISK
        # --------------------------------------------------

        if risk == "Medium Risk":

            candidates.append({
                "action": "Personalized SMS campaign",
                "cost": 10,
                "score": 0.70,
                "reason": "Moderate churn risk makes a low-cost engagement campaign appropriate."
            })

            if value == "High Value":
                candidates.append({
                    "action": "Loyalty offer",
                    "cost": 30,
                    "score": 0.80,
                    "reason": "High-value customer with moderate churn risk."
                })

            if strongest == "data":
                candidates.append({
                    "action": "Discounted data pack",
                    "cost": 30,
                    "score": 0.82,
                    "reason": "Customer shows the strongest deterioration in data usage."
                })

            elif strongest == "recharge":
                candidates.append({
                    "action": "Recharge incentive",
                    "cost": 30,
                    "score": 0.82,
                    "reason": "Customer shows the strongest deterioration in recharge frequency."
                })

            elif strongest == "outgoing":
                candidates.append({
                    "action": "Personalized engagement campaign",
                    "cost": 20,
                    "score": 0.82,
                    "reason": "Customer shows the strongest deterioration in outgoing usage."
                })

            return candidates

        # --------------------------------------------------
        # HIGH RISK
        # --------------------------------------------------

        if risk == "High Risk":

            if value == "High Value":

                candidates.append({
                    "action": "High-value loyalty offer",
                    "cost": 50,
                    "score": 0.95,
                    "reason": "Customer is both highly valuable and highly likely to churn."
                })

                if strongest == "data":
                    candidates.append({
                        "action": "Premium discounted data pack",
                        "cost": 40,
                        "score": 0.97,
                        "reason": "High-value customer has severe deterioration in data usage."
                    })

                elif strongest == "recharge":
                    candidates.append({
                        "action": "Premium recharge incentive",
                        "cost": 40,
                        "score": 0.97,
                        "reason": "High-value customer has severe deterioration in recharge frequency."
                    })

                elif strongest == "outgoing":
                    candidates.append({
                        "action": "Personalized retention call",
                        "cost": 30,
                        "score": 0.96,
                        "reason": "High-value customer has significant deterioration in outgoing usage."
                    })

            elif value == "Medium Value":

                candidates.append({
                    "action": "Personalized SMS campaign",
                    "cost": 10,
                    "score": 0.80,
                    "reason": "High churn risk requires intervention while controlling retention cost."
                })

                if strongest == "data":
                    candidates.append({
                        "action": "Discounted data pack",
                        "cost": 30,
                        "score": 0.85,
                        "reason": "Data usage is the strongest deteriorating behavior."
                    })

                elif strongest == "recharge":
                    candidates.append({
                        "action": "Recharge incentive",
                        "cost": 30,
                        "score": 0.85,
                        "reason": "Recharge frequency is the strongest deteriorating behavior."
                    })

            else:

                candidates.extend([
                    {
                        "action": "Personalized SMS campaign",
                        "cost": 10,
                        "score": 0.70,
                        "reason": "Low-cost intervention is appropriate for a lower-value high-risk customer."
                    },
                    {
                        "action": "Minimal intervention",
                        "cost": 5,
                        "score": 0.60,
                        "reason": "Customer has high churn risk but relatively low business value."
                    }
                ])

            return candidates

        return candidates

    def recommend(self, row):

        candidates = self.generate_candidates(row)

        signals, strongest = self._behavior_signals(row)

        return {
            "candidate_actions": candidates,
            "strongest_behavior_signal": strongest,
            "behavior_signals": signals
        }
    