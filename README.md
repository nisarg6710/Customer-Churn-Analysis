## Customer-segmentation-and-retention-analysis


you can use the dataset from the following site:

https://www.kaggle.com/datasets/shivam131019/telecom-churn-dataset




## Executive Summary

### The Problem
Customer churn is a major challenge in the telecom industry, particularly among **high-value customers (HVCs)** who contribute a significant share of total revenue. Losing these customers leads to significant revenue leakage, and acquiring new customers typically costs **5–10 times more** than retaining existing ones. In this project, we analyze multi-month customer behavior to identify early warning signals that indicate when high-value customers are likely to leave the network.

### The Solution
To address this problem, we built an **end-to-end churn prediction pipeline** that analyzes customer behavior across several dimensions such as recharge patterns, call usage, and data consumption. Using feature engineering techniques inspired by **RFM (Recency, Frequency, Monetary) analysis** and behavioral usage trends, the model detects changes during the **"Action Phase"**—the period when customers begin reducing engagement before actually churning. Machine learning models were trained to identify these patterns, and **SMOTE was used to address class imbalance** to improve churn detection performance.

### The Result
The final model achieved approximately **85% Recall for the churn class**, meaning it successfully identifies the majority of customers who are likely to leave. By ranking customers based on churn probability, the company can focus retention efforts on the **top 10–20% highest-risk users**, who represent the largest share of potential revenue loss. This targeted strategy enables telecom companies to **prioritize retention campaigns, reduce revenue leakage, and allocate marketing resources more efficiently**.