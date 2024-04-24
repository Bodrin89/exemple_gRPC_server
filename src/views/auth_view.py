from fastapi import APIRouter

from src.schemas.auth_schema import TokenIn, TokenOut
from src.services.auth_services import AuthJWTServices
from src.services.user_services import UserServices

auth_router = APIRouter(prefix='/auth', tags=['auth'])


@auth_router.post('/create-token', response_model=TokenOut)
async def create_token(auth_data: TokenIn) -> TokenOut:
    """Создание токена"""
    user = await UserServices.valid_user(auth_data)
    token = await AuthJWTServices.gen_access_refresh_tokens(user)
    return token
