-- Olist Customer Intelligence Platform
-- Customer Analysis Queries


-- 1. Find high-value customers

SELECT
    customer_id,
    total_spent,
    average_order_value,
    average_review_score
FROM customer_features
WHERE total_spent > 500
ORDER BY total_spent DESC;


-- 2. Revenue by retention risk

SELECT
    retention_risk,
    COUNT(*) AS customer_count,
    SUM(total_spent) AS total_revenue,
    AVG(total_spent) AS average_spending
FROM customer_features
GROUP BY retention_risk
ORDER BY retention_risk;


-- 3. Customer value segments

SELECT
    CASE
        WHEN total_spent >= 300 THEN 'High Value'
        WHEN total_spent >= 150 THEN 'Medium Value'
        ELSE 'Low Value'
    END AS customer_value_segment,
    COUNT(*) AS customer_count,
    SUM(total_spent) AS total_revenue,
    AVG(total_spent) AS average_spending
FROM customer_features
GROUP BY customer_value_segment
ORDER BY total_revenue DESC;