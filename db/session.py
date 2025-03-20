from pymongo import MongoClient

client = MongoClient(
    host="mongo",
    port=27017,
    username="article11",
    password="1J7A4s0omlrjRM03TfE0",
    authSource="admin"
)

db = client.article11_db

def get_db():
    return db