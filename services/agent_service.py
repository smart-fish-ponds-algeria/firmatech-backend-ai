import os
import logging
from datetime import datetime, timedelta
import requests
from agno.agent import Agent
from agno.models.google import Gemini
from dotenv import load_dotenv
from modules.fish_farm_models import FishFarmReportRequest, FishFarmReportResponse

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

class AgentService:
    def __init__(self):
        # Verify API key
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY environment variable not set")

        # Clear SSL environment variables to avoid [Errno 22]
        os.environ["SSL_CERT_FILE"] = ""
        os.environ["REQUESTS_CA_BUNDLE"] = ""

        # Initialize agent with Gemini API (Level 3: memory and reasoning)
        self.agent = Agent(
            model=Gemini(id="gemini-1.5-flash", api_key=api_key),
            markdown=True,
        )

    def collect_fish_counts(self, start_time: datetime, end_time: datetime) -> list:
        """
        Collect fish count data from the fish counting endpoint.
        Replace with database query if storing results persistently.
        """
        try:
            response = requests.get(
                "http://127.0.0.1:8000/fish-counting/count",
                params={"start_time": start_time.isoformat(), "end_time": end_time.isoformat()}
            )
            response.raise_for_status()
            return response.json()  # Expected: List of {"total_count": N, "timestamp": "..."}
        except requests.RequestException as e:
            logger.error(f"Failed to collect fish counts: {e}")
            return [
                {"total_count": 27, "timestamp": "2025-07-18T10:00:00Z"},
                {"total_count": 15, "timestamp": "2025-07-18T14:00:00Z"}
            ]

    def generate_report(self, request: FishFarmReportRequest) -> FishFarmReportResponse:
        """Generate a daily fish farm report in LaTeX format."""
        # Fish farming knowledge base for context
        knowledge_base = """
        You are an expert in fish farming, specializing in Talipia. Use the following guidelines:
        - Ideal water parameters: temperature 26-30°C, pH 6.5-8.5, oxygen level >5 mg/L, salinity 0-15 ppt.
        - Average Talipia length: 20-30 cm, weight: 0.5-1 kg at maturity.
        - High sick fish count (>5% of total) indicates potential health issues.
        - Water level should be stable (e.g., 1-2 meters for optimal conditions).
        - Food consumption should be 1-3% of body weight daily.
        """

        # Format input data
        data_summary = (
            f"Date: {request.timestamp.strftime('%Y-%m-%d')}\n"
            f"Total number of fish: {request.total_number_of_fish}\n"
            f"Consumed food: {request.number_of_consumed_food} kg\n"
            f"Water parameters: Temperature {request.water_params.temperature}°C, "
            f"pH {request.water_params.pH}, Oxygen {request.water_params.oxygen_level} mg/L, "
            f"Salinity {request.water_params.salinity} ppt\n"
            f"Average fish length: {request.fish_length} cm\n"
            f"Average fish weight: {request.fish_weight} kg\n"
            f"Water level: {request.water_level} m\n"
        )

        # Prompt for Gemini to generate LaTeX report
        prompt = (
            f"{knowledge_base}\n"
            "Generate a professional daily fish farm report in LaTeX format for a PDF. "
            "Include a title, date, summary of the provided data, and recommendations based on fish farming best practices. "
            "Highlight any anomalies (e.g., high sick fish count, abnormal water parameters). "
            "Use the following data:\n" + data_summary + "\n"
            "Return only the LaTeX code, properly formatted with a complete preamble and document structure."
        )

        try:
            response = self.agent.run(prompt)
            # Extract the content from RunResponse and strip Markdown code block markers
            latex_content = response.content if hasattr(response, 'content') else str(response)
            if latex_content.startswith("```latex\n") and latex_content.endswith("```"):
                latex_content = latex_content[8:-3].strip()
            logger.info("Report generated successfully")
            return FishFarmReportResponse(report=latex_content)
        except Exception as e:
            logger.error(f"Failed to generate report: {e}")
            return FishFarmReportResponse(report="Error generating report")