
from modules.fish_counting_models import FishCountResponse
from services.roboflow_service import RoboflowService
import tempfile

class FishCountController:
    def __init__(self):
        self.fish_counting_service = RoboflowService()

    async def count_fish(self, frames) -> FishCountResponse:
        """
        Accepts an iterable of streamed frames (UploadFile or bytes), analyzes each frame using RoboflowService,
        and returns the total fish count (sum of detected fish in all frames).
        """
        total_count = 0
        for frame in frames:
            # Save frame to temp file
            with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as tmp:
                if hasattr(frame, 'read'):
                    contents = await frame.read()
                else:
                    contents = frame
                tmp.write(contents)
                tmp_path = tmp.name
            # Analyze frame
            result = self.fish_counting_service.infer_image_detection(tmp_path)
            predictions = self.fish_counting_service.get_predictions(result)
            total_count += len(predictions)
        return FishCountResponse(total_count=total_count)