from fastapi import APIRouter
from .v1.routes import v1 as api_v1


api_endpoint = APIRouter()

api_endpoint.include_router(api_v1, prefix="/v1")
