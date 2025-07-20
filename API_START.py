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

# Endpoint 3: Get books within a price range (in GBP)
@app.route('/books/price/<float:min_price>/<float:max_price>', methods=['GET'])
def get_books_by_price(min_price, max_price):
    conn = sqlite3.connect('books.db')
    query = """
        SELECT title, in_stock, rating, price_gbp, price_usd
        FROM books
        WHERE price_gbp BETWEEN ? AND ?
    """
    df = pd.read_sql_query(query, conn, params=(min_price, max_price))
    conn.close()

    if df.empty:
        return jsonify({'message': 'No books found in this price range'}), 404

    return jsonify(df.to_dict(orient="records"))

# Endpoint 4: Get all books that are in stock
@app.route('/books/in-stock', methods=['GET'])
def get_books_in_stock():
    conn = sqlite3.connect('books.db')
    query = """
        SELECT title, in_stock, rating, price_gbp, price_usd
        FROM books
        WHERE in_stock = 'In stock'
    """
    df = pd.read_sql_query(query, conn)
    conn.close()

    if df.empty:
        return jsonify({'message': 'No books in stock found'}), 404

    return jsonify(df.to_dict(orient="records"))

# Endpoint 5: Get summary statistics
@app.route('/summary/stats', methods=['GET'])
def get_summary_stats():
    conn = sqlite3.connect('books.db')
    df = pd.read_sql_query("SELECT * FROM books", conn)
    conn.close()

    if df.empty:
        return jsonify({'message': 'No data available'}), 404

    summary = {
        'total_books': len(df),
        'average_price_gbp': round(df['price_gbp'].mean(), 2),
        'average_price_usd': round(df['price_usd'].mean(), 2),
        'average_rating': round(df['rating'].mean(), 2),
        'most_expensive_book': df.loc[df['price_gbp'].idxmax(), 'title'],
        'cheapest_book': df.loc[df['price_gbp'].idxmin(), 'title']
    }

    return jsonify(summary)

# Endpoint 6: Search books by keyword in title
@app.route('/books/title/<string:keyword>', methods=['GET'])
def get_books_by_title(keyword):
    conn = sqlite3.connect('books.db')
    query = """
        SELECT title, in_stock, rating, price_gbp, price_usd
        FROM books
        WHERE LOWER(title) LIKE ?
    """
    # keyword para búsqueda 
    df = pd.read_sql_query(query, conn, params=[f"%{keyword.lower()}%"])
    conn.close()

    if df.empty:
        return jsonify({'message': f'No books found with keyword: {keyword}'}), 404

    return jsonify(df.to_dict(orient="records"))

# Endpoint 7: Get books by exact rating
@app.route('/books/rating/<int:rating>', methods=['GET'])
def get_books_by_rating_exact(rating):
    conn = sqlite3.connect('books.db')
    query = '''
        SELECT title, in_stock, rating, price_gbp, price_usd
        FROM books
        WHERE rating = ?
    '''
    df = pd.read_sql_query(query, conn, params=(rating,))
    conn.close()

    if df.empty:
        return jsonify({'message': f'No books found with rating: {rating}'}), 404

    return jsonify(df.to_dict(orient="records"))

if __name__ == '__main__':
    app.run(debug=True)
