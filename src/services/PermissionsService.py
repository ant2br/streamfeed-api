from typing import List, Optional
from src.models.permissions import Permission  # Modelo para a permissão
from tortoise.exceptions import DoesNotExist
from fastapi import HTTPException

class PermissionsService:
    TENANT_ID = 1  # Definido o tenant fixo

    @staticmethod
    async def inserir_permissao(permission_data: dict) -> Permission:
        try:
            # Adiciona o tenant ao dicionário
            permission_data['tenant'] = PermissionsService.TENANT_ID
            
            # Cria a nova permissão
            new_permission = await Permission.create(**permission_data)
            return new_permission
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Error inserting permission: {str(e)}")

    @staticmethod
    async def listar_permissoes() -> List[Permission]:
        try:
            permissions = await Permission.filter(tenant=PermissionsService.TENANT_ID).all()
            return permissions
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error fetching permissions: {str(e)}")

    @staticmethod
    async def obter_permissao(permission_id: int) -> Optional[Permission]:
        try:
            permission = await Permission.get(id=permission_id, tenant=PermissionsService.TENANT_ID)
            return permission
        except DoesNotExist:
            raise HTTPException(status_code=404, detail="Permission not found")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error fetching permission: {str(e)}")

    @staticmethod
    async def atualizar_permissao(permission_id: int, permission_data: dict) -> Permission:
        try:
            permission = await Permission.get(id=permission_id, tenant=PermissionsService.TENANT_ID)
            await permission.update_from_dict(permission_data)
            await permission.save()
            return permission
        except DoesNotExist:
            raise HTTPException(status_code=404, detail="Permission not found")
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Error updating permission: {str(e)}")

    @staticmethod
    async def deletar_permissao(permission_id: int) -> bool:
        try:
            permission = await Permission.get(id=permission_id, tenant=PermissionsService.TENANT_ID)
            await permission.delete()
            return True
        except DoesNotExist:
            raise HTTPException(status_code=404, detail="Permission not found")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error deleting permission: {str(e)}")
