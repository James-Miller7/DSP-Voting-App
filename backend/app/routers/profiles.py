from fastapi import APIRouter, Depends, HTTPException
from app.models import ProfileIn, ProfileOut
from app.database import get_supabase
from app.auth import get_current_user

router = APIRouter()

@router.post("/profiles", response_model=ProfileOut)
async def create_profile(profile: ProfileIn, supabase = Depends(get_supabase), user = Depends(get_current_user)):
  result = await supabase.table("profiles").insert({
    "id": user["id"],
    "full_name": profile.full_name,
    "email": profile.email,
    "role": "member"
  }).execute()

  return result.data[0]
