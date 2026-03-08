"""Message Model and Retrieval"""

from datetime import UTC, datetime
from pathlib import Path

from pydantic import BaseModel, Field
from ulid import ULID


def now() -> datetime:
    """Default factory for submitted_at"""
    return datetime.now(tz=UTC)


class Message(BaseModel):
    """Message Model"""

    id: ULID = Field(description="Unique message id", default_factory=ULID)
    name: str = Field(description="Name")
    message: str = Field(description="Message")
    submitted_at: datetime = Field(description="Submitted at", default_factory=now)

    @property
    def submitted_at_str(self) -> str:
        """Get submitted at string"""
        return self.submitted_at.strftime("%d.%m.%Y - %H:%M")


def get_messages(data_dir: Path) -> list[Message]:
    """Get all messages"""
    messages = []
    for filename in sorted(data_dir.glob("*.json"), reverse=False):
        message = Message.model_validate_json(filename.read_text(encoding="utf-8"))
        messages.append(message)
    return messages
