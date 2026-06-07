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
