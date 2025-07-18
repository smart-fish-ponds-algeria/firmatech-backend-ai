from fastapi import APIRouter, UploadFile, File
from modules.fish_counting_models import FishCountResponse
from controllers.fish_counting_controller import FishCountController
import tempfile
import os
import time

router = APIRouter(prefix="/fish-counting", tags=["Fish Counting"])

@router.post("/count", response_model=FishCountResponse)
async def count_fish(video: UploadFile = File(...), fps: int = 5):
    """
    Endpoint to count fish in an uploaded video using RoboflowService.

    Args:
        video (UploadFile): Video file to process.
        fps (int): Frames per second to sample for detection (default: 5).

    Returns:
        FishCountResponse: Object containing the total fish count.
    """
    controller = FishCountController()

    # Save uploaded video to temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as tmp:
        tmp.write(await video.read())
        video_path = tmp.name

    try:
        # Count fish using controller
        result = await controller.count_fish(video_path, fps=fps)
        return result
    finally:
        # Clean up temporary file
        if os.path.exists(video_path):
            try:
                os.unlink(video_path)
            except PermissionError:
                time.sleep(0.1)  # Brief delay to handle file lock
                os.unlink(video_path)