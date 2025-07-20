from sqlalchemy.orm import Session
from app.models.usuario_api import UsuarioAPI
from app.schemas.usuario_api import UsuarioAPICreate
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_user_by_username(db: Session, username: str):
    return db.query(UsuarioAPI).filter(UsuarioAPI.username == username).first()

def create_usuario_api(db: Session, usuario: UsuarioAPICreate):
    hashed_password = pwd_context.hash(usuario.password)
    db_user = UsuarioAPI(username=usuario.username, hashed_password=hashed_password , email=usuario.email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)
