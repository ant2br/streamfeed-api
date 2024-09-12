from typing import List
from src.models.indicadores import Indicator
from src.dto.indicators import IndicatorCreateDTO, IndicatorUpdateDTO
from tortoise.exceptions import DoesNotExist
from fastapi import HTTPException

class IndicatorsService:
    TENANT_ID = 1  # Definido o tenant fixo

    @staticmethod
    async def listar_indicadores() -> List[Indicator]:
        try:
            indicators = await Indicator.filter(tenant=IndicatorsService.TENANT_ID).all()
            return indicators
        except Exception as e:
            raise HTTPException(status_code=500, detail="Error fetching indicators")

    @staticmethod
    async def obter_indicador(indicator_id: int) -> Indicator:
        try:
            indicator = await Indicator.get(id=indicator_id, tenant=IndicatorsService.TENANT_ID)
            return indicator
        except DoesNotExist:
            raise HTTPException(status_code=404, detail="Indicator not found")
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @staticmethod
    async def inserir_indicador(item: IndicatorCreateDTO) -> Indicator:
        try:
            item_data = item.dict()
            item_data['tenant'] = IndicatorsService.TENANT_ID
            new_indicator = await Indicator.create(**item_data)
            return new_indicator
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

    @staticmethod
    async def atualizar_indicador(indicator_id: int, item: IndicatorUpdateDTO) -> Indicator:
        try:
            indicator = await Indicator.get(id=indicator_id, tenant=IndicatorsService.TENANT_ID)
            updated_indicator = await indicator.update_from_dict(item.dict())
            await updated_indicator.save()
            return updated_indicator
        except DoesNotExist:
            raise HTTPException(status_code=404, detail="Indicator not found")
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

    @staticmethod
    async def deletar_indicador(indicator_id: int) -> bool:
        try:
            indicator = await Indicator.get(id=indicator_id, tenant=IndicatorsService.TENANT_ID)
            await indicator.delete()
            return True
        except DoesNotExist:
            raise HTTPException(status_code=404, detail="Indicator not found")
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
