# ============================================
# Olist Customer Intelligence Platform
# Model Predictor
# ============================================

import joblib
import pandas as pd


def load_model():
    """
    Load the trained Random Forest model.

    Returns:
        Trained Random Forest model
    """

    model_path = "models/retention_risk_model.joblib"

    model = joblib.load(model_path)

    return model


def predict_retention_risk(customer_data):
    """
    Predict retention risk for customer data.

    Args:
        customer_data: pandas DataFrame containing
                       the required model features.

    Returns:
        Prediction values
    """

    model = load_model()

    predictions = model.predict(customer_data)

    return predictions


if __name__ == "__main__":

    # Load the processed customer dataset
    customer_data = pd.read_csv(
        "data/processed/customer_features.csv"
    )

    # Select only the features used by the ML model
    model_features = [
        "total_orders",
        "total_items",
        "total_spent",
        "average_order_value",
        "average_review_score",
        "average_delivery_days",
        "average_delivery_delay",
        "has_review",
        "has_delivery"
    ]

    X = customer_data[model_features]

    # Make predictions
    predictions = predict_retention_risk(X)

    print("Model loaded successfully!")
    print("Predictions generated successfully!")

    print("\nFirst 10 predictions:")
    print(predictions[:10])