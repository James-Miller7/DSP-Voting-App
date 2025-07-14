from fastapi import APIRouter, Depends, HTTPException
from app.models import CandidateCreate, CandidateOut
from app.database import get_supabase
from app.auth import is_admin_user


router = APIRouter()

@router.post("/candidates", response_model=CandidateOut)
async def create_candidate(candidate: CandidateCreate, supabase = Depends(get_supabase), user = Depends(is_admin_user)):
  result = await supabase.table("candidates").insert({
    "name": candidate.name,
    "answer": candidate.answer,
    "created_by": user["id"]
  }).execute()

  return result.data[0]


@router.get("/candidates/current", response_model=CandidateOut)
async def get_current_candidate(supabase = Depends(get_supabase)):
  candidate = await supabase.table("candidates").select("*") \
              .eq("is_complete", False) \
              .order("created_at") \
              .limit(1) \
              .maybe_single() \
              .execute()
  
  if not candidate.data:
    raise HTTPException(status_code=404, detail="No more candidates to be voted on")
  
  return candidate.data


@router.delete("/candidates/reset")
async def delete_candidates(supabase = Depends(get_supabase), user = Depends(is_admin_user)):
  await supabase.table("candidates").delete().neq("id", "00000000-0000-0000-0000-000000000000").execute()
  return {"message": "All candidates deleted successfully"}