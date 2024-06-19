from pydantic import BaseModel
from typing import Optional


class User(BaseModel):
     username: str
     password: str

class CreateUser(User):
    pass

class UpdateUser(User):
     username: Optional[str] = None
     