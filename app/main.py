import logging

from fastapi import FastAPI


from app.api.api_router import api_router
from app.core.config import CONFIG


logging.basicConfig(level=logging.INFO)

app = FastAPI(
    title=CONFIG.PROJECT_NAME,
    version=CONFIG.VERSION,
)

app.include_router(api_router, prefix=CONFIG.API_V1_STR)
