"""main app"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi_problem_details import init_app as init_app_problem_details

from simon_aksw_org.routers import favicon, home
from simon_aksw_org.settings import Settings, get_settings


def create_app(settings: Settings) -> FastAPI:
    """Create FastAPI app"""
    app = FastAPI(
        title=settings.title,
        version=settings.version,
    )

    app.settings = settings  # type: ignore[attr-defined]
    init_app_problem_details(app)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.mount("/static", StaticFiles(directory=settings.static_dir), name="static")
    app.include_router(home.router)
    app.include_router(favicon.router)
    settings.logger.info(f"{settings.title} v{settings.version} initialized")
    return app


simon_aksw_org = create_app(settings=get_settings())
