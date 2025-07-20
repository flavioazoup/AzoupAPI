from sqlalchemy.orm import Session
from app.models.colecao import Colecao
from app.schemas.colecao import ColecaoCreate, ColecaoUpdate

# CRUD Functions

def get_colecoes(db: Session):
    return db.query(Colecao).all()

def get_colecao(db: Session, codigo: int):
    return db.query(Colecao).filter(Colecao.codigo == codigo).first()

def create_colecao(db: Session, colecao: ColecaoCreate):
    db_colecao = Colecao(descricao=colecao.descricao)
    db.add(db_colecao)
    db.commit()
    db.refresh(db_colecao)
    return db_colecao

def update_colecao(db: Session, codigo: int, colecao: ColecaoUpdate):
    db_colecao = get_colecao(db, codigo)
    if db_colecao:
        db_colecao.descricao = colecao.descricao
        db.commit()
        db.refresh(db_colecao)
    return db_colecao

def delete_colecao(db: Session, codigo: int):
    db_colecao = get_colecao(db, codigo)
    if db_colecao:
        db.delete(db_colecao)
        db.commit()
    return db_colecao
