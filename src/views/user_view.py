from fastapi import APIRouter, Depends

from src.models import UserModels
from src.schemas.user_schemas import UserSchemaIn, UserSchemaOut
from src.services.auth_services import AuthJWTServices
from src.services.user_services import UserServices

user_router = APIRouter(prefix='/users', tags=['auth'])


@user_router.post('/create-user', response_model=UserSchemaOut)
async def create_user(user: UserSchemaIn) -> UserModels:
    user = await UserServices.create_user(user)
    return user


@user_router.get('/get-me', response_model=UserSchemaOut)
async def get_user(user: UserModels = Depends(AuthJWTServices.get_current_user)) -> UserModels:
    return user
