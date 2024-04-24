from asyncio import Future
from datetime import datetime, timedelta

import bcrypt
import jwt
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from starlette import status

from src.config.settings import (
    ALGORITHM_JWT,
    EXPIRE_ACCESS_TOKEN_TIME,
    EXPIRE_REFRESH_TOKEN_TIME,
    SALT,
    SECRET_KEY,
    TOKEN_TYPE,
)
from src.dao.user_dao import UserDAO
from src.schemas.auth_schema import TokenOut
from src.schemas.user_schemas import UserSchemaOut


class PasswordServices:
    """Сервисы для работы с паролями"""

    @staticmethod
    async def hashed_password(password: str) -> str:
        """Хэширование пароля"""
        salt = SALT.encode('utf-8')
        pwd_bytes = password.encode('utf-8')
        return bcrypt.hashpw(pwd_bytes, salt).decode('utf-8')

    @staticmethod
    async def check_password(password: str, hashed_password: str) -> bool:
        """Проверка пароля"""
        pwd_bytes = password.encode('utf-8')
        return bcrypt.checkpw(pwd_bytes, hashed_password.encode('utf-8'))


class AuthJWTServices:
    """Сервисы для работы с JWT"""

    @staticmethod
    async def gen_access_refresh_tokens(data: dict | UserSchemaOut) -> TokenOut:
        """Генерация access и refresh токенов"""
        if isinstance(data, UserSchemaOut):
            jwt_payload = {'id': str(data.id), 'name': data.name, 'email': data.email}
        else:
            jwt_payload = {'id': str(data['id']), 'name': data['name'], 'email': data['email']}
        access_token: str = await AuthJWTServices.__encode_jwt(
            payload=jwt_payload, expire_time=EXPIRE_ACCESS_TOKEN_TIME
        )
        refresh_token: str = await AuthJWTServices.__encode_jwt(
            payload=jwt_payload, expire_time=EXPIRE_REFRESH_TOKEN_TIME
        )

        return TokenOut(access_token=access_token, refresh_token=refresh_token, token_type=TOKEN_TYPE)

    @staticmethod
    async def __encode_jwt(
        payload: dict,
        algorithm: str = ALGORITHM_JWT,
        expire_time: int = EXPIRE_ACCESS_TOKEN_TIME,
        secret_key: str = SECRET_KEY,
    ) -> str:
        """Создание токена"""
        now = datetime.utcnow()
        expire = now + timedelta(minutes=expire_time)
        to_payload = payload.copy()
        to_payload.update(exp=expire, iat=now)
        encoded_jwt = jwt.encode(payload=to_payload, key=secret_key, algorithm=algorithm)
        return encoded_jwt

    @staticmethod
    async def decode_jwt(token: str, key: str = SECRET_KEY, algorithms: str = ALGORITHM_JWT) -> dict:
        """Декодирование токена"""
        try:
            decoded_token = jwt.decode(jwt=token, key=key, algorithms=[algorithms])
            return decoded_token
        except jwt.exceptions.ExpiredSignatureError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Token expired')
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Token invalid')

    @staticmethod
    async def get_payload_token(credentials_token: HTTPAuthorizationCredentials = Depends(HTTPBearer())) -> dict:
        """Декодирование токена и получение данных из него"""
        token = credentials_token.credentials
        payload = await AuthJWTServices.decode_jwt(token)
        return payload

    @staticmethod
    async def get_current_user(payload: Future[dict] = Depends(get_payload_token)) -> UserSchemaOut:
        """Получение текущего пользователя"""
        real_payload = await payload
        user_id = int(real_payload['id'])
        user = await UserDAO.get_user_id(user_id)
        return await UserSchemaOut.from_tortoise_orm(user)
