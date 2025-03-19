from fastapi import APIRouter, HTTPException, Depends
from bson import ObjectId
from db.session import db
from schemas.user import UserResponse, UserUpdate
from core.security import oauth2_scheme, hash_password

router = APIRouter()

@router.get("/users", response_model=list[UserResponse])
async def get_all_users(token: str = Depends(oauth2_scheme)):
    users = db.users.find({}, {"hashed_password": 0})
    return [
        UserResponse(
            id=str(user["_id"]),
            username=user.get("username"),
            firstname=user["firstname"],
            name=user["name"],
            age=user["age"],
            gender=user["gender"],
            country=user["country"],
            email=user["email"],
            consent=user.get("consent", False),
            identity_verif=user.get("identity_verif", False),
            role=user.get("role", "user"),
            historic=user.get("historic", []),
            streak=user.get("streak", 0)
        ) for user in users
    ]

@router.get("/users/{user_id}", response_model=UserResponse)
async def get_user_by_id(user_id: str, token: str = Depends(oauth2_scheme)):
    user = db.users.find_one({"_id": ObjectId(user_id)}, {"hashed_password": 0})
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé.")

    return UserResponse(
        id=str(user["_id"]),
        username=user.get("username"),
        firstname=user["firstname"],
        name=user["name"],
        age=user["age"],
        gender=user["gender"],
        country=user["country"],
        email=user["email"],
        consent=user.get("consent", False),
        identity_verif=user.get("identity_verif", False),
        role=user.get("role", "user"),
        historic=user.get("historic", []),
        streak=user.get("streak", 0)
    )

@router.put("/users/{user_id}", response_model=UserResponse)
async def update_user(user_id: str, user_update: UserUpdate, token: str = Depends(oauth2_scheme)):
    existing_user = db.users.find_one({"_id": ObjectId(user_id)})
    if not existing_user:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé.")

    update_data = user_update.dict(exclude_unset=True)

    if "password" in update_data:
        hashed_password = hash_password(update_data["password"])
        update_data["hashed_password"] = hashed_password
        del update_data["password"]

    if update_data:
        db.users.update_one({"_id": ObjectId(user_id)}, {"$set": update_data})

    updated_user = db.users.find_one({"_id": ObjectId(user_id)}, {"hashed_password": 0})
    return UserResponse(
        id=str(updated_user["_id"]),
        username=updated_user.get("username"),
        firstname=updated_user["firstname"],
        name=updated_user["name"],
        age=updated_user["age"],
        gender=updated_user["gender"],
        country=updated_user["country"],
        email=updated_user["email"],
        consent=updated_user.get("consent", False),
        identity_verif=updated_user.get("identity_verif", False),
        role=updated_user.get("role", "user"),
        historic=updated_user.get("historic", []),
        streak=updated_user.get("streak", 0)
    )

@router.delete("/users/{user_id}", response_model=UserResponse)
async def delete_user(user_id: str, token: str = Depends(oauth2_scheme)):
    user = db.users.find_one({"_id": ObjectId(user_id)}, {"hashed_password": 0})
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé.")

    db.users.delete_one({"_id": ObjectId(user_id)})
    return UserResponse(
        id=str(user["_id"]),
        username=user.get("username"),
        firstname=user["firstname"],
        name=user["name"],
        age=user["age"],
        gender=user["gender"],
        country=user["country"],
        email=user["email"],
        consent=user.get("consent", False),
        identity_verif=user.get("identity_verif", False),
        role=user.get("role", "user"),
        historic=user.get("historic", []),
        streak=user.get("streak", 0)
    )