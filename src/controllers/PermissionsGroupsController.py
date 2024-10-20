from typing import List, Dict
from fastapi import APIRouter, HTTPException, Depends
from src.services.PermissionsGroupsService import PermissionsGroupsService
from src.models.user import User
from src.services.authService import AuthService

permission_groups_router = APIRouter(
    prefix="/permission-groups",
    tags=["Permission Groups"]
)

@permission_groups_router.get("/", response_model=List[Dict])
async def read_permission_groups(current_user: User = Depends(AuthService.get_current_user)):
    groups = await PermissionsGroupsService.get_all_permission_groups()
    return groups

@permission_groups_router.get("/{group_id}", response_model=Dict)
async def read_permission_group(group_id: int, current_user: User = Depends(AuthService.get_current_user)):
    group = await PermissionsGroupsService.get_group(group_id)
    if not group:
        raise HTTPException(status_code=404, detail="Permission group not found")
    return group

@permission_groups_router.post("/", response_model=Dict)
async def create_permission_group(
    item: dict,
    current_user: User = Depends(AuthService.get_current_user)
):
    new_group = await PermissionsGroupsService.create_permission_group(item)
    return new_group

@permission_groups_router.put("/{group_id}", response_model=Dict)
async def update_permission_group(
    group_id: int,
    item: dict,
    current_user: User = Depends(AuthService.get_current_user)
):
    updated_group = await PermissionsGroupsService.update_permission_group(group_id, item)
    if not updated_group:
        raise HTTPException(status_code=404, detail="Permission group not found")
    return updated_group

@permission_groups_router.delete("/{group_id}", response_model=Dict)
async def delete_permission_group(group_id: int, current_user: User = Depends(AuthService.get_current_user)):
    await PermissionsGroupsService.delete_permission_group(group_id)
    return {"detail": "Permission group deleted"}
