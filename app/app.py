# ============================================================
# Olist Customer Intelligence Platform
# Streamlit Dashboard
# ============================================================

import streamlit as st
import pandas as pd
import joblib


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Olist Customer Intelligence Platform",
    page_icon="📊",
    layout="wide"
)


# ============================================================
# LOAD CUSTOMER DATA AND MODEL
# ============================================================

customer_data = pd.read_csv(
    "data/processed/customer_features.csv"
)

loaded_model = joblib.load(
    "models/retention_risk_model.joblib"
)


# ============================================================
# CREATE CUSTOMER VALUE SEGMENTS
# ============================================================

customer_data["customer_value_segment"] = pd.cut(
    customer_data["total_spent"],
    bins=[
        -1,
        150,
        300,
        float("inf")
    ],
    labels=[
        "Low Value",
        "Medium Value",
        "High Value"
    ]
)


# ============================================================
# TITLE
# ============================================================

st.title("📊 Olist Customer Intelligence Platform")

st.write(
    "Customer analytics, business insights and retention-risk analysis"
)

st.divider()


# ============================================================
# EXECUTIVE OVERVIEW
# ============================================================

st.header("📊 Executive Overview")

total_customers = customer_data["customer_id"].nunique()

total_revenue = customer_data["total_spent"].sum()

high_risk_customers = (
    customer_data["retention_risk"] == 1
).sum()

average_spending = customer_data["total_spent"].mean()


col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Total Customers",
    f"{total_customers:,}"
)

col2.metric(
    "Total Revenue",
    f"₹{total_revenue:,.0f}"
)

col3.metric(
    "Higher-Risk Customers",
    f"{high_risk_customers:,}"
)

col4.metric(
    "Average Customer Spending",
    f"₹{average_spending:,.2f}"
)


# ============================================================
# DASHBOARD FILTERS
# ============================================================

st.divider()

st.header("🎛️ Dashboard Filters")

filter_col1, filter_col2, filter_col3 = st.columns(3)


# Retention Risk

with filter_col1:

    risk_filter = st.selectbox(
        "Retention Risk",
        [
            "All",
            "Lower Risk",
            "Higher Risk"
        ]
    )


# Customer Value

with filter_col2:

    value_filter = st.selectbox(
        "Customer Value",
        [
            "All",
            "Low Value",
            "Medium Value",
            "High Value"
        ]
    )


# State

with filter_col3:

    state_options = sorted(
        customer_data["customer_state"]
        .dropna()
        .unique()
        .tolist()
    )

    state_filter = st.selectbox(
        "Customer State",
        ["All"] + state_options
    )


# ============================================================
# APPLY FILTERS
# ============================================================

filtered_data = customer_data.copy()


if risk_filter == "Lower Risk":

    filtered_data = filtered_data[
        filtered_data["retention_risk"] == 0
    ]


elif risk_filter == "Higher Risk":

    filtered_data = filtered_data[
        filtered_data["retention_risk"] == 1
    ]


if value_filter != "All":

    filtered_data = filtered_data[
        filtered_data["customer_value_segment"]
        == value_filter
    ]


if state_filter != "All":

    filtered_data = filtered_data[
        filtered_data["customer_state"]
        == state_filter
    ]


# ============================================================
# FILTERED SUMMARY
# ============================================================

st.subheader("Filtered Customer Summary")

summary_col1, summary_col2, summary_col3 = st.columns(3)

summary_col1.metric(
    "Customers",
    f"{len(filtered_data):,}"
)

summary_col2.metric(
    "Revenue",
    f"₹{filtered_data['total_spent'].sum():,.0f}"
)


if len(filtered_data) > 0:

    filtered_average = (
        filtered_data["total_spent"].mean()
    )

else:

    filtered_average = 0


summary_col3.metric(
    "Average Spending",
    f"₹{filtered_average:,.2f}"
)


# ============================================================
# CUSTOMER OVERVIEW
# ============================================================

st.divider()

