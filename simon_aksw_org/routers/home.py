"""/ router"""

from typing import Annotated

from fastapi import APIRouter, Form
from starlette.requests import Request
from starlette.responses import HTMLResponse, RedirectResponse

from simon_aksw_org.messages import get_messages, save_message
from simon_aksw_org.settings import Settings, get_settings


class PageContext:
    """Page Context"""

    def __init__(self, settings: Settings, error: str = ""):
        self.title = settings.title
        self.birth_date = settings.birth_date
        self.death_date = settings.death_date
        self.version = settings.version
        self.published_date = settings.published_date
        self.site_key = settings.recaptcha_site_key
        self.messages = get_messages(data_dir=settings.data_dir)
        self.show_messages = settings.show_messages if len(self.messages) > 0 else False
        self.allow_messages = settings.allow_messages
        self.error = error


router = APIRouter()


@router.get("/", include_in_schema=False)
async def homepage(request: Request) -> HTMLResponse:
    """Homepage"""
    settings = get_settings()
    context = PageContext(settings)
    response: HTMLResponse = settings.templates.TemplateResponse(
        request=request, name="home.html", context={"context": context}
    )
    return response


@router.post("/", include_in_schema=False)
async def submit_statement(
    name: Annotated[str, Form()],
    message: Annotated[str, Form()],
) -> RedirectResponse:
    """Process condolence form submission"""
    settings = get_settings()
    save_message(name=name, text=message, data_dir=settings.data_dir)
    return RedirectResponse(url="/", status_code=303)
