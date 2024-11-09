from flask import Flask, jsonify
from pymongo import MongoClient, errors
import sys

app = Flask(__name__)

# MongoDB connection
try:
    client = MongoClient("mongodb://mongo:27017/", serverSelectionTimeoutMS=5000)  # 5 seconds timeout
    client.admin.command('ping')
    db = client["test_db"]
    collection = db["test_collection"]
except errors.ServerSelectionTimeoutError as err:
    print("Could not connect to MongoDB:", err)
    sys.exit(1)

@app.route('/', methods=['GET'])
def home():
    return jsonify({"message": "Welcome to Chaos World!"})

@app.route('/data', methods=['GET'])
def get_data():
    data = list(collection.find())
    for item in data:
        item["_id"] = str(item["_id"])
    return jsonify(data)

@app.route('/data', methods=['POST'])
def add_data():
    data = {"name": "Sample Data"}
    collection.insert_one(data)
    return jsonify(data), 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