st.header("👥 Customer Overview")


# Customer data table

st.subheader("Customer Data")

display_columns = [
    "customer_id",
    "customer_city",
    "customer_state",
    "total_spent",
    "average_order_value",
    "average_review_score",
    "retention_risk",
    "customer_value_segment"
]

display_data = filtered_data[
    display_columns
].copy()


display_data["retention_risk"] = (
    display_data["retention_risk"]
    .map({
        0: "Lower Risk",
        1: "Higher Risk"
    })
)


st.dataframe(
    display_data.head(100),
    width="stretch"
)


# ============================================================
# RETENTION RISK DISTRIBUTION
# ============================================================

st.subheader(
    "Customer Retention Risk Distribution"
)

risk_counts = (
    filtered_data["retention_risk"]
    .map({
        0: "Lower Risk",
        1: "Higher Risk"
    })
    .value_counts()
    .reindex(
        [
            "Lower Risk",
            "Higher Risk"
        ],
        fill_value=0
    )
)

st.bar_chart(risk_counts)


# ============================================================
# CUSTOMER VALUE SEGMENTS
# ============================================================

st.subheader("Customer Value Segments")

value_counts = (
    filtered_data[
        "customer_value_segment"
    ]
    .value_counts()
    .reindex(
        [
            "Low Value",
            "Medium Value",
            "High Value"
        ],
        fill_value=0
    )
)

st.bar_chart(value_counts)


# ============================================================
# REVENUE BY CUSTOMER VALUE SEGMENT
# ============================================================

st.subheader(
    "Revenue by Customer Value Segment"
)

segment_revenue = (
    filtered_data
    .groupby(
        "customer_value_segment",
        observed=True
    )["total_spent"]
    .sum()
    .reindex(
        [
            "Low Value",
            "Medium Value",
            "High Value"
        ],
        fill_value=0
    )
)

st.bar_chart(segment_revenue)


# ============================================================
# BUSINESS ANALYTICS
# ============================================================

st.divider()

st.header("📈 Business Analytics")


# ============================================================
# LOAD PRODUCT DATA
# ============================================================

products = pd.read_csv(
    "data/raw/olist_products_dataset.csv"
)

order_items = pd.read_csv(
    "data/raw/olist_order_items_dataset.csv"
)

category_translation = pd.read_csv(
    "data/raw/product_category_name_translation.csv"
)


# ============================================================
# PRODUCT CATEGORY ANALYSIS
# ============================================================

products_with_category = products.merge(
    category_translation,
    on="product_category_name",
    how="left"
)


items_with_category = order_items.merge(
    products_with_category[
        [
            "product_id",
            "product_category_name_english"
        ]
    ],
    on="product_id",
    how="left"
)


category_revenue = (
    items_with_category
    .groupby(
        "product_category_name_english"
    )
    .agg(
        total_revenue=("price", "sum"),
        total_orders=("order_id", "nunique"),
        total_items=("order_item_id", "count")
    )
    .reset_index()
    .sort_values(
        "total_revenue",
        ascending=False
    )
)


# ============================================================
# TOP PRODUCT CATEGORIES
# ============================================================

st.subheader(
    "Top 10 Product Categories by Revenue"
)

top_categories = category_revenue.head(10)

top_categories_chart = (
    top_categories
    .set_index(
        "product_category_name_english"
    )["total_revenue"]
    .sort_values()
)

st.bar_chart(top_categories_chart)


# ============================================================
# MONTHLY REVENUE TREND
# ============================================================

st.subheader("Monthly Revenue Trend")

orders = pd.read_csv(
    "data/raw/olist_orders_dataset.csv"
)

orders["order_purchase_timestamp"] = pd.to_datetime(
    orders["order_purchase_timestamp"]
)


# Keep delivered orders

delivered_orders = orders[
    orders["order_status"] == "delivered"
]


# Connect orders with order items

