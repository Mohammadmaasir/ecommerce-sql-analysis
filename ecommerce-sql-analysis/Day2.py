import pandas as pd

customers = pd.read_csv(r"C:\Users\MD Maasir\Downloads\archive\olist_customers_dataset.csv")
orders = pd.read_csv(r"C:\Users\MD Maasir\Downloads\archive\olist_orders_dataset.csv")
payments = pd.read_csv(r"C:\Users\MD Maasir\Downloads\archive\olist_order_payments_dataset.csv")

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
