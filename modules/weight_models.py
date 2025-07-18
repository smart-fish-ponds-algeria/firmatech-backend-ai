from pydantic import BaseModel

class WeightRequest(BaseModel):
    length: float

class WeightResponse(BaseModel):
    weight: float
