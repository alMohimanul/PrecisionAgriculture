from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from Controller.V1.diseaseDetectionController import predictive_model
from fastapi import APIRouter

router = APIRouter()

@router.post("/detect")
async def detect(file: UploadFile = File(...)):
    image_bytes = await file.read()
    response = predictive_model(image_bytes) 
    return JSONResponse(content=response)
