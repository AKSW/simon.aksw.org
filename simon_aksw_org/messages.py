"""Message Model and Retrieval"""
from datetime import datetime, UTC
from pathlib import Path
from typing import List

from pydantic import BaseModel, Field
from ulid import ULID

def now() -> datetime:
    return datetime.now(tz=UTC)

class Message(BaseModel):

    id: ULID = Field(description="Unique message id", default_factory=ULID)
    name: str = Field(description="Name")
    message: str = Field(description="Message")
    submitted_at: datetime = Field(description="Submitted at", default_factory=now)

    @property
    def submitted_at_str(self) -> str:
        return self.submitted_at.strftime("%d.%m.%Y - %H:%M")


def get_messages(data_dir: Path) -> List[Message]:
    """Get all messages"""
    messages = []
    for filename in sorted(data_dir.glob("*.json"), reverse=False):
        message = Message.model_validate_json(filename.read_text(encoding="utf-8"))
        messages.append(message)
    return messages
