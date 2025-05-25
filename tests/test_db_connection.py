
from pymongo.mongo_client import MongoClient
from dotenv import load_dotenv
import os
import ssl

# Load environment variables
load_dotenv()

mongo_uri = os.getenv("MONGO_URI")

# Create a new client and connect to the server
client = MongoClient(mongo_uri)

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)
