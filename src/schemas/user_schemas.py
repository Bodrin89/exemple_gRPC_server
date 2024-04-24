from pydantic import BaseModel, EmailStr
from tortoise.contrib.pydantic import pydantic_model_creator

from src.models.user_models import UserModels

UserSchemaOut = pydantic_model_creator(UserModels, exclude=('password',))


class UserSchemaIn(BaseModel):
    name: str
    email: EmailStr
    password: str
