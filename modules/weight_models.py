from pydantic import BaseModel
from fastapi import UploadFile

class WeightRequest(BaseModel):
    img: UploadFile

class WeightResponse(BaseModel):
    weight: float
