

from fastapi import FastAPI, HTTPException
from db import *
from models import *
app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/record-toll/{plate_number}")
async def recordToll(plate_number: str):

    data = await recordAToll(plate_number=plate_number)
    return data


@app.get("/get-latest-toll", response_model=TollModelOut)
async def getTolls():
    data = await getLatestToll()
    if data is None:
        raise HTTPException(
            status_code=404, detail="No recorded tolls avaiable.") 
    else:
        return data

@app.get("/get-tolls/{plate_number}")
async def getTolls(plate_number: str):
    data = await getVehicleTolls(plate_number=plate_number)
    if data is None:
        raise HTTPException(
            status_code=404, detail="No pending toll payments for this vehicle.")
    return data


@app.delete("/pay-toll/{toll_id}")
async def payToll(toll_id: str):
    data = await payAToll(toll_id)
    if data is None:
        raise HTTPException(
            status_code=404, detail="The given toll payment does not exist.")
    return {"message": "Toll payment successful."}



