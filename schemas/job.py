from pydantic import BaseModel
from typing import Optional
from schemas.company import Company


class JobBase(BaseModel):
    title: str
    location: Optional[str] = None
    link: Optional[str] = None
    external_id: Optional[str] = None


# -------------------------
# Job с компанией внутри
# -------------------------
class Job(JobBase):
    id: int
    company_id: Optional[int]
    company: Optional[Company]

    class Config:
        from_attributes = True
        
class JobList(BaseModel):
    id: int
    title: str
    location: Optional[str]
    company: Optional[Company]
    
    class Config:
        from_attributes = True         