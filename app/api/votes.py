from uuid import UUID
from fastapi import APIRouter, HTTPException

from app.models.votes import VoteById, VoteByLabel

router = APIRouter()

@router.post("/{poll_id}/id")
def vote_by_id(poll_id: UUID, vote: VoteById):  
    return {"message": "Vote recorded"}

@router.post("/{poll_id}/label")
def vote_by_label(poll_id: UUID, vote: VoteByLabel):
    return {"messasge": "Vote recorded"}