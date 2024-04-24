from tortoise import Tortoise
from tortoise.contrib.fastapi import register_tortoise

from src.config.settings import DATABASE_CONFIG


def connect_db(app):
    """Инициализация БД для FastAPI"""
    Tortoise.init_models(
        [DATABASE_CONFIG['apps']['models']['models'][0]], 'models'
    )  # Для инициализации моделей в схемы

    register_tortoise(app=app, config=DATABASE_CONFIG, generate_schemas=True)


async def init():
    """Инициализация БД не для FastAPI а для gRPC"""
    await Tortoise.init(db_url=DATABASE_CONFIG['connections']['default'], modules={'models': ['src.models']})
    await Tortoise.generate_schemas()
