from services.agent_service import AgentService
from modules.fish_farm_models import FishFarmReportRequest, FishFarmReportResponse

class FishFarmController:
    def __init__(self):
        self.agent_service = AgentService()

    async def generate_daily_report(self, request: FishFarmReportRequest) -> FishFarmReportResponse:
        """
        Generate a daily fish farm report using the agent service.

        Args:
            request: FishFarmReportRequest with farm data.

        Returns:
            FishFarmReportResponse with LaTeX report content.
        """
        return self.agent_service.generate_report(request)