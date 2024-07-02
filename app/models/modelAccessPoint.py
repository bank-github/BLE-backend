from pydantic import BaseModel
from typing import Optional, List

class AccessPoint(BaseModel):
     apName: str
     location: Optional[str] = None
     description: Optional[str] = None

class UpdateAccessPoint(AccessPoint):
     apName: Optional[str] = None
     
