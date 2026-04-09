# 🛒 Inventory Management System

A **Flask-based REST API + CLI application** for managing retail inventory, with OpenFoodFacts API integration and unit tests.

---

## ✨ Features

- 📦 Inventory CRUD operations  
- 🔐 CLI-based interaction  
- 🌍 OpenFoodFacts API integration  
- 🧪 Unit testing with Pytest  
- 🧱 Modular project structure  

---

## 📑 Table of Contents

- [Installation & Setup](#installation--setup)
- [Running the App](#running-the-app)
- [API Endpoints](#api-endpoints)
- [CLI Usage](#cli-usage)
- [Running Tests](#running-tests)
- [Project Structure](#project-structure)

---

## ⚙️ Installation & Setup

### 📌 Prerequisites
- Python 3.x  
- Git  

### 🚀 Steps

#### 1. Clone the repository
```bash
git clone https://github.com/YOUR_USERNAME/inventory-system.git
cd inventory-system
```

#### 2. Create and activate a virtual environment
```bash
# Create
python -m venv venv

# Activate (Windows)
.\venv\Scripts\Activate.ps1

# Activate (Mac/Linux)
source venv/bin/activate
```

#### 3. Install dependencies
```bash
pip install -r requirements.txt
```

---

## ▶️ Running the App

### Start the Flask server
```bash
python app.py
```

Server runs at:
```
http://127.0.0.1:5000
```

### Start the CLI (in another terminal)
```bash
python cli.py
```

---

## 🌐 API Endpoints

### 📥 Get all inventory items
```
GET /inventory
```

Response:
```json
{
  "status": "success",
  "count": 5,
  "inventory": []
}
```

---

### 🔍 Get a single item
```
GET /inventory/<id>
```

Response:
```json
{
  "status": "success",
  "item": {
    "id": 1,
    "product_name": "Organic Almond Milk",
    "brands": "Silk",
    "price": 3.99,
    "quantity": 50
  }
}
```

---

### ➕ Add a new item
```
POST /inventory
```

Request:
```json
{
  "product_name": "Green Tea",
  "brands": "Lipton",
  "price": 2.99,
  "quantity": 30
}
```

---

### ✏️ Update an item
```
PATCH /inventory/<id>
```

Request:
```json
{
  "price": 4.99,
  "quantity": 80
}
```

---

### ❌ Delete an item
```
DELETE /inventory/<id>
```

---

### 🌍 Search OpenFoodFacts
```
GET /inventory/search?q=<query>
```

---

## 💻 CLI Usage

Run:
```bash
python cli.py
```

### 🧾 Menu
```
1. View all inventory items
2. View a single item by ID
3. Add a new item
4. Update item
5. Delete an item
6. Search OpenFoodFacts
0. Exit
```

---

## 🧪 Running Tests

```bash
pytest test_app.py -v
```

### ✔️ Covered:
- Inventory CRUD  
- API endpoints  
- External API mocking  

---

## 📁 Project Structure

```bash
inventory-system/
├── app.py
├── cli.py
├── test_app.py
├── requirements.txt
└── README.md
```

---

## 📦 Dependencies

- Flask  
- Requests  
- Pytest  

---

## 👨‍💻 Author

Eugene Ogutu
https://github.com/C10H12O2 