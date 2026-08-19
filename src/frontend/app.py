import os
import sys

import streamlit as st
import pandas as pd
import plotly.express as px


# ============================================================
# PROJECT PATH
# ============================================================

PROJECT_ROOT = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "../.."
    )
)

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)


from src.pipeline.retention_pipeline import RetentionPipeline


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="AI Retention Intelligence",
    page_icon="📊",
    layout="wide"
)


# ============================================================
# LOAD DATA
# ============================================================

@st.cache_data
def load_customer_data():

    path = os.path.join(
        PROJECT_ROOT,
        "data",
        "final_customer_churn_predictions_with_strategy.csv"
    )

    df = pd.read_csv(path)

    numeric_columns = [
        "churn_probability",
        "avg_rech_amt_6_7",
        "rech_freq_drop",
        "data_usage_drop",
        "og_usage_drop",
        "arpu_6",
        "arpu_7",
        "arpu_8"
    ]

    for column in numeric_columns:

        if column in df.columns:

            df[column] = pd.to_numeric(
                df[column],
                errors="coerce"
            )

    # --------------------------------------------------------
    # Customer-level revenue
    # --------------------------------------------------------

    revenue_columns = [
        "arpu_6",
        "arpu_7",
        "arpu_8"
    ]

    available_revenue_columns = [
        column
        for column in revenue_columns
        if column in df.columns
    ]

    if not available_revenue_columns:

        raise ValueError(
            "No ARPU columns available to derive "
            "customer revenue."
        )

    df["avg_revenue"] = (
        df[available_revenue_columns]
        .mean(axis=1)
    )

    return df


@st.cache_resource
def load_pipeline():

    return RetentionPipeline()


df = load_customer_data()
pipeline = load_pipeline()


# ============================================================
# TITLE
# ============================================================

st.title("📊 AI Retention Intelligence Platform")

st.caption(
    "ML-driven churn prediction → behavioral segmentation → "
    "next-best-action → economic optimization"
)


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.header("Controls")

threshold = st.sidebar.slider(
    "Churn Probability Threshold",
    min_value=0.0,
    max_value=1.0,
    value=0.5,
    step=0.05
)


df["predicted_churn"] = (
    df["churn_probability"] >= threshold
)


# ============================================================
# PORTFOLIO OVERVIEW
# ============================================================

st.header("Portfolio Overview")

total_customers = len(df)

predicted_customers = int(
    df["predicted_churn"].sum()
)

average_churn = (
    df["churn_probability"].mean()
)

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Customers",
    f"{total_customers:,}"
)

col2.metric(
    "Predicted Churn",
    f"{predicted_customers:,}"
)

col3.metric(
    "Average Churn Probability",
    f"{average_churn:.1%}"
)

col4.metric(
    "Threshold",
    f"{threshold:.0%}"
)


# ============================================================
# CUSTOMER SELECTION
# ============================================================

st.header("Customer Intelligence")

customer_ids = (
    df["mobile_number"]
    .dropna()
    .unique()
)

customer_id = st.selectbox(
    "Select Customer",
    customer_ids
)

customer_rows = df[
    df["mobile_number"] == customer_id
]

if customer_rows.empty:

    st.warning("Customer not found.")

    st.stop()

customer = (
    customer_rows
    .iloc[0]
    .to_dict()
)


# ============================================================
# CUSTOMER PROFILE
# ============================================================

st.subheader(
    f"Customer {customer_id}"
)

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Churn Probability",
    f"{float(customer['churn_probability']):.2%}"
)

col2.metric(
    "Risk Segment",
    customer.get(
        "risk_segment",
        "Unknown"
    )
)

col3.metric(
    "Value Segment",
    customer.get(
        "value_segment",
        "Unknown"
    )
)

avg_revenue = customer.get("avg_revenue")

if pd.isna(avg_revenue):

    revenue_display = "Unavailable"

