"""main app"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi_problem_details import init_app as init_app_problem_details

from simon_aksw_org.routers import favicon, home
from simon_aksw_org.settings import Settings, get_settings


def create_app(settings: Settings) -> FastAPI:
    """Create FastAPI app"""
    new_app = FastAPI(
        title=settings.title, version=settings.version, docs_url=None, openapi_url=None
    )

    new_app.settings = settings  # type: ignore[attr-defined]
    init_app_problem_details(new_app)

    new_app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    new_app.mount("/static", StaticFiles(directory=settings.static_dir), name="static")
    new_app.include_router(home.router)
    new_app.include_router(favicon.router)
    settings.logger.info(f"{settings.title} v{settings.version} initialized")
    return new_app


app = create_app(settings=get_settings())
