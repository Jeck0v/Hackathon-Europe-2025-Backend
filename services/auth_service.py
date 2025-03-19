from core.security import hash_password, verify_password, create_access_token
from models.user import UserInDB
from db.session import get_db


def register_user(user_data):
    db = get_db()

    existing_user = db.users.find_one({"$or": [{"email": user_data.email}, {"username": user_data.username}]})
    if existing_user:
        return None

    hashed_password = hash_password(user_data.password)
    user_data_dict = user_data.dict()
    user_data_dict["hashed_password"] = hashed_password
    del user_data_dict["password"]

    new_user = db.users.insert_one(user_data_dict)

    return create_access_token({"sub": str(new_user.inserted_id)})


def authenticate_user(username, password):
    db = get_db()

    user = db.users.find_one({"username": username})
    if not user:
        return None

    if not verify_password(password, user.get("hashed_password", "")):
        return None

    return create_access_token({"sub": str(user["_id"])})


def get_user_by_username(username):
    db = get_db()
    user = db.users.find_one({"username": username})
    if user:
        user["id"] = str(user["_id"])
        del user["_id"]
        del user["hashed_password"]
    return user
