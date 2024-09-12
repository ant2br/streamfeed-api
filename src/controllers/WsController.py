from typing import Optional
from fastapi import APIRouter, Depends, Form, HTTPException, WebSocket, WebSocketDisconnect
from src.models.user import User
from pymongo import MongoClient
from src.dto.user import UserCreateDTO, Token, LoginBody
from src.services.UsersService import UsersService
from src.services.authService import AuthService
from datetime import timedelta
import json
import asyncio



ws_router = APIRouter(
    prefix="/ws",
    tags=["Ws"]
)

mongo_db = "symbols"
mongo_collection = "quotes"


# Conectando ao MongoDB com autenticação
client = MongoClient("mongodb://your_user:your_password@64.23.196.60:27017/")
db = client[mongo_db]
collection = db[mongo_collection]



@ws_router.get("/symbols")
async def websocket_endpoint():
    
    quotes = list(collection.find({}, {'_id': 0}))
    kc_quotes = [quote for quote in quotes if quote['symbol'].startswith('KC')]
    dol_quotes = [quote for quote in quotes if quote['symbol'].startswith('DOL')]
    response = {'KC': kc_quotes, 'DOL': dol_quotes}
    return response





@ws_router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    
    
    try:
        while True:
            quotes = list(collection.find({}, {'_id': 0}))
            kc_quotes = [quote for quote in quotes if quote['symbol'].startswith('KC')]
            dol_quotes = [quote for quote in quotes if quote['symbol'].startswith('DOL')]
            response = {'KC': kc_quotes, 'DOL': dol_quotes}
            await websocket.send_text(json.dumps(response, indent=2))
            
            await asyncio.sleep(10)
    except WebSocketDisconnect:
        print("Cliente desconectado do WebSocket")
    except Exception as e:
        print(f"Erro no WebSocket: {e}")

        await websocket.close(code=1000)

        
        
        

