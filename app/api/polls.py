from fastapi import APIRouter, HTTPException
from uuid import UUID

from app.models.polls import PollCreate
from app.services import utils

router = APIRouter()

@router.post("/create")
def create_poll(poll: PollCreate):
    new_poll = poll.create_poll()
    utils.save_poll(poll=new_poll)
    return {
        "detail": "Poll successfully created",
        "poll_id": new_poll.id,
        "poll": new_poll
    }

@router.get("/{poll_id}")
def get_poll(poll_id: UUID):
    poll = utils.get_poll(poll_id=poll_id)
    if not poll:
        raise HTTPException(
            status_code=404,
            detail="Cannot retrieve poll: the poll does not exist"
        )
    return poll