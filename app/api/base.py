import os
import logging
from fastapi import APIRouter

from app import schemas
from app.utils import common

router = APIRouter()

logger = logging.getLogger(__name__)


@router.get(
    "/",
    response_model=schemas.base.BaseResponse,)
async def root():
    return common.get_success_response(
        {
            "url": "localhost",
            "enviroment": os.getenv("BRANCH"),
            "version": os.getenv("VERSION_REVISION"),
        }
    )

@router.get(
    "/health",
    response_model=schemas.base.BaseResponse,
)
async def health():
    return common.get_success_response(
        {
            "status": "OK",
        }
    )
