from fastapi import APIRouter, HTTPException
from modules.fish_farm_models import FishFarmReportRequest, FishFarmReportResponse
from controllers.fish_farm_controller import FishFarmController

router = APIRouter(prefix="/fish-farm", tags=["Fish Farm"])

@router.post("/generate-report", response_model=FishFarmReportResponse)
async def generate_daily_report(request: FishFarmReportRequest):
    """
    Generate a daily fish farm report in LaTeX format.

    Args:
        request: FishFarmReportRequest with farm data.

    Returns:
        FishFarmReportResponse with LaTeX report content.
    """
    try:
        controller = FishFarmController()
        return await controller.generate_daily_report(request)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate report: {str(e)}")