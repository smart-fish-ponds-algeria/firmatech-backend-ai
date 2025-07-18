

from fastapi import APIRouter, UploadFile, File
from modules.disease_models import DiseaseResponse, DiseaseRequest
from controllers.disease_detection_controller import DiseaseDetectionController


router = APIRouter(prefix="/disease-detection", tags=["Disease Detection"])
controller = DiseaseDetectionController()


@router.post("/detect", response_model=DiseaseResponse)
async def detect_disease(image: UploadFile = File(...)):
    response = await controller.detect_disease(image)
    
    return response
