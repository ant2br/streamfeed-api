from pydantic import BaseModel
from typing import Optional

class UserResponseDTO(BaseModel):
    id: int
    username: str
    email: str
    full_name: Optional[str] = None
    is_active: bool
    permissionGroupId: Optional[int] = None  # Permitir valores nulos
    

    class Config:
        from_attributes = True
        
class UserCreateDTO(BaseModel):
    username: str
    email: str
    full_name: Optional[str] = None
    password: str
    permissionGroupId: Optional[int] = None  # Permitir valores nulos

    
    
class Token(BaseModel):
    access_token: str
    token_type: str
    
    
class LoginBody(BaseModel):
    username: str
    password: str
    
    
    
class UserUpdateDTO(BaseModel):
    username: str
    email: str
    full_name: Optional[str] = None
    is_active: bool
    permissionGroupId: Optional[int] = None  # Permitir valores nulos


class PasswordChangeDTO(BaseModel):
    old_password: str
    new_password: str
    confirm_password: str