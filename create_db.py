import sqlite3
# step 1 create dummy data base
conn = sqlite3.connect('amazone.db')
cursor = conn.cursor()

#step 2 create tables

#tables customers , orders , products , order_items

cursor.execute("""
CREATE TABLE IF NOT EXISTS customers(
    customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    email TEXT,
    city TEXT,
    join_date TEXT
    )
""")

# Step 3: Create products table
cursor.execute("""
CREATE TABLE IF NOT EXISTS products(
    product_id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_name TEXT NOT NULL,
    category TEXT,
    price REAL,
    stock INTEGER
)
""")


# Step 4: Create orders table
cursor.execute("""
CREATE TABLE IF NOT EXISTS orders(
    order_id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id INTEGER,
    order_date TEXT,
    total_amount REAL,
    FOREIGN KEY(customer_id) REFERENCES customers(customer_id)
)
""")


# Step 5: Create order_items table
cursor.execute("""
CREATE TABLE IF NOT EXISTS order_items(
    order_item_id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id INTEGER,
    product_id INTEGER,
    quantity INTEGER,
    item_price REAL,
    FOREIGN KEY(order_id) REFERENCES orders(order_id),
    FOREIGN KEY(product_id) REFERENCES products(product_id)
)
""")

# -----------------------------
# INSERT DUMMY DATA
# -----------------------------

# Customers Data
customers_data = [
    ("Chirag Kapoor", "chirag@gmail.com", "Delhi", "2025-01-10"),
    ("Rahul Sharma", "rahul@gmail.com", "Mumbai", "2025-02-15"),
    ("Priya Verma", "priya@gmail.com", "Pune", "2025-03-05"),
    ("Aman Singh", "aman@gmail.com", "Chandigarh", "2025-03-20"),
    ("Neha Gupta", "neha@gmail.com", "Jaipur", "2025-04-01"),
    ("Karan Malhotra", "karan@gmail.com", "Bangalore", "2025-04-10"),
    ("Simran Kaur", "simran@gmail.com", "Amritsar", "2025-04-18")
]

cursor.executemany("""
INSERT INTO customers(name, email, city, join_date)
VALUES (?, ?, ?, ?)
""", customers_data)


# Products Data
products_data = [
    ("Laptop", "Electronics", 55000, 10),
    ("Smartphone", "Electronics", 25000, 20),
    ("Headphones", "Accessories", 2000, 50),
    ("Keyboard", "Accessories", 1500, 30),
    ("Mouse", "Accessories", 800, 40),
    ("Smart Watch", "Wearable", 5000, 15),
    ("Tablet", "Electronics", 18000, 12)
]

cursor.executemany("""
INSERT INTO products(product_name, category, price, stock)
VALUES (?, ?, ?, ?)
""", products_data)


# Orders Data
orders_data = [
    (1, "2025-05-01", 57000),
    (2, "2025-05-02", 25000),
    (3, "2025-05-03", 3500),
    (4, "2025-05-04", 18000),
    (5, "2025-05-05", 5800),
    (6, "2025-05-06", 55000),
    (7, "2025-05-07", 2000)
]

cursor.executemany("""
INSERT INTO orders(customer_id, order_date, total_amount)
VALUES (?, ?, ?)
""", orders_data)


# Order Items Data
order_items_data = [
    (1, 1, 1, 55000),
    (1, 3, 1, 2000),
    (2, 2, 1, 25000),
    (3, 4, 2, 3000),
    (4, 7, 1, 18000),
    (5, 6, 1, 5000),
    (5, 5, 1, 800)
]

cursor.executemany("""
INSERT INTO order_items(order_id, product_id, quantity, item_price)
VALUES (?, ?, ?, ?)
""", order_items_data)


# Save changes
conn.commit()
conn.close()
print("Dummy data inserted successfully!")