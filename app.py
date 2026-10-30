
from flask import Flask, jsonify, render_template
import json
import os
import json

from flask import Flask, jsonify, request
from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.errors import PyMongoError

# Initialize Flask
app = Flask(__name__)

# Load environment variables
load_dotenv()

# MongoDB connection
MONGO_URI = os.getenv("MONGO_URI")

if not MONGO_URI:
    raise RuntimeError("MONGO_URI is missing from .env file")

client = MongoClient(
    MONGO_URI,
    serverSelectionTimeoutMS=5000
)

db = client["flask_todo_db"]

# MongoDB collection
todo_collection = db["todo_items"]


# ----------------------------------
# Task 1: JSON API Route
# ----------------------------------

@app.route("/api", methods=["GET"])
def get_data():

    try:
        file_path = os.path.join(app.root_path, "data.json")

        with open(file_path, "r") as file:
            data = json.load(file)

        return jsonify(data)

    except FileNotFoundError:
        return jsonify({"error": "data.json file not found"}), 404

    except json.JSONDecodeError:
        return jsonify({"error": "Invalid JSON format"}), 500


# ----------------------------------
# Task 3: Submit To-Do Item API
# ----------------------------------

@app.route("/submittodoitem", methods=["POST"])
def submit_todo_item():

    try:
        # Accept form data or JSON data
        data = request.get_json(silent=True) or request.form

        # Extract submitted fields
        item_name = data.get("itemName", "").strip()
        item_description = data.get("itemDescription", "").strip()

        # Validate input
        if not item_name or not item_description:
            return jsonify({
                "error": "Item Name and Item Description are required"
            }), 400

        # Prepare MongoDB document
        todo_data = {
            "itemName": item_name,
            "itemDescription": item_description
        }

        # Store data in MongoDB
        result = todo_collection.insert_one(todo_data)

        return jsonify({
            "message": "To-Do item submitted successfully",
            "inserted_id": str(result.inserted_id)
        }), 201

    except PyMongoError:
        return jsonify({
            "error": "Unable to save data in MongoDB"
        }), 500


# ----------------------------------
# Home Route
# ----------------------------------

@app.route("/", methods=["GET"])
def home():

    return """
        <h1>Flask To-Do Application</h1>
        <p>Backend API is running.</p>
        <a href="/api">View JSON API</a>
    """


# ----------------------------------
# Run Flask Application
# ----------------------------------
app = Flask(__name__)

# --------------------------------
# Task 1: JSON API Route
# --------------------------------

@app.route("/api", methods=["GET"])
def get_data():
    try:
        file_path = os.path.join(app.root_path, "data.json")

        with open(file_path, "r") as file:
            data = json.load(file)

        return jsonify(data)

    except FileNotFoundError:
        return jsonify({"error": "data.json file not found"}), 404

    except json.JSONDecodeError:
        return jsonify({"error": "Invalid JSON format"}), 500


# --------------------------------
# Task 3: To-Do Frontend Route
# --------------------------------

@app.route("/todo", methods=["GET"])
def todo():
    return render_template("todo.html")


# --------------------------------
# Home Route
# --------------------------------

@app.route("/", methods=["GET"])
def home():
    return """
        <h1>Flask Application</h1>
        <p>Welcome to the Flask and MongoDB project.</p>
        <a href="/api">View API Data</a><br>
        <a href="/todo">Open To-Do Page</a>
    """


# --------------------------------
# Run Flask Application
# --------------------------------

if __name__ == "__main__":
    app.run(debug=True)
