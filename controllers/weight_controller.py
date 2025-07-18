
from modules.weight_models import WeightRequest, WeightResponse
from services.roboflow_service import RoboflowService
from utils.weight_utils import estimate_weight_from_pixels
import tempfile


class WeightController:
    def __init__(self):
        self.roboflow_service = RoboflowService()

    async def predict_weight_from_upload(self, image: WeightRequest) -> WeightResponse:
        # Save uploaded image to a temp file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as tmp:
            contents = await image.read()
            tmp.write(contents)
            tmp_path = tmp.name

        # Use Roboflow to infer fish length from image
        result = self.roboflow_service.infer_image_detection(tmp_path)
        predictions = self.roboflow_service.get_predictions(result)
        if predictions:
            length = predictions[0].get('width', 0)
        else:
            length = 0
        weight = estimate_weight_from_pixels(length) if length > 0 else 0
        return WeightResponse(weight=weight)
