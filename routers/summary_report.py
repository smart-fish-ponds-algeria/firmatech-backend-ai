from fastapi import APIRouter
from modules.summary_report_models import SummaryReportRequest, SummaryReportResponse

router = APIRouter(prefix="/summary-report", tags=["Summary Report"])

@router.post("/generate", response_model=SummaryReportResponse)
async def generate_report(data: SummaryReportRequest):
    # TODO: Implement summary report generation
    return SummaryReportResponse(report="Report generated.")
