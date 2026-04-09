"""
test_app.py - Unit tests for the Inventory Management System
Tests:
  - All API endpoints (GET, POST, PATCH, DELETE)
  - OpenFoodFacts search endpoint
  - fetch_openfoodfacts() function (mocked)
Run with: pytest test_app.py -v
"""

import pytest
from unittest.mock import patch, MagicMock
from app import app, inventory, fetch_openfoodfacts

def client():
    """Creates a test client and resets inventory before each test."""
    app.config["TESTING"] = True

    inventory.clear()
    inventory.extend([
        {
            "id": 1,
            "barcode": "0038000138416",
            "product_name": "Organic Almond Milk",
            "brands": "Silk",
            "ingredients_text": "Filtered water, almonds, cane sugar",
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
            "ingredients_text": "Whole grain corn, sugar, salt",
            "quantity": 120,
            "price": 4.49,
            "category": "Cereals",
            "expiration_date": "2027-11-30"
        }
    ])

    with app.test_client() as client:
        yield client

class TestGetAllItems:

    def test_get_all_returns_200(self, client):
        """Should return a 200 status code."""
        response = client.get("/inventory")
        assert response.status_code == 200

    def test_get_all_returns_correct_count(self, client):
        """Should return the correct number of items."""
        response = client.get("/inventory")
        data = response.get_json()
        assert data["count"] == 2

    def test_get_all_returns_inventory_list(self, client):
        """Should return an inventory list with the right items."""
        response = client.get("/inventory")
        data = response.get_json()
        assert data["status"] == "success"
        assert isinstance(data["inventory"], list)
        assert data["inventory"][0]["product_name"] == "Organic Almond Milk"

class TestGetSingleItem:

    def test_get_existing_item_returns_200(self, client):
        """Should return 200 for an item that exists."""
        response = client.get("/inventory/1")
        assert response.status_code == 200

    def test_get_existing_item_returns_correct_data(self, client):
        """Should return the correct item data."""
        response = client.get("/inventory/1")
        data = response.get_json()
        assert data["status"] == "success"
        assert data["item"]["product_name"] == "Organic Almond Milk"
        assert data["item"]["brands"] == "Silk"

    def test_get_nonexistent_item_returns_404(self, client):
        """Should return 404 for an item that doesn't exist."""
        response = client.get("/inventory/999")
        assert response.status_code == 404

    def test_get_nonexistent_item_returns_error_message(self, client):
        """Should return an error message for missing item."""
        response = client.get("/inventory/999")
        data = response.get_json()
        assert data["status"] == "error"
        assert "not found" in data["message"].lower()

class TestAddItem:

    def test_add_valid_item_returns_201(self, client):
        """Should return 201 when a valid item is added."""
        new_item = {
            "product_name": "Green Tea",
            "brands": "Lipton",
            "ingredients_text": "Green tea leaves, water",
            "quantity": 30,
            "price": 2.99,
            "category": "Beverages",
            "expiration_date": "2027-06-01"
        }
        response = client.post("/inventory", json=new_item)
        assert response.status_code == 201

    def test_add_valid_item_returns_correct_data(self, client):
        """Should return the newly created item."""
        new_item = {
            "product_name": "Green Tea",
            "brands": "Lipton",
            "ingredients_text": "Green tea leaves, water",
            "quantity": 30,
            "price": 2.99,
            "category": "Beverages",
            "expiration_date": "2027-06-01"
        }
        response = client.post("/inventory", json=new_item)
        data = response.get_json()
        assert data["status"] == "success"
        assert data["item"]["product_name"] == "Green Tea"
        assert data["item"]["id"] == 3

    def test_add_item_missing_fields_returns_400(self, client):
        """Should return 400 when required fields are missing."""
        incomplete_item = {"product_name": "Green Tea"}
        response = client.post("/inventory", json=incomplete_item)
        assert response.status_code == 400

    def test_add_item_missing_fields_returns_error_message(self, client):
        """Should return a message listing missing fields."""
        incomplete_item = {"product_name": "Green Tea"}
        response = client.post("/inventory", json=incomplete_item)
        data = response.get_json()
        assert data["status"] == "error"
        assert "Missing fields" in data["message"]

