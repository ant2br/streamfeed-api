from tortoise.models import Model
from tortoise import fields

class Permission(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255, unique=True)  # Nome único da permissão
    description = fields.TextField(null=True)  # Descrição da permissão
    is_active = fields.BooleanField(default=True)  # Indica se a permissão está ativa
    tenant = fields.IntField()                             # Identificador do tenant


    class Meta:
        table = "permissions"
