from typing import List
from src.models.symbols import Symbol
from tortoise.exceptions import DoesNotExist
from fastapi import HTTPException

class SymbolService:
    TENANT_ID = 1  # Definido o tenant fixo

    @staticmethod
    async def create_symbol(symbol_data: dict):
        try:
            symbol_data['tenant'] = SymbolService.TENANT_ID
            new_symbol = await Symbol.create(**symbol_data)
            return new_symbol
        except Exception as e:
            # Tratar exceções específicas, se necessário
            raise HTTPException(status_code=400, detail=str(e))

    @staticmethod
    async def get_all_symbols():
        try:
            symbols = await Symbol.filter(tenant=SymbolService.TENANT_ID).all()
            return symbols
        except Exception as e:
            raise HTTPException(status_code=500, detail="Error fetching symbols")

    @staticmethod
    async def get_symbol_by_id(symbol_id: int):
        try:
            symbol = await Symbol.get(id=symbol_id, tenant=SymbolService.TENANT_ID)
            return symbol
        except DoesNotExist:
            raise HTTPException(status_code=404, detail="Symbol not found")
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @staticmethod
    async def update_symbol(symbol_id: int, symbol_data: dict):
        try:
            symbol = await Symbol.get(id=symbol_id, tenant=SymbolService.TENANT_ID)
            await symbol.update_from_dict(symbol_data)
            await symbol.save()
            return symbol
        except DoesNotExist:
            raise HTTPException(status_code=404, detail="Symbol not found")
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

    @staticmethod
    async def delete_symbol(symbol_id: int):
        try:
            symbol = await Symbol.get(id=symbol_id, tenant=SymbolService.TENANT_ID)
            await symbol.delete()
            return symbol
        except DoesNotExist:
            raise HTTPException(status_code=404, detail="Symbol not found")
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
