from fastapi import FastAPI
from app.models.polls import Poll

app = FastAPI()

@app.get("/test")
def test():
    return {"message": "Olakease"}

@app.post("/polls/create")
async def create_poll():
    return Poll(
        options=["yes", "no", "maybe"]
    )