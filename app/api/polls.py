from fastapi import APIRouter, HTTPException
from uuid import UUID
from enum import Enum

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

@router.get("/{poll_id}/results")
def get_results(poll_id: UUID):
    return utils.get_poll_results(poll_id)

class PollStatus(Enum):
    ACTIVE = "active"
    EXPIRED = "expired"
    ALL = "all"

@router.get("/")
def get_polls(status: PollStatus = PollStatus.ACTIVE):
    polls = utils.get_all_polls()
    if not polls:
        raise HTTPException(
            status_code=404,
            detail="No polls were found"
        )
    if status == PollStatus.ACTIVE:
        filtered_polls = [poll for poll in polls if poll.is_active()]
    elif status == PollStatus.EXPIRED:
        filtered_polls = [poll for poll in polls if not poll.is_active()]
    else: # PollStatus.ALL
        filtered_polls = polls
    return {
        "count": len(filtered_polls),
        "polls": filtered_polls
    }