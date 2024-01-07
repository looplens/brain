from fastapi import APIRouter

from .profile import router as profile_router
from .block import router as block_router
from .follow import router as follow_router
from .login import router as login_router
from .register import router as register_router

router = APIRouter()

router.include_router(profile_router, tags=["profile"])
router.include_router(block_router, tags=["blocks"])
router.include_router(follow_router, tags=["follow"])
router.include_router(login_router, tags=["login"])
router.include_router(register_router, tags=["register"])
