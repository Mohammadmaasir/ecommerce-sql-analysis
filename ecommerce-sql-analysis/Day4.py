import pandas as pd
import matplotlib.pyplot as plt
import os

os.makedirs('charts', exist_ok=True)

customers = pd.read_csv(r"C:\Users\MD Maasir\Downloads\archive\olist_customers_dataset.csv")
orders = pd.read_csv(r"C:\Users\MD Maasir\Downloads\archive\olist_orders_dataset.csv")
payments = pd.read_csv(r"C:\Users\MD Maasir\Downloads\archive\olist_order_payments_dataset.csv")
products = pd.read_csv(r"C:\Users\MD Maasir\Downloads\archive\olist_products_dataset.csv")
order_items = pd.read_csv(r"C:\Users\MD Maasir\Downloads\archive\olist_order_items_dataset.csv")
sellers = pd.read_csv(r"C:\Users\MD Maasir\Downloads\archive\olist_sellers_dataset.csv")
reviews = pd.read_csv(r"C:\Users\MD Maasir\Downloads\archive\olist_order_reviews_dataset.csv")
category = pd.read_csv(r"C:\Users\MD Maasir\Downloads\archive\product_category_name_translation.csv")

# QUERY 1 — Total Unique Customers
total_customers = customers['customer_unique_id'].nunique()
print(f"Q1 — Total Unique Customers: {total_customers}")

# QUERY 2 — Top 10 Cities by Customers
top_cities = customers.groupby('customer_city')['customer_unique_id']\
             .nunique().sort_values(ascending=False).head(10).reset_index()
top_cities.columns = ['City', 'Customers']
print(f"\nQ2 — Top 10 Cities:")
print(top_cities)

plt.figure(figsize=(12, 6))
plt.barh(top_cities['City'][::-1], top_cities['Customers'][::-1], color='#1D9E75')
plt.xlabel('Number of Customers', fontsize=12)
plt.title('Top 10 Cities by Customers', fontsize=16, fontweight='bold')
plt.tight_layout()
plt.savefig('charts/query2_top_cities.png')
plt.show()

# QUERY 3 — Total Revenue
total_revenue = payments['payment_value'].sum()
print(f"\nQ3 — Total Revenue: R$ {total_revenue:,.2f}")

# QUERY 4 — Payment Methods Distribution
payment_dist = payments.groupby('payment_type')['payment_value']\
               .sum().sort_values(ascending=False).reset_index()
payment_dist.columns = ['Payment Type', 'Revenue']
payment_dist = payment_dist[payment_dist['Payment Type'] != 'not_defined']
print(f"\nQ4 — Revenue by Payment Type:")
print(payment_dist)

# QUERY 5 — Monthly Revenue Trend
orders['order_purchase_timestamp'] = pd.to_datetime(orders['order_purchase_timestamp'])
orders_payments = orders.merge(payments, on='order_id', how='inner')
orders_payments['order_month'] = orders_payments['order_purchase_timestamp'].dt.to_period('M')
monthly_revenue = orders_payments.groupby('order_month')['payment_value'].sum().reset_index()
monthly_revenue.columns = ['Month', 'Revenue']
monthly_revenue = monthly_revenue.sort_values('Month')
monthly_revenue['Month'] = monthly_revenue['Month'].astype(str)
print(f"\nQ5 — Peak Month: {monthly_revenue.loc[monthly_revenue['Revenue'].idxmax(), 'Month']}")

plt.figure(figsize=(14, 6))
plt.plot(monthly_revenue['Month'], monthly_revenue['Revenue'],
         color='#1D9E75', linewidth=2, marker='o', markersize=5)
plt.xticks(rotation=45, ha='right')
plt.title('Monthly Revenue Trend (2016-2018)', fontsize=16, fontweight='bold')
plt.xlabel('Month', fontsize=12)
plt.ylabel('Revenue (R$)', fontsize=12)
plt.tight_layout()
plt.savefig('charts/query5_monthly_revenue.png')
plt.show()

# QUERY 6 — Top Product Categories
merged = order_items.merge(products, on='product_id')\
         .merge(category, on='product_category_name')

top_categories = merged.groupby('product_category_name_english')['price']\
                 .sum().sort_values(ascending=False).head(10).reset_index()
top_categories.columns = ['Category', 'Revenue']
print(f"\nQ6 — Top 10 Product Categories:")
print(top_categories)

plt.figure(figsize=(12, 6))
plt.barh(top_categories['Category'][::-1], top_categories['Revenue'][::-1], color='#1D9E75')
plt.xlabel('Revenue (R$)', fontsize=12)
plt.title('Top 10 Product Categories by Revenue', fontsize=16, fontweight='bold')
plt.tight_layout()
plt.savefig('charts/query6_top_categories.png')
plt.show()

