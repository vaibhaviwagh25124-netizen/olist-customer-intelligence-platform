# Olist Customer Intelligence Platform

An end-to-end customer analytics and retention-risk platform built using Python, Pandas, Scikit-learn, SQL, SHAP, and Streamlit.

## Project Overview

The Olist Customer Intelligence Platform analyzes customer purchasing behavior from the Brazilian E-Commerce Public Dataset and converts the data into actionable customer insights.

The project combines:

- Customer segmentation using RFM-style analysis
- Customer value analysis
- Review and delivery analysis
- SQL-based business analysis
- Machine learning for recency-based retention-risk classification
- SHAP-based model explainability
- Interactive Streamlit dashboard

The goal is to demonstrate an end-to-end Data Science workflow, from raw e-commerce data to analysis, machine learning, explainability, and business visualization.

## Business Problem

E-commerce businesses need to understand their customers in order to:

- Identify valuable customer groups
- Understand customer purchasing behavior
- Identify customers showing higher retention risk
- Analyze the relationship between delivery experience and customer reviews
- Understand revenue contribution across products and customer segments
- Support data-driven customer retention decisions

This project addresses these questions using the Olist e-commerce dataset.

## Objectives

1. Explore and clean e-commerce transaction data.
2. Build customer-level analytical features.
3. Segment customers based on recency and spending behavior.
4. Analyze customer reviews and delivery performance.
5. Perform business analysis using SQL.
6. Build a machine learning model for retention-risk classification.
7. Explain model predictions using SHAP.
8. Build an interactive dashboard using Streamlit.

## Dataset

This project uses the **Brazilian E-Commerce Public Dataset by Olist**, which contains approximately 100,000 orders from a Brazilian e-commerce marketplace.

The dataset includes information about:

- Customers
- Orders
- Order items
- Payments
- Reviews
- Products
- Sellers
- Geolocation
- Product categories

Dataset source:

https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce

## Technologies Used

- Python
- Pandas
- NumPy
- Scikit-learn
- XGBoost
- SHAP
- Matplotlib
- SQL / SQLite
- Streamlit
- Joblib
- Jupyter Notebook

## Project Workflow

```text
Raw Olist Dataset
       |
       v
Data Loading & Exploration
       |
       v
Data Cleaning & Merging
       |
       v
Order-Level Analysis
       |
       v
Customer-Level Feature Engineering
       |
       v
RFM-Style Customer Segmentation
       |
       v
Customer Value Analysis
       |
       v
Review & Delivery Analysis
       |
       v
Retention-Risk Classification
       |
       v
Random Forest Model
       |
       v
SHAP Explainability
       |
       v
SQL Business Analysis
       |
       v
Streamlit Dashboard
```

## Customer Analysis

Customer-level features were created from order, item, review, and delivery data.

Key features include:

- Total orders
- Total items
- Total spending
- Average order value
- Average review score
- Average delivery time
- Average delivery delay
- Review availability
- Delivery information availability
- Recency

## Customer Segmentation

An RFM-style approach was used to understand customer behavior.

Because the Olist dataset contains essentially one order per customer, traditional frequency-based repeat-purchase analysis is not meaningful for this dataset.

Therefore, the segmentation focuses primarily on:

- Recency
- Monetary value

Customer groups identified include:

- High Value - Recent
- Regular
- High Value - Inactive
- Low Value - Inactive
- Recent - Low Value

The analysis helps identify differences in customer value and recency across segments.

## Retention-Risk Model

A Random Forest classifier was developed to classify customers into two groups:

- Lower retention risk
- Higher retention risk

The target variable is based on a **recency threshold**, where customers at or above the 75th percentile of recency are classified as higher retention risk.

### Model Features

The model uses:

- Total orders
- Total items
- Total spending
- Average order value
- Average review score
- Average delivery days
- Average delivery delay
- Has review
- Has delivery

Customer ID, location fields, and recency itself were excluded from the model predictors.

## Model Performance

The Random Forest model achieved the following results on the test dataset:

