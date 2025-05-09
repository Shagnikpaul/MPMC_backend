

from fastapi import FastAPI, HTTPException, File, UploadFile
from db import *
from models import *
from fastapi.middleware.cors import CORSMiddleware
import easyocr
import cv2
import numpy as np


reader = easyocr.Reader(['en'])
origins = ["*"]


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/detect_plate/")
async def detect_license_plate(file: UploadFile = File(...)):
    try:
        # Read image file
        contents = await file.read()
        image = np.frombuffer(contents, np.uint8)
        image = cv2.imdecode(image, cv2.IMREAD_COLOR)

        if image is None:
            raise HTTPException(status_code=400, detail="Invalid image file")

        # Perform OCR
        results = reader.readtext(image, detail=0)  # Extract text only
        print('text array : ', results)
        x: str = "".join(results)
        x = x.replace("IND", "")
        await recordAToll(plate_number=x)
        return {"license_plate": x}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


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


@app.get("/get-all-tolls/")
async def getAllTolls():
    data = await getAllTheTolls()
    if data is None:
        raise HTTPException(
            status_code=404, detail="No tolls available in the database.")
    return data


@app.get("/get-vehicle-tolls/{plate_number}")
async def getVehiclesTolls(plate_number: str):
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
