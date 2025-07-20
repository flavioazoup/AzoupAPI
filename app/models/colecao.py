from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Colecao(Base):
    __tablename__ = "COLECAO"
    codigo = Column("CODIGO", Integer, primary_key=True, autoincrement=True)
    descricao = Column("DESCRICAO", String(50), nullable=False)
