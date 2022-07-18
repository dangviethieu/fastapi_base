import logging.config

from fastapi import FastAPI, requests
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app import api
from app.db.mysql import SessionLocal
from app.settings.settings import AppInfo, DocsURL
from app.utils.http_exception import include_exception_handler


logging.config.fileConfig('app/logs/logging.conf',
                        disable_existing_loggers=False)


def get_app() -> FastAPI:
    app_env = AppInfo().app_env
    if app_env == "prod":
        debug = False
    else:
        debug = True
    
    new_app = FastAPI(
        debug=debug,
        docs_url=f"/{DocsURL().docs_url}"
    )

    new_app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    new_app.include_router(api.router)
    new_app = include_exception_handler(new_app)
    return new_app

app = get_app()
app.mount("/public", StaticFiles(directory="public"), name="public")

@app.middleware("http")
async def db_session_middleware(request: requests, call_next):
    try:
        request.state.db = SessionLocal()
        response = await call_next(request)
    finally:
        request.state.db.close()
    return response