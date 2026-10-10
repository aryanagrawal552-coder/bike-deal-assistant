import joblib
import numpy as np
import pandas as pd

model = joblib.load("models/bike_price_model.pkl")
model_lower = joblib.load("models/bike_price_model_lower.pkl")
model_upper = joblib.load("models/bike_price_model_upper.pkl")
model_columns = joblib.load("models/model_columns.pkl")

OWNER_MAP = {
    "First Owner": 0,
    "Second Owner": 1,
    "Third Owner": 2,
    "Fourth Owner Or More": 3,
}


def build_input(listing):
    row = pd.DataFrame(np.zeros((1, len(model_columns))), columns=model_columns)
    row["kms_driven"] = listing["kms_driven"]
    row["age"] = listing["age"]
    row["power"] = listing["power"]
    row["owner_encoded"] = OWNER_MAP[listing["owner"]]

    brand_col = f"brand_{listing['brand']}"
    if brand_col in row.columns:
        row[brand_col] = 1

    city_col = f"city_{listing['city']}"
    if city_col in row.columns:
        row[city_col] = 1
    return row


def predict_range(listing):
    X = build_input(listing)
    point = float(np.expm1(model.predict(X)[0]))
    lower = float(np.expm1(model_lower.predict(X)[0]))
    upper = float(np.expm1(model_upper.predict(X)[0]))
    lower, upper = min(lower, upper), max(lower, upper)
    unsure = not (lower <= point <= upper)
    lower, upper = min(lower, point), max(upper, point)
    return point, lower, upper, unsure


def get_verdict(listed_price, lower, upper):
    if listed_price is None:
        return None
    if listed_price < lower:
        return "underpriced"
    if listed_price > upper:
        return "overpriced"
    return "fair"