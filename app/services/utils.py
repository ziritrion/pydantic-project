from upstash_redis import Redis
import os
from uuid import UUID
from typing import Optional

from app.models.polls import Poll
from app.models.votes import Vote

redis_client = Redis(
    url=os.getenv("KV_REST_API_URL"),
    token=os.getenv("KV_REST_API_TOKEN")
)

def save_poll(poll:Poll) -> Optional[str]:
    return redis_client.set(key=f"poll:{poll.id}", value=poll.model_dump_json())
    
def get_poll(poll_id: UUID) -> Optional[Poll]:
    poll_json = redis_client.get(key=f"poll:{poll_id}")
    if poll_json:
        return Poll.model_validate_json(poll_json)
    return None

def get_choice_id_by_label(poll_id: UUID, label: int) -> Optional[UUID]:
    poll = get_poll(poll_id=poll_id)
    if not poll:
        return None
    for choice in poll.options:
        if choice.label == label:
            return choice.id
    return None

def save_vote(poll_id: UUID, vote: Vote) -> Optional[str]:
    return redis_client.hset(f"votes:{poll_id}", vote.voter.email, vote.model_dump_json())
    
def get_vote(poll_id: UUID, email: str) -> Optional[Vote]:
    vote_json = redis_client.hget(f"votes:{poll_id}", email)
    if vote_json:
        return Vote.model_validate_json(vote_json)
    return None