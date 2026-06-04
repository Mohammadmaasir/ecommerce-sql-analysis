use ecommerce_analysis;
show tables;
select count(*) as total_customers from customers;

-- ================================================
-- QUERY: Top 10 Cities by Number of Customers
-- PURPOSE: Find which cities have the most customers
-- TABLE USED: customers
-- ================================================

SELECT customer_city,        -- the city name
       COUNT(*) AS total_customers  -- count of customers in that city
FROM customers               -- from the customers table
GROUP BY customer_city       -- group rows by each unique city
ORDER BY total_customers DESC -- sort by highest count first
LIMIT 10;                    -- show only top 10 cities

-- ================================================
-- QUERY: Total Revenue from All Orders
-- PURPOSE: Find how much total money was made
-- TABLE USED: payments
-- ================================================

SELECT ROUND(SUM(payment_value), 2) AS total_revenue -- sum all payments, round to 2 decimals
FROM payments;                                        -- from the payments table

describe payments;

-- popular payment types

select payment_type, count(payment_type) as payment_method
from payments
group by payment_type
order by payment_method desc;

-- Monthly revenue trend
-- Join orders (for date) with payments (for revenue amount)
-- Group results by year-month and sort chronologically

SELECT
    DATE_FORMAT(o.order_purchase_timestamp, '%Y-%m') AS order_month,  -- extract year-month
    ROUND(SUM(p.payment_value), 2)                   AS monthly_revenue
FROM orders   AS o                          -- main table: has the timestamps
JOIN payments AS p                          -- joined table: has the payment amounts
    ON o.order_id = p.order_id              -- link condition: same order_id in both tables
WHERE o.order_purchase_timestamp IS NOT NULL
GROUP BY order_month                        -- one row per month
ORDER BY order_month ASC;                   -- oldest to newest

-- Top 10 selling product categories by total revenue
-- Joins order_items → products → category_translation for English category names

SELECT
    ct.product_category_name_english  AS category,
    COUNT(oi.order_id)                AS total_orders,
    ROUND(SUM(oi.price), 2)           AS total_revenue
FROM order_items          AS oi
JOIN products             AS p   ON oi.product_id            = p.product_id
JOIN category_translation AS ct  ON p.product_category_name  = ct.product_category_name
GROUP BY category
ORDER BY total_revenue DESC
LIMIT 10;