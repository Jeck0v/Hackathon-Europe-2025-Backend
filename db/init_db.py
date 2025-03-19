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
            match collection :
                case 'users' :
                    print("hello")
                    db[collection].insertMany(data_user)
                case 'feed':
                    db[collection].insertMany(data_feed)
                case 'data_compromise' :
                    db[collection].insertMany(data_compromise)

initialize_database()
