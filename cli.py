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
        
def add_item():
    print("\n -- Add New Item --")
    try:
        product_name = input(" Product Name: ").strip()
        brands = input(" Brand: ").strip()
        category = input(" Category: ").strip()
        price = float(input(" Price: ").strip())
        quantity = int(input(" Quantity: ").strip())
        expiration_date = input(" Expiration Date (YYYY-MM-DD): ").strip()
        barcode = input(" Barcode (optional): ").strip()
        ingredients = input(" Ingredients (optional): ").strip()
        
    except ValueError:
        print(" [Error] Price must be a decimal and quantity must be a whole number.")
        return
    
        
    payload = {
        "product_name": product_name,
        "brands": brands,
        "category": category,
        "price": price,
        "quantity": quantity,
        "barcode": barcode or "N/A",
        "ingredients_text": ingredients or "N/A",
        "expiration_date": expiration_date
    }
    
    try:
        response = requests.post(f"{BASE_URL}/inventory", json=payload)
        data = response.json()
        
        if response.status_code == 201:
            print(f"\n Item added successfully!")
            print_item(data["item"])
        else:
            print(f"\n [Error] {data.get('message')}")
            
    except requests.exceptions.ConnectionError:
        print("\n [Error] Could not connect to the server, make sure app.py is running.")
        
 def update_item():
     try:
         item_id = int(input("\n Enter item ID to update: "))
        except ValueError:
            print(" [Error] Invalid ID, please enter a number.") 
            return
        
        print("\n What would you like to update?")
        print(" 1. Product Name")
        print(" 2. Brand")
        print(" 3. Category")
        print(" 4. Price")
        print(" 5. Quantity")
        print(" 6. Expiration Date")
        print(" 7. Barcode")
        print(" 8. Ingredients")
        choice = input(" Enter choice (1-8): ").strip()
        
        try:
            if choice == "1":
                payload = {"product_name": input(" New Product Name: ").strip()}
            elif choice == "2":
                payload = {"brands": input(" New Brand: ").strip()}
            elif choice == "3":
                payload = {"category": input(" New Category: ").strip()}
            elif choice == "4":
                payload = {"price": float(input(" New Price: ").strip())}
            elif choice == "5":
                payload = {"quantity": int(input(" New Quantity: ").strip())}
            elif choice == "6":
                payload = {"expiration_date": input(" New Expiration Date (YYYY-MM-DD): ").strip()}
            elif choice == "7":
                payload = {"barcode": input(" New Barcode: ").strip()}
            elif choice == "8":
                payload = {"ingredients_text": input(" New Ingredients: ").strip()}
                
            else:
                print(" [Error] Invalid choice.")
                return
        except ValueError:
            print(" [Error] Invalid input for price or quantity.")
            return
        
        try:
            response = requests.patch(f"{BASE_URL}/inventory/{item_id}", json=payload)
            data = response.json()
            
            if response.status_code == 200:
                print(f"\n Item updated successfully!")
                print_item(data["item"])
            else:
                print(f"\n [Error] {data.get('message')}")
        
        except requests.exceptions.ConnectionError:
            print("\n [Error] Could not connect to the server, make sure app.py is running.")
            
            
        
            