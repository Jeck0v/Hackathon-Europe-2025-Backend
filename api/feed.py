from fastapi import APIRouter, HTTPException
from bson import ObjectId
from db.session import db
from schemas.feed import FeedResponse, FeedCreate, FeedUpdate

router = APIRouter()


@router.get("/feed", response_model=list[FeedResponse])
async def get_all_data_feed():
    data_feeds = db.feed.find()
    return [
        FeedResponse(
            id_subject=str(data["_id"]),
            short_description=data["short_description"],
            image=data["image"],
            context=data["context"],
            impact=data["impact"],
            source=data["source"],
            votes=data.get("votes", {"0": 0, "1": 0, "2": 0})
        ) for data in data_feeds
    ]


@router.get("/feed/search/{searchCharacter}", response_model=list[FeedResponse])
async def search_data(searchCharacter: str):
    cursor = db.feed.find({"short_description": {"$regex": searchCharacter, "$options": "i"}})
    results = []

    async for item in cursor:
        results.append(FeedResponse(
            id_subject=str(item["_id"]),
            short_description=item["short_description"],
            image=item["image"],
            context=item["context"],
            impact=item["impact"],
            source=item["source"],
            votes=item.get("votes", {"0": 0, "1": 0, "2": 0})
        ))
    
    if not results:
        raise HTTPException(status_code=404, detail="No feed items found")
    
    return results
        

@router.get("/feed/{subject_id}", response_model=FeedResponse)
async def get_data_feed_by_id(subject_id: str):
    data_feed = db.feed.find_one({"_id": ObjectId(subject_id)})
    if not data_feed:
        raise HTTPException(status_code=404, detail="Data feed not found.")

    return FeedResponse(
        id_subject=str(data_feed["_id"]),
        short_description=data_feed["short_description"],
        image=data_feed["image"],
        context=data_feed["context"],
        impact=data_feed["impact"],
        source=data_feed["source"],
        votes=data_feed.get("votes", {"0": 0, "1": 0, "2": 0})
    )


@router.post("/feed", response_model=FeedResponse)
async def create_data_feed(data_feed: FeedCreate):
    new_data_feed = data_feed.dict()
    result = db.feed.insert_one(new_data_feed)
    new_data_feed["_id"] = result.inserted_id
    return FeedResponse(**new_data_feed)


@router.put("/feed/{subject_id}", response_model=FeedResponse)
async def update_data_feed(subject_id: str, data_feed_update: FeedUpdate):
    existing_data_feed = db.feed.find_one({"_id": ObjectId(subject_id)})
    if not existing_data_feed:
        raise HTTPException(status_code=404, detail="Data feed not found.")

    update_data = data_feed_update.dict(exclude_unset=True)
    db.feed.update_one({"_id": ObjectId(subject_id)}, {"$set": update_data})

    updated_data_feed = db.feed.find_one({"_id": ObjectId(subject_id)})
    return FeedResponse(
        id_subject=str(updated_data_feed["_id"]),
        short_description=updated_data_feed["short_description"],
        image=updated_data_feed["image"],
        context=updated_data_feed["context"],
        impact=updated_data_feed["impact"],
        source=updated_data_feed["source"],
        votes=updated_data_feed.get("votes", {"0": 0, "1": 0, "2": 0})
    )


@router.delete("/feed/{subject_id}", response_model=FeedResponse)
async def delete_data_feed(subject_id: str):
    data_feed = db.feed.find_one({"_id": ObjectId(subject_id)})
    if not data_feed:
        raise HTTPException(status_code=404, detail="Data feed not found.")

    db.feed.delete_one({"_id": ObjectId(subject_id)})
    return FeedResponse(
        id_subject=str(data_feed["_id"]),
        short_description=data_feed["short_description"],
        image=data_feed["image"],
        context=data_feed["context"],
        impact=data_feed["impact"],
        source=data_feed["source"],
        votes=data_feed.get("votes", {"0": 0, "1": 0, "2": 0})
    )