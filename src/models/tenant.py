from tortoise.models import Model
from tortoise import fields

class Tenant(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255, unique=True)      # Nome único do tenant
    owner = fields.CharField(max_length=255)                  # Nome do proprietário do tenant
    email = fields.CharField(max_length=255, unique=True)     # Email único do proprietário
    created_at = fields.DatetimeField(auto_now_add=True)      # Data de criação do tenant
    is_active = fields.BooleanField(default=True)             # Indica se o tenant está ativo

    class Meta:
        table = "tenants"  # Nome da tabela no banco de dados
