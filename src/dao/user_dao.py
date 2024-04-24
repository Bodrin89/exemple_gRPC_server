from src.models.user_models import UserModels


class UserDAO:
    @staticmethod
    async def create_user(data):
        user = await UserModels.create(**data.model_dump(exclude_unset=True))
        return user

    @staticmethod
    async def get_user_email_password(email: str, hash_password: str) -> UserModels:
        user = await UserModels.filter(email=email, password=hash_password).first()
        return user

    @staticmethod
    async def get_user_id(user_id: int) -> UserModels:
        user = await UserModels.get(id=user_id)
        return user
