from ..modules.food_models import FoodRequest, FoodResponse

class FoodController:
    def __init__(self, food_service):
        self.food_service = food_service
    
    @staticmethod
    def predict_food(data: FoodRequest) -> FoodResponse:
        """
        Predict the amount of food needed based on the provided request data.
        """