from tortoise.models import Model
from tortoise import fields

class Indicator(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255, unique=True)  # Nome do indicador único
    is_active = fields.BooleanField(default=True)           # Indica se o indicador está ativo
    differential = fields.DecimalField(max_digits=10, decimal_places=2)  # Valor diferencial
    symbol = fields.CharField(max_length=50)
    symbolDol  = fields.CharField(max_length=50, null=True)  # Symbol associado ao indicador, permite null
    tenant = fields.IntField()                             # Identificador do tenant

    class Meta:
        table = "indicators"  # Nome da tabela no banco de dados
