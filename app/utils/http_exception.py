import logging

from fastapi import Request
from fastapi.responses import JSONResponse

from app.utils.message import SERVER_ERROR

logger = logging.getLogger(__name__)


def include_exception_handler(app):
    app.add_exception_handler(ErrorRequestException, error_request)
    return app

class ErrorRequestException(Exception):
    def __init__(self, content=None):
        if isinstance(content, str):
            self.content = {
                "message": content
            }
        else:
            self.content = content

async def error_request(request: Request, exc: ErrorRequestException):
    logger.error(f"Request {request} - Error: {exc}")
    return JSONResponse(
        status_code=400,
        content={
            "status": False,
            "content": exc.content
        }
    )

def raise_exception(e, db=None):
    logger.error(f"Error: {e}")
    if db is not None:
        db.rollback()
        db.close()
    if isinstance(e, ErrorRequestException) and e.content != SERVER_ERROR:
        raise ErrorRequestException(e.content)
    return ErrorRequestException(SERVER_ERROR)