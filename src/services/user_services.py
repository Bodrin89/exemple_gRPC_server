from fastapi import HTTPException
from starlette import status

from src.dao.user_dao import UserDAO
from src.schemas.auth_schema import TokenIn
from src.schemas.user_schemas import UserSchemaIn, UserSchemaOut
from src.services.auth_services import PasswordServices


class UserServices:
    @staticmethod
    async def create_user(user_in: UserSchemaIn) -> UserSchemaOut:
        """Создание пользователя"""
        user_in.password = await PasswordServices.hashed_password(user_in.password)
        user = await UserDAO.create_user(user_in)
        user_out = await UserSchemaOut.from_tortoise_orm(user)
        return user_out

    @staticmethod
    async def valid_user(auth_data: TokenIn) -> UserSchemaOut:
        """Валидация пользователя"""
        email = auth_data.email
        password = auth_data.password
        hash_password = await PasswordServices.hashed_password(password)
        user = await UserDAO.get_user_email_password(email, hash_password)
        if user:
            return await UserSchemaOut.from_tortoise_orm(user)
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str('пользователь не найден!'))
