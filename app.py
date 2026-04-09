 
"""
app.py - Flask Rest API for the inventory management system
The endpoints:
GET   /inventory          -Fetch all items
GET   /inventory/<id>     -Fetch a single item
POST  /inventory          -Add a new item
PATCH /inventory/<id>     -Update an item
DELETE /inventory/<id>    -Remove an item
GET    /inventory/search   -Search OpenFoodFacts API for a product by name
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
    return jsonify({"status": "success", "data": {"count": len(inventory), "inventory": inventory}}), 200