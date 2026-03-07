"""Router and backend for the /favicon.ico path"""

import fastapi
from starlette.responses import RedirectResponse

router = fastapi.APIRouter()


@router.get("/favicon.ico", include_in_schema=False)
def favicon() -> RedirectResponse:
    """Redirect /favicon.ico to static files area."""
    return fastapi.responses.RedirectResponse(url="./static/favicon.ico")
