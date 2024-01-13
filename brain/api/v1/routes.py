from fastapi import APIRouter

from .users.routes import router as users_router
from .posts.routes import router as posts_router
from .search.routes import router as search_router
from .comments.routes import router as comments_router


v1 = APIRouter()


v1.include_router(users_router, prefix="/users")
v1.include_router(posts_router, prefix="/posts")
v1.include_router(search_router, prefix="/search")
v1.include_router(comments_router, prefix="/comments")
