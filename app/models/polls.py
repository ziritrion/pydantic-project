from pydantic import BaseModel, Field
from uuid import UUID, uuid4
from datetime import datetime, UTC

class Poll(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    options: list[str]
    created_at: datetime = Field(default_factory=lambda: datetime.now(tz=UTC))