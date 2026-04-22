import requests

BASE_URL = "http://127.0.0.1:5000"

def print_item(item):
    print("\n" + "=" * 45)
    print(f"  ID          : {item['id']}")
    print(f"  Name        : {item['product_name']}")
    print(f"  Brand       : {item['brands']}")
    print(f"  Category    : {item['category']}")
    print(f"  Price       : ${item['price']}")
    print(f"  Quantity    : {item['quantity']}")
    print(f"  Exp Date    : {item['expiration_date']}")
    print(f"  Barcode     : {item['barcode']}")
    print(f"  Ingredients : {item.get('ingredients_text', 'N/A')[:60]}...")
    print("=" * 45)
    
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
        print("\n [Error] Could not connect to the server kindly make sure app.py is running.")
        
def view_one():
    try:
        item_id = int(input("\n Enter item ID: "))
    except ValueError:
        print(" [Error] That's not a valid ID, please enter a number.")
        return

    try:
        response = requests.get(f"{BASE_URL}/inventory/{item_id}")
        data = response.json()

        if response.status_code == 200:
            print_item(data["item"])
        else:
            print(f"\n [Error] {data.get('message', 'Item not found')}")

    except requests.exceptions.ConnectionError:
        print("\n [Error] Could not connect to the server please make sure app.py is running.")
        
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
        print(" [Error] The price should be a decimal and quantity should be a whole number")
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
        print("\n [Error] Could not connect to the server pelase make sure app.py is running")
        
def update_item():
    try:
        item_id = int(input("\n Enter item ID to update: "))
    except ValueError:
        print(" [Error] That's not a valid ID, please enter a number.")
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
            print(" [Error] That's not a valid choice.")
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
        print("\n [Error] Could not connect to the server. Make sure app.py is running.")

def delete_item():
    try:
        item_id = int(input("\n Enter item ID to delete: "))
    except ValueError:
        print(" [Error] That's not a valid ID, please enter a number.")
        return

    confirm = input(f" Are you sure you want to delete item {item_id}? (yes/no): ").strip().lower()
    if confirm != "yes":
        print(" Deletion cancelled.")
        return

    try:
        response = requests.delete(f"{BASE_URL}/inventory/{item_id}")
        data = response.json()

        if response.status_code == 200:
            print(f"\n Item deleted successfully!")
        else:
            print(f"\n [Error] {data.get('message')}")

    except requests.exceptions.ConnectionError:
        print("\n [Error] Could not connect to the serverkindly make sure app.py is running.")
        
def search_external():
    query = input("\n Enter a product name or barcode to search on OpenFoodFacts: ").strip()
    if not query:
        print(" [Error] Search query can't be empty.")
        return

    try:
        response = requests.get(f"{BASE_URL}/inventory/search", params={"q": query})
        data = response.json()

        if response.status_code == 200:
            product = data.get("product")
            print("\n -- Search Result from OpenFoodFacts --")
            print(f" Name       : {product.get('product_name', 'N/A')}")
            print(f" Brand      : {product.get('brands', 'N/A')}")
            print(f" Barcode    : {product.get('barcode', 'N/A')}")
            print(f" Ingredients: {product.get('ingredients_text', 'N/A')[:80]}...")

            add = input("\n Want to add this product to inventory? (yes/no): ").strip().lower()
            if add == "yes":
                try:
                    price = float(input(" Set Price: ").strip())
                    quantity = int(input(" Set Quantity: ").strip())
                    category = input(" Set Category: ").strip()
                    expiration_date = input(" Set Expiration Date (YYYY-MM-DD): ").strip()
                except ValueError:
                    print(" [Error] Invalid input for price or quantity.")
                    return

                payload = {
                    "product_name": product.get("product_name", "Unknown Product"),
                    "brands": product.get("brands", "Unknown Brand"),
                    "barcode": product.get("barcode", "N/A"),
                    "ingredients_text": product.get("ingredients_text", ""),
                    "category": category,
                    "price": price,
                    "quantity": quantity,
                    "expiration_date": expiration_date
                }

                add_response = requests.post(f"{BASE_URL}/inventory", json=payload)
                add_data = add_response.json()

                if add_response.status_code == 201:
                    print(f"\n Product added to inventory!")
                    print_item(add_data["item"])
                else:
                    print(f"\n [Error] {add_data.get('message')}")
        else:
            print(f"\n [Error] {data.get('message')}")

    except requests.exceptions.ConnectionError:
        print("\n [Error] Could not connect to the server please meake sure app.py is running.")

def main():
    print("\n" + "=" * 50)
    print("Welcome to the Inventory Management System!!!!")
    print("=" * 50)

    while True:
        print("\n MENU:")
        print("  1. View all inventory items")
        print("  2. View a single item by ID")
        print("  3. Add a new item")
        print("  4. Update an existing item")
        print("  5. Delete an item")
        print("  6. Search product on OpenFoodFacts")
        print("  0. Exit")

        choice = input("\n Enter your choice (0-6): ").strip()
        if choice == "1":
            view_all()
        elif choice == "2":
            view_one()
        elif choice == "3":
            add_item()
        elif choice == "4":
            update_item()
        elif choice == "5":
            delete_item()
        elif choice == "6":
            search_external()
        elif choice == "0":
            print("\n Thanks for using the Inventory Management System. See you next time!")
            break
        else:
            print("\n [Error] Invalid choice, please enter a number between 0 and 6.")

if __name__ == "__main__":
    main()


        

        


    