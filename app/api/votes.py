from uuid import UUID
from fastapi import APIRouter, HTTPException, Depends
from typing import Union
from app.models.votes import VoteById, VoteByLabel, Vote, Voter
from app.models.polls import Poll
from app.services import utils

router = APIRouter()

def common_validations(poll_id: UUID, vote: Union[VoteById, VoteByLabel]):
    """Method that does all the common validations for all voting options; this method is meant to be injected as a dependency."""
    poll = utils.get_poll(poll_id=poll_id)
    voter_email = vote.voter.email
    # we check whether the poll exists
    if not poll:
        raise HTTPException(
            status_code=404,
            detail="The poll was not found"
        )
    # we check whether the poll is still active
    if not poll.is_active():
        raise HTTPException(
            status_code=400,
            detail="The poll has expired"
        )
    # we check whether the voter already voted in the poll
    if utils.get_vote(poll_id=poll_id, email=voter_email):
        raise HTTPException(
            status_code=400,
            detail="Already voted"
        )
        
    return poll

@router.post("/{poll_id}/id")
def vote_by_id(poll_id: UUID, vote: VoteById,
               poll: Poll = Depends(common_validations) # FastAPI dependency injection
               ):
    # we check whether the vote id is valid
    if vote.choice_id not in [choice.id for choice in poll.options]:
        raise HTTPException(
            status_code=400,
            detail="Invalid choice id specified"
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
def vote_by_label(poll_id: UUID, vote: VoteByLabel,
                  poll: Poll = Depends(common_validations) # FastAPI dependency injection
                  ):
    # We need to retrieve the UUID for the choice; we check whether it exists
    choice_id = utils.get_choice_id_by_label_given(poll=poll, label=vote.choice_label)
    if not choice_id:
        raise HTTPException(
            status_code=400,
            detail="Invalid choice label provided"
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