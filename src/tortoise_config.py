import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

TORTOISE_ORM = {
    "connections": {
        "default": "asyncpg://main_user:mysecretpassword@postgres:5432/moedas",
    },
    "apps": {
        "models": {
            "models": ["src.models", "aerich.models"],  # Inclua aerich.models
            "default": True,
        }
    }
}

