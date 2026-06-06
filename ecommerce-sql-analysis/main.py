import pandas as pd
import numpy as np
customers = pd.read_csv(r"C:\Users\MD Maasir\Downloads\archive\olist_customers_dataset.csv")
print(customers.shape)
print(customers.head())
print(customers.tail())
print(customers.head(10))
print(customers.columns)
print(customers.dtypes)
print(customers.isnull().sum())
print(customers.describe())

# ── DAY 2 ──────────────────────────────────────────────────────────────────

orders = pd.read_csv(r"C:\Users\MD Maasir\Downloads\archive\olist_orders_dataset.csv")
#filter: only delivered orders
delivered_orders = orders[orders['order_status'] == 'delivered']
print("delivered orders:", delivered_orders.shape)
print("all orders:", orders.shape)

payments = pd.read_csv(r"C:\Users\MD Maasir\Downloads\archive\olist_order_payments_dataset.csv")
#filter: orders with high payment value
high_value = payments[payments['payment_value']> 1000]
print('high value orders (above R$ 1000):', high_value.shape)

#filtering by two things at once
delivered_high_value = orders.merge(payments, on = "order_id")
delivered_high_value = delivered_high_value[
    (delivered_high_value['order_status']=='delivered')&
    (delivered_high_value['payment_value']>1000)
]
print("delivered + high value:", delivered_high_value.shape)

#GroupBy: count orders per status
order_status_counts = orders.groupby("order_status")['order_id'].count().reset_index()
order_status_counts.columns=['order_status','total_orders']
order_status_counts= order_status_counts.sort_values('total_orders',  ascending=False)
print("\n-- ORDERS BY STATUS --")
print(order_status_counts)

# GroupBy: total revenue by payment type
revenue_by_payment = payments.groupby ('payment_type')['payment_value'].sum().reset_index()
revenue_by_payment.columns = ['payment_type', 'total_revenue']
revenue_by_payment['total_revenue']= revenue_by_payment['total_revenue'].round(2)
revenue_by_payment = revenue_by_payment.sort_values('total_revenue', ascending = False)
print('\n-- REVENUE BY PAYMENT TYPE --')
print(revenue_by_payment)

# Merge: join orders with customers
orders_customers = orders.merge(customers, on='customer_id', how='inner')
print("\n--- ORDERS + CUSTOMERS ---")
print(orders_customers.shape)
print(orders_customers.head())

# ── DAY 3 ──────────────────────────────────────────────────────────────────

# Re-running group by results for charts
order_status_counts = orders.groupby('order_status')['order_id'].count().reset_index()
order_status_counts.columns = ['order_status', 'total_orders']
order_status_counts = order_status_counts.sort_values('total_orders', ascending=False)

# Bar chart: orders by status
import matplotlib.pyplot as plt
plt.figure(figsize=(10, 6))
plt.bar(order_status_counts['order_status'], order_status_counts['total_orders'], color='#1D9E75')
plt.title('Orders by Status', fontsize=16, fontweight='bold')
plt.xlabel('Order Status', fontsize=12)
plt.ylabel('Total Orders', fontsize=12)
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Pie chart: revenue by payment type
revenue_by_payment = payments.groupby('payment_type')['payment_value'].sum().reset_index()
revenue_by_payment.columns = ['payment_type', 'total_revenue']
revenue_by_payment = revenue_by_payment[revenue_by_payment['payment_type'] != 'not_defined']

plt.figure(figsize=(9, 9))
plt.pie(
    revenue_by_payment['total_revenue'],
    labels=revenue_by_payment['payment_type'],
    autopct='%1.1f%%',
    colors=['#1D9E75', '#1a1a2e', '#f4a261', '#e76f51'],
    startangle=90,
    explode=[0, 0.1, 0.2, 0.2],  # pull smaller slices out
    pctdistance=0.75,              # move percentage labels inward
    textprops={'fontsize': 12}
)
plt.title('Revenue by Payment Type', fontsize=16, fontweight='bold', pad=20)
plt.legend(
    revenue_by_payment['payment_type'],
    title="Payment Type",
    loc="lower right",
    fontsize=11
)
plt.tight_layout()
plt.show()

# Line chart: monthly revenue trend
orders['order_purchase_timestamp'] = pd.to_datetime(orders['order_purchase_timestamp'])
orders_payments = orders.merge(payments, on='order_id', how='inner')
orders_payments['order_month'] = orders_payments['order_purchase_timestamp'].dt.to_period('M')
monthly_revenue = orders_payments.groupby('order_month')['payment_value'].sum().reset_index()
monthly_revenue.columns = ['order_month', 'monthly_revenue']
monthly_revenue = monthly_revenue.sort_values('order_month')
monthly_revenue['order_month'] = monthly_revenue['order_month'].astype(str)

plt.figure(figsize=(12, 6))
plt.plot(monthly_revenue['order_month'], monthly_revenue['monthly_revenue'],
         color='#1D9E75', linewidth=2, marker='o', markersize=5)
plt.title('Monthly Revenue Trend (2016-2018)', fontsize=16, fontweight='bold')
plt.xlabel('Month', fontsize=12)
plt.ylabel('Revenue (R$)', fontsize=12)
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
