from pydantic import BaseModel, Field
from uuid import UUID, uuid4
from datetime import datetime, UTC
from typing import Optional

class Poll(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    title: str = Field(min_length=5, max_length=50)
    options: list[str]
    created_at: datetime = Field(default_factory=lambda: datetime.now(tz=UTC))
    expires_at: Optional[datetime] = None