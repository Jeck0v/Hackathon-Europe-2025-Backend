from db.session import get_db

data_user = [
    {
        "id" : "test",
        "username":"Jecko",
        "name" : "Doe",
        "firstname" : "John",
        "age" : "21",
        "country" : "France",
        "gender" : "other",
        "email": "johndoe@gmail.com",
        "password" : "1234321", 
        "consent" : False,
        "identity_verif" : False,
        "historic" : [],
        "streak" : 0
    }
]

data_feed = [
    {
        "id_subject" : "1",
        "short_description" : "",
        "image" : "",
        "context" : "",
        "impact" : [],
        "source" : "",
        "votes" : {"0" : 0, "1" : 0, "2" : 0}
    }
]

data_compromise = [
    {
        "id_subject" : "1",
        "id_user" : "1",
        "text" : ""
    }
]



def initialize_database():
    db = get_db()
    required_collections = ['users', 'feed', 'compromise']
    existing_collections = db.list_collection_names()
    for collection in required_collections:
        if collection not in existing_collections:
            db.create_collection(collection)
            print(f"Collection '{collection}' créée.")

initialize_database()
