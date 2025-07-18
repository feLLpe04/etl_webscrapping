from flask import Flask, jsonify
import sqlite3
import pandas as pd

app = Flask(__name__)

# Helper function to get all books
def get_all_books():
    conn = sqlite3.connect("books.db")
    df = pd.read_sql_query("SELECT * FROM books", conn)
    conn.close()
    return df.to_dict(orient="records")

# Endpoint 1: Return all books
@app.route('/books', methods=['GET'])
def all_books():
    data = get_all_books()
    return jsonify(data)

# Endpoint 2: Get books by title
@app.route('/books/rating/<int:rating>', methods=['GET'])
def get_books_by_rating(rating):
    conn = sqlite3.connect('books.db')
    cursor = conn.cursor()
    
    query = "SELECT * FROM books WHERE rating = ?"
    cursor.execute(query, (rating,))
    
    rows = cursor.fetchall()
    conn.close()

    if not rows:
        return jsonify({'message': 'No books found with this rating'}), 404

    columns = ['title', 'in_stock', 'rating', 'price_gbp', 'price_usd']
    results = [dict(zip(columns, row)) for row in rows]
    
    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)
