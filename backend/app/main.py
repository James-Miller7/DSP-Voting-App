from fastapi import FastAPI
from app.routers import votes

app = FastAPI()

app.include_router(votes.router)
