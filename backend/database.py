import os
from dotenv import load_dotenv
from supabase import create_async_client, AsyncClient
import asyncio

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_SERVICE_KEY = os.getenv("SUPABASE_SERVICE_KEY")

_supabase: AsyncClient | None = None


async def get_supabase() -> AsyncClient:
  global _supabase
  if _supabase:
    return _supabase
  _supabase = await create_async_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)
  return _supabase
