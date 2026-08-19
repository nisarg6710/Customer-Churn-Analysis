import os

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI


load_dotenv()


class RetentionCopilot:

    def __init__(self):

        api_key = os.getenv("GOOGLE_API_KEY")

        if not api_key:
            raise ValueError(
                "GOOGLE_API_KEY not found in .env"
            )

        self.llm = ChatGoogleGenerativeAI(
            model="gemini-3.6-flash",
            google_api_key=api_key
        )

    def generate_response(
        self,
        customer,
        decision,
        policy_context
    ):

        prompt = f"""
You are an AI Retention Strategist for a telecom company.

Your role is to explain a retention recommendation
to a business manager using the customer's ML prediction,
the decision engine's recommendation, and retrieved
company policies.

CUSTOMER INFORMATION

Customer ID:
{customer.get("mobile_number")}

Churn Probability:
{customer.get("churn_probability")}

Risk Segment:
{customer.get("risk_segment")}

Value Segment:
{customer.get("value_segment")}

Customer Segment:
{customer.get("customer_segment")}

Recharge Frequency Drop:
{customer.get("rech_freq_drop")}

Data Usage Drop:
{customer.get("data_usage_drop")}

Outgoing Usage Drop:
{customer.get("og_usage_drop")}


DECISION ENGINE

Recommended Action:
{decision.get("recommended_action")}

Action Cost:
{decision.get("action_cost")}

Reason:
{decision.get("reason")}

Strongest Behavioral Signal:
{decision.get("strongest_behavior_signal")}


RETRIEVED BUSINESS KNOWLEDGE

{policy_context}


INSTRUCTIONS

Explain the recommendation using ONLY the information
provided above.

Explain:

1. Why the customer is at risk.
2. Why the customer is valuable.
3. Which customer behavior is deteriorating.
4. Why the recommended action fits the customer.
5. Which business policy supports the recommendation.

Do NOT claim that the intervention will definitely
prevent churn.

Clearly distinguish between:
- ML prediction
- Business decision
- Retrieved company policy

Keep the answer concise and business-oriented.

Use exactly this structure:

Recommendation:
<recommended action>

Why this customer is at risk:
<explanation>

Customer value:
<explanation>

Behavioral signal:
<explanation>

Business rationale:
<explanation>

Policy support:
<explanation>

Important caveat:
<short caveat>
"""

        response = self.llm.invoke(prompt)

        if isinstance(response.content, list):
            text_parts = []

            for block in response.content:
                if isinstance(block, dict) and block.get("type") == "text":
                    text_parts.append(block.get("text", ""))

            return "\n".join(text_parts)

        return response.content

    def generate_fallback_response(self, customer, decision):

        action = decision.get(
            "recommended_action",
            "No intervention"
        )

        churn_probability = customer.get(
            "churn_probability",
            0
        )

        risk_segment = customer.get(
            "risk_segment",
            "Unknown"
        )

        value_segment = customer.get(
            "value_segment",
            "Unknown"
        )

        customer_segment = customer.get(
            "customer_segment",
            "Unknown"
        )

        behavioral_signal = decision.get(
            "strongest_behavior_signal",
            "No strong behavioral signal identified"
        )

        action_cost = decision.get(
            "action_cost",
            0
        )

        return f"""
    Recommendation:
    {action}

    Why this customer is at risk:
    The ML model predicts a churn probability of
    {churn_probability:.4f}, placing the customer in the
    {risk_segment} segment.

    Customer value:
    The customer belongs to the {value_segment} segment,
    with an overall classification of {customer_segment}.

    Behavioral signal:
    The strongest deteriorating behavioral signal identified
    by the decision engine is {behavioral_signal}.

    Business rationale:
    The decision engine recommends a {action} with an
    intervention cost of ₹{action_cost}. The recommendation
    is based on the customer's predicted churn risk,
    business value, and observed behavioral deterioration.

    Policy support:
    The recommendation follows the retention decision rules
    and customer-segment policies retrieved by the system.

    Important caveat:
    This recommendation is based on ML predictions and
    business rules. It does not guarantee that the intervention
    will prevent churn, and intervention costs are scenario
    assumptions rather than measured campaign costs.
    """.strip()