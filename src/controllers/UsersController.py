# src/controllers/users_controller.py
from typing import Optional
from fastapi import APIRouter, Depends, Form, HTTPException
from src.models.user import User
from src.dto.user import UserCreateDTO, Token, LoginBody, UserResponseDTO, UserUpdateDTO
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
    
    return user  # Retorna o objeto ORM diretamente, o Pydantic cuidará da conversão

@users_router.post("/")
async def create_user_endpoint(item: UserCreateDTO):
    return await users_service.inserir_usuario(item)

@users_router.put("/{user_id}")
async def update_user_endpoint(user_id: int, item: UserUpdateDTO, current_user: User = Depends(AuthService.get_current_user)):
    user = await users_service.atualizar_usuario(user_id, item)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@users_router.delete("/{user_id}")
async def delete_user_endpoint(user_id: int, current_user: User = Depends(AuthService.get_current_user)):
    success = await users_service.deletar_usuario(user_id)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    return {"detail": "User deleted"}


@users_router.post("/login", response_model=Token)
async def login(form_data: LoginBody):
    user = await AuthService.authenticate_user(form_data.username.lower(), form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    access_token_expires = timedelta(minutes=30)
    access_token = AuthService.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}




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
