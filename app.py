from flask import Flask, request, jsonify
from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, or_
from sqlalchemy.orm import sessionmaker, declarative_base, scoped_session


DATABASE_URI = 'mysql+mysqlconnector://root:sumit%400605@localhost:3306/inventory_db'

app = Flask(__name__)

# SQLAlchemy setup
Base = declarative_base()
engine = create_engine(DATABASE_URI)
Session = sessionmaker(bind=engine)
session = scoped_session(Session)  # Corrected to use scoped_session

# Product Model
class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    description = Column(String(500), default='')
    price = Column(Float, nullable=False)
    stock_quantity = Column(Integer, nullable=False)
    category = Column(String(100), default='')
    is_active = Column(Boolean, default=True)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'price': self.price,
            'stock_quantity': self.stock_quantity,
            'category': self.category,
            'is_active': self.is_active
        }

# Create the database table if it doesn't exist
Base.metadata.create_all(engine)

@app.teardown_appcontext
def shutdown_session(exception=None):
    session.remove()

@app.route("/")
def home():
    return jsonify({"message": "Welcome to the Product Inventory API!"}), 200

# Add a Product 
@app.route("/products", methods=["POST"])
def add_product():
    data = request.get_json()
    if not data or 'name' not in data or 'price' not in data or 'stock_quantity' not in data:
        return jsonify({"error": "Missing required fields"}), 400

    try:
        new_product = Product(
            name=data['name'],
            description=data.get('description', ''),
            price=data['price'],
            stock_quantity=data['stock_quantity'],
            category=data.get('category', '')
        )
        session.add(new_product)
        session.commit()
        return jsonify({"message": "Product added successfully", "id": new_product.id}), 201
    except Exception as e:
        session.rollback()
        return jsonify({"error": str(e)}), 500

# Get Products 
@app.route("/products", methods=["GET"])
def get_products():
    category = request.args.get('category')
    sort_by = request.args.get('sort_by')
    order = request.args.get('order', 'asc')  # default asc
    search_query = request.args.get('search')
    page = request.args.get('page', 1, type=int)
    limit = request.args.get('limit', 10, type=int)

    query = session.query(Product).filter(Product.is_active == True)

    # Category filter
    if category:
        query = query.filter(Product.category == category)
    
    # Search filter (case-insensitive)
    if search_query:
        search_pattern = f"%{search_query}%"
        query = query.filter(or_(
            Product.name.ilike(search_pattern),
            Product.description.ilike(search_pattern)
        ))

    # Sorting
    if sort_by == 'price':
        query = query.order_by(Product.price.desc() if order == 'desc' else Product.price)

    # Pagination
    offset = (page - 1) * limit
    products = query.offset(offset).limit(limit).all()

    return jsonify([product.to_dict() for product in products]), 200

# Get Product by ID 
@app.route("/products/<int:id>", methods=["GET"])
def get_product_by_id(id):
    product = session.query(Product).filter_by(id=id, is_active=True).first()
    if not product:
        return jsonify({"error": "Product not found"}), 404
    return jsonify(product.to_dict()), 200

# Update Product 
@app.route("/products/<int:id>", methods=["PUT"])
def update_product(id):
    data = request.get_json()
    product = session.query(Product).filter_by(id=id, is_active=True).first()
    if not product:
        return jsonify({"error": "Product not found"}), 404

    if 'name' in data:
        product.name = data['name']
    if 'description' in data:
        product.description = data['description']
    if 'price' in data:
        product.price = data['price']
    if 'stock_quantity' in data:
        product.stock_quantity = data['stock_quantity']
        alert_message = None
        if product.stock_quantity < 5:
            alert_message = f" Low stock alert for product ID {id}: Stock is at {product.stock_quantity}"
    if 'category' in data:
        product.category = data['category']

    try:
        session.commit()
        response = {"message": "Product updated successfully"}
        if alert_message:
            response["alert"] = alert_message
        return jsonify(response), 200
    except Exception as e:
        session.rollback()
        return jsonify({"error": str(e)}), 500


# Soft Delete Product 
@app.route("/products/<int:id>", methods=["DELETE"])
def delete_product(id):
    product = session.query(Product).filter_by(id=id, is_active=True).first()
    if not product:
        return jsonify({"error": "Product not found"}), 404
    
    try:
        product.is_active = False
        session.commit()
        return jsonify({"message": "Product soft-deleted successfully"}), 200
    except Exception as e:
        session.rollback()
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
