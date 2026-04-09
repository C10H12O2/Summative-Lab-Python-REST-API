 
"""
app.py - Flask Rest API for the inventory management system
The endpoints:
GET   /inventory          -Fetch all items
GET   /inventory/<id>     -Fetch a single item
POST  /inventory          -Add a new item
PATCH /inventory/<id>     -Update an item
DELETE /inventory/<id>    -Remove an item
GET    /inventory/search  -Search OpenFoodFacts API for a product by name
 """
 
from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

inventory = [
    {
        "id":1,
        "product_name": "Organic Almond Milk",
        "brands": "Silk",
        "ingredients_text": "Filtered water, almonds, cane sugar, sea salt, sunflower lecithin, gellan gum",
        "quantity": 50,
        "price": 3.99,
        "category": "Beverages",
        "expiration_date": "2027-12-31"
    },
    
    {
                "id":2,
        "product_name": "Cheerios Cereal",
        "brands": "General Mills",
        "ingredients_text": "Whole grain corn, sugar, salt, natural flavors, vitamin and mineral blend",
        "quantity": 120,
        "price": 4.49,
        "category": "Cereals",
        "expiration_date": "2027-11-30"
    },
    
    {
                "id":3,
        "product_name": "Peanut Butter Cream",
        "brands": "Blue Band",
        "ingredients_text": "Roasted, peanuts, sugar, contains 2% or less of molasses, salt, hydrogenated egetable oils",
        "quantity": 75,
        "price": 5.29,
        "category": "Spreads",
        "expiration_date": "2027-12-14"
    },
    
    {
                "id":4,
        "product_name": "Whole wheat bread",
        "brands": "Supa Loaf",
        "ingredients_text": "Whole wheat flour, water, sugar, yeast, soybean oil, salt",
        "quantity": 47,
        "price": 2.79,
        "category": "Bakery",
        "expiration_date": "2026-6-22"
    },
    
    {
                "id":5,
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
    return jsonify({"status": "success", "count": len(inventory), "inventory": inventory}), 200

@app.route("/inventory/<int:item_id>", methods=["GET"])
def get_item(item_id):
    item = next((i for i in inventory if i["id"] == item_id), None)
    if item is None:
        return jsonify({"status": "error", "message": f"Item with ID {item_id} not found"}), 404
    return jsonify({"status": "success", "item": item}), 200

@app.route ("/inventory", methods = ["POST"])
def add_item():
    data = request.get_json()
    
    required_fields = ["product_name", "brands", "ingredients_text", "quantity", "price", "category", "expiration_date"]
    missing = [f for f in required_fields if f not in data]
    
    if missing:
        return jsonify({"status": "error", "message": f"Missing fields: {missing}"}), 400
    
    new_item = {
        "id": next_id(),
        "product_name": data["product_name"],
        "brands": data["brands"],
        "ingredients_text": data.get("ingredients_text", ""),
        "quantity": data["quantity"],
        "price": data["price"],
        "category": data["category"],
        "expiration_date": data["expiration_date"]
    }
    
    inventory.append(new_item)
    return jsonify({"status": "success", "message": "Item added successfully", "item": new_item}), 201

@app.route("/inventory/<int:item_id>", methods=["PATCH"])
def update_item(item_id):
    item = next((i for i in inventory if i["id"] == item_id), None)
    if item is None:
        return jsonify({"status": "error", "message": f"Item with ID {item_id} not found"}), 404

    data = request.get_json()
    
    updatable_fields = ["product_name", "brands", "ingredients_text", "quantity", "price", "category", "expiration_date"]
    for field in updatable_fields:
        if field in data:
            item[field] = data[field]
            
    return jsonify({"status": "success", "message": "Item updated successfully", "item": item}), 200
    