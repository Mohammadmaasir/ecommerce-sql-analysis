import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, classification_report

# Load datasets
orders = pd.read_csv(r"C:\Users\MD Maasir\Downloads\archive\olist_orders_dataset.csv")
payments = pd.read_csv(r"C:\Users\MD Maasir\Downloads\archive\olist_order_payments_dataset.csv")
order_items = pd.read_csv(r"C:\Users\MD Maasir\Downloads\archive\olist_order_items_dataset.csv")

print("Datasets loaded successfully")
print(f"Orders shape: {orders.shape}")
print(f"Payments shape: {payments.shape}")
print(f"Order items shape: {order_items.shape}")

# Convert date columns to datetime
orders['order_purchase_timestamp'] = pd.to_datetime(orders['order_purchase_timestamp'])
orders['order_delivered_customer_date'] = pd.to_datetime(orders['order_delivered_customer_date'])
orders['order_estimated_delivery_date'] = pd.to_datetime(orders['order_estimated_delivery_date'])

# Keep only delivered orders
orders_delivered = orders[orders['order_status'] == 'delivered'].copy()

# Drop rows with missing dates
orders_delivered = orders_delivered.dropna(subset=[
    'order_delivered_customer_date',
    'order_estimated_delivery_date',
    'order_purchase_timestamp'
])

# Create target variable — 1 = Late, 0 = On Time
orders_delivered['is_late'] = (
    orders_delivered['order_delivered_customer_date'] >
    orders_delivered['order_estimated_delivery_date']
).astype(int)

# Create feature — estimated delivery days
orders_delivered['estimated_days'] = (
    orders_delivered['order_estimated_delivery_date'] -
    orders_delivered['order_purchase_timestamp']
).dt.days

# Create feature — actual delivery days
orders_delivered['actual_days'] = (
    orders_delivered['order_delivered_customer_date'] -
    orders_delivered['order_purchase_timestamp']
).dt.days

print(f"\nDelivered orders: {orders_delivered.shape[0]}")
print(f"\nLate vs On Time:")
print(orders_delivered['is_late'].value_counts())

# Merge payments — get payment value per order
payment_agg = payments.groupby('order_id')['payment_value'].sum().reset_index()
payment_agg.columns = ['order_id', 'payment_value']

# Merge order items — get freight value and item count
items_agg = order_items.groupby('order_id').agg(
    freight_value=('freight_value', 'sum'),
    item_count=('order_item_id', 'count'),
    avg_price=('price', 'mean')
).reset_index()

# Merge everything together
df = orders_delivered[['order_id', 'estimated_days', 'actual_days', 'is_late']]
df = df.merge(payment_agg, on='order_id', how='left')
df = df.merge(items_agg, on='order_id', how='left')

# Drop any remaining nulls
df = df.dropna()

print(f"\nFinal dataset shape: {df.shape}")
print(f"\nFeatures:")
print(df.head())

# Define features and target
X = df[['estimated_days', 'payment_value', 'freight_value', 'item_count', 'avg_price']]
y = df['is_late']

# Split data — 80% training, 20% testing
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

print(f"Training samples: {X_train.shape[0]}")
print(f"Testing samples: {X_test.shape[0]}")

# Model 1 — Logistic Regression
lr_model = LogisticRegression(max_iter=1000)
lr_model.fit(X_train, y_train)
lr_predictions = lr_model.predict(X_test)
lr_accuracy = accuracy_score(y_test, lr_predictions)
print(f"\nLogistic Regression Accuracy: {lr_accuracy*100:.2f}%")

# Model 2 — Decision Tree
dt_model = DecisionTreeClassifier(max_depth=5, random_state=42)
dt_model.fit(X_train, y_train)
dt_predictions = dt_model.predict(X_test)
dt_accuracy = accuracy_score(y_test, dt_predictions)
print(f"Decision Tree Accuracy: {dt_accuracy*100:.2f}%")

