from pydantic import BaseModel

from src.config.settings import TOKEN_TYPE


class TokenIn(BaseModel):
    email: str
    password: str


class TokenOut(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = TOKEN_TYPE