# QUERY 7 — Average Delivery Time
orders['order_purchase_timestamp'] = pd.to_datetime(orders['order_purchase_timestamp'])
orders['order_delivered_customer_date'] = pd.to_datetime(orders['order_delivered_customer_date'])

delivered = orders.dropna(subset=['order_delivered_customer_date']).copy()
delivered['delivery_days'] = (delivered['order_delivered_customer_date'] -
                               delivered['order_purchase_timestamp']).dt.days

avg_delivery = delivered['delivery_days'].mean()
print(f"\nQ7 — Average Delivery Time: {avg_delivery:.1f} days")

plt.figure(figsize=(10, 5))
plt.hist(delivered['delivery_days'], bins=40, color='#1D9E75', edgecolor='white')
plt.axvline(avg_delivery, color='red', linestyle='--', linewidth=2,
            label=f'Avg: {avg_delivery:.1f} days')
plt.title('Delivery Time Distribution', fontsize=16, fontweight='bold')
plt.xlabel('Days', fontsize=12)
plt.ylabel('Number of Orders', fontsize=12)
plt.legend()
plt.tight_layout()
plt.savefig('charts/query7_delivery_time.png')
plt.show()

plt.figure(figsize=(7, 7))
plt.pie(payment_dist['Revenue'], labels=payment_dist['Payment Type'],
        autopct='%1.1f%%', startangle=140,
        colors=['#1D9E75', '#1a1a2e', '#f4a261', '#e76f51'])
plt.title('Revenue by Payment Method', fontsize=16, fontweight='bold')
plt.tight_layout()
plt.savefig('charts/query4_payment_methods.png')
plt.show()

# QUERY 8 — Top Sellers by Revenue
top_sellers = order_items.groupby('seller_id')['price']\
              .sum().sort_values(ascending=False).head(10).reset_index()
top_sellers.columns = ['Seller ID', 'Revenue']
top_sellers['Seller ID'] = top_sellers['Seller ID'].str[:8] + '...'
print(f"\nQ8 — Top 10 Sellers by Revenue:")
print(top_sellers)

plt.figure(figsize=(12, 6))
plt.bar(top_sellers['Seller ID'], top_sellers['Revenue'], color='#1D9E75')
plt.xticks(rotation=45, ha='right')
plt.title('Top 10 Sellers by Revenue', fontsize=16, fontweight='bold')
plt.ylabel('Revenue (R$)', fontsize=12)
plt.xlabel('Seller ID', fontsize=12)
plt.tight_layout()
plt.savefig('charts/query8_top_sellers.png')
plt.show()

# QUERY 9 — Review Score Distribution
review_dist = reviews['review_score'].value_counts().sort_index().reset_index()
review_dist.columns = ['Score', 'Count']
print(f"\nQ9 — Review Score Distribution:")
print(review_dist)

five_star_pct = (reviews['review_score'] == 5).sum() / len(reviews) * 100
print(f"5-Star Percentage: {five_star_pct:.1f}%")

plt.figure(figsize=(8, 5))
plt.bar(review_dist['Score'], review_dist['Count'],
        color=['#E53935','#FB8C00','#FDD835','#43A047','#1D9E75'])
plt.title('Review Score Distribution', fontsize=16, fontweight='bold')
plt.xlabel('Score', fontsize=12)
plt.ylabel('Number of Reviews', fontsize=12)
plt.tight_layout()
plt.savefig('charts/query9_review_scores.png')
plt.show()

# QUERY 10 — On-Time Delivery Rate
delivered_orders = orders[orders['order_status'] == 'delivered'].copy()
delivered_orders['order_estimated_delivery_date'] = pd.to_datetime(delivered_orders['order_estimated_delivery_date'])
delivered_orders['order_delivered_customer_date'] = pd.to_datetime(delivered_orders['order_delivered_customer_date'])
delivered_orders = delivered_orders.dropna(subset=['order_delivered_customer_date','order_estimated_delivery_date'])

delivered_orders['on_time'] = delivered_orders['order_delivered_customer_date'] <= \
                               delivered_orders['order_estimated_delivery_date']

on_time_pct = delivered_orders['on_time'].sum() / len(delivered_orders) * 100
late_pct = 100 - on_time_pct
print(f"\nQ10 — On-Time Delivery Rate: {on_time_pct:.1f}%")

plt.figure(figsize=(6, 6))
plt.pie([on_time_pct, late_pct], labels=['On Time', 'Late'],
        autopct='%1.1f%%', colors=['#1D9E75','#E53935'], startangle=90)
plt.title('On-Time vs Late Delivery Rate', fontsize=16, fontweight='bold')
plt.tight_layout()
plt.savefig('charts/query10_ontime_delivery.png')
plt.show()