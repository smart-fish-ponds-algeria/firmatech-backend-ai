from pydantic import BaseModel

class SummaryReportRequest(BaseModel):
    # Add fields as needed to aggregate platform data
    pass

class SummaryReportResponse(BaseModel):
    report: str
    pdf_url: str = None
    sms_sent: bool = False