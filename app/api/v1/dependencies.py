def get_db_dep(client_id: str):
    """
    Dependência para FastAPI: retorna a sessão SQLAlchemy correta para o client_id.
    """
    return next(get_db(client_id))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.colecao import Base
from app.core.database import get_client_info

from threading import Lock

# Cache de engines por client_id
_engine_cache = {}
_engine_lock = Lock()

def get_db(client_id: str):
    """
    Cria uma sessão SQLAlchemy dinâmica para o banco do client_id, cacheando o engine.
    """
    with _engine_lock:
        if client_id not in _engine_cache:
            client = get_client_info(client_id)
            # Esperado: connection_string = "host:porta//caminho/para/banco.FDB"
            try:
                conn_str_raw = client['connection_string']
                print(f"[DEBUG] connection_string original: {repr(conn_str_raw)}")
                host_port, db_path = conn_str_raw.strip().split('//', 1)
                print(f"[DEBUG] host_port: {repr(host_port)}")
                print(f"[DEBUG] db_path (antes strip): {repr(db_path)}")
                host, port = host_port.strip().split(':', 1)
                host = host.strip()
                port = port.strip()
                db_path = db_path.lstrip('/').strip()
                print(f"[DEBUG] host: {repr(host)}")
                print(f"[DEBUG] port: {repr(port)}")
                print(f"[DEBUG] db_path: {repr(db_path)}")
            except Exception as e:
                raise Exception(f"connection_string inválida: {repr(client['connection_string'])} - erro: {e}")
            conn_str = f"firebird+fdb://{client['username']}:{client['password_banco']}@{host}:{port}//{db_path}"
            print(f"[DEBUG] connection string final: {repr(conn_str)}")
            engine = create_engine(
                conn_str,
                echo=True
            )
            _engine_cache[client_id] = engine
        else:
            engine = _engine_cache[client_id]
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
