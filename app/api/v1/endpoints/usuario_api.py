from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta, datetime
from jose import jwt
from sqlalchemy.orm import Session
from app.core.security import SECRET_KEY, ALGORITHM
from app.repositories.usuario_api import get_user_by_username, verify_password, create_usuario_api
from app.core.auth_database import get_auth_db
from app.schemas.usuario_api import UsuarioAPICreate, UsuarioAPIOut

router = APIRouter()

@router.post("/usuario", response_model=UsuarioAPIOut)
def criar_usuario_api(usuario: UsuarioAPICreate, db: Session = Depends(get_auth_db)):
    if get_user_by_username(db, usuario.username):
        raise HTTPException(status_code=400, detail="Usuário já existe")
    return create_usuario_api(db, usuario)

@router.post("/token")
def login_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_auth_db)):
    user = get_user_by_username(db, form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuário ou senha inválidos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    expire = datetime.utcnow() + timedelta(minutes=60)
    to_encode = {"sub": user.username, "exp": expire}
    access_token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return {"access_token": access_token, "token_type": "bearer"}
