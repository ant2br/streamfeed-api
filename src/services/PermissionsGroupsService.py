from typing import List, Dict
from src.models.permissionGroup import PermissionGroup
from src.models.permissions import Permission
from tortoise.exceptions import DoesNotExist
from fastapi import HTTPException

class PermissionsGroupsService:
    TENANT_ID = 1

    @staticmethod
    async def create_permission_group(group_data: dict) -> Dict:
        try:
            permissions = group_data.pop('permissions', [])
            group_data['tenant'] = PermissionsGroupsService.TENANT_ID

            new_group = await PermissionGroup.create(**group_data)

            if permissions:
                permission_objects = await Permission.filter(id__in=permissions)
                if len(permission_objects) != len(permissions):
                    raise HTTPException(status_code=400, detail="Some permissions do not exist.")
                await new_group.permissions.add(*permission_objects)  # Isso deve criar registros em PermissionGroupPermission

            return await PermissionsGroupsService.serialize_group(new_group)
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))


    @staticmethod
    async def get_all_permission_groups() -> List[Dict]:
        try:
            groups = await PermissionGroup.filter(tenant=PermissionsGroupsService.TENANT_ID).all()
            return [await PermissionsGroupsService.serialize_group(group) for group in groups]
        except Exception as e:
            raise HTTPException(status_code=500, detail="Error fetching permission groups")

    @staticmethod
    async def get_group(group_id: int) -> Dict:
        try:
            group = await PermissionGroup.get(id=group_id, tenant=PermissionsGroupsService.TENANT_ID)
            return await PermissionsGroupsService.serialize_group(group)
        except DoesNotExist:
            raise HTTPException(status_code=404, detail="Permission group not found")
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @staticmethod
    async def update_permission_group(group_id: int, group_data: dict) -> Dict:
        try:
            group = await PermissionGroup.get(id=group_id, tenant=PermissionsGroupsService.TENANT_ID)

            if 'permissions' in group_data:
                permissions = group_data.pop('permissions')
                permission_objects = await Permission.filter(id__in=permissions)
                await group.permissions.clear()
                await group.permissions.add(*permission_objects)

            await group.update_from_dict(group_data)
            await group.save()
            return await PermissionsGroupsService.serialize_group(group)
        except DoesNotExist:
            raise HTTPException(status_code=404, detail="Permission group not found")
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

    @staticmethod
    async def delete_permission_group(group_id: int) -> None:
        try:
            group = await PermissionGroup.get(id=group_id, tenant=PermissionsGroupsService.TENANT_ID)
            await group.delete()
        except DoesNotExist:
            raise HTTPException(status_code=404, detail="Permission group not found")
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @staticmethod
    async def serialize_group(group: PermissionGroup) -> Dict:
        permissions = await group.permissions.all()
        return {
            "id": group.id,
            "name": group.name,
            "is_active": group.is_active,
            "tenant": group.tenant,
            "permissions": [permission.id for permission in permissions]
        }
