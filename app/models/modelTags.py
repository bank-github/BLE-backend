from pydantic import BaseModel
from typing import Optional


class Tags(BaseModel):
     tagMac: str
     assetName: str
     description: str
     deviceClass: str

class CreateTags(Tags):
     pass

class UpdateTags(Tags):
     tagMac: Optional[str] = None
     assetName: Optional[str] = None
     description: Optional[str] = None
     deviceClass: Optional[str] = None
     
