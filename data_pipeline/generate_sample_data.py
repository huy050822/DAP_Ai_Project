from faker import Faker
from datetime import datetime, timedelta
import random
from pymongo import MongoClient
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# MongoDB connection
MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
client = MongoClient(MONGODB_URI)
db = client.ecommerce

# Initialize Faker
fake = Faker()

product_names = [
    "Laptop", "Smartphone", "Tablet", "Headphones", "Smart Watch", 
    "Camera", "Speaker", "Mouse", "Keyboard", "Monitor",
    "Printer", "Scanner", "External HDD", "USB Drive", "Router",
    "Gaming Console", "Microphone", "Webcam", "Graphics Card", "RAM"
]

products = [
    {
        "product_id": f"P{i}",
        "name": name,
        "price": round(random.uniform(10.0, 1000.0), 2)
    }
    for i, name in enumerate(product_names, 1)
]

# Create sample customers
customers = [
    {
        "customer_id": f"C{i}",
        "name": fake.name(),
        "location": fake.city(),
        "email": fake.email(),
        "phone": fake.phone_number()
    }
    for i in range(1, 101)  # Increased to 100 customers
]

# Clear existing data
db.products.delete_many({})
db.customers.delete_many({})
db.orders.delete_many({})

# Create sample orders
orders = []
for _ in range(1000):  # Increased to 1000 orders
    product = random.choice(products)
    customer = random.choice(customers)
    order_date = fake.date_time_between(start_date='-30d', end_date='now')
    
    order = {
        "order_id": fake.unique.random_number(digits=8),
        "Product_ID": product["product_id"],
        "Name_Product": product["name"],
        "Product_Price": product["price"],
        "Quantity_Product": random.randint(1, 10),
        "Invoice_Date": order_date,
        "Customer_ID": customer["customer_id"],
        "Name_Customer": customer["name"],
        "Location_Customer": customer["location"],
        "Information_Customer": {
            "email": customer["email"],
            "phone": customer["phone"]
        }
    }
    orders.append(order)

# Insert data into MongoDB
try:
    db.products.insert_many(products)
    print("Products inserted successfully")
    
    db.customers.insert_many(customers)
    print("Customers inserted successfully")
    
    db.orders.insert_many(orders)
    print("Orders inserted successfully")
    
except Exception as e:
    print(f"Error: {str(e)}")

print("Sample data generation completed!")

# Verify most frequent products
result = db.orders.aggregate([
    {
        "$group": {
            "_id": "$product_name",
            "total_quantity": {"$sum": "$quantity"},
            "order_count": {"$sum": 1}
        }
    },
    {"$sort": {"total_quantity": -1}},
    {"$limit": 5}
])

print("\nTop 5 Most Frequent Products:")
for doc in list(result):
    print(f"Product: {doc['_id']}")
    print(f"Total Quantity: {doc['total_quantity']}")
    print(f"Number of Orders: {doc['order_count']}")
    print("---")
