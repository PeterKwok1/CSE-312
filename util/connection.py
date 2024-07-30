import os
import pymongo

mongo_uri = f"mongodb://{os.environ["MONGO_USERNAME"]}:{os.environ["MONGO_PASSWORD"]}@{os.environ["MONGO_HOST"]}:{os.environ["MONGO_PORT"]}/?authSource=admin"
client = pymongo.MongoClient(mongo_uri)
db = client.chat_app_db
