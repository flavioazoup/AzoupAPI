from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.schemas.colecao import Colecao, ColecaoCreate, ColecaoUpdate
from app.repositories.colecao import (
    get_colecoes, get_colecao, create_colecao, update_colecao, delete_colecao
)

from app.api.v1.dependencies import get_db_dep
from app.core.security import get_current_user
from app.core.database import get_connection

router = APIRouter()


@router.get("/colecao/{client_id}", response_model=List[Colecao])
def listar_colecoes(
    client_id: str,
    db: Session = Depends(get_db_dep),
    user: str = Depends(get_current_user)
):
    return get_colecoes(db)


@router.get("/colecao/{client_id}/{codigo}", response_model=Colecao)
def buscar_colecao(
    client_id: str,
    codigo: int,
    db: Session = Depends(get_db_dep),
    user: str = Depends(get_current_user)
):
    colecao = get_colecao(db, codigo)
    if not colecao:
        raise HTTPException(status_code=404, detail="Coleção não encontrada")
    return colecao


@router.post("/colecao/{client_id}", response_model=Colecao)
def criar_colecao(
    client_id: str,
    colecao: ColecaoCreate,
    db: Session = Depends(get_db_dep),
    user: str = Depends(get_current_user)
):
    return create_colecao(db, colecao)


@router.put("/colecao/{client_id}/{codigo}", response_model=Colecao)
def atualizar_colecao(
    client_id: str,
    codigo: int,
    colecao: ColecaoUpdate,
    db: Session = Depends(get_db_dep),
    user: str = Depends(get_current_user)
):
    db_colecao = update_colecao(db, codigo, colecao)
    if not db_colecao:
        raise HTTPException(status_code=404, detail="Coleção não encontrada")
    return db_colecao


@router.delete("/colecao/{client_id}/{codigo}", response_model=Colecao)
def deletar_colecao(
    client_id: str,
    codigo: int,
    db: Session = Depends(get_db_dep),
    user: str = Depends(get_current_user)
):
    db_colecao = delete_colecao(db, codigo)
    if not db_colecao:
        raise HTTPException(status_code=404, detail="Coleção não encontrada")
    return db_colecao