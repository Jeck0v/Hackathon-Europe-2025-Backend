from core.security import hash_password, verify_password, create_access_token
from models.user import UserInDB
from db.session import get_db

def register_user(user_data):
    db = get_db()
    existing_user = db.users.find_one({"$or": [{"email": user_data.email}, {"username": user_data.username}]})
    if existing_user:
        return None
    user_data.password = hash_password(user_data.password)
    db.users.insert_one(user_data.dict())
    return create_access_token({"sub": user_data.username})

def authenticate_user(username, password):
    db = get_db()
    user = db.users.find_one({"username": username})
    if not user or not verify_password(password, user["password"]):
        return None
    return create_access_token({"sub": user["username"]})

def get_user_by_username(username):
    db = get_db()
    return db.users.find_one({"username": username})