else:

    revenue_display = (
        f"₹{float(avg_revenue):.2f}"
    )

col4.metric(
    "Average Revenue",
    revenue_display
)


# ============================================================
# BEHAVIORAL SIGNALS
# ============================================================

st.subheader(
    "Behavioral Signals"
)

behavior_columns = {
    "Recharge Frequency Drop":
        "rech_freq_drop",

    "Data Usage Drop":
        "data_usage_drop",

    "Outgoing Usage Drop":
        "og_usage_drop"
}

behavior_cols = st.columns(
    len(behavior_columns)
)

for column, (label, field) in zip(
    behavior_cols,
    behavior_columns.items()
):

    value = customer.get(field)

    if value is None or pd.isna(value):

        display_value = "Unavailable"

    else:

        display_value = f"{float(value):.0f}"

    column.metric(
        label,
        display_value
    )


# ============================================================
# ECONOMIC DECISION
# ============================================================

st.header(
    "💰 Economic Retention Decision"
)

if st.button(
    "Evaluate Retention Action",
    type="primary"
):

    if (
        "avg_revenue" not in customer
        or pd.isna(customer["avg_revenue"])
    ):

        st.error(
            "Economic evaluation cannot run because "
            "this customer does not have a valid "
            "revenue value."
        )

    else:

        with st.spinner(
            "Evaluating customer economics..."
        ):

            try:

                result = (
                    pipeline.process_customer(
                        customer
                    )
                )

                st.session_state[
                    "customer_result"
                ] = result

            except Exception as e:

                st.error(
                    f"Economic evaluation failed: {e}"
                )


# ============================================================
# DISPLAY ECONOMIC RESULT
# ============================================================

if "customer_result" in st.session_state:

    result = st.session_state[
        "customer_result"
    ]

    evaluated_actions = result[
        "evaluated_actions"
    ]

    economic_decision = result[
        "economic_decision"
    ]

    st.subheader(
        "Candidate Actions"
    )

    action_df = pd.DataFrame(
        evaluated_actions
    )

    display_columns = [
        column
        for column in [
            "action",
            "cost",
            "expected_retained_revenue",
            "expected_net_value",
            "roi",
            "business_viability"
        ]
        if column in action_df.columns
    ]

    st.dataframe(
        action_df[display_columns],
        use_container_width=True,
        hide_index=True
    )

    st.subheader(
        "Final Economic Decision"
    )

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Recommended Action",
        economic_decision["action"]
    )

    col2.metric(
        "Intervention Cost",
        f"₹{economic_decision['cost']:.2f}"
    )

    col3.metric(
        "Expected Net Value",
        f"₹{economic_decision['expected_net_value']:.2f}"
    )

    col4.metric(
        "ROI",
        f"{economic_decision['roi']:.2f}x"
    )

    st.info(
        economic_decision.get(
            "reason",
            ""
        )
    )


# ============================================================
# CHURN ANALYTICS
# ============================================================

st.header(
    "📈 Churn Analytics"
)

fig = px.scatter(
    df,
    x="avg_rech_amt_6_7",
    y="rech_freq_drop",
    color="risk_segment",
    hover_data=[
        "mobile_number",
        "churn_probability",
        "value_segment"
    ],
    title="Recharge Behavior vs Churn Risk"
)

fig.update_traces(
    marker=dict(size=7)
)

st.plotly_chart(
    fig,
    use_container_width=True
)


# ============================================================
# CUSTOMER DATASET
# ============================================================

st.header(
    "Customer Dataset"
)

available_columns = [
    column
    for column in [
        "mobile_number",
        "churn_probability",
        "risk_segment",
        "value_segment",
        "customer_segment",
        "avg_revenue",
        "rech_freq_drop",
        "data_usage_drop",
        "og_usage_drop"
    ]
    if column in df.columns
]

st.dataframe(
    df[available_columns],
    use_container_width=True,
    hide_index=True
)