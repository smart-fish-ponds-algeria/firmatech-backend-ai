import os
import logging
from datetime import datetime, timedelta
import requests
from agno.agent import Agent
from agno.models.google import Gemini
from dotenv import load_dotenv
from modules.fish_farm_models import FishFarmReportRequest, FishFarmReportResponse, FishedDetails, TankMeasurements

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

        # Clear SSL environment variables
        os.environ["SSL_CERT_FILE"] = ""
        os.environ["REQUESTS_CA_BUNDLE"] = ""

        # Initialize agent with Gemini API
        self.agent = Agent(
            model=Gemini(id="gemini-1.5-flash", api_key=api_key),
            markdown=True,
        )

    def generate_report(self, request: FishFarmReportRequest) -> FishFarmReportResponse:
        """Generate a daily fish farm report in LaTeX format for multiple tanks."""

        knowledge_base = """
        You are an expert in fish farming, specializing in Talipia. Use the following guidelines:
        - Ideal water parameters: temperature 26-30°C, pH 6.5-8.5, oxygen level >5 mg/L, salinity 0-15 ppt.
        - Suspended solids: <20 mg/L; Nitrite: <0.1 mg/L; Nitrate: <50 mg/L; Ammonia: <0.05 mg/L.
        - Average Talipia length: 20-30 cm, weight: 0.5-1 kg at maturity.
        - High sick fish count (>5% of total) indicates potential health issues.
        - Water level should be stable (e.g., 1-2 meters).
        - Food consumption should be 1-3% of body weight daily.
        - Multiple tanks may be reported; summarize each tank's status and provide overall recommendations.
        """

        # Aggregate data from all tanks
        data_summary = f"Date: {request.timestamp.strftime('%Y-%m-%d')}\n\n"
        for idx, tank_measure in enumerate(request.waterTanksMeasures, 1):
            tank = tank_measure.tank
            measures = tank_measure.measures
            food = tank_measure.number_of_consumed_food
            fish_details = tank.fishDetails or FishedDetails()

            # Summarize measurements (use the latest or average if multiple)
            latest_measure = measures[-1] if measures else TankMeasurements(
                tankId=tank.id or "unknown",
                timestamp=request.timestamp,
                water_level=0.0,
                suspended_solids=0.0,
                salinity=0.0,
                pH=0.0,
                nitrite=0.0,
                nitrate=0.0,
                ammonia=0.0,
                temperature=0.0,
                O2=0.0
            )

            data_summary += (
                f"Tank {idx} (ID: {tank.id or 'N/A'}, Active: {tank.isActive}):\n"
                f"  Dimensions: {tank.details.length}m x {tank.details.width}m, Volume: {tank.details.volume} m³\n"
                f"  Responsible: User ID {tank.responsible}\n"
                f"  Fish Details:\n"
                f"    - Total fish: {fish_details.total_fish_count}\n"
                f"    - Sick fish: {fish_details.total_fish_sick}\n"
                f"    - Average fish length: {fish_details.fish_length} cm\n"
                f"    - Average fish weight: {fish_details.fish_weight} kg\n"
                f"    - Has sick fish: {tank.hasSick or (fish_details.total_fish_sick > 0)}\n"
                f"  Consumed food: {food} kg\n"
                f"  Latest Measurements (Timestamp: {latest_measure.timestamp.strftime('%Y-%m-%d %H:%M:%S')}):\n"
                f"    - Water level: {latest_measure.water_level} m\n"
                f"    - Temperature: {latest_measure.temperature}°C\n"
                f"    - pH: {latest_measure.pH}\n"
                f"    - Oxygen (O2): {latest_measure.O2} mg/L\n"
                f"    - Salinity: {latest_measure.salinity} ppt\n"
                f"    - Suspended Solids: {latest_measure.suspended_solids} mg/L\n"
                f"    - Nitrite: {latest_measure.nitrite} mg/L\n"
                f"    - Nitrate: {latest_measure.nitrate} mg/L\n"
                f"    - Ammonia: {latest_measure.ammonia} mg/L\n"
            )

        prompt = (
            f"{knowledge_base}\n"
            "Generate a professional daily fish farm report in LaTeX format for a PDF. "
            "Include a title, date, summary of the provided data for each tank, and overall recommendations based on fish farming best practices. "
            "Highlight any anomalies (e.g., high sick fish count, abnormal water parameters) for each tank. "
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