from db.session import get_db

data_user = [
    {
    }
]

data_feed = [
    {
        "id_subject" : "1",
        "short_description" : "asasd",
        "image" : "asasd",
        "context" : "asdasd",
        "impact" : [],
        "source" : "asasd",
        "votes" : {"0" : 0, "1" : 0, "2" : 0}
    },
    {
        "id_subject" : "2",
        "short_description" : "asasd",
        "image" : "asasd",
        "context" : "asdasd",
        "impact" : [],
        "source" : "asasd",
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
            
            # Make it better (just did it to be quick)
            try:
                match collection:
                    case 'users':
                        db[collection].insert_many(data_user)
                    case 'feed':
                        db[collection].insert_many(data_feed)
                    case 'compromise':
                        db[collection].insert_many(data_compromise)
            except Exception as e:
                print(f"Error inserting data into {collection}: {e}")

initialize_database()
