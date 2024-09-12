from typing import List
from fastapi import APIRouter, HTTPException, Depends
from src.models.user import User
from src.models.symbols import Symbol
from src.dto.Symbols import SymbolCreateDTO, SymbolUpdateDTO, SymbolResponseDTO
from src.services.SymbolsService import SymbolService
from src.services.authService import AuthService

symbol_service = SymbolService()

symbols_router = APIRouter(
    prefix="/symbols",
    tags=["Symbols"]
)

@symbols_router.get("/", response_model=List[SymbolResponseDTO])
async def read_symbols(current_user: User = Depends(AuthService.get_current_user)):
    symbols = await symbol_service.get_all_symbols()
    return [SymbolResponseDTO.from_orm(symbol) for symbol in symbols]

@symbols_router.get("/{symbol_id}", response_model=SymbolResponseDTO)
async def read_symbol(symbol_id: int, current_user: User = Depends(AuthService.get_current_user)):
    symbol = await symbol_service.get_symbol_by_id(symbol_id)
    if not symbol:
        raise HTTPException(status_code=404, detail="Symbol not found")
    return symbol  

@symbols_router.post("/", response_model=SymbolResponseDTO)
async def create_symbol(symbol: SymbolCreateDTO, current_user: User = Depends(AuthService.get_current_user)):
    new_symbol = await symbol_service.create_symbol(symbol.dict())
    return SymbolResponseDTO.from_orm(new_symbol)

@symbols_router.put("/{symbol_id}", response_model=SymbolResponseDTO)
async def update_symbol(symbol_id: int, symbol: SymbolUpdateDTO, current_user: User = Depends(AuthService.get_current_user)):
    updated_symbol = await symbol_service.update_symbol(symbol_id, symbol.dict())
    if not updated_symbol:
        raise HTTPException(status_code=404, detail="Symbol not found")
    return SymbolResponseDTO.from_orm(updated_symbol)

@symbols_router.delete("/{symbol_id}")
async def delete_symbol(symbol_id: int, current_user: User = Depends(AuthService.get_current_user)):
    success = await symbol_service.delete_symbol(symbol_id)
    if not success:
        raise HTTPException(status_code=404, detail="Symbol not found")
    return {"detail": "Symbol deleted"}
