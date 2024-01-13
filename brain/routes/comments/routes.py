from fastapi import APIRouter

from .create import router as create_router
from .delete import router as delete_router
from .comments import router as comments_router


router = APIRouter()


router.include_router(comments_router, tags=["comments"])
router.include_router(create_router, tags=["create"])
router.include_router(delete_router, tags=["delete"])
