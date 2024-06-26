from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class Location(BaseModel):
    tagMac: str
    deviceClass: str
    location: str
    avg_rssi: float
    timeStamp: datetime

class UpdateLocation(Location):
    tagMac: Optional[str] = None
    deviceClass: Optional[str] = None
    location: Optional[str] = None
    avg_rssi: float
    timeStamp: Optional[str] = None