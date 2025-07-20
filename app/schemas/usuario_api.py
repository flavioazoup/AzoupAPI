from pydantic import BaseModel
from typing import Optional

class UsuarioAPICreate(BaseModel):
    username: str
    password: str
    email: Optional[str] = None

class UsuarioAPIOut(BaseModel):
    id: int
    username: str
    email: Optional[str] = None

    class Config:
        orm_mode = True
