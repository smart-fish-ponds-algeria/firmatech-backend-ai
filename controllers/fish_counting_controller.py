from ..modules.fish_counting_models import FishCountResponse, FishCountRequest

class FishCountController:
    def __init__(self, fish_counting_service):
        self.fish_counting_service = fish_counting_service
    
    async def count_fish(self, file: FishCountRequest) -> FishCountResponse:
        # Call the service to process the image and count fish
        total_count = await self.fish_counting_service.process_image(file)
        return FishCountResponse(total_count=total_count)