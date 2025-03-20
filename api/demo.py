from fastapi import APIRouter, HTTPException, Depends
from bson import ObjectId
from db.session import db
from schemas.demo import DEMOCompromiseResponse, DEMOCompromiseCreate, DEMOCompromiseUpdate

router = APIRouter()


@router.get("/demo", response_model=list[DEMOCompromiseResponse])
async def get_all_demo_compromises():
    demo_compromises = db.DEMO_compromise.find()
    return [
        DEMOCompromiseResponse(
            id_subject=str(data["_id"]),
            text=data["text"]
        ) for data in demo_compromises
    ]


@router.get("/demo/{subject_id}", response_model=DEMOCompromiseResponse)
async def get_demo_compromise_by_id(subject_id: str):
    demo_compromise = db.DEMO_compromise.find_one({"_id": subject_id})
    if not demo_compromise:
        raise HTTPException(status_code=404, detail="Data compromise not found.")

    return [
        DEMOCompromiseResponse(
        id_subject=str(data["_id"]),
        text=data["text"]
        ) for data in demo_compromise
    ]

@router.post("/demo", response_model=DEMOCompromiseResponse)
async def create_demo_compromise(DEMO_compromise: DEMOCompromiseCreate):
    new_data_compromise = DEMO_compromise.dict()
    result = db.DEMO_compromise.insert_one(new_data_compromise)
    new_data_compromise["_id"] = result.inserted_id
    return DEMOCompromiseResponse(**new_data_compromise)


@router.put("/demo/{subject_id}", response_model=DEMOCompromiseResponse)
async def update_demo_compromise(subject_id: str, demo_compromise_update: DEMOCompromiseUpdate):
    existing_demo_compromise = db.DEMO_compromise.find_one({"_id": ObjectId(subject_id)})
    if not existing_demo_compromise:
        raise HTTPException(status_code=404, detail="Data compromise not found.")

    update_data = demo_compromise_update.dict(exclude_unset=True)
    db.DEMO_compromise.update_one({"_id": ObjectId(subject_id)}, {"$set": update_data})

    updated_demo_compromise = db.DEMO_compromise.find_one({"_id": ObjectId(subject_id)})
    return DEMOCompromiseResponse(
        id_subject=str(updated_demo_compromise["_id"]),
        text=updated_demo_compromise["text"]
    )


@router.delete("/demo/{subject_id}", response_model=DEMOCompromiseResponse)
async def delete_demo_compromise(subject_id: str):
    demo_compromise = db.DEMO_compromise.find_one({"_id": ObjectId(subject_id)})
    if not demo_compromise:
        raise HTTPException(status_code=404, detail="Data compromise not found.")

    db.DEMO_compromise.delete_one({"_id": ObjectId(subject_id)})
    return DEMOCompromiseResponse(
        id_subject=str(demo_compromise["_id"]),
        text=demo_compromise["text"]
    )