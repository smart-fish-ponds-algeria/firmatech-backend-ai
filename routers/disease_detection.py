
from fastapi import APIRouter, UploadFile, File
from modules.disease_models import DiseaseResponse

router = APIRouter(prefix="/disease-detection", tags=["Disease Detection"])

@router.post("/detect", response_model=DiseaseResponse)
async def detect_disease(image: UploadFile = File(...)):
    # TODO: Implement disease detection logic
    return DiseaseResponse(isSick=False)
