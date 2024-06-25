from pydantic import BaseModel
from datetime import datetime

class History(BaseModel):
    tagMac: str
    deviceClass: str
    location: str
    avg_rssi: float
    timeStamp: datetime
    assetName: str = None  # Optional field, default to None if not present
