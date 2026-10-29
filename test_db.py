import os
from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.errors import PyMongoError

load_dotenv()

uri = os.getenv("MONGO_URI")

if not uri:
    print("MONGO_URI not found in .env")
else:
    try:
        client = MongoClient(uri, serverSelectionTimeoutMS=5000)
        client.admin.command("ping")
        print("SUCCESS: MongoDB Atlas connected!")
        client.close()
    except PyMongoError as error:
        print("CONNECTION ERROR:", repr(error))