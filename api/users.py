from fastapi import APIRouter, HTTPException, Depends
from bson import ObjectId
from db.session import db
from schemas.user import UserResponse, UserUpdate
from schemas.feed import FeedUpdate
from schemas.compromise import CompromiseUpdate
from core.security import oauth2_scheme, hash_password

router = APIRouter()


@router.get("/users", response_model=list[UserResponse])
async def get_all_users(token: str = Depends(oauth2_scheme)):
    users = db.users.find({}, {"hashed_password": 0})
    return [
        UserResponse(
            id_user=str(user["_id"]),
            username=user.get("username", "undefined"),
            firstname=user.get("firstname", ""),
            name=user.get("name", ""),
            age=int(user.get("age", 0)),
            gender=user.get("gender", "undefined"),
            country=user.get("country", "undefined"),
            email=user.get("email", "undefined@example.com"),
            consent=user.get("consent", False),
            identity_verif=user.get("identity_verif", False),
            role=user.get("role", "user"),
            historic=user.get("historic", []),
            streak=int(user.get("streak", 0))
        ) for user in users
    ]


@router.get("/users/{user_id}", response_model=UserResponse)
async def get_user_by_id(user_id: str, token: str = Depends(oauth2_scheme)):
    user = db.users.find_one({"_id": ObjectId(user_id)}, {"hashed_password": 0})
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé.")

    return UserResponse(
        id_user=str(user["_id"]),
        username=user.get("username", "undefined"),
        firstname=user.get("firstname", ""),
        name=user.get("name", ""),
        age=int(user.get("age", 0)),
        gender=user.get("gender", "undefined"),
        country=user.get("country", "undefined"),
        email=user.get("email", "undefined@example.com"),
        consent=user.get("consent", False),
        identity_verif=user.get("identity_verif", False),
        role=user.get("role", "user"),
        historic=user.get("historic", []),
        streak=int(user.get("streak", 0))
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
        id_user=str(updated_user["_id"]),
        username=updated_user.get("username"),
        firstname=updated_user.get("firstname", ""),
        name=updated_user.get("name", ""),
        age=updated_user.get("age", ""),
        gender=updated_user.get("gender", ""),
        country=updated_user.get("country", ""),
        email=updated_user.get("email", ""),
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
        id_user=str(user["_id"]),
        username=user.get("username"),
        firstname=user.get("firstname", ""),
        name=user.get("name", ""),
        age=user.get("age", ""),
        gender=user.get("gender", ""),
        country=user.get("country", ""),
        email=user.get("email", ""),
        consent=user.get("consent", False),
        identity_verif=user.get("identity_verif", False),
        role=user.get("role", "user"),
        historic=user.get("historic", []),
        streak=user.get("streak", 0)
    )


@router.put("/users/{user_id}/vote/{feed_id}", response_model=UserResponse)
async def user_vote(user_id: str, feed_id: str, user_vote: int, user_vote_detail: str,
                    token: str = Depends(oauth2_scheme)):
    user = db.users.find_one({"_id": ObjectId(user_id)})
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé.")

    feed = db.feed.find_one({"_id": ObjectId(feed_id)})
    if not feed:
        raise HTTPException(status_code=404, detail="Feed non trouvé.")

    user["streak"] += 1
    user["historic"].append({"feed_id": feed_id, "feed_title": feed["short_description"], "response": user_vote})

    if user_vote == "2" or user_vote == "3":
        compromise = db.compromise.find_one({"_id": ObjectId(compromise_id)})
        if not compromise:
            raise HTTPException(status_code=404, detail="Feed non trouvé.")
        compromise["id_subject"] = feed_id
        compromise["id_user"] = user_id
        if user_vote_detail:
            compromise["text"] = user_vote_detail

    # See with the team how the user_vote will be stored, for now it'll stay simple
    feed["votes"][str(user_vote)] += 1

    db.users.update_one({"_id": ObjectId(user_id)}, {"$set": user})

    db.feed.update_one({"_id": ObjectId(feed_id)}, {"$set": feed})

    return {"status": 200, "message": "voted"}


@router.get("/users/{user_id}/history", response_model=UserResponse)
async def get_user_history_by_id(user_id: str, token: str = Depends(oauth2_scheme)):
    user = db.users.find_one({"_id": ObjectId(user_id)}, {"hashed_password": 0})
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé.")

    return user["historic"]