# Detailed report
print(f"\nLogistic Regression Report:")
print(classification_report(y_test, lr_predictions, target_names=['On Time', 'Late']))

print(f"\nDecision Tree Report:")
print(classification_report(y_test, dt_predictions, target_names=['On Time', 'Late']))

from sklearn.utils import resample

# Separate majority and minority classes
df_ontime = df[df['is_late'] == 0]
df_late = df[df['is_late'] == 1]

# Upsample late orders to match on-time orders
df_late_upsampled = resample(df_late,
    replace=True,
    n_samples=len(df_ontime),
    random_state=42
)

# Combine balanced dataset
df_balanced = pd.concat([df_ontime, df_late_upsampled])

print(f"\nBalanced dataset:")
print(df_balanced['is_late'].value_counts())

# Redefine features and target
X = df_balanced[['estimated_days', 'payment_value', 'freight_value', 'item_count', 'avg_price']]
y = df_balanced['is_late']

# Split again
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Retrain both models
lr_model = LogisticRegression(max_iter=1000)
lr_model.fit(X_train, y_train)
lr_predictions = lr_model.predict(X_test)
lr_accuracy = accuracy_score(y_test, lr_predictions)
print(f"\nLogistic Regression Accuracy: {lr_accuracy*100:.2f}%")

dt_model = DecisionTreeClassifier(max_depth=5, random_state=42)
dt_model.fit(X_train, y_train)
dt_predictions = dt_model.predict(X_test)
dt_accuracy = accuracy_score(y_test, dt_predictions)
print(f"Decision Tree Accuracy: {dt_accuracy*100:.2f}%")

print(f"\nLogistic Regression Report:")
print(classification_report(y_test, lr_predictions, target_names=['On Time', 'Late']))

print(f"\nDecision Tree Report:")
print(classification_report(y_test, dt_predictions, target_names=['On Time', 'Late']))

# Add purchase month and day of week as features
df_balanced['purchase_month'] = pd.to_datetime(
    df_balanced['order_id'].map(
        orders_delivered.set_index('order_id')['order_purchase_timestamp']
    )
).dt.month

df_balanced['purchase_dayofweek'] = pd.to_datetime(
    df_balanced['order_id'].map(
        orders_delivered.set_index('order_id')['order_purchase_timestamp']
    )
).dt.dayofweek

# Redefine features with new columns
X = df_balanced[[
    'estimated_days', 'payment_value', 'freight_value',
    'item_count', 'avg_price', 'purchase_month', 'purchase_dayofweek'
]]
y = df_balanced['is_late']

# Split again
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Retrain Decision Tree only — it was better
dt_model = DecisionTreeClassifier(max_depth=7, random_state=42)
dt_model.fit(X_train, y_train)
dt_predictions = dt_model.predict(X_test)
dt_accuracy = accuracy_score(y_test, dt_predictions)

print(f"Improved Decision Tree Accuracy: {dt_accuracy*100:.2f}%")
print(classification_report(y_test, dt_predictions, target_names=['On Time', 'Late']))

import matplotlib.pyplot as plt

# Feature importance
feature_names = ['estimated_days', 'payment_value', 'freight_value',
                 'item_count', 'avg_price', 'purchase_month', 'purchase_dayofweek']

importances = dt_model.feature_importances_
feature_importance_df = pd.DataFrame({
    'Feature': feature_names,
    'Importance': importances
}).sort_values('Importance', ascending=False)

print("\nFeature Importance:")
print(feature_importance_df)

plt.figure(figsize=(10, 6))
plt.barh(feature_importance_df['Feature'][::-1],
         feature_importance_df['Importance'][::-1],
         color='#1D9E75')
plt.title('Feature Importance - Late Delivery Predictor', fontsize=16, fontweight='bold')
plt.xlabel('Importance Score', fontsize=12)
plt.tight_layout()
plt.savefig('charts/feature_importance.png')
plt.show()