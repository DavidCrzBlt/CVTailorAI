from pydantic import BaseModel
from typing import Optional

# --- User ---
class UserProfileBase(BaseModel):
    full_name: str
    headline: Optional[str] = None
    skills: Optional[str] = None
    tools: Optional[str] = None
    experience_md: Optional[str] = None

class UserProfileCreate(UserProfileBase):
    pass

class UserProfileRead(UserProfileBase):
    id: int
    class Config:
        orm_mode = True


# --- Job ---
class JobPostingBase(BaseModel):
    company: Optional[str] = None
    title: Optional[str] = None
    source_url: Optional[str] = None
    raw_description: str

class JobPostingCreate(JobPostingBase):
    pass

class JobPostingRead(JobPostingBase):
    id: int
    class Config:
        orm_mode = True
