from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

inventory = [
        {
        "id": 1,
        "barcode": "0038000138416",
        "product_name": "Organic Almond Milk",
        "brands": "Silk",
        "ingredients_text": "Filtered water, almonds, cane sugar, sea salt, sunflower lecithin, gellan gum",
        "quantity": 50,
        "price": 3.99,
        "category": "Beverages",
        "expiration_date": "2027-12-31"
    },
    {
        "id": 2,
        "barcode": "016000275287",
        "product_name": "Cheerios Cereal",
        "brands": "General Mills",
        "ingredients_text": "Whole grain corn, sugar, salt, natural flavors, vitamin and mineral blend",
        "quantity": 120,
        "price": 4.49,
        "category": "Cereals",
        "expiration_date": "2027-11-30"
    },
    {
        "id": 3,
        "barcode": "021130126026",
        "product_name": "Peanut Butter Cream",
        "brands": "Blue Band",
        "ingredients_text": "Roasted peanuts, sugar, contains 2% or less of molasses, salt, hydrogenated vegetable oils",
        "quantity": 75,
        "price": 5.29,
        "category": "Spreads",
        "expiration_date": "2027-12-14"
    },
    {
        "id": 4,
        "barcode": "041270890014",
        "product_name": "Whole Wheat Bread",
        "brands": "Supa Loaf",
        "ingredients_text": "Whole wheat flour, water, sugar, yeast, soybean oil, salt",
        "quantity": 47,
        "price": 2.79,
        "category": "Bakery",
        "expiration_date": "2026-06-22"
    },
    {
        "id": 5,
        "barcode": "036800105522",
        "product_name": "Orange Juice",
        "brands": "Tropicana",
        "ingredients_text": "100% pure squeezed orange juice",
        "quantity": 60,
        "price": 4.19,
        "category": "Beverages",
        "expiration_date": "2026-12-31"
    }
]

def next_id():
    return max(item["id"] for item in inventory) + 1 if inventory else 1

@app.route("/inventory", methods=["GET"])
def get_all_items():
    return jsonify({"status": "success","count": len(inventory),"inventory": inventory}), 200
    
@app.route("/inventory/<int:item_id>", methods=["GET"])
def get_item(item_id):
    item = next((i for i in inventory if i["id"] == item_id), None)
    if item is None:
        return jsonify({"status": "error","message": f"Couldn't find an item with ID {item_id}" }), 404
    return jsonify({"status": "success", "item": item}), 200

@app.route("/inventory", methods=["POST"])
def add_item():
    data = request.get_json()
    required_fields = ["product_name", "brands", "ingredients_text", "quantity", "price", "category", "expiration_date"]
    missing = [f for f in required_fields if f not in data]

    if missing:
        return jsonify({"status": "error","message": f"Missing required fields: {missing}"
        }), 400

    new_item = {
        "id": next_id(),
        "barcode": data.get("barcode", "N/A"), 
        "product_name": data["product_name"],
        "brands": data["brands"],
        "ingredients_text": data.get("ingredients_text", ""),
        "quantity": data["quantity"],
        "price": data["price"],
        "category": data["category"],
        "expiration_date": data["expiration_date"]
    }
    
@app.route("/inventory", methods=["POST"])  
def add_item():
    data = request.get_json()
    required_fields = ["product_name", "brands", "ingredients_text", "quantity", "price", "category", "expiration_date"]
    missing = [f for f in required_fields if f not in data]

    if missing:
        return jsonify({
            "status": "error",
            "message": f"Missing required fields: {missing}"
        }), 400

    new_item = {
        "id": next_id(),
        "barcode": data.get("barcode", "N/A"),  
        "product_name": data["product_name"],
        "brands": data["brands"],
        "ingredients_text": data.get("ingredients_text", ""),
        "quantity": data["quantity"],
        "price": data["price"],
        "category": data["category"],
        "expiration_date": data["expiration_date"]
    }
    
    inventory.append(new_item)
    return jsonify({"status": "success","message": "Item added successfully","item": new_item}), 201

@app.route("/inventory/<int:item_id>", methods=["PATCH"])
def update_item(item_id):
    item = next((i for i in inventory if i["id"] == item_id), None)
    if item is None:
        return jsonify({"status": "error","message": f"Couldn't find an item with ID {item_id}"}), 404
    
    data = request.get_json()
    
    updatable_fields = ["product_name", "brands", "ingredients_text", "quantity", "price", "category", "barcode", "expiration_date"]
    for field in updatable_fields:
        if field in data:
            item[field] = data[field]

    return jsonify({"status": "success","message": "Item updated successfully","item": item}), 200

@app.route("/inventory/<int:item_id>", methods=["DELETE"])
def delete_item(item_id):
    global inventory
    item = next((i for i in inventory if i["id"] == item_id), None)
    if item is None:
        return jsonify({"status": "error","message": f"Couldn't find an item with ID {item_id}"}), 404 
  
    inventory = [i for i in inventory if i["id"] != item_id]
    return jsonify({"status": "success","message": "Item deleted successfully"}), 200

def fetch_openfoodfacts(query):
    try:
        if query.isdigit():
            url = f"https://world.openfoodfacts.org/api/v0/product/{query}.json"
            response = requests.get(url, timeout=5)
            data = response.json()

            if data.get("status") == 1:
                p = data["product"]
                return {"barcode": query,"product_name": p.get("product_name", "Unknown Product"),"brands": p.get("brands", "Unknown Brand"),
                        "ingredients_text": p.get("ingredients_text", "Unknown Ingredients")
                }
        else:
           url = "https://world.openfoodfacts.org/cgi/search.pl"
           params = {"search_terms": query,"search_simple": 1,"action": "process","json": 1,"page_size": 1}
           response = requests.get(url, params=params, timeout=5)
           data = response.json()

           products = data.get("products", [])
           if products:
                p = products[0]
                return {
                    "barcode": p.get("code", "N/A"),
                    "product_name": p.get("product_name", "Unknown Product"),
                    "brands": p.get("brands", "Unknown Brand"),
                    "ingredients_text": p.get("ingredients_text", "Unknown Ingredients")
                }

    except requests.exceptions.RequestException as e:
        print(f"[OpenFoodFacts Error] {e}")
    return None 

@app.route("/inventory/search", methods=["GET"])
def search_external():
    query = request.args.get("q", "").strip()
    if not query:
        return jsonify({"status": "error","message": "Please provide a search query using ?q=yourquery" }), 400
    result = fetch_openfoodfacts(query)
    if result is None:
        return jsonify({"status": "error","message": "Couldn't find that product on OpenFoodFacts"}), 404
    return jsonify({"status": "success", "product": result}), 200

if __name__ == "__main__":
    app.run(debug=True)

