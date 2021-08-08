from fastapi import APIRouter

from app.api.endpoints import users, login, bikes, bike_models

api_router = APIRouter()
api_router.include_router(
    users.router,
    tags=["users"],
    prefix="/users",
)
api_router.include_router(
    login.router,
    tags=["login"],
)
api_router.include_router(
    bikes.router,
    tags=["bikes"],
    prefix="/bikes",
)
api_router.include_router(
    bike_models.router,
    tags=["bike_models"],
    prefix="/bike_models",
)
