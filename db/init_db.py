from db.session import get_db

def initialize_database():
    db = get_db()
    required_collections = ['users', 'votes', 'news', 'social']
    existing_collections = db.list_collection_names()
    for collection in required_collections:
        if collection not in existing_collections:
            db.create_collection(collection)
            print(f"Collection '{collection}' créée.")

    if db.users.count_documents({}) == 0:
        users = [
            {
                "_id": "65f123abc456def789ghi012",
                "username": "john_doe",
                "email": "john@example.com",
                "hashed_password": "hashed_version_of_password",
                "created_at": "2024-03-07T12:00:00",
                "is_active": True
            },
        ]
        db.users.insert_many(users)
        print("Données de test pour 'users' insérées.")

initialize_database()