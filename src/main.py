from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from tortoise.contrib.fastapi import register_tortoise
from src.controllers.UsersController import users_router
from src.controllers.WsController import ws_router
from src.controllers.SymbolsController import symbols_router
from src.controllers.IndicatorsController import indicators_router
from src.controllers.PermissionsController import permissions_router
from src.controllers.PermissionsGroupsController import permission_groups_router

from dotenv import load_dotenv
import os

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

app = FastAPI(
    title="API de Indicadores e Símbolos",
    description="Esta API permite gerenciar indicadores e símbolos financeiros.",
    version="1.0.0",
    contact={
        "name": "Brener",
        "email": "brener@example.com",
    },
    license_info={
        "name": "Fechado",
        "url": "https://example.com/license",  # Substitua pelo link da sua licença se houver
    },
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)

app.include_router(users_router, prefix="/api")
app.include_router(ws_router)

app.include_router(indicators_router, prefix="/api")
app.include_router(symbols_router, prefix="/api")
app.include_router(permission_groups_router , prefix="/api")
app.include_router(permissions_router  , prefix="/api")



@app.get("/", tags=["Raiz"], summary="Retorna uma mensagem de boas-vindas")
def root(): 
    return "Hello world"

# Configuração do Tortoise-ORM
DATABASE_URL = os.getenv('DATABASE_URL')  # Usa a variável de ambiente ou um padrão

register_tortoise(
    app,
    db_url="asyncpg://main_user:mysecretpassword@postgres:5432/moedas",
    modules={"models": ["src.models"]},  # Ajuste o módulo conforme sua estrutura de projeto
    add_exception_handlers=True,
)
