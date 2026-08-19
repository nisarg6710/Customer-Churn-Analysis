# 📊 AI Retention Intelligence Platform

> **ML-driven churn prediction, behavioral intelligence,
> next-best-action recommendation, and economic retention optimization
> for customer-level decision making.**

## Overview

The **AI Retention Intelligence Platform** is an end-to-end customer
churn and retention decision system.

Instead of stopping at:

> "Which customers are likely to churn?"

the platform extends churn prediction into:

> **"Which retention action should we take, and is that action
> economically worthwhile for this customer?"**

The system combines customer churn probability, behavioral deterioration
signals, customer value, retention strategies, intervention costs, and
customer-level revenue to produce an **economically informed retention
decision**.

------------------------------------------------------------------------

## 🎯 Problem Statement

Traditional churn prediction systems primarily identify customers who
are likely to leave.

However, a high churn probability alone does not answer important
business questions:

-   Which customers should receive an intervention?
-   Which retention action should be selected?
-   How much revenue is actually at risk?
-   Is the intervention worth its cost?
-   Which action produces the highest expected business value?

The goal of this project is to bridge the gap between **churn
prediction** and **business decision making**.

------------------------------------------------------------------------

## 💡 Solution

The platform follows a multi-stage decision pipeline:

``` text
Customer Data
      ↓
Feature Engineering
      ↓
Churn Prediction
      ↓
Risk & Value Segmentation
      ↓
Behavioral Signal Analysis
      ↓
Retention Strategy
      ↓
Candidate Retention Actions
      ↓
Customer-Level Revenue Estimation
      ↓
Economic / ROI Simulation
      ↓
Best Economic Action
      ↓
Streamlit Decision Dashboard
```

This allows the system to move from **prediction → recommendation →
economic optimization**.

------------------------------------------------------------------------

# 🚀 Key Features

### 1. Churn Prediction

The platform uses customer behavioral and usage information to generate
a:

``` text
churn_probability
```

This probability is used throughout the downstream decision pipeline.

------------------------------------------------------------------------

### 2. Risk Segmentation

Customers are categorized into risk groups such as:

-   Low Risk
-   Medium Risk
-   High Risk

The frontend also allows the user to dynamically change the churn
probability threshold.

------------------------------------------------------------------------

### 3. Customer Value Segmentation

Customers are additionally categorized according to their business
value.

Example:

``` text
Low Value
Medium Value
High Value
```

This allows churn risk to be considered together with customer value.

------------------------------------------------------------------------

### 4. Behavioral Intelligence

The platform derives and displays behavioral signals including:

-   Recharge frequency change
-   Data usage change
-   Outgoing usage change
-   Recharge amount behavior
-   Voice usage behavior
-   Other engineered customer-level behavioral features

These signals help explain why a customer may be at risk.

------------------------------------------------------------------------

### 5. Next-Best-Action Recommendation

The system generates candidate retention interventions based on the
customer's risk and behavioral profile.

Example actions include:

``` text
Personalized SMS campaign
Discounted data pack
```

Each candidate action has an associated intervention cost.

------------------------------------------------------------------------

### 6. Customer-Level Revenue

The economic engine uses customer-specific revenue rather than a
hardcoded revenue assumption.

The current implementation derives average customer revenue from:

``` text
ARPU Month 6
ARPU Month 7
ARPU Month 8
```

using:

``` text
Average Revenue = mean(ARPU_6, ARPU_7, ARPU_8)
```

This value is then passed into the economic evaluation for the selected
customer.

------------------------------------------------------------------------

### 7. Economic Retention Simulation

For every candidate intervention, the system calculates:

-   Retention probability assumption
-   Revenue at risk
-   Expected retained revenue
-   Intervention cost
-   Expected net value
-   ROI
-   Business viability

The economic engine explicitly treats intervention effectiveness values
as **scenario assumptions**, not causal estimates.

------------------------------------------------------------------------

## 💰 Economic Decision Framework

For a customer:

### Revenue at Risk

``` text
Revenue at Risk
    = Churn Probability × Average Revenue
```

### Expected Retained Revenue

``` text
Expected Retained Revenue
    = Revenue at Risk × Retention Probability Assumption
```

### Expected Net Value

``` text
Expected Net Value
    = Expected Retained Revenue − Intervention Cost
```

### ROI

For an intervention with a positive cost:

``` text
ROI
    = Expected Net Value / Intervention Cost
```

