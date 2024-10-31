## diff sql and python pandas ，show me some examples

# Sample data creation
import pandas as pd
import sqlite3
import numpy as np

# Create sample DataFrame
df = pd.DataFrame({
    'customer_id': [1, 2, 3, 4, 5],
    'name': ['John', 'Emma', 'Alex', 'Sarah', 'Mike'],
    'age': [25, 30, 35, 28, 42],
    'city': ['NYC', 'LA', 'Chicago', 'NYC', 'LA'],
    'purchase_amount': [100, 200, 150, 300, 250]
})

# Create orders DataFrame
orders = pd.DataFrame({
    'order_id': [1, 2, 3, 4, 5, 6],
    'customer_id': [1, 2, 1, 3, 4, 2],
    'amount': [100, 200, 150, 300, 250, 175]
})

# 1. Basic Selection
# SQL:
"""
SELECT name, age 
FROM customers 
WHERE age > 30;
"""
# Pandas:
df_filtered = df[df['age'] > 30][['name', 'age']]

# 2. Aggregation
# SQL:
"""
SELECT city, 
       COUNT(*) as customer_count,
       AVG(purchase_amount) as avg_purchase
FROM customers
GROUP BY city;
"""
# Pandas:
city_stats = df.groupby('city').agg({
    'customer_id': 'count',
    'purchase_amount': 'mean'
}).rename(columns={'customer_id': 'customer_count', 'purchase_amount': 'avg_purchase'})

# 3. Joining Tables
# SQL:
"""
SELECT c.name, SUM(o.amount) as total_purchases
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.name;
"""
# Pandas:
customer_purchases = df.merge(
    orders, 
    on='customer_id'
).groupby(['customer_id', 'name'])['amount'].sum().reset_index()

# 4. Window Functions
# SQL:
"""
SELECT name,
       purchase_amount,
       AVG(purchase_amount) OVER (PARTITION BY city) as city_avg
FROM customers;
"""
# Pandas:
df['city_avg'] = df.groupby('city')['purchase_amount'].transform('mean')

# 5. Conditional Updates
# SQL:
"""
UPDATE customers
SET purchase_amount = purchase_amount * 1.1
WHERE city = 'NYC';
"""
# Pandas:
df.loc[df['city'] == 'NYC', 'purchase_amount'] *= 1.1

# 6. Complex Filtering
# SQL:
"""
SELECT *
FROM customers
WHERE city IN ('NYC', 'LA')
AND purchase_amount > (
    SELECT AVG(purchase_amount) 
    FROM customers
);
"""
# Pandas:
avg_purchase = df['purchase_amount'].mean()
filtered_df = df[
    (df['city'].isin(['NYC', 'LA'])) & 
    (df['purchase_amount'] > avg_purchase)
]

