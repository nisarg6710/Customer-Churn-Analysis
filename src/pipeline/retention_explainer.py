from src.llm.retention_copilot import RetentionCopilot
from src.rag.retriever import load_retriever


class RetentionExplainer:

    def __init__(self):

        self.copilot = RetentionCopilot()
        self.retriever = load_retriever()

    def explain(
        self,
        customer,
        decision
    ):

        query = f"""
        Customer is {customer.get("risk_segment")}
        and {customer.get("value_segment")}.
        Recommended action: {decision.get("recommended_action")}.
        Strongest behavioral signal:
        {decision.get("strongest_behavior_signal")}.
        Find the relevant retention policies and decision rules.
        """

        documents = self.retriever.invoke(query)

        policy_context = "\n\n".join(
            document.page_content
            for document in documents
        )

        explanation = self.copilot.generate_response(
            customer=customer,
            decision=decision,
            policy_context=policy_context
        )

        return {
            "customer_id":
                customer.get("mobile_number"),

            "recommended_action":
                decision.get("recommended_action"),

            "explanation":
                explanation,

            "policy_context":
                policy_context
        }