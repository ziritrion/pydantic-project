from fastapi import FastAPI
from app.models.polls import PollCreate

app = FastAPI()

@app.get("/test")
def test():
    return {"message": "Olakease"}

@app.post("/polls/create")
def create_poll(poll: PollCreate):
    new_poll = poll.create_poll()
    return {
        "detail": "Poll successfully created",
        "poll_id": new_poll.id
    }