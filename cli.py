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
    
def view_all():
    try:
        response = requests.get(f"{BASE_URL}/inventory")
        data = response.json()
        items = data.get("inventory", [])
        
        if not items:
            print("\n No items in inventory.")
            return
        
        print(f"\n Total Items: {len(items)}")
        for item in items:
            print_item(item)
            
    except requests.exceptions.ConnectionError:
        print("\n [Error] Could not connect to the server, make sure app.py is running.")
        
def view_one():
    try:
        item_id = int(input("\n Enter item ID: "))
    except ValueError:
        print(" [Error] Invalid ID, please enter a number.") 
        return
    
    try:
        response = requests.get(f"{BASE_URL}/inventory/{item_id}")
        data = response.json()
        
        if response.status_code == 200:
            print_item(data["item"])
        else:
            print(f"\n [Error] {data.get('message', 'Item not found')}")    
            
    except requests.exceptions.ConnectionError:
        print("\n [Error] Could not connect to the server, make sure app.py is running.")  