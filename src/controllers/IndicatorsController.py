from typing import List
from fastapi import APIRouter, HTTPException, Depends
from src.models.user import User
from src.services.authService import AuthService
from src.dto.indicators import IndicatorCreateDTO, IndicatorUpdateDTO, IndicatorResponseDTO
from src.services.IndicatorsService import IndicatorsService

indicators_service = IndicatorsService()

indicators_router = APIRouter(
    prefix="/indicators",
    tags=["Indicators"]
)

@indicators_router.get("/", response_model=List[IndicatorResponseDTO])
async def read_indicators(current_user: User = Depends(AuthService.get_current_user)):
    indicators = await indicators_service.listar_indicadores()
    return [IndicatorResponseDTO.from_orm(indicator) for indicator in indicators]

@indicators_router.get("/{indicator_id}", response_model=IndicatorResponseDTO)
async def read_indicator(indicator_id: int, current_user: User = Depends(AuthService.get_current_user)):
    indicator = await indicators_service.obter_indicador(indicator_id)
    if not indicator:
        raise HTTPException(status_code=404, detail="Indicator not found")
    return IndicatorResponseDTO.from_orm(indicator)

@indicators_router.post("/", response_model=IndicatorResponseDTO)
async def create_indicator(item: IndicatorCreateDTO, current_user: User = Depends(AuthService.get_current_user)):
    new_indicator = await indicators_service.inserir_indicador(item)
    return IndicatorResponseDTO.from_orm(new_indicator)

@indicators_router.put("/{indicator_id}", response_model=IndicatorResponseDTO)
async def update_indicator(indicator_id: int, item: IndicatorUpdateDTO, current_user: User = Depends(AuthService.get_current_user)):
    updated_indicator = await indicators_service.atualizar_indicador(indicator_id, item)
    if not updated_indicator:
        raise HTTPException(status_code=404, detail="Indicator not found")
    return IndicatorResponseDTO.from_orm(updated_indicator)

@indicators_router.delete("/{indicator_id}", response_model=dict)
async def delete_indicator(indicator_id: int, current_user: User = Depends(AuthService.get_current_user)):
    success = await indicators_service.deletar_indicador(indicator_id)
    if not success:
        raise HTTPException(status_code=404, detail="Indicator not found")
    return {"detail": "Indicator deleted"}
