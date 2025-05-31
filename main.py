from dotenv import load_dotenv
load_dotenv(dotenv_path='.env')

from fastapi import FastAPI

from app.api import polls

app = FastAPI(
    title="Polls API",
    description="A simple API to create and vote on polls",
    version="0.1",
    openapi_tags=[
        {
            "name": "polls",
            "description": "Operations related to creating and viewing polls",
        }
    ]
)

app.include_router(polls.router, prefix="/polls", tags=["polls"])