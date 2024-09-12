from typing import Optional
from pydantic import BaseModel

class SymbolCreateDTO(BaseModel):
    code: str
    is_active: bool
    tenant: Optional[int] = None  # Opcional, se não for fornecido

class SymbolUpdateDTO(BaseModel):
    code: Optional[str] = None
    is_active: Optional[bool] = None
    tenant: Optional[int] = None

class SymbolResponseDTO(BaseModel):
    id: int
    code: str
    is_active: bool
    tenant: int

    class Config:
        from_attributes = True