The final recommendation considers the economic value of the available
interventions rather than simply selecting the action with the highest
retention probability.

------------------------------------------------------------------------

## 🧠 Economic Decision Example

For a selected customer, the dashboard can produce results such as:

  --------------------------------------------------------------------------
  Candidate                Cost       Expected   Expected Net            ROI
  Action                              Retained          Value 
                                       Revenue                
  -------------- -------------- -------------- -------------- --------------
  Personalized              ₹10         ₹54.19         ₹44.19          4.42x
  SMS campaign                                                

  Discounted                ₹30        ₹108.38         ₹78.38          2.61x
  data pack                                                   
  --------------------------------------------------------------------------

Although the SMS campaign has the higher ROI, the discounted data pack
produces the higher **expected net value**.

Therefore, the system can recommend:

``` text
Discounted data pack
```

This demonstrates an important distinction between **ROI percentage**
and **absolute expected business value**.

------------------------------------------------------------------------

# 🖥️ Streamlit Dashboard

The project includes an interactive Streamlit frontend.

The dashboard provides:

### Portfolio Overview

-   Total customers
-   Predicted churn count
-   Average churn probability
-   Adjustable churn threshold

### Customer Intelligence

-   Customer selection
-   Churn probability
-   Risk segment
-   Value segment
-   Average revenue

### Behavioral Signals

-   Recharge frequency change
-   Data usage change
-   Outgoing usage change

### Economic Retention Decision

-   Candidate interventions
-   Intervention costs
-   Expected retained revenue
-   Expected net value
-   ROI
-   Business viability
-   Final recommended action
-   Decision explanation

### Churn Analytics

Interactive Plotly visualizations are provided to explore relationships
between customer behavior and churn risk segments.

### Customer Dataset

The dashboard also exposes the processed customer-level dataset and
relevant decision features.

------------------------------------------------------------------------

# 🏗️ Project Architecture

The major components are organized as follows:

``` text
src/
│
├── business/
│   ├── action_effectiveness.py
│   ├── action_evaluator.py
│   └── retention_roi.py
│
├── pipeline/
│   └── retention_pipeline.py
│
├── graph/
│   └── retention_graph.py
│
└── frontend/
    └── app.py
```

Supporting project directories include:

``` text
data/
tests/
test_temp/
```

------------------------------------------------------------------------

# 🔄 Core Business Flow

The economic decision layer works approximately as follows:

``` text
Customer
   │
   ├── churn_probability
   ├── avg_revenue
   ├── behavioral signals
   ├── risk_segment
   └── value_segment
          │
          ▼
   Retention Strategy
          │
          ▼
   Candidate Actions
          │
          ├── Action A
          ├── Action B
          └── ...
          │
          ▼
   ActionEvaluator
          │
          ▼
   RetentionROISimulator
          │
          ├── Revenue at Risk
          ├── Expected Retained Revenue
          ├── Expected Net Value
          └── ROI
          │
          ▼
   Economic Decision
```

------------------------------------------------------------------------

# 📁 Data

The current dashboard consumes:

``` text
data/final_customer_churn_predictions_with_strategy.csv
```

The processed dataset contains customer-level information including:

-   Customer identifier
-   Telecom usage features
-   Recharge features
-   ARPU features
-   Engineered behavioral signals
-   Churn probability
-   Risk segment
-   Value segment
-   Customer segment
-   Recommended action
-   Risk rank

The current dataset contains **6,003 customer records**.

------------------------------------------------------------------------

# 🛠️ Technology Stack

### Programming

-   Python

### Data Processing

-   Pandas
-   NumPy

### Machine Learning

-   Scikit-learn / trained ML pipeline
-   Engineered behavioral features

### Business Intelligence

-   Custom economic decision engine
-   ROI simulation
-   Customer-level revenue analysis

### Frontend

-   Streamlit
-   Plotly

### Application Architecture

-   Modular Python source structure
-   Pipeline-based processing
-   Graph-based retention orchestration

### Optional AI Layer

The project supports an optional Gemini integration controlled through
environment configuration.

For the current stable implementation, the core retention and economic
decision pipeline does **not depend on Gemini**.

------------------------------------------------------------------------

# ⚙️ Installation

## 1. Clone the repository

``` bash
git clone <repository-url>
cd <project-directory>
```

## 2. Create a virtual environment

``` bash
python -m venv venv
```

### Windows

