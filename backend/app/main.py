from fastapi import FastAPI
from app.routers import votes, candidates, profiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.models import APIKey, APIKeyIn
from fastapi.security import HTTPBearer
from fastapi.openapi.utils import get_openapi


app = FastAPI()

app.include_router(votes.router)
app.include_router(candidates.router)
app.include_router(profiles.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def custom_openapi():
  if app.openapi_schema:
    return app.openapi_schema


  openapi_schema = get_openapi(
    title="DSP Voting API",
    version="1.0.0",
    description="Voting system powered by FastAPI + Supabase",
    routes=app.routes,
  )
  openapi_schema["components"]["securitySchemes"] = {
    "bearerAuth": {
      "type": "http",
      "scheme": "bearer",
      "bearerFormat": "JWT"
    }
  }
  for path in openapi_schema["paths"].values():
    for method in path.values():
      method["security"] = [{"bearerAuth": []}]

  app.openapi_schema = openapi_schema
  return app.openapi_schema

app.openapi = custom_openapi
