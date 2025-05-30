from fastapi import FastAPI
from app.models.polls import Poll

app = FastAPI()

@app.get("/test")
def test():
    return {"message": "Olakease"}

@app.post("/polls/create")
async def create_poll(poll: Poll) -> Poll:
    return Poll(
        title="my poll",
        options=["yes", "no", "maybe"]
    )