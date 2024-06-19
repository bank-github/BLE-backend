from pydantic import BaseModel
from typing import Optional


class Tags(BaseModel):
     tagMac: str
     assetName: str

class CreateTags(Tags):
     pass

class UpdateTags(Tags):
     tagMac: Optional[str] = None
     
