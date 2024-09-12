import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

TORTOISE_ORM = {
    "connections": {
        "default": "asyncpg://teste:teste@64.23.196.60:5433/teste",
    },
    "apps": {
        "models": {
            "models": ["src.models", "aerich.models"],  # Inclua aerich.models
            "default": True,
        }
    }
}

