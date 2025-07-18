from modules.disease_models import DiseaseResponse, DiseaseRequest
from services.roboflow_service import RoboflowService
import tempfile


class DiseaseDetectionController:
    def __init__(self):
        self.disease_detection_service = RoboflowService()


    async def detect_disease(self, img: DiseaseRequest) -> DiseaseResponse:
        """
        Detect diseases based on the provided image upload.
        """
        # Save uploaded image to a temp file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as tmp:
            contents = await img.read()
            tmp.write(contents)
            tmp_path = tmp.name

        # Call the service to process the data and detect diseases
        result = self.disease_detection_service.infer_image_diseases(tmp_path)
        predictions = self.disease_detection_service.get_predictions(result)

        # Example: Use first prediction for response, customize as needed
        if predictions:
            pred = predictions[0]
            is_sick = pred.get('confidence', 0) > 0.5  # threshold can be adjusted
            disease = pred.get('class', None)
        else:
            is_sick = False
            disease = None

        return DiseaseResponse(isSick=is_sick, disease=disease)