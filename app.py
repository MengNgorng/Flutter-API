from flask import Flask, jsonify, request
from flask_cors import CORS
import mysql.connector
import bcrypt

app = Flask(__name__)
CORS(app)


# MySQL connection setup
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",  # Change to your MySQL host if necessary
        user="root",  # MySQL user (default is 'root' for localhost)
        password="",  # MySQL password (leave blank if none)
        database="api"  # The name of your database ('ma' in this case)
    )


# Root route
@app.get('/')
def home():
    return jsonify({"message": "Welcome to the API"})


# Route to get all products
@app.get('/products/')
def getProducts():
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('SELECT * FROM product')
        data = cursor.fetchall()
        product_list = []
        for item in data:
            product_list.append(
                {
                    "id": item[0],
                    "title": item[1],
                    "price": item[4],
                    "description": item[6],
                    "category": item[3],
                    "image": item[5],
                    "rating": {
                        "rate": 3.9,  # Placeholder, you can replace with actual rating logic
                        "count": 120  # Placeholder for rating count
                    }
                }
            )
        return jsonify(product_list)
    except Exception as e:
        return jsonify({"error": "Database error", "message": str(e)}), 500
    finally:
        cursor.close()
        conn.close()


# Route to get a single product by its ID
@app.get('/products/<int:product_id>')
def getProduct(product_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('SELECT * FROM product WHERE id = %s', (product_id,))
        data = cursor.fetchone()
        if data:
            product = {
                "id": data[0],
                "title": data[1],
                "price": data[4],
                "description": data[6],
                "category": data[3],
                "image": data[5],
                "rating": {
                    "rate": 3.9,  # Placeholder
                    "count": 120  # Placeholder
                }
            }
            return jsonify(product)
        else:
            return jsonify({"error": "Product not found"}), 404
    except Exception as e:
        return jsonify({"error": "Database error", "message": str(e)}), 500
    finally:
        cursor.close()
        conn.close()


if __name__ == '__main__':
    app.run()
