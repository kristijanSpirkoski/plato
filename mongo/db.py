from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

from mongo.credentials import uri

# Set the Stable API version when creating a new client
db = MongoClient(uri, server_api=ServerApi('1'))

# Send a ping to confirm a successful connection
def ping():
    try:
        db.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
    except Exception as e:
        print(e)