| Metric | Score |
|---|---:|
| Accuracy | 0.7323 |
| Precision | 0.4620 |
| Recall | 0.4208 |
| F1 Score | 0.4404 |
| ROC-AUC | 0.7068 |

A Logistic Regression model was also evaluated as a baseline.

The Random Forest model provided better retention-risk detection than the baseline Logistic Regression model, particularly in recall and F1 score.

## Model Explainability

SHAP (SHapley Additive exPlanations) was used to understand which features had greater influence on the Random Forest model's retention-risk predictions.

The analysis showed that delivery-related features and customer spending features had relatively high model importance.

SHAP values describe the influence of features on model predictions; they should not be interpreted as proof that a feature directly causes retention or churn.

## Review and Delivery Analysis

The project also examines the relationship between delivery experience and customer review scores.

Average delivery time differed across review-score groups, with higher review scores generally associated with shorter delivery times in this dataset.

This is a descriptive association and does not establish a causal relationship.

## SQL Analysis

SQLite was used for business-oriented customer analysis.

Example analyses include:

- Identifying high-spending customers
- Comparing higher-risk and lower-risk customer groups
- Calculating revenue by customer-value segment
- Comparing average customer spending

SQL queries are available in:

```text
sql/customer_analysis.sql
```

## Streamlit Dashboard

An interactive Streamlit dashboard was developed to make the analysis easier to explore.

### Executive Overview

- Total customers
- Total revenue
- Higher-risk customers
- Average customer spending

### Filters

- Retention risk
- Customer value segment
- Customer state

### Customer Analytics

- Customer-level data
- Retention-risk distribution
- Customer value segments
- Revenue by customer segment

### Business Analytics

- Top product categories by revenue
- Monthly product revenue

### Model Explainability

- SHAP feature importance

### Customer Analysis

Users can select a customer and view:

- Total spending
- Average order value
- Review score
- Delivery days
- Retention-risk prediction
- Prediction probability

## Project Structure

```text
Olist Customer Intelligence Platform
|
|-- app/
|   |-- app.py
|
|-- data/
|   |-- raw/
|   |-- processed/
|
|-- models/
|
|-- notebooks/
|   |-- 01_data_exploration.ipynb
|
|-- reports/
|
|-- sql/
|   |-- customer_analysis.sql
|
|-- src/
|   |-- data_loader.py
|   |-- model_predictor.py
|
|-- .gitignore
|-- README.md
|-- requirements.txt
```

## How to Run the Project

### 1. Clone the repository

```bash
git clone <repository-url>
cd "Olist Customer Intelligence Platform"
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

### 3. Activate the virtual environment

Windows:

```bash
venv\Scripts\activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Prepare the dataset

Download the Olist dataset from Kaggle and place the CSV files inside:

```text
data/raw/
```

The raw and processed data files are excluded from Git using `.gitignore`.

### 6. Run the Streamlit dashboard

```bash
streamlit run app/app.py
```

The dashboard will open in your browser.

## Important Project Limitation

The Olist dataset contains essentially one order per customer, which limits the ability to measure true repeat purchasing and future churn.

Therefore, the machine learning target in this project is a **recency-based retention-risk proxy**, rather than a true future churn label.

The model should therefore be interpreted as identifying customers with higher recency-based retention risk within this dataset, not as predicting whether a customer will definitely churn in the future.

Similarly, the project focuses on historical customer value analysis rather than claiming a fully validated future Customer Lifetime Value (CLV) prediction.

## Key Learning Outcomes

This project demonstrates practical experience with:

- Data cleaning and preprocessing
- Pandas-based data analysis
- Feature engineering
- Customer segmentation
- Exploratory data analysis
- SQL analytics
- Machine learning classification
- Model evaluation
- SHAP explainability
- Model persistence using Joblib
- Streamlit dashboard development
- End-to-end project organization

## Author

**Vaibhavi Wagh**

Final-year B.Tech student in Artificial Intelligence and Data Science.

---

**Project:** Olist Customer Intelligence Platform

**Focus:** Customer Analytics | Retention Risk | Machine Learning | Explainable AI | Business Intelligence