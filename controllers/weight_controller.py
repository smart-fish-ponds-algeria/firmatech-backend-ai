
from modules.weight_models import WeightRequest, WeightResponse
from services.roboflow_service import RoboflowService
from dotenv import load_dotenv
import tempfile
import os

load_dotenv()

class WeightController:
    def __init__(self):
        self.roboflow_service = RoboflowService(
            api_url = os.getenv("ROBOFLOW_API_URL"),
            api_key = os.getenv("ROBOFLOW_API_KEY")
        )

    async def predict_weight_from_upload(self, image: WeightRequest) -> WeightResponse:
        # Save uploaded image to a temp file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as tmp:
            contents = await image.read()
            tmp.write(contents)
            tmp_path = tmp.name

        # Use Roboflow to infer fish length from image
        result = self.roboflow_service.infer_image(tmp_path)
        predictions = self.roboflow_service.get_predictions(result)
        if predictions:
            length = predictions[0].get('width', 0)
        else:
            length = 0
        weight = 0.0196 * (length ** 2.9868) if length > 0 else 0
        return WeightResponse(weight=weight)
