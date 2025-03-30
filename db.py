
from dotenv import load_dotenv
import os
import motor.motor_asyncio
from models import *
from contextlib import asynccontextmanager
from pymongo import ReturnDocument
from datetime import datetime

load_dotenv()  # take environment variables


# Represents an ObjectId field in the database.
# It will be represented as a `str` on the model so that it can be serialized to JSON.


client = motor.motor_asyncio.AsyncIOMotorClient(os.getenv('MONGO'))
db = client.get_database('mpmc')
tolls = db.get_collection('tolls')


async def recordAToll(plate_number: str):
    try:
        new_toll = TollModelIn(plate_number=plate_number,
                               toll_fee=50, time=datetime.now())
    except Exception:
        print("Missing Parameters", Exception.with_traceback())
        return {"message": "error"}
    await tolls.insert_one(new_toll.model_dump())
    return {"message": "toll recorded"}


async def getVehicleTolls(plate_number: str):

    pipeline = [
        # Match tolls for the given plate number
        {"$match": {"plate_number": plate_number}},
        # Sum all amounts
        {"$group": {"_id": None, "total_fee": {
            "$sum": "$toll_fee"}, "toll_list": {"$push": "$$ROOT"}}}
    ]
    amount = await tolls.aggregate(pipeline).to_list(length=1)
    if (amount == []):
        return {"message": "No recorded toll available for this vehicle..."}
    else:
        data = TollsModel(
            due_amount=amount[0]['total_fee'], tolls=amount[0]['toll_list'][::-1])
        return data


async def payAToll(toll_id: str):
    data = await tolls.find_one_and_delete({"_id": ObjectId(toll_id)})
    return data


async def getLatestToll():
    data = await tolls.find_one({}, sort=[("_id", -1)])
    if data is None:
        return None
    else:
        return TollModelOut.model_validate(data)
