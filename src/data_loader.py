# ============================================
# Olist Customer Intelligence Platform
# Data Loader
# ============================================

import pandas as pd


def load_customer_features():
    """
    Load the processed customer feature dataset.

    Returns:
        pandas.DataFrame: Customer feature data
    """

    # Location of the processed dataset
    file_path = "data/processed/customer_features.csv"

    # Read the CSV file
    customer_features = pd.read_csv(file_path)

    return customer_features


if __name__ == "__main__":
    # Load the dataset
    data = load_customer_features()

    # Display basic information
    print("Customer features loaded successfully!")
    print("Rows:", data.shape[0])
    print("Columns:", data.shape[1])

    print("\nFirst 5 rows:")
    print(data.head())