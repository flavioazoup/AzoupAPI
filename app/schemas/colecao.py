from pydantic import BaseModel
from typing import Optional

class ColecaoBase(BaseModel):
    descricao: str

class ColecaoCreate(ColecaoBase):
    pass

class ColecaoUpdate(ColecaoBase):
    pass

class ColecaoInDBBase(ColecaoBase):
    codigo: int

    class Config:
        orm_mode = True

class Colecao(ColecaoInDBBase):
    pass
