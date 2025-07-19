from pydantic import BaseModel
from typing import Dict, Optional
from datetime import datetime

class WaterParams(BaseModel):
    temperature: float         # in Celsius – water temperature
    pH: float                  # pH level – measure of acidity/basicity
    oxygen_level: float        # in mg/L – dissolved oxygen
    salinity: float            # in ppt – salt concentration
    suspended_solids: float    # in mg/L – particles suspended in water (turbidity indicator)
    nitrite: float             # in mg/L – toxic nitrogen compound (NO₂⁻)
    nitrate: float             # in mg/L – less toxic nitrogen compound (NO₃⁻)
    ammonia: float             # in mg/L – toxic nitrogenous waste (NH₃/NH₄⁺)
    O2: float                  # in % or mg/L – oxygen saturation or total oxygen (redundant with oxygen_level unless purposefully distinct)


class FishFarmReportRequest(BaseModel):
    total_number_of_fish: int
    number_of_consumed_food: float  # in kg
    water_params: WaterParams
    fish_length: float  # average length in cm
    fish_weight: float  # average weight in kg
    water_level: float  # in meters
    timestamp: Optional[datetime] = datetime.now()

class FishFarmReportResponse(BaseModel):
    report: str  # LaTeX content for PDF report