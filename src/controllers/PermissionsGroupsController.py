# from typing import List
# from fastapi import APIRouter, HTTPException, Depends
# from src.dto import PermissionGroupResponseDTO
# from src.services.PermissionsGroupsService import PermissionsGroupsService
# from src.models.user import User
# from src.services.authService import AuthService

# permission_groups_service = PermissionsGroupsService()

# permission_groups_router = APIRouter(
#     prefix="/permission-groups",
#     tags=["Permission Groups"]
# )

# @permission_groups_router.get("/", response_model=List[PermissionGroupResponseDTO])
# async def read_permission_groups(current_user: User = Depends(AuthService.get_current_user)):
#     groups = await permission_groups_service.get_all_permission_groups()  # Suponha que este método exista
#     return [PermissionGroupResponseDTO.from_orm(group) for group in groups]

# @permission_groups_router.get("/{group_id}", response_model=PermissionGroupResponseDTO)
# async def read_permission_group(group_id: int, current_user: User = Depends(AuthService.get_current_user)):
#     group = await permission_groups_service.get_group(group_id)
#     if not group:
#         raise HTTPException(status_code=404, detail="Permission group not found")
#     return PermissionGroupResponseDTO.from_orm(group)

# @permission_groups_router.post("/", response_model=PermissionGroupResponseDTO)
# async def create_permission_group(
#     item: PermissionGroupResponseDTO.PermissionGroupCreateDTO,
#     current_user: User = Depends(AuthService.get_current_user)
# ):
#     try:
#         new_group = await permission_groups_service.create_permission_group(item)
#         return PermissionGroupResponseDTO.from_orm(new_group)
#     except Exception as e:
#         raise HTTPException(status_code=400, detail=str(e))

# @permission_groups_router.put("/{group_id}", response_model=PermissionGroupResponseDTO)
# async def update_permission_group(
#     group_id: int,
#     item: PermissionGroupResponseDTO.PermissionGroupUpdateDTO,
#     current_user: User = Depends(AuthService.get_current_user)
# ):
#     try:
#         updated_group = await permission_groups_service.update_permission_group(group_id, item)
#         if not updated_group:
#             raise HTTPException(status_code=404, detail="Permission group not found")
#         return PermissionGroupResponseDTO.from_orm(updated_group)
#     except Exception as e:
#         raise HTTPException(status_code=400, detail=str(e))

# @permission_groups_router.delete("/{group_id}", response_model=dict)
# async def delete_permission_group(group_id: int, current_user: User = Depends(AuthService.get_current_user)):
#     success = await permission_groups_service.delete_permission_group(group_id)
#     if not success:
#         raise HTTPException(status_code=404, detail="Permission group not found")
#     return {"detail": "Permission group deleted"}
