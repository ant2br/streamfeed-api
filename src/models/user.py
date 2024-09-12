# src/models/users.py
from tortoise.models import Model
from tortoise import fields

class User(Model):
    id = fields.IntField(pk=True)
    username = fields.CharField(max_length=150, unique=True)  # Nome de usuário único
    email = fields.CharField(max_length=255, unique=True)     # Email único
    full_name = fields.CharField(max_length=255)              # Nome completo do usuário
    hashed_password = fields.CharField(max_length=255)        # Senha armazenada de forma segura
    is_active = fields.BooleanField(default=True)             # Indica se o usuário está ativo
    is_superuser = fields.BooleanField(default=False)         # Indica se o usuário é um administrador
    tenant = fields.IntField()

    class Meta:
        table = "users"  # Nome da tabela no banco de dados
