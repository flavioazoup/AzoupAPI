
# Conexão dinâmica com múltiplos bancos Firebird a partir da tabela INFOCLIENTE
import fdb
from app.core.auth_database import get_auth_db
from sqlalchemy import text

def get_client_info(client_id: str, db_session=None):
    # Busca os dados do cliente na tabela INFOCLIENTE do banco de autenticação
    close_session = False
    if db_session is None:
        from app.core.auth_database import AuthSessionLocal
        db_session = AuthSessionLocal()
        close_session = True
    try:
        query = text("""
            SELECT database_path, connection_string, username, password_banco, min_connections, max_connections
            FROM INFOCLIENTE WHERE id = :client_id
        """)
        result = db_session.execute(query, {"client_id": client_id}).fetchone()
        if not result:
            raise ValueError("Cliente não encontrado")
        keys = ["database_path", "connection_string", "username", "password_banco", "min_connections", "max_connections"]
        client = dict(zip(keys, result))
        return client
    finally:
        if close_session:
            db_session.close()

def get_connection(client_id: str, db_session=None):
    client = get_client_info(client_id, db_session)
    return fdb.connect(
        dsn=client["connection_string"],
        user=client["username"],
        password=client["password_banco"]
    )
