"""Re-Captcha v2 validation"""

import httpx
from pydantic import BaseModel

API_VERIFY_URL = "https://www.google.com/recaptcha/api/siteverify"


class ValidationResponse(BaseModel):
    """Response Token Validation Response

    {'success': True, 'challenge_ts': '2026-03-08T21:48:08Z', 'hostname': 'localhost'}
    """

    success: bool


class ResponseToken:
    """Response token"""

    def __init__(self, token: str, secret_key: str):
        self.token = token
        self.secret_key = secret_key

    async def is_valid(self) -> bool:
        """Check if response token is valid"""
        async with httpx.AsyncClient() as client:
            response = await client.post(
                url=API_VERIFY_URL,
                data={"secret": self.secret_key, "response": self.token},
            )
        validation = ValidationResponse(**response.json())
        return validation.success
