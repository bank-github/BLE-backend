from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class Location(BaseModel):
    tagMac: str
    location: str
    max_rssi: float
    timeStamp: datetime

class UpdateLocation(Location):
    tagMac: Optional[str] = None
    location: Optional[str] = None
    max_rssi: float
    timeStamp: Optional[str] = None