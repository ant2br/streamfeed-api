import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

TORTOISE_ORM = {
    "connections": {
        "default": os.getenv('DATABASE_URL'),
    },
    "apps": {
        "models": {
            "models": ["src.models", "aerich.models"],  # Inclua aerich.models
            "default": True,
        }
    }
}

