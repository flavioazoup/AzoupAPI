from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.usuario_api import UsuarioAPI, Base
from passlib.context import CryptContext

# String de conexão
SQLALCHEMY_AUTH_DATABASE_URL = "firebird+fdb://SYSDBA:ZPFs1st3m4s@18.228.48.187:3050//opt/firebird/data/AZOUPFB5.FDB"

auth_engine = create_engine(SQLALCHEMY_AUTH_DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=auth_engine)

# Cria a tabela se não existir
Base.metadata.create_all(bind=auth_engine)

# Configuração do hash de senha
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

session = SessionLocal()
try:
    # Note que não definimos o ID - será gerado automaticamente
    novo_usuario = UsuarioAPI(
        username="testeuser2",
        hashed_password=pwd_context.hash("senha123"),
        email="testeuser2@exemplo.com"
    )
    session.add(novo_usuario)
    session.commit()
    
    # Refresh para obter o ID gerado
    session.refresh(novo_usuario)
    print("Usuário inserido com sucesso! ID:", novo_usuario.id)
    
except Exception as e:
    session.rollback()
    print("Erro ao inserir usuário:", e)
    import traceback
    traceback.print_exc()
finally:
    session.close()