from tortoise.models import Model
from tortoise import fields

class Symbol(Model):
    id = fields.IntField(pk=True)
    code = fields.CharField(max_length=50, unique=True)    # Código único do símbolo
    is_active = fields.BooleanField(default=True)           # Indica se o símbolo está ativo
    tenant = fields.IntField()                             # Identificador do tenant

    class Meta:
        table = "symbols"  # Nome da tabela no banco de dados
