# app.py for Order Service
from flask import Flask, request, jsonify
from pymongo import MongoClient

app = Flask(__name__)

# Connect to MongoDB
client = MongoClient("mongo", 27017)  # 'mongo' is the service name in Kubernetes
db = client['microservices_db']
orders_collection = db['orders']

orders = []

@app.route('/orders', methods=['GET'])
def get_orders():
    orders = list(orders_collection.find({}, {"_id": 0}))  
    return jsonify(orders)

@app.route('/orders', methods=['POST'])
def add_order():
    order = request.json
    orders_collection.insert_one(order)
    return jsonify({"message": "Order added successfully"}), 201

@app.route('/orders/<int:order_id>', methods=['GET'])
def get_order(order_id):
    for order in orders:
        if order['id'] == order_id:
            return jsonify(order), 200
    return jsonify({"error": "Order not found"}), 404

@app.route('/orders/<int:order_id>', methods=['PUT'])
def update_order(order_id):
    for order in orders:
        if order['id'] == order_id:
            order.update(request.get_json())
            return jsonify(order), 200
    return jsonify({"error": "Order not found"}), 404

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
