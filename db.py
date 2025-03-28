
from dotenv import load_dotenv
import os
import motor.motor_asyncio

from contextlib import asynccontextmanager

load_dotenv()  # take environment variables


# Represents an ObjectId field in the database.
# It will be represented as a `str` on the model so that it can be serialized to JSON.





client = motor.motor_asyncio.AsyncIOMotorClient(os.getenv('MONGO'))
db = client.get_database('mpmc')
cars = db.get_collection('cars')







async def recordACar(plate_number: str):
    data = await cars.find_one({"plate_number":plate_number})

    if data is None:
        new_data = {
            "plate_number": plate_number,
            "due_amount": 50
        }
        d = await cars.insert_one(new_data)
        print(d)
        return new_data
    add_amount = cars.update_one({"plate_number": plate_number}, {"$set": {"due_amount":(int(data['due_amount'])+50)}})
    data = await cars.find_one({"plate_number":plate_number})
    return data
    


async def getACar(plate_number: str):
    data = await cars.find_one({"plate_number":plate_number})
    return data