from fastapi import APIRouter


from modules.food_models import FoodRequest, FoodResponse

router = APIRouter(prefix="/food-prediction", tags=["Food Prediction"])


@router.post("/predict", response_model=FoodResponse)
async def predict_food(data: FoodRequest):
    # TODO: Implement food prediction logic
    return FoodResponse(estimated_food=0.0)
