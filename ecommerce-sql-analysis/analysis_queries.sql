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

