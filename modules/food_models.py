from pydantic import BaseModel

class FoodRequest(BaseModel):
    length: float
    water_params: dict

class FoodResponse(BaseModel):
    estimated_food: float
