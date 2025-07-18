
from inference_sdk import InferenceHTTPClient
from typing import List, Dict, Any
import os

from dotenv import load_dotenv

load_dotenv()

class RoboflowService:
    def __init__(self, api_url: str = None, api_key: str = None):
        api_key = api_key or os.getenv("ROBOFLOW_API_KEY")
        api_url = api_url or os.getenv("ROBOFLOW_API_URL")
        if not api_url or not api_key:
            raise ValueError("API URL and API Key must be provided")
        self.client = InferenceHTTPClient(api_url=api_url, api_key=api_key)

    def infer_image_detection(self, image_path: str) -> Dict[str, Any]:
        result = self.client.infer(image_path, model_id=os.getenv("ROBOFLOW_DETECTION_MODEL_ID"))
        return result
    
    def infer_image_diseases(self, image_path: str) -> Dict[str, Any]:
        result = self.client.infer(image_path, model_id=os.getenv("ROBOFLOW_DISEASES_MODEL_ID"))
        return result

    def get_predictions(self, result: Dict[str, Any]) -> List[Dict[str, Any]]:
        return result.get("predictions", [])
