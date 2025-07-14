from fastapi import Request, HTTPException, Depends
from app.database import get_supabase

async def get_current_user(request: Request, supabase = Depends(get_supabase)):
    token = request.headers.get("Authorization")
    if not token or not token.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid auth token")
    
    access_token = token.replace("Bearer ", "")
    try:
        user_response = await supabase.auth.get_user(access_token)
        if not user_response or not user_response.user:
            raise HTTPException(status_code=401, detail="Invalid token")

        user_id = user_response.user.id

        profile_resp = await supabase.table("profiles") \
            .select("*") \
            .eq("id", user_id) \
            .maybe_single() \
            .execute()

        profile = profile_resp.data
        if not profile:
            raise HTTPException(status_code=404, detail="User profile not found")
        return profile

    except Exception:
        raise HTTPException(status_code=401, detail="Could not validate token")
  
async def is_admin_user(user = Depends(get_current_user), supabase = Depends(get_supabase)):
  profile = await supabase.table("profiles").select("*").eq("id",user["id"]).single().execute()

  if not profile.data or profile.data["role"] != "admin":
    raise HTTPException(status_code=403, detail="Admin access required")
  
  return user
