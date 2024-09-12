from pydantic import BaseModel
from typing import Optional

class IndicatorCreateDTO(BaseModel):
    name: str
    differential: float
    is_active: bool
    symbol: Optional[str] = None  # Opcional se não for fornecido

class IndicatorUpdateDTO(BaseModel):
    name: Optional[str] = None
    differential: Optional[float] = None
    is_active: Optional[bool] = None
    symbol: Optional[str] = None

class IndicatorResponseDTO(BaseModel):
    id: int
    name: str
    differential: float
    is_active: bool
    symbol: str

    class Config:
        from_attributes = True
