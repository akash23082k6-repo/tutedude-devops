
from flask import Flask, jsonify, render_template
import json
import os

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
