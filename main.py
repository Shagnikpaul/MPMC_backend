

from fastapi import FastAPI, HTTPException
from bson.json_util import dumps,loads
from db import *
from models import *
app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/record-car/{plate_number}", response_model=CarModel)
async def recordCar(plate_number: str):
    data = await recordACar(plate_number=plate_number)
    return data
   

@app.get("/get-car/{plate_number}", response_model=CarModel)
async def getCar(plate_number: str):
    data = await getACar(plate_number=plate_number)
    if data is None:
        raise HTTPException(status_code=404, detail="Car not found")
    return data