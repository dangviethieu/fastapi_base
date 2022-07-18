from fastapi import APIRouter

from app.api.base import router as base_router
from app.api.users import router as users_router


router = APIRouter()

router.include_router(base_router, tags=["Base"])
router.include_router(users_router, tags=["Users"])