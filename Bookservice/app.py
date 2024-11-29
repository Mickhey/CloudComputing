# app.py
from flask import Flask, request, jsonify
from pymongo import MongoClient

app = Flask(__name__)

# Connect to MongoDB
client = MongoClient("mongo", 27017)  # 'mongo' is the service name in Kubernetes
db = client['microservices_db']
books_collection = db['books']

books = []

@app.route('/books', methods=['GET'])
def get_books():
    books = list(books_collection.find({}, {"_id": 0})) 
    return jsonify(books)

@app.route('/books', methods=['POST'])
def add_book():
    book = request.json
    books_collection.insert_one(book)
    return jsonify({"message": "Book added successfully"}), 201

@app.route('/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    for book in books:
        if book['id'] == book_id:
            return jsonify(book), 200
    return jsonify({"error": "Book not found"}), 404

@app.route('/books/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    for book in books:
        if book['id'] == book_id:
            book.update(request.get_json())
            return jsonify(book), 200
    return jsonify({"error": "Book not found"}), 404

@app.route('/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    for book in books:
        if book['id'] == book_id:
            books.remove(book)
            return jsonify({"message": "Book deleted"}), 200
    return jsonify({"error": "Book not found"}), 404

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
