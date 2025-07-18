
from ..modules.disease_models import DiseaseResponse, DiseaseRequest

class DiseaseDetectionController:
    def __init__(self, disease_detection_service):
        self.disease_detection_service = disease_detection_service

    def detect_disease(self, data: DiseaseRequest) -> DiseaseResponse:
        """
        Detect diseases based on the provided request data.
        """
        # Call the service to process the data and detect diseases
        result = self.disease_detection_service.detect(data)
        return DiseaseResponse(diseases=result.diseases, confidence=result.confidence)