from pydantic import BaseModel
from typing import Optional, List
from datetime import date

class rssi(BaseModel):
     time: str
     rssi: str

class SignalReport(BaseModel):
     tagMac: str
     location: str
     deviceClass: str
     rssi: list[rssi]
     timeStamp: date 
     major: Optional[str] = None
     minor: Optional[str] = None
     dynamicValue: Optional[str] = None
     battery: str
