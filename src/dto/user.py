from pydantic import BaseModel
from typing import Optional

class UserResponseDTO(BaseModel):
    id: int
    username: str
    email: str
    full_name: Optional[str] = None
    is_active: bool

    class Config:
        from_attributes = True
        
class UserCreateDTO(BaseModel):
    username: str
    email: str
    full_name: Optional[str] = None
    password: str
    
    
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

