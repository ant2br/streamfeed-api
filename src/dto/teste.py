from pydantic import BaseModel
from typing import Optional


class Item(BaseModel):
    nome: str
    descricao: Optional[str] = None
    preco: float
    em_estoque: bool
    
class BookResponseDTO(BaseModel):
    id: int
    nome: str
    descricao: Optional[str] = None
    preco: float
    em_estoque: bool

    class Config:
        from_attributes = True
