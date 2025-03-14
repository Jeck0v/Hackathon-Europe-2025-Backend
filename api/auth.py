from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from models.user import User
from models.user import UserResponse
from schemas.user import UserResponse, Token
from db.session import db
from services.auth_service import hash_password, verify_password, create_access_token
from datetime import timedelta
from core.config import ACCESS_TOKEN_EXPIRE_MINUTES
from bson import ObjectId

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

@router.post("/register", response_model=UserResponse)
async def register_user(user: User):
    existing_user = db.users.find_one({"email": user.email})
    if existing_user:
        raise HTTPException(status_code=400, detail="Email déjà utilisé.")

    hashed_password = hash_password(user.password)
    user_data = user.dict()
    user_data["hashed_password"] = hashed_password
    del user_data["password"]

    new_user = db.users.insert_one(user_data)
    created_user = db.users.find_one({"_id": new_user.inserted_id})

    return UserResponse(
        id=str(created_user["_id"]),
        username=created_user.get("username"),
        firstname=created_user["firstname"],
        name=created_user["name"],
        email=created_user["email"],
        role=created_user.get("role", "user")
    )


@router.post("/login", response_model=Token)
async def login_user(form_data: OAuth2PasswordRequestForm = Depends()):
    user = db.users.find_one({"username": form_data.username})
    if not user:
        raise HTTPException(status_code=401, detail="Nom d'utilisateur incorrect.")

    hashed_password = user.get("hashed_password")
    if not hashed_password or not verify_password(form_data.password, hashed_password):
        raise HTTPException(status_code=401, detail="Mot de passe incorrect.")

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": str(user["_id"])}, expires_delta=access_token_expires)

    return Token(access_token=access_token, token_type="bearer")

@router.get("/users", response_model=list[UserResponse])
async def get_all_users():
    users = db.users.find()
    return [
        UserResponse(
            id=str(user["_id"]),
            username=user.get("username"),
            firstname=user["firstname"],
            name=user["name"],
            email=user["email"],
            role=user.get("role", "user")
        ) for user in users
    ]


@router.get("/users/{user_id}", response_model=UserResponse)
async def get_user_by_id(user_id: str, token: str = Depends(oauth2_scheme)):
    user = db.users.find_one({"_id": ObjectId(user_id)})
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé.")

    # verif
    print({
        "id": str(user["_id"]),
        "username": user.get("username"),
        "firstname": user["firstname"],
        "name": user["name"],
        "email": user["email"],
        "role": user.get("role", "user")
    })

    return UserResponse(
        id=str(user["_id"]),
        username=user.get("username"),
        firstname=user["firstname"],
        name=user["name"],
        email=user["email"],
        role=user.get("role", "user")
    )
