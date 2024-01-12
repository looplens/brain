from fastapi import APIRouter
from .create import router as create_router
from .like import router as like_router


router = APIRouter()


router.include_router(create_router, tags=["create"])
router.include_router(like_router, tags=["like"])
