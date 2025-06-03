from upstash_redis import Redis
import os
from uuid import UUID
from typing import Optional

from app.models.polls import Poll
from app.models.votes import Vote
from app.models.results import PollResults, Result

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

def get_all_polls() -> list[Poll]:
    poll_keys = redis_client.keys("poll:*") # get all the poll keys
    poll_jsons = redis_client.mget(*poll_keys) # batch get, unpacked list
    polls = [Poll.model_validate_json(pj) for pj in poll_jsons if pj]        
    return polls

def get_choice_id_by_label(poll_id: UUID, label: int) -> Optional[UUID]:
    poll = get_poll(poll_id=poll_id)
    return get_choice_id_by_label_given(poll=poll, label=label)

def get_choice_id_by_label_given(poll: Poll, label: int) -> Optional[UUID]:
    if not poll:
        return None
    for choice in poll.options:
        if choice.label == label:
            return choice.id
    return None

def save_vote(poll_id: UUID, vote: Vote) -> Optional[str]:
    vote_result = redis_client.hset(
        key=f"votes:{poll_id}",
        field=vote.voter.email,
        value=vote.model_dump_json()
    )
    vote_count = redis_client.hincrby(
        key=f"votes_count:{poll_id}",
        field=str(vote.choice_id),
        increment=1
    )
    
def get_vote(poll_id: UUID, email: str) -> Optional[Vote]:
    vote_json = redis_client.hget(f"votes:{poll_id}", email)
    if vote_json:
        return Vote.model_validate_json(vote_json)
    return None

def get_vote_count(poll_id: UUID) -> dict[UUID, int]:
    vote_counts = redis_client.hgetall(key=f"votes_count:{poll_id}")
    return {
        UUID(choice_id): int(count)
        for choice_id, count in vote_counts.items()
    }

def get_poll_results(poll_id: UUID) -> Optional[PollResults]:
    poll = get_poll(poll_id=poll_id)
    if not poll:
        return None
    vote_counts = get_vote_count(poll_id=poll_id)
    total_votes = sum(vote_counts.values())
    results = [
        Result(
            description=choice.description,
            vote_count=vote_counts.get(choice.id, 0)
        )
        for choice in poll.options
    ]
    results = sorted(results, key=lambda x: x.vote_count, reverse=True) # ordering by vote_count, most votes goes first
    return PollResults(
        title=poll.title,
        total_votes=total_votes,
        results=results
    )