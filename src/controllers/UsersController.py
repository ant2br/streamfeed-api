from typing import Optional
from fastapi import APIRouter, Depends, Form, HTTPException
from src.models.user import User
from src.dto.user import PasswordChangeDTO, UserCreateDTO, Token, LoginBody, UserResponseDTO, UserUpdateDTO
from src.services.UsersService import UsersService
from src.services.authService import AuthService
from datetime import timedelta

users_service = UsersService()

users_router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@users_router.get("/", response_model=list[UserResponseDTO])
async def read_users(current_user: User = Depends(AuthService.get_current_user)):
    usuarios = await users_service.listar_usuarios()

    # Mapeia cada usuário para o DTO manualmente
    return [UserResponseDTO.from_orm(usuario) for usuario in usuarios]

@users_router.get("/{user_id}", response_model=UserResponseDTO)
async def read_user(user_id: int, current_user: User = Depends(AuthService.get_current_user)):
    user = await users_service.obter_usuario(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return UserResponseDTO.from_orm(user)  # Retorna o DTO de usuário

@users_router.post("/", response_model=UserResponseDTO)
async def create_user_endpoint(item: UserCreateDTO):
    user = await users_service.inserir_usuario(item)
    return UserResponseDTO.from_orm(user)  # Retorna o DTO do usuário criado

@users_router.put("/{user_id}", response_model=UserResponseDTO)
async def update_user_endpoint(user_id: int, item: UserUpdateDTO, current_user: User = Depends(AuthService.get_current_user)):
    user = await users_service.atualizar_usuario(user_id, item)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return UserResponseDTO.from_orm(user)  # Retorna o DTO do usuário atualizado

@users_router.delete("/{user_id}")
async def delete_user_endpoint(user_id: int, current_user: User = Depends(AuthService.get_current_user)):
    success = await users_service.deletar_usuario(user_id)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    return {"detail": "User deleted"}

@users_router.post("/login", response_model=dict)  # Modificado para incluir o UserResponseDTO
async def login(form_data: LoginBody):
    user = await AuthService.authenticate_user(form_data.username.lower(), form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect username or password")

    access_token_expires = timedelta(minutes=60)
    access_token = AuthService.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires,
        no_expiration=user.never_expire
    )
    
    return {"access_token": access_token, "token_type": "bearer", "user": UserResponseDTO.from_orm(user)}

@users_router.post("/change-password")
async def change_password(
    body: PasswordChangeDTO, 
    current_user: User = Depends(AuthService.get_current_user)
):
    if not AuthService.verify_password(body.old_password, current_user.hashed_password):
        raise HTTPException(status_code=400, detail="Old password is incorrect")
    
    if body.new_password != body.confirm_password:
        raise HTTPException(status_code=400, detail="New password and confirmation do not match")
    
    await users_service.alterar_senha(current_user.id, body.new_password)
    
    return {"detail": "Password changed successfully"}

@users_router.post("/{user_id}/reset-password")
async def reset_password(user_id: int, current_user: User = Depends(AuthService.get_current_user)):
    # Busca o usuário no banco de dados
    user = await users_service.obter_usuario(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Define uma nova senha temporária
    nova_senha = "Alterar123@"
    
    # Atualiza a senha do usuário no banco de dados
    await users_service.alterar_senha(user_id, nova_senha)
    
    return {"detail": "Password reset successfully"}

@users_router.post("/token", response_model=Token, include_in_schema=False)
async def login(
    username: str = Form(...),
    password: str = Form(...),
    form_data: Optional[LoginBody] = None
):
    if form_data:
        username = form_data.username
        password = form_data.password

    user = await AuthService.authenticate_user(username.lower(), password)
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect username or password")

    access_token_expires = timedelta(minutes=30)
    access_token = AuthService.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
