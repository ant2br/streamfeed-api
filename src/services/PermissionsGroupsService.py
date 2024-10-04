from typing import List, Optional
from src.models.permissionGroup import PermissionGroup  # Modelo para o grupo de permissões
from tortoise.exceptions import DoesNotExist
from fastapi import HTTPException

class PermissionsGroupsService:
    TENANT_ID = 1  # Definido o tenant fixo

    @staticmethod
    async def create_permission_group(group_data: dict):
        try:
            group_data['tenant'] = PermissionsGroupsService.TENANT_ID
            new_group = await PermissionGroup.create(**group_data)
            return new_group
        except Exception as e:
            # Tratar exceções específicas, se necessário
            raise HTTPException(status_code=400, detail=str(e))

    @staticmethod
    async def get_all_permission_groups():
        try:
            groups = await PermissionGroup.filter(tenant=PermissionsGroupsService.TENANT_ID).all()
            return groups
        except Exception as e:
            raise HTTPException(status_code=500, detail="Error fetching permission groups")

    @staticmethod
    async def get_group(group_id: int):
        try:
            group = await PermissionGroup.get(id=group_id, tenant=PermissionsGroupsService.TENANT_ID)
            return group
        except DoesNotExist:
            raise HTTPException(status_code=404, detail="Permission group not found")
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @staticmethod
    async def update_permission_group(group_id: int, group_data: dict):
        try:
            group = await PermissionGroup.get(id=group_id, tenant=PermissionsGroupsService.TENANT_ID)
            await group.update_from_dict(group_data)
            await group.save()
            return group
        except DoesNotExist:
            raise HTTPException(status_code=404, detail="Permission group not found")
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

    @staticmethod
    async def delete_permission_group(group_id: int):
        try:
            group = await PermissionGroup.get(id=group_id, tenant=PermissionsGroupsService.TENANT_ID)
            await group.delete()
            return group
        except DoesNotExist:
            raise HTTPException(status_code=404, detail="Permission group not found")
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
