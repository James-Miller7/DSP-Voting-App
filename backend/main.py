from fastapi import FastAPI
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import text
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

# SQLAlchemy engine + session
engine = create_async_engine(DATABASE_URL, echo=True)
AsyncSessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)
Base = declarative_base()

app = FastAPI()

@app.get("/")
async def read_root():
    async with AsyncSessionLocal() as session:
        result = await session.execute(text("SELECT 'Hello from PostgreSQL!'"))
        msg = result.scalar()
        return {"message": msg}
