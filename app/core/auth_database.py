# Configuração do banco de dados exclusivo para autenticação dos usuários da API
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_AUTH_DATABASE_URL = "firebird+fdb://SYSDBA:ZPFs1st3m4s@18.228.48.187:3050//opt/firebird/data/AZOUPFB5.FDB"


auth_engine = create_engine(SQLALCHEMY_AUTH_DATABASE_URL, echo=True)
AuthSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=auth_engine)

def get_auth_db():
    db = AuthSessionLocal()
    try:
        yield db
    finally:
        db.close()
