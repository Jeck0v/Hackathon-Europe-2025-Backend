from db.session import get_db

def initialize_database():
    db = get_db()
    required_collections = ['users', 'votes', 'news', 'social']
    existing_collections = db.list_collection_names()
    for collection in required_collections:
        if collection not in existing_collections:
            db.create_collection(collection)
            print(f"Collection '{collection}' créée.")

initialize_database()
