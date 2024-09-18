from pydantic import BaseModel
from typing import Optional

class IndicatorCreateDTO(BaseModel):
    name: str
    differential: float
    is_active: bool
    symbolDol: Optional[str] = None  # Opcional se não for fornecido
    symbol: Optional[str] = None  # Opcional se não for fornecido

class IndicatorUpdateDTO(BaseModel):
    name: Optional[str] = None
    differential: Optional[float] = None
    is_active: Optional[bool] = None
    symbolDol: Optional[str] = None  
    symbol: Optional[str] = None

class IndicatorResponseDTO(BaseModel):
    id: int
    name: str
    differential: float
    is_active: bool
    symbol: str
    symbolDol: Optional[str] = None  

    class Config:
        from_attributes = True
