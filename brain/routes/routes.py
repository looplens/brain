from fastapi import APIRouter

from .users.routes import router as users_router
from .posts.routes import router as posts_router
from .search.routes import router as search_router

router = APIRouter()

router.include_router(users_router, prefix="/users")
router.include_router(posts_router, prefix="/posts")
router.include_router(search_router, prefix="/search")
