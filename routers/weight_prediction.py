from fastapi import APIRouter
from modules.weight_models import WeightResponse
from controllers.weight_controller import WeightController
from fastapi import File, UploadFile, Form

router = APIRouter(prefix="/weight-prediction", tags=["Weight Prediction"])

weight_controller = WeightController()

@router.post("/predict", response_model=WeightResponse)
async def predict_weight(
    image: UploadFile = File(...),
):
    return await weight_controller.predict_weight_from_upload(image)
