
from fastapi import FastAPI
from app.api.v1.endpoints import colecao, usuario_api

app = FastAPI(title="AzoupAPI", version="v1")

app.include_router(usuario_api.router, prefix="/v1", tags=["UsuarioAPI"])
app.include_router(colecao.router, prefix="/v1", tags=["Colecao"])