class TestUpdateItem:

    def test_update_existing_item_returns_200(self, client):
        """Should return 200 when updating an existing item."""
        response = client.patch("/inventory/1", json={"price": 5.99})
        assert response.status_code == 200

    def test_update_price_changes_correctly(self, client):
        """Should correctly update the price field."""
        client.patch("/inventory/1", json={"price": 5.99})
        response = client.get("/inventory/1")
        data = response.get_json()
        assert data["item"]["price"] == 5.99

    def test_update_quantity_changes_correctly(self, client):
        """Should correctly update the quantity field."""
        client.patch("/inventory/1", json={"quantity": 100})
        response = client.get("/inventory/1")
        data = response.get_json()
        assert data["item"]["quantity"] == 100

    def test_update_nonexistent_item_returns_404(self, client):
        """Should return 404 when updating an item that doesn't exist."""
        response = client.patch("/inventory/999", json={"price": 5.99})
        assert response.status_code == 404

    def test_update_does_not_change_unspecified_fields(self, client):
        """Should only update specified fields, leaving others unchanged."""
        client.patch("/inventory/1", json={"price": 9.99})
        response = client.get("/inventory/1")
        data = response.get_json()
        assert data["item"]["product_name"] == "Organic Almond Milk"

class TestDeleteItem:

    def test_delete_existing_item_returns_200(self, client):
        """Should return 200 when deleting an existing item."""
        response = client.delete("/inventory/1")
        assert response.status_code == 200

    def test_delete_removes_item_from_inventory(self, client):
        """Item should no longer exist after deletion."""
        client.delete("/inventory/1")
        response = client.get("/inventory/1")
        assert response.status_code == 404

    def test_delete_reduces_inventory_count(self, client):
        """Inventory count should decrease by 1 after deletion."""
        client.delete("/inventory/1")
        response = client.get("/inventory")
        data = response.get_json()
        assert data["count"] == 1

    def test_delete_nonexistent_item_returns_404(self, client):
        """Should return 404 when deleting an item that doesn't exist."""
        response = client.delete("/inventory/999")
        assert response.status_code == 404

class TestSearchExternal:

    def test_search_missing_query_returns_400(self, client):
        """Should return 400 when no query is provided."""
        response = client.get("/inventory/search")
        assert response.status_code == 400

    def test_search_empty_query_returns_400(self, client):
        """Should return 400 when query is empty string."""
        response = client.get("/inventory/search?q=")
        assert response.status_code == 400

    @patch("app.fetch_openfoodfacts")
    def test_search_found_returns_200(self, mock_fetch, client):
        """Should return 200 when product is found."""
        mock_fetch.return_value = {
            "barcode": "123456",
            "product_name": "Test Product",
            "brands": "Test Brand",
            "ingredients_text": "Water, sugar"
        }
        response = client.get("/inventory/search?q=TestProduct")
        assert response.status_code == 200

    @patch("app.fetch_openfoodfacts")
    def test_search_not_found_returns_404(self, mock_fetch, client):
        """Should return 404 when product is not found on OpenFoodFacts."""
        mock_fetch.return_value = None
        response = client.get("/inventory/search?q=xyzunknownproduct")
        assert response.status_code == 404

class TestFetchOpenFoodFacts:

    @patch("app.requests.get")
    def test_barcode_lookup_returns_product(self, mock_get):
        """Should return product data when barcode lookup succeeds."""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "status": 1,
            "product": {
                "product_name": "Almond Milk",
                "brands": "Silk",
                "ingredients_text": "Water, almonds"
            }
        }
        mock_get.return_value = mock_response

        result = fetch_openfoodfacts("0038000138416")
        assert result is not None
        assert result["product_name"] == "Almond Milk"
        assert result["brands"] == "Silk"
        assert result["barcode"] == "0038000138416"

    @patch("app.requests.get")
    def test_barcode_lookup_not_found_returns_none(self, mock_get):
        """Should return None when barcode is not found."""
        mock_response = MagicMock()
        mock_response.json.return_value = {"status": 0}
        mock_get.return_value = mock_response

        result = fetch_openfoodfacts("0000000000000")
        assert result is None

    @patch("app.requests.get")
    def test_name_search_returns_product(self, mock_get):
        """Should return product data when name search succeeds."""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "products": [
                {
                    "code": "123456",
                    "product_name": "Cheerios",
                    "brands": "General Mills",
                    "ingredients_text": "Whole grain oats"
                }
            ]
        }
        mock_get.return_value = mock_response

        result = fetch_openfoodfacts("Cheerios")
        assert result is not None
        assert result["product_name"] == "Cheerios"
        assert result["brands"] == "General Mills"

    @patch("app.requests.get")
    def test_name_search_no_results_returns_none(self, mock_get):
        """Should return None when name search finds no products."""
        mock_response = MagicMock()
        mock_response.json.return_value = {"products": []}
        mock_get.return_value = mock_response

        result = fetch_openfoodfacts("xyzunknownproduct")
        assert result is None

    @patch("app.requests.get")
    def test_network_error_returns_none(self, mock_get):
        """Should return None when a network error occurs."""
        import requests as req
        mock_get.side_effect = req.exceptions.RequestException("Network error")

        result = fetch_openfoodfacts("Cheerios")
        assert result is None
