import pandas as pd
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[2]

DATA_PATH = (
    BASE_DIR
    / "data"
    / "final_customer_churn_predictions_with_strategy.csv"
)


df = pd.read_csv(DATA_PATH)


def get_customer(customer_id):

    matches = df[
        df["mobile_number"].astype(str) ==
        str(customer_id)
    ]

    if matches.empty:
        return {
            "error": "Customer not found"
        }

    row = matches.iloc[0]

    return row.to_dict()