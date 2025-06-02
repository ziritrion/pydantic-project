from pydantic import BaseModel, EmailStr, Field
from datetime import datetime, UTC
from uuid import UUID

class VoterCreate(BaseModel):
    """The Voter write model, consists of only an email address."""
    email: EmailStr

class Voter(VoterCreate):
    """The Voter read model."""
    voted_at: datetime = Field(default_factory=lambda: datetime.now(tz=UTC))

class Vote(BaseModel):
    """The Vote read model."""
    poll_id: UUID
    choice_id: UUID
    voter: Voter

class VoteById(BaseModel):
    choice_id: UUID
    voter: VoterCreate

class VoteByLabel(BaseModel):
    choice_label: int
    voter: VoterCreate