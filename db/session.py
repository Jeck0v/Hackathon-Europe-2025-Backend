from pymongo import MongoClient

client = MongoClient(
    host="mongo",
    port=27017,
    username="article11",
    password="-)i8N~x4r9cVX8"
)

db = client.article11_db

def get_db():
    return db
