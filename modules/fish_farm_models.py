from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class WaterTankDetails(BaseModel):
    length: float  # in meters
    width: float   # in meters
    volume: float  # in cubic meters

class FishedDetails(BaseModel):
    total_fish_count: Optional[int] = 0  # Total number of fish in the tank
    total_fish_sick: Optional[int] = 0   # Number of sick fish
    fish_length: Optional[float] = 0.0   # Average fish length in cm
    fish_weight: Optional[float] = 0.0   # Average fish weight in kg

class TankMeasurements(BaseModel):
    tankId: str  # ObjectId as string
    timestamp: datetime
    water_level: float  # in meters
    suspended_solids: float  # in mg/L
    salinity: float  # in ppt
    pH: float  # pH level
    nitrite: float  # in mg/L
    nitrate: float  # in mg/L
    ammonia: float  # in mg/L
    temperature: float  # in Celsius
    O2: float  # in mg/L (assumed to be dissolved oxygen, same as oxygen_level)

class WaterTank(BaseModel):
    id: Optional[str] = None  # ObjectId as string
    details: WaterTankDetails
    responsible: str  # ObjectId as string
    isActive: bool
    fishDetails: Optional[FishedDetails] = None
    hasSick: Optional[bool] = False  # Derived from total_fish_sick > 0

class WaterTankMeasures(BaseModel):
    tank: WaterTank
    measures: List[TankMeasurements]
    number_of_consumed_food: float  # in kg

class FishFarmReportRequest(BaseModel):
    waterTanksMeasures: List[WaterTankMeasures]
    timestamp: Optional[datetime] = datetime.now()

class FishFarmReportResponse(BaseModel):
    report: str  # LaTeX content for PDF report