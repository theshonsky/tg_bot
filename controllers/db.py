import os
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

from pymongo import MongoClient
def get_database():

    MONGO_URI = os.getenv("MONGO_URI")

    client = MongoClient(MONGO_URI)

    return client['test']
  