from fastapi import APIRouter, Depends, HTTPException
from app.models import VoteCreate
from app.database import get_supabase
from app.auth import get_current_user, is_admin_user

router = APIRouter()


@router.post("/votes")
async def submit_vote(vote: VoteCreate, user = Depends(get_current_user), supabase = Depends(get_supabase)):
  existing = await supabase.table("votes").select('*') \
            .eq("candidate_id", vote.candidate_id) \
            .eq("user_id", user.id) \
            .maybe_single() \
            .execute()
  if existing.data:
    raise HTTPException(status_code=400, detail="You already voted for this person")
  
  result = await supabase.table("votes").insert({
            "candidate_id": vote.candidate_id,
            "vote_value": vote.vote_value,
            "user_id": user.id
  }).execute()


  return {"success": True, "data": result.data}

@router.delete("/votes/reset")
async def reset_votes(supabase = Depends(get_supabase), user = Depends(is_admin_user)):
  await supabase.table("votes").delete().execute()
  return {"message": "All votes deleted successfully"}

@router.get("/votes/nonvoters/{candidate_id}")
async def get_non_voters(candidate_id: str, supabase = Depends(get_supabase), user = Depends(is_admin_user)):
  members_response = await supabase.table("profiles").select("id, full_name").eq("role", "member")
  members = members_response.data

  votes_response = await supabase.table("votes").select("user_id").eq("candidate_id", candidate_id).execute()
  voted_user_ids = {vote['user_id'] for vote in votes_response.data}

  non_voters = [user for user in members if user['id'] not in voted_user_ids]

  return {"non_voters": non_voters}

@router.get("votes/results/{candidate_id}")
async def get_vote_results(candidate_id: str, supabase = Depends(get_supabase), user = Depends(is_admin_user)):
  response = await supabase.table("votes").select("vote_value").eq("candidate_id", candidate_id).execute()
  votes = response.data

  if not votes:
    return {"message": "No votes for this person", "passed": False}
  
  total = len(votes)
  yes_votes = sum(1 for vote in votes if vote["vote_vale"] is True)
  percentage_of_yes = yes_votes / total
  passed = percentage_of_yes >= 0.80

  return {
    "total_votes": total,
    "yes_votes": yes_votes,
    "percentage_of_yes": percentage_of_yes,
    "passed": passed
  }



