from pydantic import BaseModel, EmailStr
from typing import Optional

class VoteCreate(BaseModel):
  candidate_id: str
  vote_value: bool

class CandidateCreate(BaseModel):
  name: str
  answer: Optional[str] = None

class UserProfile(BaseModel):
  email: EmailStr
  full_name: str
  id: str
  role: str

class CandidateOut(BaseModel):
  id: str
  name: str
  answer: Optional[str] = None




