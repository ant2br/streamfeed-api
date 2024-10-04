
from tortoise.models import Model
from tortoise import fields

class PermissionGroup(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255, unique=True)  # Nome do grupo
    permissions = fields.ManyToManyField('models.Permission', related_name='groups')  # Relacionamento com Permissões
    is_active = fields.BooleanField(default=True)  # Indica se o grupo está ativo
    tenant = fields.IntField()                             # Identificador do tenant

    class Meta:
        table = "permission_groups"
