from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

# Database setup
def init_db():
    with sqlite3.connect("database.db") as conn:
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS products (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    description TEXT,
                    price REAL NOT NULL,
                    stock_quantity INTEGER NOT NULL,
                    category TEXT,
                    is_active INTEGER DEFAULT 1)''')
        conn.commit()

init_db()

# Helper function to get a database connection
def get_db_connection():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row  # This allows fetching rows as dictionaries
    return conn

# Add a Product
@app.route("/products", methods=["POST"])
def add_product():
    data = request.get_json()
    if not data or 'name' not in data or 'price' not in data or 'stock_quantity' not in data:
        return jsonify({"error": "Missing required fields"}), 400

    name = data['name']
    description = data.get('description', '')
    price = data['price']
    stock_quantity = data['stock_quantity']
    category = data.get('category', '')

    try:
        conn = get_db_connection()
        conn.execute("INSERT INTO products (name, description, price, stock_quantity, category) VALUES (?, ?, ?, ?, ?)",
                     (name, description, price, stock_quantity, category))
        conn.commit()
        product_id = conn.cursor().lastrowid
        conn.close()
        return jsonify({"message": "Product added successfully", "id": product_id}), 201
    except sqlite3.Error as e:
        return jsonify({"error": str(e)}), 500

# Get All Products with optional filtering, sorting, and pagination
@app.route("/products", methods=["GET"])
def get_products():
    category = request.args.get('category')
    sort_by = request.args.get('sort_by')
    search_query = request.args.get('search')
    page = request.args.get('page', 1, type=int)
    limit = request.args.get('limit', 10, type=int)
    
    conn = get_db_connection()
    query = "SELECT * FROM products WHERE is_active=1"
    params = []

    if category:
        query += " AND category = ?"
        params.append(category)

    if search_query:
        query += " AND (name LIKE ? OR description LIKE ?)"
        params.append(f"%{search_query}%")
        params.append(f"%{search_query}%")
    
    if sort_by == 'price':
        query += " ORDER BY price"
    
    # Pagination
    offset = (page - 1) * limit
    query += " LIMIT ? OFFSET ?"
    params.append(limit)
    params.append(offset)

    products = conn.execute(query, tuple(params)).fetchall()
    conn.close()
    
    products_list = [dict(product) for product in products]
    return jsonify(products_list), 200

# Get a single product by ID
@app.route("/products/<int:id>", methods=["GET"])
def get_product_by_id(id):
    conn = get_db_connection()
    product = conn.execute("SELECT * FROM products WHERE id=? AND is_active=1", (id,)).fetchone()
    conn.close()
    
    if product is None:
        return jsonify({"error": "Product not found"}), 404
    
    return jsonify(dict(product)), 200

# Update a Product
@app.route("/products/<int:id>", methods=["PUT"])
def update_product(id):
    data = request.get_json()
    conn = get_db_connection()
    
    product = conn.execute("SELECT * FROM products WHERE id=? AND is_active=1", (id,)).fetchone()
    if product is None:
        conn.close()
        return jsonify({"error": "Product not found"}), 404

    # Build update query dynamically
    updates = []
    params = []
    
    if 'name' in data:
        updates.append("name = ?")
        params.append(data['name'])
    if 'description' in data:
        updates.append("description = ?")
        params.append(data['description'])
    if 'price' in data:
        updates.append("price = ?")
        params.append(data['price'])
    if 'stock_quantity' in data:
        updates.append("stock_quantity = ?")
        params.append(data['stock_quantity'])
        # Optional: Low-stock alert check
        if data['stock_quantity'] < 5:
            print(f"Low stock alert for product ID {id}: Stock is at {data['stock_quantity']}")
    if 'category' in data:
        updates.append("category = ?")
        params.append(data['category'])

    if not updates:
        conn.close()
        return jsonify({"error": "No fields to update"}), 400

    query = "UPDATE products SET " + ", ".join(updates) + " WHERE id = ?"
    params.append(id)
    
    conn.execute(query, tuple(params))
    conn.commit()
    conn.close()
    
    return jsonify({"message": "Product updated successfully"}), 200

# Soft Delete Product
@app.route("/products/<int:id>", methods=["DELETE"])
def delete_product(id):
    conn = get_db_connection()
    product = conn.execute("SELECT id FROM products WHERE id=? AND is_active=1", (id,)).fetchone()
    
    if product is None:
        conn.close()
        return jsonify({"error": "Product not found"}), 404
    
    conn.execute("UPDATE products SET is_active=0 WHERE id=?", (id,))
    conn.commit()
    conn.close()
    
    return jsonify({"message": "Product soft-deleted successfully"}), 200

if __name__ == "__main__":
    app.run(debug=True)