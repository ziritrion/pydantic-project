from dotenv import load_dotenv
load_dotenv(dotenv_path='.env')

from fastapi import FastAPI, HTTPException
from app.models.polls import PollCreate
from app.services import utils
from uuid import UUID

app = FastAPI()

@app.get("/test")
def test():
    return {"message": "Olakease"}

@app.post("/polls/create")
def create_poll(poll: PollCreate):
    new_poll = poll.create_poll()
    utils.save_poll(poll=new_poll)
    return {
        "detail": "Poll successfully created",
        "poll_id": new_poll.id,
        "poll": new_poll
    }

@app.get("/polls/{poll_id}")
def get_poll(poll_id: UUID):
    poll = utils.get_poll(poll_id=poll_id)
    if not poll:
        raise HTTPException(
            status_code=404,
            detail="Cannot retrieve poll: the poll does not exist"
        )
    return poll