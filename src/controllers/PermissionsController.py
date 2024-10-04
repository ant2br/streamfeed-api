from typing import List
from fastapi import APIRouter, HTTPException, Depends
from src.models.user import User
from src.services.authService import AuthService
from src.dto.permissions import PermissionCreateDTO, PermissionUpdateDTO, PermissionResponseDTO
from src.services.PermissionsService import PermissionsService

permissions_service = PermissionsService()

permissions_router = APIRouter(
    prefix="/permissions",
    tags=["Permissions"]
)

@permissions_router.get("/", response_model=List[PermissionResponseDTO])
async def read_permissions(current_user: User = Depends(AuthService.get_current_user)):
    permissions = await permissions_service.listar_permissoes()
    return [PermissionResponseDTO.from_orm(permission) for permission in permissions]

@permissions_router.get("/{permission_id}", response_model=PermissionResponseDTO)
async def read_permission(permission_id: int, current_user: User = Depends(AuthService.get_current_user)):
    permission = await permissions_service.obter_permissao(permission_id)
    if not permission:
        raise HTTPException(status_code=404, detail="Permission not found")
    return PermissionResponseDTO.from_orm(permission)

@permissions_router.post("/", response_model=PermissionResponseDTO)
async def create_permission(
    item: PermissionCreateDTO,
    current_user: User = Depends(AuthService.get_current_user)
):
    try:
        # Converte o DTO para dicionário antes de passar para o serviço
        permission_data = item.dict()
        new_permission = await permissions_service.inserir_permissao(permission_data)
        return PermissionResponseDTO.from_orm(new_permission)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@permissions_router.put("/{permission_id}", response_model=PermissionResponseDTO)
async def update_permission(
    permission_id: int, 
    item: PermissionUpdateDTO, 
    current_user: User = Depends(AuthService.get_current_user)
):
    try:
        updated_permission = await permissions_service.atualizar_permissao(permission_id, item.dict())
        if not updated_permission:
            raise HTTPException(status_code=404, detail="Permission not found")
        return PermissionResponseDTO.from_orm(updated_permission)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@permissions_router.delete("/{permission_id}", response_model=dict)
async def delete_permission(
    permission_id: int, 
    current_user: User = Depends(AuthService.get_current_user)
):
    success = await permissions_service.deletar_permissao(permission_id)
    if not success:
        raise HTTPException(status_code=404, detail="Permission not found")
    return {"detail": "Permission deleted"}
