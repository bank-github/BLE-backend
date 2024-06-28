from pydantic import BaseModel
from typing import Optional, List

class AccessPoint(BaseModel):
     apName: str
     location: str
     description: Optional[List[str]] = "-"

class UpdateAccessPoint(AccessPoint):
     password: Optional[str] = None
     
