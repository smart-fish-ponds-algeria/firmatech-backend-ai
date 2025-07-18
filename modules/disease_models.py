from pydantic import BaseModel
from fastapi import UploadFile, File

class DiseaseRequest(BaseModel):
    img: UploadFile


class DiseaseResponse(BaseModel):
    isSick: bool
    disease: str = None
