from fastapi import APIRouter

from memes.routers import router


api_router = APIRouter()
api_router.include_router(router, prefix="/memes", tags=["memes"])
