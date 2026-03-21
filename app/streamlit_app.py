import streamlit as st
import pandas as pd
import joblib
import plotly.express as px

st.title("Telecom Customer Churn Dashboard")

# Load data
df = pd.read_csv("data/final_customer_churn_predictions_with_strategy.csv")

df["avg_rech_amt_6_7"] = pd.to_numeric(df["avg_rech_amt_6_7"], errors="coerce")
df["rech_freq_drop"] = pd.to_numeric(df["rech_freq_drop"], errors="coerce")

# Load model
model = joblib.load("models/churn_rf_model.pkl")

st.header("Customer Churn Predictions")

##threshold slider can be varied
threshold = st.slider(
    "Churn Probability Threshold",
    0.0,
    1.0,
    0.5
)

df["predicted_churn"] = df["churn_probability"] >= threshold

## customer lookup
# customer_id = st.text_input("Enter Customer Mobile Number")
customer_id = st.selectbox(
    "Select Customer",
    df["mobile_number"].unique()
)

if customer_id:

    try:

        customer_id = int(customer_id)

        customer = df[df["mobile_number"] == customer_id]

        if customer.empty:
            st.warning("Customer not found")
        else:
            row = customer.iloc[0]

            st.subheader("Customer Summary")

            col1, col2, col3 = st.columns(3)

            prediction = "Churn Likely" if row["churn_probability"] >= threshold else "Safe"

            col1.metric("Churn Probability", round(row["churn_probability"], 2))
            col2.metric("Prediction", prediction)
            col3.metric("Avg Recharge", round(row["avg_rech_amt_6_7"],2))

            predicted = df[df["predicted_churn"]]

            st.write("Customers predicted to churn:", len(predicted))

            st.write("Customer Details")

            st.write(customer)
    
    except Exception as e:
        st.error("Enter a valid mobile number. Error is: {e}")


## interactive plots
st.write(df[["avg_rech_amt_6_7", "rech_freq_drop"]].describe())
fig = px.scatter(
    df,
    x="avg_rech_amt_6_7",
    y="rech_freq_drop",
    color="risk_segment",
    title="Customer Recharge Behavior vs Churn Risk",
    opacity=0.6
)
st.plotly_chart(fig)


## roi calculator
offer_cost = st.number_input("Retention Offer Cost", value=10)
avg_revenue = st.number_input("Average Revenue Per User", value=50)
customers_saved = st.number_input("Customers Saved", value=400)

profit = customers_saved * avg_revenue - customers_saved * offer_cost

st.write("Estimated Profit:", profit)

# st.write(df.columns)