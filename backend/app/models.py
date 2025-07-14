from pydantic import BaseModel, EmailStr
from typing import Optional
from enum import Enum

class UserRole(str, Enum):
    member = "member"
    admin = "admin"

class VoteCreate(BaseModel):
  vote_value: bool

class CandidateCreate(BaseModel):
  name: str
  answer: Optional[str] = None

class UserProfile(BaseModel):
  email: EmailStr
  full_name: str
  id: str
  role: UserRole

class CandidateOut(BaseModel):
  id: str
  name: str
  answer: Optional[str] = None




