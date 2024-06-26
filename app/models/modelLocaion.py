from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class Location(BaseModel):
    tagMac: str
    deviceClass: str
    location: str
    avg_rssi: float
    timeStamp: datetime
    assetName: Optional[str] = None  # Optional field, default to None if not present

class UpdateLocation(Location):
    tagMac: Optional[str] = None
    deviceClass: Optional[str] = None
    location: Optional[str] = None
    avg_rssi: float
    timeStamp: Optional[str] = None