from uuid import UUID
from fastapi import APIRouter, HTTPException

from app.models.votes import VoteById, VoteByLabel, Vote, Voter
from app.services import utils

router = APIRouter()

@router.post("/{poll_id}/id")
def vote_by_id(poll_id: UUID, vote: VoteById):
    # first we check whether the voter already voted in the poll
    if utils.get_vote(poll_id=poll_id, email=vote.voter.email):
        raise HTTPException(
            status_code=400,
            detail="Already voted"
        )
    vote = Vote(
        poll_id=poll_id,
        choice_id=vote.choice_id,
        voter=Voter(
            **vote.voter.model_dump() # using unpacking to pass the arguments to the class
        )
    )
    utils.save_vote(poll_id=poll_id, vote=vote)
    return {"message": "Vote recorded", "vote": vote}

@router.post("/{poll_id}/label")
def vote_by_label(poll_id: UUID, vote: VoteByLabel):
    # We need to retrieve the UUID for the choice; we check whether it exists
    choice_id = utils.get_choice_id_by_label(poll_id=poll_id, label=vote.choice_label)
    if not choice_id:
        raise HTTPException(status_code=400, detail="Invalid choice label provided.")
    # we check whether the voter already voted in the poll
    if utils.get_vote(poll_id=poll_id, email=vote.voter.email):
        raise HTTPException(
            status_code=400,
            detail="Already voted"
        )
    vote = Vote(
        poll_id=poll_id,
        choice_id=choice_id,
        voter=Voter(
            **vote.voter.model_dump() # using unpacking to pass the arguments to the class
        )
    )
    utils.save_vote(poll_id=poll_id, vote=vote)
    return {"message": "Vote recorded", "vote": vote}