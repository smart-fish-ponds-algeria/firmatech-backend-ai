from fastapi import APIRouter


from modules.weight_models import WeightRequest, WeightResponse

router = APIRouter(prefix="/weight-prediction", tags=["Weight Prediction"])


@router.post("/predict", response_model=WeightResponse)
async def predict_weight(data: WeightRequest):
    # Weight (g) = 0.0196 × Length^2.9868
    weight = 0.0196 * (data.length ** 2.9868)
    return WeightResponse(weight=weight)
