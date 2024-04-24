from debug_toolbar.middleware import DebugToolbarMiddleware
from fastapi import FastAPI

from src.config.db_connect import connect_db
from src.views.auth_view import auth_router
from src.views.user_view import user_router

app = FastAPI(
    title='Tortoise_auth_microservice',
    debug=True,
)

app.include_router(user_router)
app.include_router(auth_router)

app.add_middleware(
    DebugToolbarMiddleware,
    panels=['debug_toolbar.panels.tortoise.TortoisePanel'],
)

connect_db(app)  # Для инициализации моделей в схемы и применения настоек Tortoise ORM
