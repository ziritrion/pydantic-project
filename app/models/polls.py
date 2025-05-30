from pydantic import BaseModel, Field, field_validator
from uuid import UUID, uuid4
from datetime import datetime, UTC
from typing import Optional
from fastapi import HTTPException

from app.models.choice import Choice

class PollCreate(BaseModel):
    """Poll write data model"""
    title: str = Field(min_length=5, max_length=50)
    options: list[str]
    expires_at: Optional[datetime] = None
    
    @field_validator("options")
    @classmethod
    def validate_options(cls, o: list[str]) -> list[str]:
        if len(o) < 2 or len(o) > 5:
            #raise ValueError("A poll must contain between 2 and 5 choices.")
            raise HTTPException(
                status_code=400,
                detail="A poll must contain between 2 and 5 choices.")
        return o
    
    def create_poll(self) -> "Poll":
        """
        Create a new Poll instance with auto-incrementing labels for Choices, e.g. 1, 2, 3
        
        This will be used in the POST /polls/create endpoint
        """
        # create a list of Choices from list[str]
        choices = [
            Choice(
                description=desc,
                label=index + 1
            )
            for index, desc in enumerate(self.options)
        ]
        # validate expiration date
        if self.expires_at is not None and self.expires_at < datetime.now(tz=UTC):
            #raise ValueError("A poll's expiration date must be in the future.")
            raise HTTPException(
                status_code=400,
                detail="A poll's expiration date must be in the future."
            )
        # return instance of Poll
        return Poll(title=self.title, options=choices, expires_at=self.expires_at)

class Poll(PollCreate):
    """Poll read data model, with uuid and creation date"""
    id: UUID = Field(default_factory=uuid4)
    options: list[Choice]
    created_at: datetime = Field(default_factory=lambda: datetime.now(tz=UTC))
    