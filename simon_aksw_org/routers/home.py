"""/ router"""

from typing import Annotated

import httpx
from fastapi import APIRouter, Form
from starlette.requests import Request
from starlette.responses import HTMLResponse, RedirectResponse, Response

from simon_aksw_org.messages import get_messages, save_message
from simon_aksw_org.recaptcha import ResponseToken
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
    return settings.templates.TemplateResponse(
        request=request, name="home.html", context={"context": context}
    )


@router.post("/", include_in_schema=False)
async def submit_statement(
    request: Request,
    name: Annotated[str, Form()],
    message: Annotated[str, Form()],
    g_recaptcha_response: Annotated[str, Form(alias="g-recaptcha-response")] = "",
) -> Response:
    """Process condolence form submission"""
    settings = get_settings()
    settings.logger.info(f"{name} submitted a message ... captcha: {g_recaptcha_response}")
    response_token = ResponseToken(
        token=g_recaptcha_response, secret_key=settings.recaptcha_secret_key.get_secret_value()
    )

    if await response_token.is_valid():
        message_id = save_message(name=name, text=message, data_dir=settings.data_dir)
        context = PageContext(settings)
        return RedirectResponse(url=f"/#message-{message_id}", status_code=303)
    context = PageContext(settings)
    context.error = "reCAPTCHA validation failed"
    status_code = httpx.codes.BAD_REQUEST
    return settings.templates.TemplateResponse(
        request=request, name="home.html", context={"context": context}, status_code=status_code
    )
