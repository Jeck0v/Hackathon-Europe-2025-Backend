from fastapi import APIRouter, HTTPException, Depends
from bson import ObjectId
from db.session import db
from schemas.feed import DataFeedResponse, DataFeed, DataFeedUpdate


# Verifier la secu du code

router = APIRouter()

@router.get("/feed", response_model=list[DataFeedResponse])
async def get_all_data_feed():
    data_feeds = db.data_feed.find()
    return [
        DataFeedResponse(
            id_subject=str(data["_id"]),
            short_description=data["short_description"],
            image=data["image"],
            context=data["context"],
            impact=data["impact"],
            source=data["source"],
            votes=data.get("votes", {"0": 0, "1": 0, "2": 0})
        ) for data in data_feeds
    ]

@router.get("/feed/{subject_id}", response_model=DataFeedResponse)
async def get_data_feed_by_id(subject_id: str):
    data_feed = db.data_feed.find_one({"_id": ObjectId(subject_id)})
    if not data_feed:
        raise HTTPException(status_code=404, detail="Data feed not found.")
    
    return DataFeedResponse(
        id_subject=str(data_feed["_id"]),
        short_description=data_feed["short_description"],
        image=data_feed["image"],
        context=data_feed["context"],
        impact=data_feed["impact"],
        source=data_feed["source"],
        votes=data_feed.get("votes", {"0": 0, "1": 0, "2": 0})
    )

@router.post("/feed", response_model=DataFeedResponse)
async def create_data_feed(data_feed: DataFeed):
    new_data_feed = data_feed.dict()
    result = db.data_feed.insert_one(new_data_feed)
    new_data_feed["_id"] = result.inserted_id
    return DataFeedResponse(**new_data_feed)

@router.put("/feed/{subject_id}", response_model=DataFeedResponse)
async def update_data_feed(subject_id: str, data_feed_update: DataFeedUpdate):
    existing_data_feed = db.data_feed.find_one({"_id": ObjectId(subject_id)})
    if not existing_data_feed:
        raise HTTPException(status_code=404, detail="Data feed not found.")

    update_data = data_feed_update.dict(exclude_unset=True)
    db.data_feed.update_one({"_id": ObjectId(subject_id)}, {"$set": update_data})

    updated_data_feed = db.data_feed.find_one({"_id": ObjectId(subject_id)})
    return DataFeedResponse(
        id_subject=str(updated_data_feed["_id"]),
        short_description=updated_data_feed["short_description"],
        image=updated_data_feed["image"],
        context=updated_data_feed["context"],
        impact=updated_data_feed["impact"],
        source=updated_data_feed["source"],
        votes=updated_data_feed.get("votes", {"0": 0, "1": 0, "2": 0})
    )

@router.delete("/feed/{subject_id}", response_model=DataFeedResponse)
async def delete_data_feed(subject_id: str):
    data_feed = db.data_feed.find_one({"_id": ObjectId(subject_id)})
    if not data_feed:
        raise HTTPException(status_code=404, detail="Data feed not found.")

    db.data_feed.delete_one({"_id": ObjectId(subject_id)})
    return DataFeedResponse(
        id_subject=str(data_feed["_id"]),
        short_description=data_feed["short_description"],
        image=data_feed["image"],
        context=data_feed["context"],
        impact=data_feed["impact"],
        source=data_feed["source"],
        votes=data_feed.get("votes", {"0": 0, "1": 0, "2": 0})
    )