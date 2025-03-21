from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from db.session import db
from schemas.user import UserResponse, Token, UserCreate
from core.security import hash_password, verify_password, create_access_token
from datetime import timedelta
from core.config import settings
from bson import ObjectId

router = APIRouter(tags=["Auth"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

@router.post("/register", response_model=UserResponse)
async def register_user(user: UserCreate):
    existing_user = db.users.find_one({"email": user.email})
    if existing_user:
        raise HTTPException(status_code=400, detail="Email déjà utilisé.")

    hashed_password = hash_password(user.password)
    user_data = user.dict()
    user_data["hashed_password"] = hashed_password
    del user_data["password"]

    new_user = db.users.insert_one(user_data)
    created_user = db.users.find_one({"_id": new_user.inserted_id}, {"hashed_password": 0})

    return UserResponse(
        id_user=str(created_user["_id"]),
        username=created_user.get("username"),
        firstname=created_user["firstname"],
        name=created_user["name"],
        age=created_user["age"],
        gender=created_user["gender"],
        country=created_user["country"],
        email=created_user["email"],
        consent=created_user.get("consent", False),
        identity_verif=created_user.get("identity_verif", False),
        role=created_user.get("role", "user"),
        historic=created_user.get("historic", []),
        streak=created_user.get("streak", 0)
    )

@router.post("/login", response_model=Token)
async def login_user(form_data: OAuth2PasswordRequestForm = Depends()):
    user = db.users.find_one({"username": form_data.username})
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect Username.")

    hashed_password = user.get("hashed_password")
    if not hashed_password or not verify_password(form_data.password, hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect Password.")

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": str(user["_id"])}, expires_delta=access_token_expires)

    return Token(access_token=access_token, token_type="bearer", id_user=str(user["_id"]))