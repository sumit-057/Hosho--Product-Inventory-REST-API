# Hosho--Product-Inventory-REST-API
# Product Inventory REST API

This project's goal is to create a simple RESTful API to manage a product inventory. This API is built using Flask (a Python framework) and uses SQLAlchemy ORM for database management (compatible with databases like SQLite, MySQL, and PostgreSQL).

### Features

* **Add Product**: Add new products with their name, description, price, stock, and category.
* **Get All Products**: View a list of all products. You can also filter by category, sort by price, and search by name or description.
* **Get Product by ID**: Fetch a single product using its unique ID.
* **Update Product**: Modify existing product details, like its price or stock quantity.
* **Soft Delete Product**: Instead of permanently removing a product from the database, it's marked as inactive (`is_active=0`).
* **Search**: Search for products by name or description.
* **Pagination**: The product list is divided into smaller pages for efficient data loading.
* **Low-stock Alert**: A console alert is triggered when a product's stock drops below 5.

---

### Prerequisites

To run this project, you need to have the following installed on your computer:

* **Python 3.x**
* **pip** (Python package installer)

---

### Setup Steps

Follow these steps to set up and run the project:

1.  **Clone the Repository**

    Open your terminal or command prompt and clone the repository to your local machine:
    ```bash
    git clone [https://github.com/sumit-057/Hosho--Product-Inventory-REST-API.git](https://github.com/sumit-057/Hosho--Product-Inventory-REST-API.git)
    ```
    Then, navigate into the project directory:
    ```bash
    cd Hosho--Product-Inventory-REST-API
    ```

2.  **Install Dependencies**

    Install the required Python libraries:
    ```bash
    pip install Flask
    ```
    or if pip not work proceed with:
    ```bash
    pip3 install Flask
    ```

3.  **Run the Application**

    Start the Flask application by running this command:
    ```bash
    python app.py
    ```
    or:
    ```bash
    python3 app.py
    ```
    The application will now be running at `http://127.0.0.1:5000`.

---

### API Endpoints

You can use a tool like **Postman** to test these API endpoints.

| Endpoint                  | Method   | Description                                                                     | Example Request Body (JSON) |
| ------------------------- | -------- | ------------------------------------------------------------------------------- | --------------------------- |
| `/products`               | **`POST`** | Creates a new product.                                                          | `{ "name": "...", "price": ... }` |
| `/products`               | **`GET`** | Gets a list of all active products. Use query parameters for filtering and sorting: `?category=Electronics&sort_by=price&search=phone&page=1&limit=10` | N/A |
| `/products/<int:id>`      | **`GET`** | Gets a single product by its ID.                                                | N/A |
| `/products/<int:id>`      | **`PUT`** | Updates an existing product.                                                    | `{ "price": 12.99, "stock_quantity": 25 }` |
| `/products/<int:id>`      | **`DELETE`**| Soft-deletes a product by setting `is_active=0`.                               | N/A |

---

### Postman Collection

### URL :- https://sumitsolanki-3191248.postman.co/workspace/Sumit-Solanki's-Workspace~b7a50add-c90c-4483-867e-1e15b5e0db3d/collection/47928026-5fa1bba6-72b1-468b-876a-9c4c92f2bdc3?action=share&creator=47928026

You can easily test the API by importing our Postman Collection.

1.  Download the `ProductInventory_API.json` file from the GitHub repository.
2.  Open Postman.
3.  Click the **`Import`** button.
4.  Upload the downloaded JSON file.

You can now use the collection to run all the pre-configured requests.
