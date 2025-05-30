from pydantic import BaseModel, Field
from uuid import UUID, uuid4

class Choice(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    description: str = Field(min_length=1, max_length=100)
    label: int = Field(ge=1, le=5)