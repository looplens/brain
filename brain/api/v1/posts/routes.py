from fastapi import APIRouter

from .create import router as create_router
from .like import router as like_router
from .delete import router as delete_router
from .likes import router as likes_router
from .bookmark import router as bookmark_router
from .posts import router as posts_router


router = APIRouter()


router.include_router(posts_router, tags=["posts"])

router.include_router(create_router, tags=["create"])
router.include_router(delete_router, tags=["delete"])

router.include_router(like_router, tags=["like"])
router.include_router(likes_router, tags=["likes"])

router.include_router(bookmark_router, tags=["bookmark"])

