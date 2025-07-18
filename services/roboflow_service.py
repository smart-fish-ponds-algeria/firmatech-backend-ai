
from inference_sdk import InferenceHTTPClient
from typing import List, Dict, Any
import os


class RoboflowService:
    def __init__(self, api_url: str = None, api_key: str = None):
        self.client = InferenceHTTPClient(api_url=api_url, api_key=api_key)

    def infer_image(self, image_path: str) -> Dict[str, Any]:
        result = self.client.infer(image_path, model_id=os.getenv("ROBOFLOW_MODEL_ID"))
        return result

    def get_image_width(self, result: Dict[str, Any]) -> Dict[str, int]:
        return {
            "width": result["image"]["width"],
        }

    def get_predictions(self, result: Dict[str, Any]) -> List[Dict[str, Any]]:
        return result.get("predictions", [])

# Example usage:
# service = RoboflowService(api_url="https://serverless.roboflow.com", api_key="xvLawhjWhtU0ptPpzaw0")
# result = service.infer_image("test.jpeg", model_id="talipia-fish-detection/2")
# dims = service.get_image_dimensions(result)
# print("Width:", dims["width"])
# print("Height:", dims["height"])
# for pred in service.get_predictions(result):
#     print(f"Class: {pred['class']}, Confidence: {pred['confidence']}")
