"""/ router"""

from dataclasses import dataclass

from bs4 import BeautifulSoup
from fastapi import APIRouter, Form
from starlette.requests import Request
from starlette.responses import HTMLResponse, RedirectResponse

from simon_aksw_org.messages import Message, get_messages
from simon_aksw_org.settings import get_settings

router = APIRouter()


@router.get("/", include_in_schema=False)
async def homepage(request: Request) -> HTMLResponse:
    """Homepage"""
    settings = get_settings()

    messages = get_messages(data_dir=settings.data_dir)

    @dataclass
    class PageContext:
        """Page Context"""

        title: str = settings.title
        birth_date: str = settings.birth_date
        death_date: str = settings.death_date
        version: str = settings.version
        published_date: str = settings.published_date

    context = {
        "messages": messages,
        "context": PageContext(),
        "show_messages": settings.show_messages if len(messages) > 0 else False,
        "allow_messages": settings.allow_messages,
    }

    response: HTMLResponse = settings.templates.TemplateResponse(
        request=request, name="home.html", context=context
    )
    return response


@router.post("/", include_in_schema=False)
async def submit_statement(
    name: str = Form(...),
    message: str = Form(...),
) -> RedirectResponse:
    """Process condolence form submission"""
    settings = get_settings()
    soup = BeautifulSoup(message, 'html.parser')
    entry = Message(name=name, message=soup.get_text())
    file_path = settings.data_dir / f"{entry.id!s}.json"
    file_path.write_text(entry.model_dump_json(indent=2))
    return RedirectResponse(url="/", status_code=303)
