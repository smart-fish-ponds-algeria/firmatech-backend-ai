from ..modules.summary_report_models import SummaryReportRequest, SummaryReportResponse


class SummaryController:
    def __init__(self, summary_service):
        self.summary_service = summary_service

    async def generate_summary_report(self, request: SummaryReportRequest) -> SummaryReportResponse:
        """
        Generate a summary report based on the provided request data.
        """
        report = await self.summary_service.create_summary_report(request)
        return SummaryReportResponse(report=report)