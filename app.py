
import os

from flask import Flask, render_template, request, redirect, url_for
from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.errors import PyMongoError

load_dotenv()

app = Flask(__name__)

# Connect to MongoDB Atlas
mongo_uri = os.getenv("MONGO_URI")
client = None
collection = None

if mongo_uri:
    client = MongoClient(
        mongo_uri,
        serverSelectionTimeoutMS=5000
    )

    db = client["flask_assignment"]
    collection = db["form_submissions"]


@app.route("/", methods=["GET", "POST"])
def home():
    error = None

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        message = request.form.get("message", "").strip()

        # Validate form fields
        if not name or not email or not message:
            error = "Please fill in all fields."

        elif collection is None:
            error = "Database configuration is missing."

        else:
            try:
                # Insert data into MongoDB Atlas
                collection.insert_one({
                    "name": name,
                    "email": email,
                    "message": message
                })

                # Redirect only after successful insertion
                return redirect(url_for("success"))

            except PyMongoError:
                # Log technical details in the terminal
                app.logger.exception("MongoDB insertion failed")

                # Show a friendly error on the same page
                error = (
                    "Unable to save data. "
                    "Please check your database connection and try again."
                )

    # Display errors without redirecting
    return render_template("form.html", error=error)


@app.route("/success")
def success():
    return render_template("success.html")


if __name__ == "__main__":
    app.run(debug=True)
