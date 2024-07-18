from pydantic import BaseModel
from typing import Optional


class Tags(BaseModel):
     tagMac: str
     assetName: Optional[str] = "unknown"
     assetType: Optional[str] = "other"
     battery : Optional[str] = "-"
     description: Optional[str] = "-"
     deviceClass: Optional[str] = "-"

class CreateTags(Tags):
     pass

class UpdateTags(Tags):
     tagMac: Optional[str] = None
     assetName: Optional[str] = None
     description: Optional[str] = None
     deviceClass: Optional[str] = None
     