monthly_data = delivered_orders[
    [
        "order_id",
        "order_purchase_timestamp"
    ]
].merge(
    order_items[
        [
            "order_id",
            "price"
        ]
    ],
    on="order_id",
    how="inner"
)


# Create month column

monthly_data["purchase_month"] = (
    monthly_data[
        "order_purchase_timestamp"
    ]
    .dt.to_period("M")
    .astype(str)
)


# Calculate monthly product revenue

monthly_revenue = (
    monthly_data
    .groupby("purchase_month")["price"]
    .sum()
)


st.line_chart(monthly_revenue)

st.caption(
    "Monthly product revenue from delivered orders."
)


# ============================================================
# MODEL EXPLAINABILITY
# ============================================================

st.divider()

st.header("🧠 Model Explainability")

st.subheader(
    "SHAP Feature Importance"
)


# Load SHAP results

shap_importance = pd.read_csv(
    "data/processed/shap_importance.csv"
)


# Sort features for visualization

shap_chart = (
    shap_importance
    .set_index("feature")["importance"]
    .sort_values()
)


st.bar_chart(shap_chart)


st.caption(
    "Higher mean absolute SHAP values indicate greater "
    "model influence on retention-risk predictions."
)


# ============================================================
# CUSTOMER ANALYSIS
# ============================================================

st.divider()

st.header("🔎 Customer Analysis")

st.subheader(
    "Customer Risk Lookup"
)


customer_options = filtered_data[
    "customer_id"
].tolist()


if len(customer_options) == 0:

    st.warning(
        "No customers match the selected filters."
    )

else:

    selected_customer = st.selectbox(
        "Select a Customer ID",
        customer_options
    )


    # Get selected customer

    selected_data = customer_data[
        customer_data["customer_id"]
        == selected_customer
    ].iloc[0]


    # --------------------------------------------------------
    # CUSTOMER METRICS
    # --------------------------------------------------------

    col1, col2, col3, col4 = st.columns(4)


    col1.metric(
        "Total Spent",
        f"₹{selected_data['total_spent']:,.2f}"
    )


    col2.metric(
        "Average Order Value",
        f"₹{selected_data['average_order_value']:,.2f}"
    )


    col3.metric(
        "Review Score",
        f"{selected_data['average_review_score']:.2f}"
    )


    col4.metric(
        "Delivery Days",
        f"{selected_data['average_delivery_days']:.1f}"
    )


    # --------------------------------------------------------
    # CUSTOMER DETAILS
    # --------------------------------------------------------

    st.subheader("Customer Details")


    detail_col1, detail_col2 = st.columns(2)


    with detail_col1:

        st.write(
            f"**Customer ID:** "
            f"{selected_data['customer_id']}"
        )

        st.write(
            f"**City:** "
            f"{selected_data['customer_city']}"
        )

        st.write(
            f"**State:** "
            f"{selected_data['customer_state']}"
        )


    with detail_col2:

        st.write(
            f"**Total Items:** "
            f"{selected_data['total_items']}"
        )

        st.write(
            f"**Value Segment:** "
            f"{selected_data['customer_value_segment']}"
        )

        st.write(
            f"**Current Risk Label:** "
            f"{'Higher Risk' if selected_data['retention_risk'] == 1 else 'Lower Risk'}"
        )


    # ========================================================
    # ML PREDICTION
    # ========================================================

    st.subheader(
        "🤖 Retention-Risk Prediction"
    )


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


    customer_input = selected_data[
        model_features
    ].to_frame().T


    prediction = loaded_model.predict(
        customer_input
    )[0]


    prediction_probability = (
        loaded_model
        .predict_proba(customer_input)[0][1]
    )


    if prediction == 1:

        st.warning(
            "⚠️ Higher Retention Risk"
        )

    else:

        st.success(
            "✅ Lower Retention Risk"
        )


    st.write(
        f"Model risk probability: "
        f"**{prediction_probability:.2%}**"
    )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "Olist Customer Intelligence Platform | "
    "Python • Pandas • Scikit-learn • SQL • Streamlit"
)