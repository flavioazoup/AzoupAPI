# Configuração do banco de dados exclusivo para autenticação dos usuários da API
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import os
from dotenv import load_dotenv

load_dotenv()

SQLALCHEMY_AUTH_DATABASE_URL = os.getenv("AUTH_DB_URL")

auth_engine = create_engine(SQLALCHEMY_AUTH_DATABASE_URL, echo=True)
AuthSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=auth_engine)

def get_auth_db():
    """
    Retorna uma sessão do banco de autenticação, usando a string de conexão do .env
    """
    db = AuthSessionLocal()
    try:
        yield db
    finally:
        db.close()
