from pydantic import BaseModel
from typing import Optional, List

class Address(BaseModel):
     province: str
     district: str

class Setting_Message(BaseModel):
     name: str
     password: str
     hobby: Optional[List[str]] = None
     address: Address

class CreateSetting_Message(Setting_Message):
     pass

class UpdateSetting_Message(Setting_Message):
     password: Optional[str] = None
     
