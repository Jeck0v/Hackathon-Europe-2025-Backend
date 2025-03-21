from fastapi import APIRouter, HTTPException, Depends
from bson import ObjectId
from db.session import db
from schemas.compromise import CompromiseResponse, CompromiseCreate, CompromiseUpdate

router = APIRouter(tags=["Compromise"])


@router.get("/compromise", response_model=list[CompromiseResponse])
async def get_all_data_compromises():
    data_compromises = db.data_compromise.find()
    return [
        CompromiseResponse(
            id_subject=str(data["_id"]),
            id_user=data["id_user"],
            text=data["text"]
        ) for data in data_compromises
    ]


@router.get("/compromise/{subject_id}", response_model=CompromiseResponse)
async def get_data_compromise_by_id(subject_id: str):
    data_compromise = db.data_compromise.find_one({"_id": ObjectId(subject_id)})
    if not data_compromise:
        raise HTTPException(status_code=404, detail="Data compromise not found.")

    return CompromiseResponse(
        id_subject=str(data_compromise["_id"]),
        id_user=data_compromise["id_user"],
        text=data_compromise["text"]
    )


@router.post("/compromise", response_model=CompromiseResponse)
async def create_data_compromise(data_compromise: CompromiseCreate):
    new_data_compromise = data_compromise.dict()
    result = db.data_compromise.insert_one(new_data_compromise)
    new_data_compromise["_id"] = result.inserted_id
    return CompromiseResponse(**new_data_compromise)


@router.put("/compromise/{subject_id}", response_model=CompromiseResponse)
async def update_data_compromise(subject_id: str, data_compromise_update: CompromiseUpdate):
    existing_data_compromise = db.data_compromise.find_one({"_id": ObjectId(subject_id)})
    if not existing_data_compromise:
        raise HTTPException(status_code=404, detail="Data compromise not found.")

    update_data = data_compromise_update.dict(exclude_unset=True)
    db.data_compromise.update_one({"_id": ObjectId(subject_id)}, {"$set": update_data})

    updated_data_compromise = db.data_compromise.find_one({"_id": ObjectId(subject_id)})
    return CompromiseResponse(
        id_subject=str(updated_data_compromise["_id"]),
        id_user=updated_data_compromise["id_user"],
        text=updated_data_compromise["text"]
    )


@router.delete("/compromise/{subject_id}", response_model=CompromiseResponse)
async def delete_data_compromise(subject_id: str):
    data_compromise = db.data_compromise.find_one({"_id": ObjectId(subject_id)})
    if not data_compromise:
        raise HTTPException(status_code=404, detail="Data compromise not found.")

    db.data_compromise.delete_one({"_id": ObjectId(subject_id)})
    return CompromiseResponse(
        id_subject=str(data_compromise["_id"]),
        id_user=data_compromise["id_user"],
        text=data_compromise["text"]
    )