``` bash
venv\Scripts\activate
```

### Linux / macOS

``` bash
source venv/bin/activate
```

## 3. Install dependencies

``` bash
pip install -r requirements.txt
```

------------------------------------------------------------------------

# 🔐 Environment Configuration

Create a `.env` file in the project root if environment variables are
required.

Example:

``` env
USE_GEMINI=False
```

`USE_GEMINI=False` keeps the core application independent of the
optional Gemini/LLM layer.

The economic calculations and retention decisions should remain
deterministic and should not depend on an LLM generating financial
values.

------------------------------------------------------------------------

# ▶️ Running the Application

From the project root:

``` bash
streamlit run src/frontend/app.py
```

The Streamlit application will open in the browser.

------------------------------------------------------------------------

# 👤 Using the Dashboard

### Step 1 --- Set the churn threshold

Use the sidebar slider to change the probability threshold used to
classify predicted churn.

### Step 2 --- Select a customer

Choose a customer from the customer selector.

### Step 3 --- Review customer intelligence

Inspect:

-   Churn probability
-   Risk segment
-   Value segment
-   Average revenue
-   Behavioral signals

### Step 4 --- Evaluate retention actions

Click:

``` text
Evaluate Retention Action
```

The platform evaluates all available candidate interventions.

### Step 5 --- Review the economic decision

Compare:

-   Intervention cost
-   Expected retained revenue
-   Expected net value
-   ROI
-   Business viability

The system then presents the final recommended action.

------------------------------------------------------------------------

# 📊 Design Principles

## Prediction ≠ Decision

A customer being highly likely to churn does not automatically mean that
every retention intervention is worthwhile.

The project therefore separates:

``` text
Churn Prediction
        ↓
Retention Strategy
        ↓
Economic Evaluation
```

------------------------------------------------------------------------

## Customer-Level Economics

The system avoids relying on a universal hardcoded revenue value.

Instead, customer-specific ARPU information is used to estimate the
revenue exposed to churn.

------------------------------------------------------------------------

## ROI vs Net Value

The project distinguishes between:

``` text
ROI
```

and:

``` text
Expected Net Value
```

A lower-cost action can have a higher ROI while still generating less
absolute business value.

This allows the decision layer to consider the actual expected economic
contribution of an intervention.

------------------------------------------------------------------------

## Scenario-Based Intervention Effectiveness

Retention effectiveness values are treated as:

> **scenario assumptions and not causal estimates.**

Therefore, the economic simulator should be interpreted as a
**decision-support and scenario-analysis framework**, not as proof that
a specific intervention causally prevents churn.

------------------------------------------------------------------------

# ⚠️ Limitations

The current system has several important limitations:

1.  Intervention effectiveness values are scenario assumptions rather
    than experimentally estimated causal effects.

2.  Revenue is estimated using historical ARPU information rather than a
    complete lifetime-value model.

3.  ROI represents expected economic value under the defined
    assumptions.

4.  The system does not yet perform online experimentation or A/B
    testing of retention interventions.

5.  Customer behavior and intervention response may change over time.

These limitations should be considered when interpreting economic
recommendations.

------------------------------------------------------------------------

# 🔮 Future Improvements

Potential extensions include:

-   Causal uplift modeling for intervention effectiveness
-   Treatment-effect estimation
-   A/B testing integration
-   Customer Lifetime Value (CLV) modeling
-   Budget-constrained portfolio optimization
-   Multi-period retention optimization
-   More sophisticated intervention cost models
-   Automated campaign execution
-   Explainable ML for churn predictions
-   LLM-powered natural-language decision explanations
-   Monitoring and model drift detection
-   Production deployment and API integration

------------------------------------------------------------------------

# 🎯 Project Outcome

The final system demonstrates a transition from a traditional churn
prediction workflow:

``` text
"Who is likely to churn?"
```

to a more business-oriented retention workflow:

``` text
"Who is likely to churn?"
            ↓
"Why are they at risk?"
            ↓
"What retention actions are available?"
            ↓
"How much revenue is at risk?"
            ↓
"Which action provides the best expected economic value?"
```

The resulting platform combines **machine learning, behavioral
analytics, business rules, economic simulation, and interactive decision
support** into a single customer retention intelligence workflow.

------------------------------------------------------------------------

## 📌 Status

**Project Status: Completed --- Core end-to-end retention intelligence
pipeline and Streamlit dashboard implemented and tested.**
