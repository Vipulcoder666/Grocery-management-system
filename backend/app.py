from flask import Flask, jsonify, request
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)

# Database connection
def get_db_connection():
    conn = sqlite3.connect('../database/grocery.db')
    conn.row_factory = sqlite3.Row
    return conn


# Create table if not exists
def create_table():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        price REAL NOT NULL,
        quantity INTEGER NOT NULL
    )
    """)

    conn.commit()
    conn.close()


# Home route
@app.route("/")
def home():
    return "Grocery Management System Backend Running"


# GET all products
@app.route("/products", methods=["GET"])
def get_products():
    conn = get_db_connection()
    products = conn.execute("SELECT * FROM products").fetchall()
    conn.close()

    product_list = []

    for product in products:
        product_list.append({
            "id": product["id"],
            "name": product["name"],
            "price": product["price"],
            "quantity": product["quantity"]
        })

    return jsonify(product_list)


# ADD new product
@app.route("/products", methods=["POST"])
def add_product():
    data = request.get_json()

    name = data["name"]
    price = data["price"]
    quantity = data["quantity"]

    conn = get_db_connection()
    conn.execute(
        "INSERT INTO products (name, price, quantity) VALUES (?, ?, ?)",
        (name, price, quantity)
    )
    conn.commit()
    conn.close()

    return jsonify({"message": "Product added successfully"})

@app.route("/products/<int:id>", methods=["DELETE"])
def delete_product(id):

    conn = get_db_connection()
    conn.execute("DELETE FROM products WHERE id = ?", (id,))
    conn.commit()
    conn.close()

    return jsonify({"message": "Product deleted successfully"})

@app.route("/products/<int:id>", methods=["PUT"])
def update_product(id):

    data = request.get_json()

    name = data["name"]
    price = data["price"]
    quantity = data["quantity"]

    conn = get_db_connection()

    conn.execute(
        "UPDATE products SET name=?, price=?, quantity=? WHERE id=?",
        (name, price, quantity, id)
    )

    conn.commit()
    conn.close()

    return jsonify({"message": "Product updated successfully"})


if __name__ == "__main__":
    create_table()
    app.run(debug=True)