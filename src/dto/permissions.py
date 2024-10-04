from pydantic import BaseModel
from typing import Optional

class PermissionBaseDTO(BaseModel):
    name: str
    description: Optional[str] = None  # Campo opcional para descrição
    is_active: bool

class PermissionCreateDTO(PermissionBaseDTO):
    pass

class PermissionUpdateDTO(PermissionBaseDTO):
    pass

class PermissionResponseDTO(PermissionBaseDTO):
    id: int

    class Config:
        from_attributes = True
