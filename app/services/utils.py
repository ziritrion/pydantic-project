from upstash_redis import Redis
import os
from uuid import UUID
from typing import Optional

from app.models.polls import Poll

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