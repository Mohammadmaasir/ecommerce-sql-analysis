# E-Commerce SQL Analysis

Exploratory data analysis of the Brazilian E-Commerce dataset using MySQL.  
The dataset contains 100,000+ orders from 2016–2018 across 9 relational tables.

---

## Objectives

- Practice real-world SQL on a large relational dataset
- Uncover business insights across customers, revenue, products, sellers, and logistics
- Build a foundation for future machine learning work on delivery satisfaction prediction

---

## Dataset

**Source:** [Brazilian E-Commerce Public Dataset by Olist](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce) — Kaggle  
**Tables:** customers, orders, order_items, payments, reviews, products, sellers, geolocation, category_translation  
**Size:** 99,441 customers, 100,000+ orders, 2016–2018

---

## Key Findings

| # | Analysis | Finding |
|---|----------|---------|
| 1 | Total customers | 99,441 unique customers |
| 2 | Top city by customers | São Paulo — 15,540 customers |
| 3 | Total revenue | R$ 16,008,872.12 |
| 4 | Most used payment method | Credit card — 76,795 orders (76.8%) |
| 5 | Peak revenue month | November 2017 — R$ 1,194,882 (Black Friday spike) |
| 6 | Top product category | Health & beauty — R$ 1,258,681 |
| 7 | Average delivery time | 12.5 days |
| 8 | Top seller revenue | R$ 507,166 (nearly double #2) |
| 9 | Review score | 57.8% five-star, 77% positive overall |
| 10 | On-time delivery rate | 91.9% delivered on or before estimated date |

---

## Business Insights

- **High-value vs high-volume:** Health & beauty leads in revenue despite fewer orders than bed & bath — product price matters more than order count.
- **Black Friday effect:** November 2017 shows a clear revenue spike, confirming seasonal demand patterns in Brazilian e-commerce.
- **Delivery and satisfaction link:** 8.1% of orders were delivered late — likely the primary driver of 1-star reviews (11.5% of all reviews).
- **Seller concentration:** The top seller generated nearly double the revenue of #2, indicating uneven seller performance distribution.

---

## Tools Used

- MySQL 8.0
- SQL (JOINs, GROUP BY, DATEDIFF, DATE_FORMAT, CASE WHEN, Window Functions)

---

## Files

- `analysis_queries.sql` — all 10 SQL queries with inline comments

---

## Author

Mohammad Maasir  
BTech Computer Science — All Saints' College of Technology, Bhopal  
[GitHub](https://github.com/Mohammadmaasir)
