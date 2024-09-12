from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from src.dto.user import UserCreateDTO
from src.models.user import User
from dotenv import load_dotenv
import os
load_dotenv()


# Configurações para JWT
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/users/token")

class AuthService:
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        return AuthService.pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt

    @staticmethod
    def decode_access_token(token: str) -> dict:
        try:
            decoded_jwt = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            return decoded_jwt
        except JWTError:
            raise HTTPException(status_code=401, detail="Invalid token")

    @staticmethod
    async def authenticate_user(username: str, password: str) -> Optional[User]:
        user = await User.filter(email=username).first()
        if user and AuthService.verify_password(password, user.hashed_password):
            return user
        return None

    @staticmethod
    async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
        credentials_exception = HTTPException(
            status_code=401,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = AuthService.decode_access_token(token)
            username: str = payload.get("sub")
            if username is None:
                raise credentials_exception
            user = await User.filter(username=username).first()
            if user is None:
                raise credentials_exception
        except JWTError:
            raise credentials_exception
        return user
