from fastapi import APIRouter, UploadFile, File

from modules.fish_counting_models import FishCountResponse 

router = APIRouter(prefix="/fish-counting", tags=["Fish Counting"])

@router.post("/count", response_model=FishCountResponse)
async def count_fish(video: UploadFile = File(...)):
    # TODO: Implement fish counting logic
    return FishCountResponse(total_count=0)
