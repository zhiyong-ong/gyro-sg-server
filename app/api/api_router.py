from fastapi import APIRouter

from app.api.endpoints import users, login, bikes

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
