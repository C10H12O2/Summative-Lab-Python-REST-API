"""
cli.py - Command Line Interface for the inventory Management System
It's primarily goinfg to interact with the Flask API running at http://127.0.0.1:5000
"""
import requests

BASE_URL = "http://127.0.0.1:5000"

def print_item(item):
    print("\n" + "=" * 45)
    print(f"  ID          : {item['id']}")
    print(f"  Name        : {item['product_name']}")
    print(f"  Brand       : {item['brands']}")
    print(f"  Category    : {item['category']}")
    print(f"  Price       : ${item['price']:}")
    print(f"  Quantity    : {item['quantity']}")
    print(f"  Exp Date    : {item['expiration_date']}")
    print(f"  Barcode     : {item['barcode']}")
    print(f"  Ingredients : {item.get('ingredients_text', 'N/A')[:60]}...")
    print("=" * 45 )