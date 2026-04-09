"""
app_test.py - This is just to run tests for the Inventory Management System
    Tests:
    - All API endpoints (GET POST PATCH DELETE)
    - OpenFoodFacts search enpoint
    - fetch_openfoodfacts() function (mocked)
It will all be ran using: pytest app_test.py -v   
"""

import pytest
from unittest.mock import patch, MagicMock
from app import app, inventory, fetch_openfoodfacts

@pytest.fixture
def client():
    """
    This creates a test client and resets the inventory before each test
    """
    app.cofig['TESTING'] = True
    
    inventory.clear()
    inventory.extend([
        {
        "id":1,
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
        "id":2,
        "barcode": "016000275287",
        "product_name": "Cheerios Cereal",
        "brands": "General Mills",
        "ingredients_text": "Whole grain corn, sugar, salt, natural flavors, vitamin and mineral blend",
        "quantity": 120,
        "price": 4.49,
        "category": "Cereals",
        "expiration_date": "2027-11-30"
    }
    ])
    
    with app.test_client() as client:
        yield client