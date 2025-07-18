from pydantic import BaseModel
from fastapi import UploadFile, File

class FishCountRequest(BaseModel):
    file: UploadFile = File(...)

class FishCountResponse(BaseModel):
    total_count: int