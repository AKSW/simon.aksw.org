"""/ router"""

from dataclasses import dataclass

from fastapi import APIRouter
from starlette.requests import Request
from starlette.responses import HTMLResponse

from simon_aksw_org.settings import get_settings

router = APIRouter()


@router.get("/", include_in_schema=False)
async def homepage(request: Request) -> HTMLResponse:
    """Homepage"""
    settings = get_settings()

    @dataclass
    class PageContext:
        """Page Context"""

        title: str = settings.title
        birth_date: str = settings.birth_date
        death_date: str = settings.death_date
        version: str = settings.version
        published_date: str = settings.published_date

    response: HTMLResponse = settings.templates.TemplateResponse(
        request=request, name="home.html", context={"context": PageContext()}
    )
    return response
